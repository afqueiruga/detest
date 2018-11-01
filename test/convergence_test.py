import HydrogeologyTesting as hgtest

import numpy as np
import unittest as ut

problems = [
    hgtest.oracles.mechanics_constant,
    hgtest.oracles.poroelastic_constant,
    hgtest.oracles.terzaghi,
]

class Meta_ConvergenceTest(ut.TestCase):
    def test_convergence(self):
        " Add an error equal to C * h^n and verify we get O(n)"
        for problem in problems:
            for test in problem.tests:
                def mycode(params, h):
                    " A precisely perturbed code "
                    orc = test(params)
                    pts = np.random.rand( 10, orc.ptdim )
                    fields = orc(pts)
                    ans = orc(pts)
                    for _ in ans.keys():
                        ans[_] = ans[_]*(1.0+0.0001*h)
                    #print ans
                    ans['points'] = pts
                    return ans
                etr = hgtest.ConvergenceTestRunner(test,mycode, 1.0)
                self.assertTrue( etr.test() )
