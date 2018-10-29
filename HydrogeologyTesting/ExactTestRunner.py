from __future__ import print_function
from TestRunner import TestRunner

class ExactTestRunner(TestRunner):
    """
    Give this clas one problem and one script, and it will run it with a
    bunch of permutations and assert that the error is within machine
    precision. This class uses the standard unittest framework because
    the tests should be _cheap_.

    There is an optional rigor parameter which controls just how far it will
    go.
    """
    def __init__(self, problem, script, rigor=1):
        self.problem = problem
        self.script = script
    def test(self):
        passed = True
        #params = self.problem.parameters
        oracle = self.problem()
        params = oracle.params
        def runit(h,dt):
            ans = self.script(params,h,dt)
            errors = self.calc_errors(oracle,ans)
            return [ ans[k] for k in oracle.keys() ]
        estimate = runit(1.0,1.0)
        errors = self.calc_errors(oracle, estimate)
        for k,v in errors.iteritems():
            if v>1.0e-15:
                print("Failed test ",test," for key ",k)
                passed = False
        return passed

class ExactTestingSuite():
    """
    Initialize this class to run All of the Tests.
    It works by populating the unittest framework.
    """
    def __init__(self, TESTS):
        pass
