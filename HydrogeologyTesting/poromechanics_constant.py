"""
Similar to the constant strain problems for mechanics, but these are for a
*sealed* poroelastic material. The fluid pressures changes in response to
the instantaneous loading. These are the static solutions, after the flow
and stresses have relaxed.

It is imperative that a poroelasticity solver pass these as ExactTests.

"""

parameters = {
    'K_d': 10.0e9,
    'G': 10.0e9,
    'K_s': 100.0*10.0e9,
    'K_f':1.0e11,
    'phi':0.22,
    'k':1.0e-13,
    'eta':1.0e-3,

    'H':100.0,
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
