# coding: utf8-interpy
"""Testing mixed Python and interpy string interpolation."""

var1 = 'interpy'

# % interpolation after interpy interpolation
pyold_after_interpy_interp = "#{var1} %s" % ('python')
pyold_after_interpy_expect = 'interpy python'

# {} interpolation after interpy interpolation
pynew_after_interpy_interp = "#{var1} {var2}".format(var2='python')
pynew_after_interpy_expect = 'interpy python'

# formatted {} interpolation after interpy interpolation
pynew_fmt_after_interpy_interp = "#{var1} {:08d}".format(23)
pynew_fmt_after_interpy_expect = 'interpy 00000023'

# % interpolation before interpy interpolation
pyold_before_interpy_interp = "%s #{var1}" % ('python')
pyold_before_interpy_expect = 'python interpy'

# {} interpolation before interpy interpolation
pynew_before_interpy_interp = "{var2} #{var1}".format(var2='python')
pynew_before_interpy_expect = 'python interpy'

# formatted {} interpolation before interpy interpolation
pynew_fmt_before_interpy_interp =  "{:08d} #{var1}".format(23)
pynew_fmt_before_interpy_expect = '00000023 interpy'

