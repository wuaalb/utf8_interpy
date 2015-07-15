"""Python source code pre-processor which implements Ruby-like string interpolation."""
from io import BytesIO
import tokenize
from . import compat

# scan left-to-right
#   find opening tag #{
#   find corresponding closing tag }; exception if none found
#   store begin/end column pairs
#
# 'xyz #{foobar} xyz' -> b = 4, e = 13
# 'xyz '+str(foobar)+' xyz'
def interpolate_string(s):
    be_pairs = []

    # find matching #{ .. } tags
    stag = '#{'
    etag = '}'
    pos = 0
    while pos != -1:
        pos = s.find(stag, pos)
        if pos != -1:
            b = pos
            level = 1
            pos += len(stag)
            while pos < len(s):
                if s[pos] == '{':
                    level += 1
                elif s[pos] == '}':
                    level -= 1
                    if level == 0:
                        e = pos+1
                        be_pairs.append((b, e))
                        break
                elif s[pos] == '\n':
                    print('Warning: Interpy opening tag found, but no matching closing tag (newline).')
                    break
                pos += 1
        if pos >= len(s):
            print('Warning: Interpy opening tag found, but no matching closing tag (end of string).')
            break

    # get type of quotes used (single or triple)
    if len(s) >= 7 and s[0:3] == '"""' and s[-3:] == '"""':
        oquotes = '"""'
        cquotes = '"""'
    else:
        assert(len(s) >= 3 and s[0] == '"' and s[-1] == '"')
        oquotes = '"'
        cquotes = '"'

    # replace string tags with interpolation expressions
    s_out = ''
    pos = 0
    for b, e in be_pairs:
        s_out += s[pos:b] # lhs
#        s_out += cquotes + '+' + compat.text_type_str + '(' + unescape_quotes(s[b+len(stag):e-len(etag)]) + ')+' + oquotes # interpolation
        s_out += cquotes + '+' + compat.text_type_str + '(' + s[b+len(stag):e-len(etag)] + ')+' + oquotes # interpolation
        pos = e
    s_out += s[pos:] # final rhs
    # Note:
    # Above code is not optimal in the sense of generating the most compact expression, 
    # and will generate some superfluous ..+""+.. type code.
    # E.g.
    # in:  '"#{foobar}#{foobar}"'
    # out: '""+str(foobar)+""+str(foobar)+""'
    # opt: 'str(foobar)+str(foobar)'
    #
    # However this avoids an issue where strings are concatenated without a + operator, e.g.
    # "#{foobar}" "#{foobar}" -> generates two string tokens
    # ""+str(foobar)+"" ""+str(foobar)+"" -> OK
    # str(foobar) str(foobar) -> NG
    #
    # The superfluous empty string concatenation may add *some* run-time overhead, but this should 
    # be negligible.

    s_out = '(' + s_out + ')' # add brackets so we can combine python string interpolation with interpy string interpolation

    return s_out

def interpolate_string_and_tokenize(s, start, end):
    #print('INTERPOLATING "%s"' % s.__repr__()) # XXX: debug
    s_out = interpolate_string(s)

    s_srow, s_scol = start
    s_erow, s_ecol = end

    # tokenize preprocessed string
    try:
        stream = BytesIO(s_out.encode('utf-8'))
        tokens = compat.tokenize(stream.readline)
        tokens = list(tokens)
    except tokenize.TokenError:
        # probably invalid markup inside string, just return unprocessed string token
        print('Warning: Unhandled exception tokenizing interpy interpolated string; invalid markup inside string?')
        tokens = [compat.TokenInfo(tokenize.STRING, s, (s_srow, s_scol), (s_erow, s_ecol), s)]
        return tokens, 0
    
    # strip initial ENCODING token (it is already in the parent token stream)
    if hasattr(tokenize, 'ENCODING') and tokens[0][0] == tokenize.ENCODING: # Py2 doesn't generate initial ENCODING token
        tokens = tokens[1:]

    # strip final ENDMARKER token (because it terminates untokenize)
    if tokens[-1][0] == tokenize.ENDMARKER:
        tokens = tokens[:-1]

    # fix row and column offsets to match those of outer token stream
    tokens_fixed = []
    for tok in tokens:
        tok_type, tok_str, (srow, scol), (erow, ecol), tok_line = tok
        
        row1 = tokens[0][2][0] # row index of first line
        assert row1 == 1 # assume row indexes start at 1, with 0 reserved for the ENCODING token

        # first line continues outer token stream line
        # following lines start at col 0
        scoloff = s_scol if srow == row1 else 0
        ecoloff = s_scol if erow == row1 else 0
        tokens_fixed.append(compat.TokenInfo(tok_type, tok_str, (srow - row1 + s_srow, scol + scoloff), (erow - row1 + s_srow, ecol + ecoloff), tok_line))

    if len(tokens_fixed) == 0:
        col_offset = 0
    else:
        tok_type, tok_str, (srow, scol), (erow, ecol), tok_line = tokens_fixed[-1] # last token
        col_offset = ecol - s_ecol # column offset from pre-processing inserted characters
        # (pre-processing never adds rows, so row_offset = 0 always)
    
    return tokens_fixed, col_offset

def is_double_quoted(s):
    """Check if string is non-raw single quoted with double quotes."""
    # "foobar"      -> True
    # """foobar"""  -> True
    # 'foobar'      -> False
    # '''foobar'''  -> False
    # r"foobar"     -> False
    # r"""foobar""" -> False
    # r'foobar'     -> False
    # r'''foobar''' -> False
    return (len(s) >= 3 and s[0] == '"' and s[-1] == '"') or (len(s) >= 7 and s[0:3] == '"""' and s[-3:] == '"""')

def is_docstring(cur_tok_type, cur_tok_str, cur_scol, prev_tok_type):
    """Check if token is docstring."""
    # check if triple quoted string
    is_triple = cur_tok_type == tokenize.STRING and \
        ((len(cur_tok_str) >= 7 and ((cur_tok_str[0:3] == '"""' and cur_tok_str[-3:] == '"""') or (cur_tok_str[0:3] == "'''" and cur_tok_str[-3:] == "'''"))) or \
        (len(cur_tok_str) >= 8 and ((cur_tok_str[0:4] == 'r"""' and cur_tok_str[-3:] == '"""') or (cur_tok_str[0:4] == "r'''" and cur_tok_str[-3:] == "'''"))))
    # check if directly after indent (e.g. first line after def, class, ..), or on first column (module docstring)
    return is_triple and (prev_tok_type == tokenize.INDENT or cur_scol == 0)

#def unescape_quotes(s):
#    """Unescape backslashed quotes in Python expressions, outputs unicode string."""
#    return s.replace(r'\"', '"').replace(r'\'', '\'')

def tokenize_and_preprocess(readline):
    tokens = compat.tokenize(readline)

    last_interp_row        = -1
    last_interp_col_offset = 0
    prev_tok_type          = None
    pprev_tok_type         = None
    while 1:
        try:
            token = next(tokens)
        except StopIteration:
            break

        tok_type, tok_str, (srow, scol), (erow, ecol), tok_line = token
        if srow == last_interp_row:
            # token on same line as last interpolation, 
            # so token after interpolated tokens; shift columns
            col_offset = last_interp_col_offset
        else:
            # no interpolation previous to token on same line
            col_offset = 0
            last_interp_col_offset = 0 # new line, so reset interpolation column offset

        scol += col_offset
        if srow == erow: # single line token, also offset end column
            ecol += col_offset

        is_possible_interp_str = tok_type == tokenize.STRING and is_double_quoted(tok_str) and not is_docstring(tok_type, tok_str, scol, prev_tok_type)
        
        if is_possible_interp_str and (prev_tok_type == tokenize.STRING or (prev_tok_type == tokenize.NL and pprev_tok_type == tokenize.STRING)):
            # current token is string and previous token is string (or string on new line); means 
            # these two strings are concatenated without explicit '+';
            # we add '+' here because pre-procesing may add parenthesis
            token_interp = compat.TokenInfo(tokenize.OP, u'+', (srow, scol), (srow, scol+1), tok_line)
            #print('a:'+str(token_interp)) # XXX: DEBUG
            yield token_interp
            scol += 1
            if srow == erow: # single line token, also offset end column
                ecol += 1
            last_interp_col_offset += 1

        pprev_tok_type = prev_tok_type
        prev_tok_type = tok_type

        if is_possible_interp_str:
            tokens_interp, interp_col_offset = interpolate_string_and_tokenize(tok_str, (srow, scol), (erow, ecol))
            last_interp_row = erow
            last_interp_col_offset += interp_col_offset # add for case of multiple interpolations on the same line
            for token_interp in tokens_interp:
                #print('i:'+str(token_interp)) # XXX: DEBUG
                yield token_interp
        else:
            token_interp = compat.TokenInfo(tok_type, tok_str, (srow, scol), (erow, ecol), tok_line) # same as input token, but position possibly changed
            #print('  '+str(token_interp)) # XXX: DEBUG
            yield token_interp