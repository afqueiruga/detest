"""
This test is just a demonstration of my technique for making testcases.
"""

import unittest as ut

# A class generator. Easier than metaclass, and works in all 2.7 and 3.6
def make_testcase(suite):
    return type('MyTestCase',                   # The class name
                (ut.TestCase,),                 # Inherit only TestCase
                {fn.name : fn for fn in suite}) # Generate a dictionary

# Now how to use it:

# Define your own generator
def MyTestFunctionGenerator(a,b):
    """Generates class methods for a unittest object"""
    def fn(self):
        """Performs one test"""
        self.assertTrue( a*b == 100 )
    fn.name = "test_{0}_{1}".format(a,b)
    return fn

# Make a list of classmethods corresponding to what you want to test
test_list = [
    MyTestFunctionGenerator(50,2),
    MyTestFunctionGenerator(5,20),
    MyTestFunctionGenerator(-50,-2),
    #MyTestFunctionGenerator(10,11), # Fails intentionally
]

# Now create a new type.  Note that we must _name_ the type.
#`make_testcase(test_list)` alone will do nothing, as the framework
# won't discover it
MyTestCase = make_testcase(test_list)
