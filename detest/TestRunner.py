# Parent class
#import unittest as ut
import numpy as np

class TestRunner(): #ut.TestCase):
    """
    Give this clas one problem and one script, and it will run a _convergence_
    test on the code, automatically.
    """
    def __init__(self, problem, script, params=None,
                 scratch_space='./detest_report', extra_name=''):
        self.problem = problem
        self.script = script
        self.name = "exact_"+problem.name+('_'+extra_name+'_' if extra_name else '')
        self.params = params
        if scratch_space:
            self.cwd = scratch_space
        else:
            self.cwd = '.'

    def calc_errors(self, oracle, estimate):
        errors = {}
        orc = oracle(estimate['points'])
        regularized = lambda x : x if x > 1.0e-8 else 1.0e-8
        for field in orc.keys():
            expected = orc[field]
            e = np.linalg.norm(estimate[field] - expected)\
                / regularized(np.linalg.norm(expected))
            errors[field] = e
        return errors

    def test(self):
        return False
