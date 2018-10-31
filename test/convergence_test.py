import HydrogeologyTesting as hgtest

import numpy as np
import unittest as ut

problems = [
    hgtest.mechanics_constant,
    hgtest.poromechanics_constant,
    hgtest.terzaghi,
]

class ConvergenceTest(ut.TestCase):
    def test_convergence(self):
        " Add an error equal to C * h^n and verify we get O(n)"
        for problem in problems:
            for test in problem.tests:
                def mycode(params, h,dt):
                    " An exact code "
                    orc = test(params)
                    pts = np.random.rand( 10, orc.ptdim )
                    fields = orc(pts)
                    ans = orc(pts)
                    for _ in ans.keys():
                        ans[_] += np.linalg.norm(ans[_])*0.1*h
                    ans['points'] = pts
                    return ans
                etr = hgtest.NumericalTestRunner(test,mycode, 1.0)
                self.assertTrue( etr.test() )
