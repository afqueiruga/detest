import HydrogeologyTesting as hgtest

import numpy as np
import unittest as ut

problems = [
    hgtest.oracles.mechanics_constant,
    hgtest.oracles.poroelastic_constant,
    hgtest.oracles.terzaghi,
]

class IdentityTest(ut.TestCase):
    def test_identity(self):
        " Make sure the oracles themselves pass the tests "
        for problem in problems:
            for test in problem.tests:
                def mycode(params, h):
                    " An exact code "
                    orc = test(params)
                    pts = np.random.rand( 10, orc.ptdim )
                    fields = orc(pts)
                    ans = orc(pts)
                    ans['points'] = pts
                    return ans
                etr = hgtest.ExactTestRunner(test,mycode)
                self.assertTrue( etr.test() )
                
    def test_wrong(self):
        " Make sure the test says its wrong for a messed up oracle "
        for problem in problems:
            for test in problem.tests:
                def mycode(params, h):
                    " An gaurunteed wrong code "
                    orc = test(params)
                    pts = np.random.rand( 10, orc.ptdim )
                    fields = orc(pts)
                    ans = orc(pts)
                    for _ in ans.keys():
                        ans[_] += 1.0
                    ans['points'] = pts
                    return ans
                etr = hgtest.ExactTestRunner(test,mycode)
                self.assertFalse( etr.test() )

