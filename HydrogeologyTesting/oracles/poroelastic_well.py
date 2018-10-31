"""
Constant flow production from an infinitely large reservoir, with poromechanics.


"""
parameters = {
    'K_d': 10.0e9,
    'G': 10.0e9,
    'K_s': 100.0*10.0e9,
    'K_f':1.0e11,
    'phi':0.22,
    'k':1.0e-13,
    'eta':1.0e-3,

    'Q':-1.0e5,
}

def solution(params):
    # Yoink out the parameters
    K_d = params['K_d']
    G = params['G']
    K_s = params['K_s']
    K_f = params['K_f']
    phi = params['phi']
    k_eta = params['k']/params['eta']

    domH = params['H']
    Load = params['Load']
