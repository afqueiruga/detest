"""
It works by populating the unittest framework.

This will churn through all of the numerical tests. It is very expensive.

It can operate in a randomized testing fashion to minimize the cost
of testing incremental updates. That is, you can configure it to do a
subsample set frequently, and then schedule the exhaustive tests less
frequently.
"""

from .ExactTest import ExactTest
from .ConvergenceTest import ConvergenceTest

import unittest as ut

def make_suite(suite):
    def make_test(test):
        def fn(self):
            return self.assertTrue(test())
        return fn
    attrs = {
        'test_'+e.name : make_test(e.test) for e in suite
    }
    return type('MySuite', (ut.TestCase,), attrs)
