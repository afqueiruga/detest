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
    K_d  = params['K_d']
    G    = params['G']
    Load = params['Load']
    eps = Load / (K_d+4.0*G/3.0)
    sigyy = Load
    sigxx = sigzz = Load * (3.0*K_d-2.0*G)/(3.0*K_d+4.0*G)
    sigxy = 0.0
    def U(x,y,z):
        return np.array([eps*x,0,0])
    return {'eps':np.array([[eps,0.0,0.0],
                            [0.0,0.0,0.0],
                            [0.0,0.0,0.0]),
            'sigma':np.array([[sigxx,sigxy,0.0],
                              [sigxy,sigyy,0.0],
                              [0.0,  0.0,  sigzz]),
            'U':U}

def shear(parameters):
    K_d  = params['K_d']
    G    = params['G']
    Load = params['Load']
    eps_anal = Load / G
    sigxx_anal = sigyy_anal = sigzz_anal = 0.0
    sigxy_anal = Load
    def U(x,y,z):
        return np.array([0,eps*x,0])
    return {'eps':np.array([[0.0,eps,0.0],
                            [eps,0.0,0.0],
                            [0.0,0.0,0.0]),
            'sigma':np.array([[sigxx,sigxy,0.0],
                              [sigxy,sigyy,0.0],
                              [0.0,  0.0,  sigzz]),
            'U':U}
def isotropic(parameters):
    pass

def random_patch(parameters):
    pass

# A list of the ones in here in case you want to loop
tests = [uniaxial, shear]
