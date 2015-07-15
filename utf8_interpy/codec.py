"""Codec to be used as a Python source file encoding (only)."""
import codecs
from io import BytesIO
from . import compat
from . import preprocessor

encoding_name    = 'utf8-interpy'
encoding_aliases = ['utf8_interpy', 'utf8interpy']
encoding_base    = 'utf-8'

# Aliases of base utf-8 codec functionality we rely on
# Note:
# There are many ways of obtaining these functions and classes, 
# but we try to use documented functions as much as possible
_utf8_decode = codecs.getdecoder(encoding_base)       # equivalent to codecs.utf_8_decode(.., final=True)
_utf8_encode = codecs.getencoder(encoding_base)
_Utf8IncrementalDecoder = codecs.getincrementaldecoder(encoding_base)
_Utf8IncrementalEncoder = codecs.getincrementalencoder(encoding_base)
_Utf8StreamReader = codecs.getreader(encoding_base)
_Utf8StreamWriter = codecs.getwriter(encoding_base)

# Interactive debugger helper
# >>> from utf8_interpy.codec import transform_bytes_string; _s = lambda input: eval(transform_bytes_string(b'"' + input.encode('utf-8') + b'"'))
# >>> test = 'foobar'
# >>> _s("#{test}")
# 'foobar'

def transform_bytes_stream(stream):
    """Transform bytes stream to bytes string."""
    try:
        return compat.untokenize(preprocessor.tokenize_and_preprocess(stream.readline))
        #return compat.untokenize(compat.tokenize(stream.readline)) # XXX: debug, pass-through without pre-processing
    except Exception as e:
        # on any kind of error, we simply output the input without transformation and let the interpreter inform user
        print('Unhandled exception applying UTF8-Interpy pre-processing!')
        print(e)

        stream.seek(0) # rewind to start of stream
        return stream.read()

def transform_bytes_string(input):
    """Transform bytes string to bytes string."""
    stream = BytesIO(input)
    return transform_bytes_stream(stream)

def _transform_as_utf8_encoded(stream):
    """Transform bytes stream to bytes string, 
    forcing encoding during transformation to be UTF-8 if  
    '# coding: utf8-interpy' cookie is found, to avoid 
    circular dependencies."""
    # Because our transform uses tokenize.tokenize() on Py3, which internally calls 
    # decode() of the codec specified in the '# coding: xyz' cookie, we should avoid 
    # the case where this codec is 'utf8-interpy' because utf8_interpy's decode() again 
    # calls transform, which calls tokenize, which calls decode, which calls transform, 
    # etc.
    # As a work-around, we here read the 'coding' cookie and if it is 'utf8-interpy', 
    # we transform the string without the cookie, which will cause tokenize to consider 
    # it to have the default utf-8 encoding; finally we re-add the cookie string to the 
    # beginning of the transformed output.

    encoding, lns = compat.detect_encoding(stream.readline)
    head = b''.join(lns)

    if encoding == encoding_name or encoding in encoding_aliases:
        data = stream.read()           # transform without encoding cookie
        data = transform_bytes_string(data)
        #head = head.replace(b'utf8-interpy', b'utf-8')	# change to utf-8 encoding, to avoid 'unknown encoding' error in some IDE's (e.g. PTVS 2.1, 2.2RC)
        data = head + data             # reconstruct transformed output
    else:
        data = head + stream.read()    # tranform with first (non-cookie) line
        data = transform_bytes_string(data)

    return data


# Stateless encoding and decoding functions
interpy_encode = _utf8_encode                           # just use utf8

def interpy_decode(input, errors='strict'):
    # when importing a file in Py3, input will be a memoryview, 
    # but BytesIO takes this fine, so no need to do input.tobytes()
    stream = BytesIO(input)
    input = _transform_as_utf8_encoded(stream)
    return _utf8_decode(input, errors)

# Incremental encoder and decoder
# Note:
# Because our decoder uses tokenize, we need the entire input before we 
# can decode (even tokenizing line-by-line doesn't work properly for 
# multi-line statements, multi-line strings, etc.).
InterpyIncrementalEncoder = _Utf8IncrementalEncoder     # just use utf8

class InterpyIncrementalDecoder(_Utf8IncrementalDecoder):
    def __init__(self, errors='strict'):
        _Utf8IncrementalDecoder.__init__(self, errors)

    def _buffer_decode(self, input, errors, final):
        if not final:
            #stream = BytesIO(input)
            #line = stream.readline()
            #if b'\n' in line:
            #    return interpy_decode(line, errors) # decode single line
            #else:
            #    return u'', 0                       # wait until we have received at least one full line
            return u'', 0                           # wait until we have received entire input
        else:
            return interpy_decode(input, errors)    # decode all remaining

# Stream reader and writer
InterpyStreamWriter = _Utf8StreamWriter                 # just use utf8

class InterpyStreamReader(_Utf8StreamReader):
    def __init__(self, stream, errors='strict'):
        stream = BytesIO(_transform_as_utf8_encoded(stream))        # transform input stream (all at once)
        _Utf8StreamReader.__init__(self, stream, errors)            # pass onto UTF-8 stream reader


# Register the codec search function
def search_interpy(encoding):
    if encoding == encoding_name or encoding in encoding_aliases:
        return codecs.CodecInfo(
            name=encoding_name,
            encode=interpy_encode,
            decode=interpy_decode,
            incrementalencoder=InterpyIncrementalEncoder,
            incrementaldecoder=InterpyIncrementalDecoder,
            streamwriter=InterpyStreamWriter,
            streamreader=InterpyStreamReader
            )
    else:
        return None

codecs.register(search_interpy)