# Parent class
#import unittest as ut
import numpy as np
import os

class TestRunner(): #ut.TestCase):
    """
    Give this clas one problem and one script, and it will run a _convergence_
    test on the code, automatically.
    """
    def __init__(self, problem, script, params=None,
                 scratch_space='./detest_report', extra_name='', report=False,report_cfg={}):
        self.problem = problem
        self.script = script
        self.name = "exact_"+problem.name+('_'+extra_name+'_' if extra_name else '')
        self.params = params
        self.report = False
        if scratch_space:
            self.cwd = scratch_space
        else:
            self.cwd = '.'
        os.makedirs(self.cwd, exist_ok=True)
        self.report_cfg = {
            'idx':-1,
        }
        self.report_cfg.update(report_cfg)
        
    def calc_errors(self, oracle, estimate):
        errors = {}
        orc = oracle(estimate['points'])
        # regularized = lambda x : x if x > 1.0e-8 else 1.0e-8
        regularized = lambda x : x if x > 0.0 else 1.0
        for field in orc.keys():
            expected = orc[field]
            e = np.linalg.norm(estimate[field].ravel() - expected.ravel())\
                / regularized(np.linalg.norm(expected))
            # e = np.linalg.norm(estimate[field].ravel()-expected.ravel()) / float(len(expected))
            errors[field] = e
        # from IPython import embed ; embed()
        return errors

    def test(self):
        return False
