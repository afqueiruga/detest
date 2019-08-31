"""
Constant flow production from an infinitely large reservoir, with poromechanics.


"""

import numpy as np
from scipy.special import exp1

default_parameters = {
    'K_d': 10.0e9,
    'G': 10.0e9,
    'K_s': 100.0*10.0e9,
    'K_f':1.0e11,
    'phi':0.22,
    'k':1.0e-13,
    'eta':1.0e-3,

    'Q':-1.0e5,
    'P_background' : 9.5e6,
}

class PoroelasticWell():
    name = "PoroelasticWell"
    space_dim = 1
    time_dep = True
    ptdim = 2
    outputs = ['P','U']
    def __init__(self,in_params=None):
        params = default_parameters.copy()
        if in_params:
            params.update(in_params)
        self.params = params
        # Yoink out the parameters
        K_d = params['K_d']
        G = params['G']
        K_s = params['K_s']
        K_f = params['K_f']
        phi = params['phi']
        k_eta = params['k']/params['eta']

        P_background = params['P_background']
        Q_s = params['Q']
        alpha = 1.0 - K_d/K_s

        M = K_s/(alpha-phi*(1.0-K_s/K_f))
        # K_u = alpha**2*M + K_d
        # K_u = (K_d + alpha**2*M)  * 12.0*K_d/(21.0*K_d-9.0*alpha**2*M) # Mark's
        K_u = K_d * (12*alpha**2*M + 21*K_d)/( 21*K_d - 9*alpha**2*M)
        H = K_u + 4.0*G/3.0
        D = k_eta*(M - alpha**2 * M**2 /H)
        # D = k_eta * M * (K_d+4.0*G/3.0) / (K_u+4.0*G/3)
        def U(r,t):
            xi = r**2/(4.0*D*t)
            f_xi = (1 - np.exp(-xi) ) / xi + exp1(xi)
            return Q_s * alpha * f_xi * r / ( 8.0*np.pi*k_eta* (K_d + 4.0*G/3.0) )

        def P(r,t):
            xi = r**2/(4.0*D*t)
            return Q_s / (4.0*np.pi*k_eta) * exp1(xi) + P_background

        self.U = U
        self.P = P

    def __call__(self, xt):
        return {'P':self.P(xt[:,0],xt[:,1]),
                'U':self.U(xt[:,0],xt[:,1])}

tests = [ PoroelasticWell ]
