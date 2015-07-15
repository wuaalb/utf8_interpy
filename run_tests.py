import sys
import unittest

import utf8_interpy.codec
# NOTE: we import the codec explicitly, so we import modules that use utf8-interpy encoding without installing the utf8_interpy package

# test modules
from tests import basics
from tests import invalid
from tests import mixed
from tests import concatenated
from tests import continuation
from tests import escaped
from tests import docstring
if sys.version_info.major >= 3:
    from tests import unicode_identifiers
from tests import exceptions



class Utf8InterpyTestCases(unittest.TestCase):
    """Test cases for utf8-interpy; generated dynamically."""
    pass


def create_expect_test_method(interp, expect):
    """Helper function that generates a test method which compares an actual value to an expected value."""
    def test_expected(self):
        self.assertEqual(interp, expect)
    return test_expected

def discover_expect_tests_and_add_methods(test, test_cases):
    """Helper function which discover 'xyz_interp', 'xyz_expect' pairs in a given 'test' module; 
    and dynamically generates test methods and adds them to the 'test_cases' class."""
    added = 0

    for attr in dir(test):
        if attr.endswith('_interp'):
            attr_interp = attr
            base = attr_interp[0:-len('_interp')]
            attr_expect = base + '_expect'

            if not attr_expect in test.__dict__:
                print('Warning: Actual value \'%s\' found, without corresponding expected value \'%s\'!' % (attr_interp, attr_expect))
                continue

            test_method = create_expect_test_method(test.__dict__[attr_interp], test.__dict__[attr_expect])
            test_method.__name__ = 'test_expected_' + base

            if test_method.__name__ in test_cases.__dict__:
                print('Warning: duplicate test method \'%s\' skipped!' % test_method.__name__)
                continue

            setattr(test_cases, test_method.__name__, test_method)
            added += 1
        elif attr.endswith('_expect'):
            attr_expect = attr
            base = attr_expect[0:-len('_expect')]
            attr_interp = base + '_interp'
            if not attr_interp in test.__dict__:
                print('Warning: Expected value \'%s\' found, without corresponding actual value \'%s\'!' % (attr_expect, attr_interp))

    if added == 0:
        print('Warning: No tests were added for module \'%s\'...' % test.__name__)


# create test cases from test modules
discover_expect_tests_and_add_methods(basics, Utf8InterpyTestCases)
discover_expect_tests_and_add_methods(invalid, Utf8InterpyTestCases)
discover_expect_tests_and_add_methods(mixed, Utf8InterpyTestCases)
discover_expect_tests_and_add_methods(concatenated, Utf8InterpyTestCases)
discover_expect_tests_and_add_methods(continuation, Utf8InterpyTestCases)
discover_expect_tests_and_add_methods(escaped, Utf8InterpyTestCases)
discover_expect_tests_and_add_methods(docstring, Utf8InterpyTestCases)
if sys.version_info.major >= 3:
    discover_expect_tests_and_add_methods(unicode_identifiers, Utf8InterpyTestCases)


def create_raises_test_method(fun, raises):
    def test_raises(self):
        with self.assertRaises(raises):
            fun()
    return test_raises

def discover_exception_tests_and_add_methods(test, test_cases):
    added = 0

    for attr in dir(test):
        if attr.endswith('_fun'):
            attr_fun = attr
            base = attr_fun[0:-len('_fun')]
            attr_raises = base + '_raises'

            if not attr_raises in test.__dict__:
                print('Warning: Function \'%s\' found, without corresponding expected exception \'%s\'!' % (attr_fun, attr_raises))
                continue

            test_method = create_raises_test_method(test.__dict__[attr_fun], test.__dict__[attr_raises])
            test_method.__name__ = 'test_raises_' + base

            if test_method.__name__ in test_cases.__dict__:
                print('Warning: duplicate test method \'%s\' skipped!' % test_method.__name__)
                continue

            setattr(test_cases, test_method.__name__, test_method)
            added += 1
        elif attr.endswith('_raises'):
            attr_raises = attr
            base = attr_raises[0:-len('_expect')]
            attr_fun = base + '_fun'
            if not attr_fun in test.__dict__:
                print('Warning: Expected exception \'%s\' found, without corresponding function \'%s\'!' % (attr_raises, attr_fun))

    if added == 0:
        print('Warning: No tests were added for module \'%s\'...' % test.__name__)

discover_exception_tests_and_add_methods(exceptions, Utf8InterpyTestCases)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Utf8InterpyTestCases)
    unittest.TextTestRunner(verbosity=2).run(suite)
