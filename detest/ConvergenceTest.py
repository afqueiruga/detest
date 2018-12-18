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
                 h_path=None,
                 use_db=False,
                 **kwargs):
        self.expected_order = expected_order
        if h_path is None:
            h_path = np.linspace(0.1,2.0, 20)
        self.h_path = h_path
        self.use_db = use_db
        TestRunner.__init__(self,problem,script,**kwargs)

    def run_cases(self, h_dt_path):
        self.oracle = self.problem(self.params)
        params = self.oracle.params
        def runit(h):
            return self.script(params,h)
        if self.use_db:
            sdb = SimDataDB(self.cwd+"/conv_"+self.name+"_errors.db")
            runit = sdb.Decorate('test',[('h','FLOAT'),],
                                 [('points','ARRAY')]+[ (k,'ARRAY') for k in self.oracle.outputs ],
                                 memoize=True,dictreturn=True)(runit)

        # TODO this should be asynchronous
        self.raw = []
        for h in self.h_path:
            estimate = runit(h)
            errors = self.calc_errors(self.oracle,estimate)
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
        """ Make plots to generate a report """
        import matplotlib
        matplotlib.use('agg')
        from matplotlib import pylab as plt
        # sdb = SimDataDB(self.cwd+"/conv_"+self.oracle.name+"_errors.db")
        # Make the contour plots

        for f in self.problem.outputs:
            if self.raw[0][1][f].shape[0] == self.raw[0][1]['points'].shape[0]:
                plt.close('all')
                plt.figure()
                # Plot each sample
                for h,estimate,errors in self.raw:
                    y = estimate[f]
                    if len(y.shape)>1:
                        y = y[:,0]
                    x = estimate['points'][:,self.report_cfg['idx']]
                    ind = np.argsort(x)
                    plt.plot(x[ind],y[ind],'-+',label='h='+str(h),markevery=0.1)
                # Plot the oracle
                yo = self.oracle( estimate['points'] )[f]
                plt.plot(x,yo,'--',label='oracle')
                plt.legend()
                # Label the axes
                try:
                    plt.xlabel(self.report_cfg['x_label'])
                except KeyError:
                    plt.xlabel('x')
                try:
                    plt.ylabel(self.report_cfg['labels'][f])
                except KeyError:
                    plt.ylabel(f)
                plt.tight_layout()
                plt.savefig(self.cwd+"/"+self.name+"_"+f+"_contours.pdf")
        # Make a log log error plots
        plt.figure()
        for f in self.problem.outputs:
            plt.loglog(self.field_errors[f][:,0],
                       self.field_errors[f][:,1],'+-',label=f)
        plt.legend()
        plt.xlabel('log(h)')
        plt.ylabel('log(error)')
        plt.tight_layout()
        plt.savefig(self.cwd+"/"+self.name+"_error.pdf")


    def print_report(self):
        #for h,_,errors in self.raw:
        #    print(h,": ",errors)
        for k in self.field_orders:
            print(k,": ",self.field_orders[k])


    def test(self):
        passed = False
        self.run_cases(self.h_path)
        passed = self.analyze_cases()
        if self.report:
            self.plot_results()
            self.print_report()
        return passed
