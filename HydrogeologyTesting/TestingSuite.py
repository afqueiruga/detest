"""
It works by populating the unittest framework.

This will churn through all of the numerical tests. It is very expensive.

It can operate in a randomized testing fashion to minimize the cost
of testing incremental updates. That is, you can configure it to do a
subsample set frequently, and then schedule the exhaustive tests less
frequently.
"""

from .ExactTestRunner import ExactTestRunner
from .ConvergenceTestRunner import ConvergenceTestRunner

import unittest as ut

def fill_suite(cls, suite):
    for entry in suite:
        setattr(cls, 'test_{0}'.format(entry.name), entry.test)
        
def make_suite(suite):
    attrs = {
        'test_'+e.name : e.test for e in suite
    }
    return type('MySuite', (ut.TestCase,), attrs)
