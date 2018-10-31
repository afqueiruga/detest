from __future__ import print_function
import numpy as np
import scipy
from SimDataDB import SimDataDB

from TestRunner import TestRunner

def rate(hs,es):
    " Calculate convergence rate "
    return scipy.stats.linregress([np.log(h) for h in hs],
                                  [np.log(e) for e in es])[0]

class NumericalTestRunner(TestRunner):
    """
    Give this clas one problem and one script, and it will run a _convergence_
    test on the code, automatically.
    """
    def __init__(self, problem, script, expected_order,h_path=None,scratch_space = None):
        self.expected_order = expected_order
        if h_path is None:
            h_path = np.linspace(0.5,2.0, 6)
        self.h_path = h_path
        TestRunner.__init__(self,problem,script,scratch_space)
        
    def run_cases(self, h_dt_path):
        oracle = self.problem()
        params = oracle.params
        sdb = SimDataDB(self.cwd+"/errors.db")
        #@sdb.Decorate('test',
        #             [('h','FLOAT'),],
        #             [ (k,'ARRAY') for k in oracle.keys() ])
        def runit(h):
            ans = self.script(params,h)
            errors = self.calc_errors(oracle,ans)
            return ans, errors
        # TODO this should be asynchronous
        self.raw = []
        for h in self.h_path:
            estimate,errors = runit(h)
            self.raw.append((h,estimate,errors))

    def analyze_cases(self):

        return False

    def plot_results(self):
        from matplotlib import pylab as plt
        for t in tables:
            plt.figure()
            for m in methods:
                plt.loglog(*e(t,m),**mykwargs(m))
            plt.legend()
            plt.show()

    def print_report(self):
        for h,_,errors in self.raw:
            print(h,": ",errors)

    def test(self):
        passed = False
        self.run_cases(self.h_path)
        if False:
            self.plot_results()
        passed = self.analyze_cases()
        self.print_report()
        return passed


class NumericalTestingSuite():
    """
    This will churn through all of the numerical tests. It is very expensive.

    It can operate in a randomized testing fashion to minimize the cost
    of testing incremental updates. That is, you can configure it to do a
    subsample set frequently, and then schedule the exhaustive tests less
    frequently.
    """
    def __init__(self, TESTS):
        pass
