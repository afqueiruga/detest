import HydrogeologyTesting as hgtest

import numpy as np
import unittest as ut



def myUniaxial(params, h):
    return {}
def myShear(params, h):
    return {}
def myTerzaghi(params, h):
    return {}


suite = [
    hgtest.ExactTestRunner(hgtest.oracles.mechanics_constant.Uniaxial, myUniaxial),
    hgtest.ExactTestRunner(hgtest.oracles.mechanics_constant.Shear,    myShear),
    hgtest.NumericalTestRunner(hgtest.oracles.terzaghi.Terzaghi, myTerzaghi, 1),
]


class Box(ut.TestCase):
    pass
hgtest.fill_suite(Box, suite)


#MyTests()
