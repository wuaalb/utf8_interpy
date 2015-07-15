# coding: utf8-interpy

var1 = 'foo'
var2 = 'bar'

def fun(s):
    return s

# string concatenation with +
concat_plus_interp = "#{var1}" + "#{var2}"
concat_plus_expect = 'foobar'

# string concatenation with +, with continuation
concat_plus_cont_interp = "#{var1}" + \
                          "#{var2}"
concat_plus_cont_expect = 'foobar'

# string concatenation without +, lhs and rhs of concatenation both are interpolations
concat_strstr_interp = "#{var1}" "#{var2}"
concat_strstr_expect = 'foobar'

# string concatenation inside parenthesis on new line, lhs and rhs of concatenation both are interpolations
concat_strstr_fun_interp = fun("#{var1}"
                               "#{var2}")
concat_strstr_fun_expect = 'foobar'

# string concatenation without +, with continuation
concat_strstr_cont_interp = "#{var1}" \
                            "#{var2}"
concat_strstr_cont_expect = 'foobar'

# string concatenation without +, lhs and rhs of concatenation both are non-interpolations
concat_strstr_pp_interp = "#{var1}xyz" "xyz#{var2}"
concat_strstr_pp_expect = 'fooxyzxyzbar'

# string concatenation inside parenthesis on new line, lhs and rhs of concatenation both are non-interpolations
concat_strstr_fun_pp_interp = fun("#{var1}xyz"
                                  "xyz#{var2}")
concat_strstr_fun_pp_expect = 'fooxyzxyzbar'


