# coding: utf8-interpy

# accessing undeclared indentifier inside interpolation
def name_error_fun():
    foobar = "#{invalid}"
name_error_raises = NameError

# invalid calculation inside interpolation
def divzero_error_fun():
    foobar = "#{10/0}"
divzero_error_raises = ZeroDivisionError

# syntax error in imported module
def syntax_error1_fun():
    from . import syntax_error1
syntax_error1_raises = SyntaxError

def syntax_error2_fun():
    from . import syntax_error2
syntax_error2_raises = SyntaxError
