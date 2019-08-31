description = """
This file contains the analytical solution to the heat equation on a square
domain.

The solutions it returns are of T(x,y,t).

dT/dt = div k grad T + f

This is a good one to converge to numerically.
"""

default_parameters = {
    'K_d': 10.0e9,
    'K_s': 100.0*10.0e9,
    'K_f':1.0e11,
    'phi':0.22,
    'k':1.0e-13,
    'eta':1.0e-3,

    'source':-1.0e5,
}

class SquareHomogenousHeatEquation():
    name = 'StaticSquarePoisson'
    space_dim = 2
    time_dep = False
    ptdim = 3
    def __init__(self,in_params=None):
        params = default_parameters.copy()
        if in_params:
            params.update(in_params)
        self.params = params
        # Yoink out the parameters
        K_d = params['K_d']
        K_s = params['K_s']
        K_f = params['K_f']
        phi = params['phi']
        k_eta = params['k']/params['eta']
        domH = 1.0
        self.source = params['source']
        # Only onle coefficent
        alpha = biot = 1.0 - K_d / K_s
        M = K_s/(alpha-phi*(1.0-K_s/K_f))
        self.k = k_eta / self.source
    def __call__(self, xt):
        pass
        return {'P':self.P(xt[:,0],xt[:,1], xt[:,2])}

class SquareForcedHeatEquation():
    name = 'StaticSquarePoisson'
    space_dim = 2
    time_dep = False
    ptdim = 3
    def __init__(self,in_params=None):
        params = default_parameters.copy()
        if in_params:
            params.update(in_params)
        self.params = params
        # Yoink out the parameters
        K_d = params['K_d']
        K_s = params['K_s']
        K_f = params['K_f']
        phi = params['phi']
        k_eta = params['k']/params['eta']
        domH = 1.0
        self.source = params['source']
        # Only onle coefficent
        alpha = biot = 1.0 - K_d / K_s
        M = K_s/(alpha-phi*(1.0-K_s/K_f))
        self.k = k_eta / self.source
    def __call__(self, xt):
        pass
        return {'P':self.P(xt[:,0],xt[:,1], xt[:,2])}

tests = [SquareHomogenousHeatEquation, SquareForcedHeatEquation]
