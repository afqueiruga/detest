import HydrogeologyTesting as hgtest

import numpy as np
import unittest as ut



def myUniaxial(params, h):
    " An exact code "
    orc = hgtest.oracles.mechanics_constant.Shear(params)
    pts = np.random.rand( 10, orc.ptdim )
    fields = orc(pts)
    ans = orc(pts)
    ans['points'] = pts
    return ans

def myShear(params, h):
    " An exact code "
    orc = hgtest.oracles.mechanics_constant.Shear(params)
    pts = np.random.rand( 10, orc.ptdim )
    fields = orc(pts)
    ans = orc(pts)
    ans['points'] = pts
    return ans

def myTerzaghi(params, h):
    " A perturbed code "
    orc = hgtest.oracles.terzaghi.Terzaghi(params)
    pts = np.random.rand( 10, orc.ptdim )
    fields = orc(pts)
    ans = orc(pts)
    for _ in ans.keys():
        ans[_] = ans[_]*(1.0+0.0001*h)
    ans['points'] = pts
    return ans



suite = [
    hgtest.ExactTestRunner(hgtest.oracles.mechanics_constant.Uniaxial, myUniaxial),
    hgtest.ExactTestRunner(hgtest.oracles.mechanics_constant.Shear,    myShear),
    hgtest.ConvergenceTestRunner(hgtest.oracles.terzaghi.Terzaghi, myTerzaghi, 1),
]


#class Box(ut.TestCase):
#    pass
#hgtest.fill_suite(Box, suite)

Box = hgtest.make_suite(suite)
