import HydrogeologyTesting as hgtest

import numpy as np
import unittest as ut

problems = [
    hgtest.mechanics_constant,
    hgtest.terzaghi,
]

class IdentityTest(ut.TestCase):
    def test_identity(self):
        " Make sure the oracles pass the tests "
        for problem in problems:
            for test in problem.tests:
                def mycode(params, h,dt):
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
        " Make sure the test says its wrong for all of them "
        for problem in problems:
            for test in problem.tests:
                def mycode(params, h,dt):
                    " An gaurunteed wrong code "
                    orc = test(params)
                    pts = np.array([[0.0,0.0,0.0]])
                    fields = orc(pts)
                    ans = orc(pts)
                    for _ in ans.keys():
                        ans[_] += 1.0
                    ans['points'] = pts
                    return ans
                etr = hgtest.ExactTestRunner(test,mycode)
                self.assertFalse( etr.test() )
