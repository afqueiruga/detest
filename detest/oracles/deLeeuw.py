from __future__ import print_function
import numpy as np

"""
This file contains the analytical solution to de Leeuw's consolidation
problem. It's similar to Mandel's problem, but is cylindrically symmetric.

It's a dynamic problem with one spatial dimension, radius.
The solutions it returns are P(r,t) and U(r,t).

This is a good one to converge to numerically.

Verruijt, Theory and Problems in Poroelasticity, 2013
"""

from sympy import erf, besselj, var, nsolve, pi, cos, exp, Sum, lambdify
from scipy.special import erf as sperf

default_parameters = {
    'K_d': 10.0e9,
    'G': 10.0e9,
    'K_s': 100.0*10.0e9,
    'K_f':1.0e11,
    'phi':0.22,
    'k':1.0e-13,
    'eta':1.0e-3,

    'R':10.0,
    'Load':-1.0e5,
    'P_background':0.0,
}


class DeLeeuw():
    name = "DeLeeuw"
    space_dim = 1
    time_dep = True
    ptdim = 2
    outputs = ['P',]
    def __init__(self, in_params=None):
        params = default_parameters
        if in_params:
            params.update(in_params)
        self.params = params
        # Yoink out the parameters
        K_d = params['K_d']
        G = params['G']
        K_s = params['K_s']
        K_f = params['K_f']
        phi = params['phi']
        k = params['k']
        eta = params['eta']

        R = params['R']
        Load = params['Load']

        alpha = 1.0-K_d/K_s
        S  = phi/K_f+(alpha-phi)/K_s
        p0 = -alpha / ( alpha**2 + S*(K_d+1.0/3.0*G) ) * Load
        m  = 0.5* ( K_d+4.0*G/3.0 )/( 2.0*G )  * (alpha**2+S*(K_d+G/3.0))/(alpha**2)
        # c  = ( k/eta )/(  S+alpha**2/(K_d+4.0/3.0*G)  )
        c = (k/eta) * ( K_d+4.0*G/3.0 )/( alpha**2 + S*(K_d+4.0*G/3.0) )
        var('xi')
        J0 = lambda x : besselj(0,x)
        J1 = lambda x : besselj(1,x)
        g=(2*m*xi*J0(xi)-J1(xi))
        # xi_j = [ nsolve(g,xi,j) for j in np.linspace(0,39,14) ]
        xi_j = [nsolve(g,xi,0)]
        for j in range(50):
            last = xi_j[-1]
            new = nsolve(g,xi,(last+1.0e-4,last+(1.2*pi.evalf())),solver='bisect' )
            xi_j.append(new)
        print(xi_j)
        term = lambda r,t,j : ( J0(xi_j[j])-J0(xi_j[j]*r/R) )/\
            ( (1-m*xi_j[j]**2-0.25*m)*J0(xi_j[j]) ) \
            * exp(-xi_j[j]**2*c*t/R**2)

        def P(r,t):
            return np.array([
                sum([float(p0*term(r_,t_,i).evalf()) for i in range(len(xi_j))])
                for r_,t_ in zip(r,t) ]) + params['P_background']
        def U(r,t):
            # TODO put in the u solution. Is there one?
            return np.array([0.0])
        self.P = P
        self.U = U
    def __call__(self, xt):
        return {'P':self.P(xt[:,0],xt[:,1])}
                # 'U':self.U(xt[:,0],xt[:,1])}

tests = [DeLeeuw]