"""
Similar to the constant strain problems for mechanics, but these are for a
*sealed* poroelastic material. The fluid pressures changes in response to
the instantaneous loading. These are the static solutions, after the flow
and stresses have relaxed.

It is imperative that a poroelasticity solver pass these as ExactTests.

"""
import numpy as np

default_parameters = {
    'K_d': 10.0e9,
    'G': 10.0e9,
    'K_s': 100.0*10.0e9,
    'K_f':1.0e11,
    'phi':0.22,

    'Load':-1.0e5,
    'P_background':0.0,
}

class UndrainedUniaxial():
    name = "UndrainedUniaxial"
    space_dim = 3
    time_dep = False
    ptdim = 3
    outputs = ['sigma','U','P']
    def __init__(self, in_params=None):
        params = default_parameters.copy()
        if in_params:
            params.update(in_params)
        self.params = params
        K_d  = params['K_d']
        G    = params['G']
        K_f = params['K_f']
        K_s = params['K_s']
        phi = params['phi']
        Load = params['Load']
        P_background = params['P_background']
        alpha = 1.0-K_d/K_s
        M = K_s/(alpha-phi*(1.0-K_s/K_f))
        K_u = alpha**2*M + K_d
        H = (K_d+4.0*G/3.0)

        self.P0 = -alpha/H / ( 1.0/M + alpha**2/H) * Load + P_background
        self.eps = Load / (K_u + 4.0*G/3.0)
        sigyy_back = - P_background
        sigxx_back = - alpha*P_background - (K_d-2.0/3.0*G)/(H) * (1.0-alpha)*P_background
        self.sigyy = Load + sigyy_back
        self.sigxx = self.sigzz = (Load) * (3.0*K_u-2.0*G)/(3.0*K_u+4.0*G) + sigxx_back
        self.sigxy = 0.0
    def __call__(self, x):
        return {#'eps':np.array([[0.0,0.0,0.0],
                #                [0.0,self.eps,0.0],
                #                [0.0,0.0,0.0]]),
                'sigma':np.array([[self.sigxx,self.sigxy,0.0],
                                  [self.sigxy,self.sigyy,0.0],
                                  [0.0,  0.0,  self.sigzz]]),
                'U':np.array([ [0,self.eps*_,0] for _ in x[:,1] ]),
                'P':np.array([ self.P0 for _ in x[:,0]]),
                }

class UndrainedShear():
    name = "UndrainedShear"
    space_dim = 3
    time_dep = False
    ptdim = 3
    outputs = ['sigma','U','P']
    def __init__(self, in_params=None):
        params = default_parameters
        if in_params:
            params.update(in_params)
        self.params = params

        K_d  = params['K_d']
        G    = params['G']
        Load = params['Load']
        self.eps = Load / G
        self.sigxx = self.sigyy = self.sigzz = 0.0
        self.sigxy = Load

    def __call__(self, x):
        return {#'eps':np.array([[0.0,self.eps,0.0],
                #                [self.eps,0.0,0.0],
                #                [0.0,0.0,0.0]]),
                'sigma':np.array([[self.sigxx,self.sigxy,0.0],
                                  [self.sigxy,self.sigyy,0.0],
                                  [0.0,  0.0,  self.sigzz]]),
                'U':np.array([ [0,self.eps*_,0] for _ in x[:,0] ]),
                'P':np.zeros([x.shape[0]]),
        }

def isotropic(parameters):
    pass

def random_patch(parameters):
    pass

tests = [UndrainedUniaxial, UndrainedShear]
