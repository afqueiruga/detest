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
}

class UndrainedUniaxial():
    def __init__(self, params=default_parameters):
        # self.default_params = default_parameters
        self.space_dim = 3
        self.time_dep = False
        self.ptdim = 3
        self.params = params
        K_d  = params['K_d']
        G    = params['G']
        K_f = params['K_f']
        K_s = params['K_s']
        phi = params['phi']
        Load = params['Load']
        alpha = 1.0-K_d/K_s
        M = K_s/(alpha-phi*(1.0-K_s/K_f))
        K_u = alpha**2*M + K_d
        H = (K_d+4.0*G/3.0)
        
        self.P0 = alpha/H / ( 1.0/M + alpha**2/H) * Load
        self.eps = Load / (K_u + 4.0*G/3.0)
        self.sigyy = Load
        self.sigxx = self.sigzz = Load * (3.0*K_u-2.0*G)/(3.0*K_u+4.0*G)
        self.sigxy = 0.0
    def __call__(self, x):
        return {'eps':np.array([[self.eps,0.0,0.0],
                                [0.0,0.0,0.0],
                                [0.0,0.0,0.0]]),
                'sigma':np.array([[self.sigxx,self.sigxy,0.0],
                                  [self.sigxy,self.sigyy,0.0],
                                  [0.0,  0.0,  self.sigzz]]),
                'U':np.array([ [self.eps*_,0,0] for _ in x[:,0] ]),
                'P':self.P0,
                }

class UndrainedShear():
    def __init__(self, params=default_parameters):
        self.space_dim = 3
        self.time_dep = False
        self.ptdim = 3
        self.params = params
        K_d  = params['K_d']
        G    = params['G']
        Load = params['Load']
        self.eps = Load / G
        self.sigxx = self.sigyy = self.sigzz = 0.0
        self.sigxy = Load

    def __call__(self, x):
        return {'eps':np.array([[0.0,self.eps,0.0],
                                [self.eps,0.0,0.0],
                                [0.0,0.0,0.0]]),
                'sigma':np.array([[self.sigxx,self.sigxy,0.0],
                                  [self.sigxy,self.sigyy,0.0],
                                  [0.0,  0.0,  self.sigzz]]),
                'U':np.array([ [0,self.eps*_,0] for _ in x[:,0] ]),
                'P':0.0,
        }

def isotropic(parameters):
    pass

def random_patch(parameters):
    pass

tests = [UndrainedUniaxial, UndrainedShear]