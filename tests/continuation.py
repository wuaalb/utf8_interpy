# coding: utf8-interpy

var1 = 'foo'
var2 = 'bar'

def fun(s1, s2):
    return s1+s2

# continuation within single quoted string
cont_single_interp = "#{var1}\
#{var2}"
cont_single_expect = 'foobar'

# line break in triple quoted string
cont_triple_interp = """#{var1}
#{var2}"""
cont_triple_expect = 'foo\nbar'

cont_triple_fun_interp = fun("""aa
bb""", '''cc
dd''')
cont_triple_fun_expect = 'aa\nbbcc\ndd'

