import numpy as np

name = "odes"

description = """
This file contains some basic ODEs with analytical solutions
"""

default_parameters = {
'x0':1.0,
'v0':0.0,
'u0':0.0,
'm':1.0,
'k':2.0,
'f':3.0,
'T_max':10.0
}

class Decay():
    """
    du / dt = - k u
    """
    name = "Decay"
    space_dim = 0
    time_dep = True
    ptdim = 1
    def __init__(self,params=default_parameters):
        self.params = params
    def __call__(self,t):
        u = - self.params['u0']*np.exp( self.params['k']*t)
        return {'u':u}

class Oscillator():
    """
    Classical harmonic oscillator

    dx / dt = v
    m dv / dt = -k x
    """
    name = "Oscillator"
    space_dim = 0
    time_dep = True
    ptdim = 1
    def __init__(self,params=default_parameters):
        self.params = params
        self.omega = np.sqrt(self.params['k'] / self.params['m'])
        self.amplitude = self.params['x0'] # TODO
        self.phase = 0.0

    def __call__(self,t):
        x = self.amplitude * np.cos(self.omega * t + self.phase)
        v = - self.amplitude*self.omega * np.sin(self.omega * t + self.phase)
        return {'x':x,'v':v}

class ElectricCurrentDAE():
    """

    Watch out: This one is not a normal ODE
    """
    name = "ElectricCurrentDAE"
    space_dim = 0
    time_dep = True
    ptdim = 1
    def __init__(self,params=default_parameters):
        self.params = params
    def __call__(self,t):
        x = t
        v = t
        T = t
        I = t
        return {'x':x,'v':v,'T':T,'I':I}

tests = [Decay, Oscillator, ElectricCurrentDAE]
