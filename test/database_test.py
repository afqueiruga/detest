import detest

import numpy as np
import unittest as ut


def myTerzaghi(params, h):
    " A perturbed code "
    orc = detest.oracles.Terzaghi(params)
    pts = np.random.rand( 10, orc.ptdim )
    fields = orc(pts)
    ans = orc(pts)
    for _ in ans.keys():
        ans[_] = ans[_]*(1.0+0.0001*h)
    ans['points'] = pts
    return ans

class DatabaseTest(ut.TestCase):
    def test(self):
        ct = detest.ConvergenceTest(detest.oracles.Terzaghi, myTerzaghi, 1, use_db = True)
        self.assertTrue(ct.test())

    
