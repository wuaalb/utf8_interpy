# coding: utf8-interpy
"""Testing basic interpy interpolations."""

var = 'foobar'

# Different types of string literals
# ----------------------------------

# single quote
single_quoted_interp = '#{var}'
single_quoted_expect = '#{var}' # single quoted strings are not interpolated

# double quote
double_quoted_interp = "#{var}"
double_quoted_expect = 'foobar'

# triple single quote
triple_single_quoted_interp = '''#{var}'''
triple_single_quoted_expect = '#{var}' # triple single quoted strings are not interpolated

# triple double quote
triple_double_quoted_interp = """#{var}"""
triple_double_quoted_expect = 'foobar'

# raw single quote
raw_single_quoted_interp = r'#{var}'
raw_single_quoted_expect = '#{var}' # raw strings are not interpolated

# raw double quote
raw_double_quoted_interp = r"#{var}"
raw_double_quoted_expect = '#{var}' # raw strings are not interpolated

# raw triple single quote
raw_triple_single_quoted_interp = r'''#{var}'''
raw_triple_single_quoted_expect = '#{var}' # raw strings are not interpolated

# raw triple double quote
raw_triple_double_quoted_interp = r"""#{var}"""
raw_triple_double_quoted_expect = '#{var}' # raw strings are not interpolated


# Basic use cases
# ---------------

var1 = 'aa'
var2 = 'bbbbbbb'
# strings chosen so that:
#   len('#{var1}') != len('aa'), len('#{var2}') != len('bbbbbbb'), 
#   len('#{var1}')+len('#{var2}') != len('aa')+en('bbbbbbb')

def fun(s1, s2):
    return s1+s2

# single interpolation, no prefix/suffix
basic01_interp = "#{var1}"
basic01_expect = 'aa'

# single interpolation, prefix
basic02_interp = "pre#{var1}"
basic02_expect = 'preaa'

# single interpolation, suffix
basic03_interp = "#{var1}post"
basic03_expect = 'aapost'

# single interpolation, prefix and suffix
basic04_interp = "pre#{var1}post"
basic04_expect = 'preaapost'

# double interpolation, no prefix/suffix/inner text
basic05_interp = "#{var1}#{var2}"
basic05_expect = 'aabbbbbbb'

# double interpolation, no prefix/suffix, with inner text
basic06_interp = "#{var1}xx#{var2}"
basic06_expect = 'aaxxbbbbbbb'

# double interpolation, prefix, no inner text
basic07_interp = "pre#{var1}#{var2}"
basic07_expect = 'preaabbbbbbb'

# double interpolation, prefix, with inner text
basic08_interp = "pre#{var1}xx#{var2}"
basic08_expect = 'preaaxxbbbbbbb'

# double interpolation, suffix, no inner text
basic09_interp = "#{var1}#{var2}post"
basic09_expect = 'aabbbbbbbpost'

# double interpolation, suffix, with inner text
basic10_interp = "#{var1}xx#{var2}post"
basic10_expect = 'aaxxbbbbbbbpost'

# double interpolation, prefix and suffix, no inner text
basic11_interp = "pre#{var1}#{var2}post"
basic11_expect = 'preaabbbbbbbpost'

# double interpolation, prefix and suffix, with inner text
basic12_interp = "pre#{var1}xx#{var2}post"
basic12_expect = 'preaaxxbbbbbbbpost'

# ...

# two interpolated quotes on same line
double_fun_interp = fun("#{var1}", "#{var2}")
double_fun_expect = 'aabbbbbbb'



# do simple calculation inside interpolation
calc_interp = "1 + 1 = #{1+1}"
calc_expect = '1 + 1 = 2'


alist = ['fo', 'ob', 'ar']
adict = {'foobar' : 123}

# get element from list by index
list_interp = "#{alist[1]}"
list_expect = 'ob'

# get element from dictionary by string literal key
dict_lit_interp = "#{adict['foobar']}"
dict_lit_expect = '123'

# get element from dictionary by string variable key
dict_var_interp = "#{adict[var]}"
dict_var_expect = '123'
