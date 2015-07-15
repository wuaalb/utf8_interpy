# coding: utf8-interpy
"""module level docstring #{test}
this another line
"""

# double quotes docstring with interpolation
def myfun1(a, b):
    """this is a docstring #{var1}"""
    return a + b

# double quotes docstring without interpolation
def myfun2(a, b):
    """this is a docstring"""
    return a + b

# single quotes docstring with interpolation
def myfun3(a, b):
    '''this is a docstring  #{var1}'''
    return a + b

# single quotes docstring without interpolation
def myfun4(a, b):
    '''this is a docstring'''
    return a + b

# ...
# XXX: these are not checked
