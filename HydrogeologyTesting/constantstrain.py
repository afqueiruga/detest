"""
These are constant strain problems for mechanics.

A finite element code will solve these to within machine precision. Codes
based on non-standard "theories" or models will not necessarily capture
these. It is imperative that a mechanics solver pass these as ExactTests.
"""

parameters = {
    'K': 10.0e9,
    'G': 10.0e9,

    'Load':-1.0e5,
}

def uniaxial(parameters):
    pass
def shear(parameters):
    pass
def isotropic(parameters):
    pass

def random_patch(parameters):
    pass
