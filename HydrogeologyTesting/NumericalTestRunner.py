import numpy as np
import SimDataDB as sdb

class NumericalTestRunner():
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
        for field in oracle.keys():
            expected = oracle[field](estimate['points'])
            e = np.linalg.norm(estimate[field] - expected)\
                / np.linalg.norm(expected)
            errors[field] = errors
        return errors

    def test(self, params, hs, dts):
        oracle = self.problem(params)
        # Put the results in a db
        sdb = SimDataDB(self.cwd+"/errors.db")
        @sdb.Decorate('test',
                     [('h':'FLOAT'),('dt':'FLOAT')],
                     [ (k:'ARRAY') for k in oracle.keys() ])
        def runit(h,dt):
            ans = script(params,h,dt)
            errors = self.calc_errors(oracle,estimate)
            return [ ans[k] for k in oracle.keys() ]
        # TODO this should be asynchronous
        for h in hs:
            for dt in dts:
                estimate = runit(h,dt)


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
