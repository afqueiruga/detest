import HydrogeologyTesting as hgtest

import unittest as ut

problems = [
    hgtest.mechanics_constant,
]

class IdentityTest(ut.TestCase):
    def test(self):
        for problem in problems:
            def mycode(params, h,dt):
                " An exact code "
                return problem(params)
            etr = hgtest.ExactTestRunner(problem,mycode)
            
            self.assertTrue( etr.test() )
