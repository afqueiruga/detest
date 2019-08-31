"""
These are constant strain problems for mechanics.

A finite element code will solve these to within machine precision. Codes
based on non-standard "theories" or models will not necessarily capture
these. It is imperative that a mechanics solver pass these as ExactTests.
"""

import numpy as np

default_parameters = {
    'K': 10.0e9,
    'G': 10.0e9,

    'Load':-1.0e5,
}

class Uniaxial():
    name = "mechanics_constant_Uniaxial"
    space_dim = 3
    time_dep = False
    ptdim = 3
    outputs = ['sigma','U']
    def __init__(self, in_params=None):
        params = default_parameters.copy()
        if in_params:
            params.update(in_params)
        self.params = params
        K_d  = params['K']
        G    = params['G']
        Load = params['Load']
        self.eps = Load / (K_d+4.0*G/3.0)
        self.sigyy = Load
        self.sigxx = self.sigzz = Load * (3.0*K_d-2.0*G)/(3.0*K_d+4.0*G)
        self.sigxy = 0.0
    def __call__(self, x):
        return {#'eps':np.array([[0.0,0.0,0.0],
                #                [0.0,self.eps,0.0],
                #                [0.0,0.0,0.0]]),
                'sigma':np.array([[self.sigxx,self.sigxy,0.0],
                                  [self.sigxy,self.sigyy,0.0],
                                  [0.0,  0.0,  self.sigzz]]),
                'U':np.array([ [0,self.eps*_,0] for _ in x[:,1] ])
                }

class Shear():
    name = "mechanics_constant_Shear"
    space_dim = 3
    time_dep = False
    ptdim = 3
    outputs = ['sigma','U']
    def __init__(self, in_params=None):
        params = default_parameters.copy()
        if in_params:
            params.update(in_params)
        self.params = params
        K_d  = params['K']
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
                'U':np.array([ [0,self.eps*_,0] for _ in x[:,0] ])
        }



class isotropic():
    def __init__(self,params):
        pass
    def __call__(self,x,y,z):
        return {}
class random_patch():
    def __init__(self,params):
        pass
    def __call__(self,x,y,z):
        return {}


# A list of the ones in here in case you want to loop
tests = [Uniaxial, Shear]
