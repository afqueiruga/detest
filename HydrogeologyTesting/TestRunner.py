# Parent class
#import unittest as ut
import numpy as np

class TestRunner(): #ut.TestCase):
    """
    Give this clas one problem and one script, and it will run a _convergence_
    test on the code, automatically.
    """
    def __init__(self, problem, script, scratch_space = None):
        self.problem = problem
        self.script = script
        if scratch_space:
            self.cwd = scratch_space
        else:
            self.cwd = '.'

    def calc_errors(self, oracle, estimate):
        errors = {}
        orc = oracle(estimate['points'])
        for field in orc.keys():
            expected = orc[field]
            e = np.linalg.norm(estimate[field] - expected)\
                / np.linalg.norm(expected)
            errors[field] = errors
        return errors

    def test(self):
        return True
