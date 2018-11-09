import detest
import numpy as np
import unittest as ut



def myUniaxial(params, h):
    " An exact code "
    orc = detest.oracles.mechanics_constant.Uniaxial(params)
    pts = np.random.rand( 10, orc.ptdim )
    fields = orc(pts)
    ans = orc(pts)
    ans['points'] = pts
    return ans

def myShear(params, h):
    " An exact code "
    orc = detest.oracles.mechanics_constant.Shear(params)
    pts = np.random.rand( 10, orc.ptdim )
    fields = orc(pts)
    ans = orc(pts)
    ans['points'] = pts
    return ans

def myTerzaghi(params, h):
    " A perturbed code "
    orc = detest.oracles.terzaghi.Terzaghi(params)
    pts = np.random.rand( 10, orc.ptdim )
    fields = orc(pts)
    ans = orc(pts)
    for _ in ans.keys():
        ans[_] = ans[_]*(1.0+0.0001*h)
    ans['points'] = pts
    return ans



suite = [
    detest.ExactTestRunner(detest.oracles.mechanics_constant.Uniaxial, myUniaxial),
    detest.ExactTestRunner(detest.oracles.mechanics_constant.Shear,    myShear),
    detest.ConvergenceTestRunner(detest.oracles.terzaghi.Terzaghi, myTerzaghi, 1),
]


Box = detest.make_suite(suite)
