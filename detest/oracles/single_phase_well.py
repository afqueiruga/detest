"""
Constant flow production from an infinitely large reservoir, without poromechanics.


"""

import numpy as np
from scipy.special import exp1

default_parameters = {
    'K_s': 100.0*10.0e9,
    'K_f':2.24e9,
    'phi':0.22,
    'k':1.0e-13,
    'eta':1.0e-3,

    'Q':-1.0e5,
    'P_background' : 9.5e6,
}

class SinglePhaseWell():
    name = "SinglePhaseWell"
    space_dim = 1
    time_dep = True
    ptdim = 2
    default_params = default_parameters
    outputs = ['P']
    def __init__(self,in_params=None):
        params = self.default_params.copy()
        if in_params:
            params.update(in_params)
        self.params = params
        # Yoink out the parameters
        K_s = params['K_s']
        K_f = params['K_f']
        phi = params['phi']
        k_eta = params['k']/params['eta']

        P_background = params['P_background']
        Q_s = params['Q']
        #alpha = 1.0 - K_d/K_s

        M = K_f/phi #?
        D = k_eta*M

        # TODO This is wrong
        def P(r,t):
            xi = r**2/(4.0*D*t)
            return Q_s / (4.0*np.pi*k_eta) * exp1(xi) + P_background

        self.P = P

    def __call__(self, xt):
        return {'P':self.P(xt[:,0],xt[:,1])}


class SteadySinglePhaseWell():
    name = "SteadySinglePhaseWell"
    space_dim = 1
    time_dep = False
    ptdim = 1
    default_params = default_parameters
    outputs = ['P']
    def __init__(self,in_params=None):
        params = self.default_params.copy()
        if in_params:
            params.update(in_params)
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
        K_u = alpha**2*M + K_d
        H = K_u + 4.0*G/3.0
        D = k_eta*(M - alpha**2 * M**2 /H)

        # TODO This is wrong
        def P(r):
            xi = r**2/(4.0*D*t)
            return Q_s / (4.0*np.pi*k_eta) * exp1(xi) + P_background

        self.P = P

    def __call__(self, xt):
        return {'P':self.P(xt[:,0],xt[:,1])}


tests = [ SinglePhaseWell ]
