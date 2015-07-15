# coding: utf8-interpy
"""Testing invalid interpy interpolations."""

# invalid 1 (interpolation not closed)                                  -> simply doesn't find ending } and doesn't interpolate string
invalid1_interp = "#{"
invalid1_expect = '#{'

# invalid 2 (newline inside interpolation)                              -> simply doesn't find ending } and doesn't interpolate string
invalid2_interp = """#{
}"""
invalid2_expect = '''#{
}'''

# invalid 3 (nested interpolations / comment inside interpolation)      -> causes exception when tokenizing interpolated string
invalid3_interp = "#{#{var}}"               
invalid3_expect = '#{#{var}}'
