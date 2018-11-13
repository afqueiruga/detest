from __future__ import print_function
import numpy as np
import scipy.stats
from collections import defaultdict
from SimDataDB import SimDataDB

from .TestRunner import TestRunner

def rate(hs,es):
    " Calculate convergence rate "
    return scipy.stats.linregress([np.log(h) for h in hs],
                                  [np.log(e) for e in es])[0]

class ConvergenceTest(TestRunner):
    """
    Give this clas one problem and one script, and it will run a _convergence_
    test on the code, automatically.
    """
    def __init__(self, problem, script, expected_order,
                 params = None,
                 h_path=None,scratch_space = None):
        self.expected_order = expected_order
        if h_path is None:
            h_path = np.linspace(0.1,2.0, 20)
        self.h_path = h_path
        TestRunner.__init__(self,problem,script,
                            params=params,
                            scratch_space=scratch_space)
        
    def run_cases(self, h_dt_path):
        oracle = self.problem(self.params)
        params = oracle.params

        sdb = SimDataDB(self.cwd+"/conv_"+oracle.name+"_errors.db")
        @sdb.Decorate('test',[('h','FLOAT'),],
                      [('points','ARRAY')]+[ (k,'ARRAY') for k in oracle.outputs ], memoize=False)
        def runit(h):
            ans = self.script(params,h)
            return ans
        # TODO this should be asynchronous
        self.raw = []
        for h in self.h_path:
            estimate = runit(h)
            errors = self.calc_errors(oracle,estimate)
            self.raw.append((h,estimate,errors))

    def analyze_cases(self):
        self.field_errors = defaultdict(lambda : [])
        for h,_,errors in self.raw:
            for k in errors:
                v = errors[k]
                self.field_errors[k].append( (h,v) )
        for k in self.field_errors.keys():
            self.field_errors[k] = np.array(self.field_errors[k])
        passed=True
        self.field_orders = {}
        for k in self.field_errors:
            es = self.field_errors[k]
            order = rate(es[:,0],es[:,1])
            self.field_orders[k] = order
            # TODO check if nan: that means exact
            if np.abs(order-self.expected_order) > 5.0e-2:
                passed=False
        return passed

    def plot_results(self):
        from matplotlib import pylab as plt
        for t in tables:
            plt.figure()
            for m in methods:
                plt.loglog(*e(t,m),**mykwargs(m))
            plt.legend()
            plt.show()

    def print_report(self):
        #for h,_,errors in self.raw:
        #    print(h,": ",errors)
        for k in self.field_orders:
            print(k,": ",self.field_orders[k])

            
    def test(self):
        passed = False
        self.run_cases(self.h_path)
        if False:
            self.plot_results()
        passed = self.analyze_cases()
        self.print_report()
        return passed

