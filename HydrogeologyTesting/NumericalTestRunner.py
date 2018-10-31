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
    def __init__(self, problem, script, expected_order,h_dt_path=None,scratch_space = None):
        self.expected_order = expected_order
        if h_dt_path is None:
            hs = np.linspace(0.5,2.0, 6)
            h_dt_path = [ (_,1.0) for _ in hs ]
        self.h_dt_path = h_dt_path
        TestRunner.__init__(self,problem,script,scratch_space)
        
    def run_cases(self, h_dt_path):
        oracle = self.problem()
        params = oracle.params
        sdb = SimDataDB(self.cwd+"/errors.db")
        #@sdb.Decorate('test',
        #             [('h','FLOAT'),('dt','FLOAT')],
        #             [ (k,'ARRAY') for k in oracle.keys() ])
        def runit(h,dt):
            ans = self.script(params,h,dt)
            errors = self.calc_errors(oracle,ans)
            return ans, errors
        # TODO this should be asynchronous
        self.raw = []
        for h,dt in h_dt_path:
            estimate,errors = runit(h,dt)
            self.raw.append((h,dt,estimate,errors))

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
        for t in tables:
            print t

    def test(self):
        passed = False
        self.run_cases(self.h_dt_path)
        print self.raw
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
