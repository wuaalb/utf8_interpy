# coding: utf8-interpy

# using backslash escaped characters inside
#esc_test1_interp = "#{\"escaped string literal\"}"
#esc_test1_expect = 'escaped string literal'

#esc_test2_interp = "#{\'escaped string literal\'}"
#esc_test2_expect = 'escaped string literal'

esc_test3_interp = "#{'escaped string\nliteral'}"
esc_test3_expect = 'escaped string\nliteral'

esc_test4_interp = "#{'escaped \'string\' literal'}"
esc_test4_expect = 'escaped \'string\' literal'

