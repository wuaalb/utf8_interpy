"""Py2/Py3 compatibility helpers for the tokenize module."""
import sys
import tokenize as pytokenize

# text type as string
if sys.version_info.major >= 3:
    text_type_str = 'str'
else:
    text_type_str = 'unicode'
    #text_type_str = 'str'     # change to use non-unicode text on Py2

# tokenize.TokenInfo
if sys.version_info.major >= 3:
    TokenInfo = pytokenize.TokenInfo
else:
    class TokenInfo(tuple):
        def __new__(cls, type, string, start, end, line):
            return tuple.__new__(cls, (type, string, start, end, line))

        def __str__(self):
            # do slightly nicer display for debugging (Py2 only)
            type, string, start, end, line = self
            return 'TokenInfo: %-8s %-20s %-20s %-20s %s' % (pytokenize.tok_name[type], string.__repr__(), start.__repr__(), end.__repr__(), line.__repr__())

# tokenize.detect_encoding()
try:
    detect_encoding = pytokenize.detect_encoding
except:
    def detect_encoding(readline):
        return 'utf-8', []
    # Py2 doesn't have tokenize.detect_encoding(), but as this function is only used to avoid 
    # a circular function call problem which only happens in Py3 (Py2 tokenize.generate_tokens() doesn't call decode()), 
    # we just return the default encoding (utf-8) without actually reading any lines.
    # Alternatively, we could copy a slightly modified version of Py3's tokenize.detect_encoding() implementation here.

# tokenize.tokenize() and tokenize.untokenize()
if sys.version_info.major >= 3:
    tokenize = pytokenize.tokenize
    untokenize = pytokenize.untokenize
else:
    def tokenize(readline):
        tokens = pytokenize.generate_tokens(readline)

        # convert text to unicode
        for token in tokens:
            tok_type, tok_str, (srow, scol), (erow, ecol), tok_line = token
            tok_str = tok_str.decode('utf-8')
            tok_line = tok_line.decode('utf-8')
        
            yield TokenInfo(tok_type, tok_str, (srow, scol), (erow, ecol), tok_line)
    
    def untokenize(tokens):
        # convert to bytes string
        return pytokenize.untokenize(tokens).encode('utf-8')

# contents of module
__all__ = [text_type_str, TokenInfo, detect_encoding, tokenize, untokenize]
