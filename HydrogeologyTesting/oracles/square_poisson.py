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
    'K_s': 100.0*10.0e9,
    'K_f':1.0e11,
    'phi':0.22,
    'k':1.0e-13,
    'eta':1.0e-3,

    'source':-1.0e5,
}

class SquarePoisson():
    name = 'SquarePoisson'
    space_dim = 2
    time_dep = True
    ptdim = 3
    def __init__(self,params=default_parameters):

        self.params = params
        # Yoink out the parameters
        K_d = params['K_d']
        K_s = params['K_s']
        K_f = params['K_f']
        phi = params['phi']
        k_eta = params['k']/params['eta']

        domH = 1.0
        source = params['source']

        # Poisson Ratio
        nu = (3.0*K_d - 2.0*G)/(6.0*K_d+2.0*G)

        alpha = biot = 1.0 - K_d / K_s

        M = K_s/(alpha-phi*(1.0-K_s/K_f))


    def __call__(self, xt):
        k = self.params['k']/self.params['eta']
        panal = np.empty(X.shape[0])
        t = lambda k,x,y : np.sin(k*np.pi*(1.0+x)/2.0)/( k*k*k * np.sinh( k*np.pi )) * \
            ( np.sinh( k*np.pi*(1.0+y)/2.0 ) + np.sinh( k*np.pi*(1.0-y)/2.0) )
        for i,y in enumerate(X):
            panal[i] = (1.0-y[0]**2.0)/2.0 - 16.0/(np.pi)**3 * \
                sum([t(k,y[0],y[1]) for k in xrange(1,101,2) ])
        return panal

        return {'P':self.P(xt[:,0],xt[:,1]),
                'U':self.P(xt[:,0],xt[:,1])}


tests = [Terzaghi]
