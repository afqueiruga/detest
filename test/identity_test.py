import HydrogeologyTesting as hgtest

import unittest as ut

problems = [
    hgtest.mechanics_constant,
]

class IdentityTest(ut.TestCase):
    def test_identity(self):
        " Make sure the oracles pass the tests "
        for problem in problems:
            def mycode(params, h,dt):
                " An exact code "
                return problem(params)
            etr = hgtest.ExactTestRunner(problem,mycode)
            
            self.assertTrue( etr.test() )
    def test_wrong(self):
        " Make sure the test says its wrong for all of them "
        for problem in problems:
            def mycode(params, h,dt):
                " An gaurunteed wrong code "
                ans = problem(params)
                for _ in ans.keys():
                    ans[_] += 1.0
                return ans
            etr = hgtest.ExactTestRunner(problem,mycode)
            
            self.assertFalse( etr.test() )
