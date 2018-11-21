from __future__ import print_function
from .TestRunner import TestRunner

class ExactTest(TestRunner):
    """
    Give this clas one problem and one script, and it will run it with a
    bunch of permutations and assert that the error is within machine
    precision. This class uses the standard unittest framework because
    the tests should be _cheap_.

    There is an optional rigor parameter which controls just how far it will
    go.
    """
    def test(self):
        passed = True
        # TODO: randomized testing of parameters
        oracle = self.problem(self.params)
        params = oracle.params
        def runit(h):
            ans = self.script(params,h)
            errors = self.calc_errors(oracle,ans)
            return ans, errors
        estimate, errors = runit(1.0)
        for k in errors:
            v = errors[k]
            if v>1.0e-15:
                print("Failed test key ",k,": error was ",v,".")
                passed = False
        return passed
