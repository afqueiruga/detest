"""
This test is just a demonstration of my technique for making testcases.
"""

import unittest as ut


class MyTestFunctionGenerator():
    def __init__(self,a,b):
        self.a,self.b = a,b
        self.name = str(a)+'_'+str(b)
    def fn(self):
        return self.a*self.b == 100

test_list = [
    MyTestFunctionGenerator(50,2),
    MyTestFunctionGenerator(5,20),
    MyTestFunctionGenerator(-50,-2),
    MyTestFunctionGenerator(10,11),
]


def make_testcase(suite):
    def make_classmethod(rawtestfunc):
        def fn(self):
            self.assertTrue(rawtestfunc())
        return fn
    return type('MyTestCase',(ut.TestCase,),
                {'test_'+A.name : make_classmethod(A.fn) for A in suite})
                
MyTestCase = make_testcase(test_list)
