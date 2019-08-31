from __future__ import print_function

description = """
This file contains the analytical solution to the heat equation on a line
domain from [0,1].

The solutions it returns are of u(x,t).

du/dt =  k d^2/dx^2 u + f
u(0,t) = 0
u(1,t) = 0
u(x,0) = u0(x)

The parameters f and u0 are functions of x; this class does the work in sympy 
to generate the solution from the Green's funciton.
This is a good one to converge to numerically.

Andrei D Polyanin, 2005, http://eqworld.ipmnet.ru/en/solutions/lpde/heat-toc.pdf
"""

import sympy
import numpy as np
default_parameters = {
    'k':1.0,
    'f': lambda x : 0.0,
    'u0': lambda x : 4*x*(1-x)
}

class HeatEquation1D():
    name = 'HeatEquation1D'
    space_dim = 1
    time_dep = True
    ptdim = 2
    outputs = ['u']
    def __init__(self,in_params=None):
        params = default_parameters.copy()
        if in_params:
            params.update(in_params)
        self.params = params
        # Yoink out the parameters
        self.k = params['k']
        u0 = params['u0']
        f = params['f']
        n,xi = sympy.symbols('n xi',positive=True)
        green1 = sympy.integrate(sympy.sin(n*sympy.pi*xi)*u0(xi),(xi,0,1))
        term1 = sympy.lambdify([n],green1)
        self.terms = [ term1(n) for n in range(1,21) ]
        print(self.terms)
    def __call__(self, xt):
        tot = np.zeros(xt.shape[0])
        for nminus1,tn in enumerate(self.terms):
            n = nminus1+1
            tot += 2.0*np.sin(n*np.pi*xt[:,0])*np.exp(-self.k*n**2*np.pi**2*xt[:,1])*tn
        return {'u':tot}

tests = [HeatEquation1D]
