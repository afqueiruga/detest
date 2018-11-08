import numpy as np

"""
This file contains the analytical solution to de Leeuw's consolidation
problem. It's similar to Mandel's problem, but is cylindrically symmetric.

It's a dynamic problem with one spatial dimension, radius.
The solutions it returns are P(r,t) and U(r,t).

This is a good one to converge to numerically.
"""

from sympy import erf, besselj, var, nsolve, pi, cos, exp, Sum, lambdify
from scipy.special import erf as sperf

parameters = {
    'K_d': 10.0e9,
    'G': 10.0e9,
    'K_s': 100.0*10.0e9,
    'K_f':1.0e11,
    'phi':0.22,
    'k':1.0e-13,
    'eta':1.0e-3,

    'R':10.0,
    'Load':-1.0e5,
}



def solution(params):
    # Yoink out the parameters
    K_d = params['K_d']
    G = params['G']
    K_s = params['K_s']
    K_f = params['K_f']
    phi = params['phi']
    k = params['k']
    eta = params['eta']

    domR = params['R']
    Load = params['Load']

    alpha = 1.0-K_d/K_s
    S  = phi/K_f+(alpha-phi)/K_s
    p0 = alpha / ( alpha**2 + S*(K_d+1.0/3.0*G) ) * Load
    m  = 0.5*eta*(alpha**2+S*(K+G/3))/(alpha**2)
    c  = ( k/eta )/(  S+alpha**2/(K_d+4.0/3.0*G)  )

    var('xi')
    J0 = lambda x : besselj(0,x)
    J1 = lambda x : besselj(1,x)
    g=(2*m*xi*J0(xi)-J1(xi))
    xi_j = [ nsolve(g,xi,j) for j in np.linspace(0,39,14) ]

    term = lambda r,t,j : ( J0(xi_j[j])-J0(xi_j[j]*r/R) )/\
        ( (1-m*xi_j[j]**2-0.25*m)*J0(xi_j[j]) ) \
        * exp(-xi_j[j]**2*c*t/R**2)

    def P(r,t):
        return sum([term(r,t,i) for i in range(1,13)])
    def U(r,t):
        # TODO put in the u solution. Is there one?
        return 0.0
    return {'P':P}
