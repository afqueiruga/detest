"""The traditional nonlinear pendulum with R=1."""

import numpy as np
from scipy.special import ellipj, ellipk


class PendulumTheta():
    """
    The fully nonlinear pendulum, in theta

    d^theta / dt^2 = g sin(theta)
    """
    name = "PendulumTheta"
    space_dim = 0
    time_dep = True
    ptdim = 1
    outputs = ['theta', 'v']
    default_parameters = {
        'theta0': 1.0,
        'v0': 0.0,
        'g': 9.81,
    }

    def __init__(self, in_params=None):
        self.params = self.default_parameters.copy()
        if in_params: self.params.update(in_params)
        self.g = self.params['g']

    def __call__(self, t):
        S = np.sin(0.5 * (self.theta0))
        K_S = ellipk(S**2)
        omega_0 = np.sqrt(9.81)
        sn, cn, dn, ph = ellipj(K_S - omega_0 * t, S**2)
        theta = 2.0 * np.arcsin(S * sn)
        d_sn_du = cn * dn
        d_sn_dt = -omega_0 * d_sn_du
        d_theta_dt = 2.0 * S * d_sn_dt / np.sqrt(1.0 - (S * sn)**2)
        return {'theta': theta, 'v': d_theta_dt}


class PendulumXY():
    """
    The fully nonlinear pendulum, in x,y

    d^theta / dt^2 = g sin(theta)
    """
    name = "PendulumXY"
    space_dim = 0
    time_dep = True
    ptdim = 1
    outputs = ['x', 'y', 'vx', 'vy']
    default_parameters = {
        'theta0': 1.0,
        'v0': 0.0,
        'T_max': 10.0,
        'g': 9.81,
    }

    def __init__(self, in_params=None):
        self.params = self.default_parameters.copy()
        if in_params: self.params.update(in_params)
        self.g = self.params['g']

    def __call__(self, t):
        S = np.sin(0.5 * (self.theta0))
        K_S = ellipk(S**2)
        omega_0 = np.sqrt(9.81)
        sn, cn, dn, ph = ellipj(K_S - omega_0 * t, S**2)
        theta = 2.0 * np.arcsin(S * sn)
        d_sn_du = cn * dn
        d_sn_dt = -omega_0 * d_sn_du
        d_theta_dt = 2.0 * S * d_sn_dt / np.sqrt(1.0 - (S * sn)**2)
        return {
            'x': np.cos(theta),
            'y': np.sin(theta),
            'vx': -d_theta_dt * np.sin(theta),
            'vy': d_theta_dt * np.cos(theta),
        }


tests = [PendulumXY, PendulumTheta]
