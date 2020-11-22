"""Westergard's solution for a thin crack in tension.

Returns a displacment that's functions of x,y, with the crack at the center.

The trick to this problem is to use the analytical solution as the outer
dirrichlet boundary conditions because the true BCs are at infinity.

Note: this problem is discontinuous across y=0, x in [-c,c].

TODO Migrate from periflakes. See:
https://github.com/afqueiruga/PeriFlakes/blob/9db16490b2579582310634b4f2ca23d53028ac1d/PeriFlakes/lfm.py#L23
"""

parameters = {
    'K': 10.0e9,
    'G': 10.0e9,
    'W': 1.0,
    'Lcrack': 0.1,
    'Load': 10.0,
}


class ThinCrack():
    name = "ThinCrack"
    space_dim = 2
    time_dep = False
    ptdim = 2

    def __init__(self, params):
        def U(x, u):
            pass

        self.U = U

    def __call__(self, x):
        return {'U': U}
