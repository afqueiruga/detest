import numpy as np

name = "terzaghi"

description = """
This file contains the analytical solution to Terzaghi's consolidation problem.

It's a dynamic problem with one spatial dimension, height.
The solutions it returns are P(z,t) and U(z,t).

This is a good one to converge to numerically.
"""

default_parameters = {
    'K_d': 10.0e9,
    'G': 10.0e9,
    'K_s': 100.0*10.0e9,
    'K_f':1.0e11,
    'phi':0.22,
    'k':1.0e-13,
    'eta':1.0e-3,

    'H':100.0,
    'Load':-1.0e5,
    'P_background':0.0,
}

class Terzaghi():
    name = "Terzaghi"
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
        P_back = params['P_background']
        domH = params['H']
        Load = params['Load']

        # Poisson Ratio
        nu = (3.0*K_d - 2.0*G)/(6.0*K_d+2.0*G)

        alpha = biot = 1.0 - K_d / K_s
        Q = K_d/alpha
        H = K_d+4.0*G/3.0
        M = K_s/(alpha-phi*(1.0-K_s/K_f))
        K_u = alpha**2*M + K_d
        a = 1.0/H#( 1.0 - 2.0*nu) / ( 2.0*G*(1.0-nu) )
        ai = 1.0/(K_u + 4.0*G/3.0)

        p0 = -alpha/H / ( 1.0/M + alpha**2/H) * Load
        Cf = (k_eta) / ( a * alpha**2.0 + 1.0/M )
        uinf = a * Load * domH
        pressure_mass = biot/K_d

        def P(z,t):
            term = lambda m, z,t : 1.0/(2.0*m+1.0) \
                   * np.exp( - ((2.0*m+1.0)*np.pi/(2.0*domH))**2 * Cf * t ) \
                   * np.sin( (2.0*m+1.0)*np.pi/(2.0*domH) * z )
            return P_back + 4.0/np.pi* p0 * np.sum( [term(m, z,t) for m in np.arange(0.0,30.0) ],axis=0)

        def U(z,t):
            term = lambda m, z,t : 1.0/(2.0*m+1.0)**2 \
                   * np.exp( - ((2.0*m+1.0)*np.pi/(2.0*domH))**2 * Cf * t ) \
                   * np.cos( (2.0*m+1.0)*np.pi/(2.0*domH) * z )
            return a*Load*(domH-z) - 8.0/(np.pi**2) * (a-ai)*(domH)*Load\
                * np.sum( [term(m, z,t) for m in np.arange(0.0,30.0) ], axis=0)
        self.P = P
        self.U = U
    def __call__(self, xt):
        return {'P':self.P(xt[:,0],xt[:,1]),
                'U':self.U(xt[:,0],xt[:,1])}


tests = [Terzaghi]
