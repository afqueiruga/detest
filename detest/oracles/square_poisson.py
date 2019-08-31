import numpy as np

description = """
This file contains the analytical solution to the square Poisson problem.

The solutions it returns are P(x,y).

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

class SquarePoisson():
    name = 'StaticSquarePoisson'
    space_dim = 2
    time_dep = False
    ptdim = 3
    def __init__(self,params=default_parameters):
        self.params = params.copy()
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
        k = self.k
        panal = np.empty(X.shape[0])
        t = lambda k,x,y : np.sin(k*np.pi*(1.0+x)/2.0)/( k*k*k * np.sinh( k*np.pi )) * \
            ( np.sinh( k*np.pi*(1.0+y)/2.0 ) + np.sinh( k*np.pi*(1.0-y)/2.0) )
        for i,y in enumerate(X):
            panal[i] = (1.0-xt[0]**2.0)/2.0 - 16.0/(np.pi)**3 * \
                sum([t(k,yt[0],yt[1]) for k in xrange(1,101,2) ])
        return {'P':panal}


tests = [SquarePoisson]
