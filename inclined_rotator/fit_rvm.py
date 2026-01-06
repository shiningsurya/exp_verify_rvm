"""
fit for period, alpha, zeta, phi0, pa0

can also make it {period, alpha, zeta}
"""

import os
import numpy as np

from scipy.optimize import minimize

from filter_response import FilterResponseModel
FilterResponse  = FilterResponseModel ("filter_response.npz")

import ultranest
import ultranest.stepsampler

################################
# FIPQ  = 0.3672
# FIMQ  = 0.1109
# FIPU  = 0.5167
# FIMU  = 0.2885
FIPQ, FIMQ, FIPU, FIMU  = 2.236, 1.357, 4.107, 2.022
################################
FAC    = 100.
# with np.load ("restream.npz") as rs:
with np.load ("combvarystream.npz") as rs:
    LONGS    = np.array ( rs['longs'] )
    DATA_III = FAC * np.array ( rs['I_ra'] )
    DATA_IPQ = FAC * np.array ( rs['I+Q_ra'] )
    DATA_IMQ = FAC * np.array ( rs['I-Q_ra'] )
    DATA_IPU = FAC * np.array ( rs['I+U_ra'] )
    DATA_IMU = FAC * np.array ( rs['I-U_ra'] )
################################
def get_rvm (long, alpha, zeta, phi0, pa0=0. ):
    """
    RVM model
    input is radians
    output is radians

    from Everett+Weisberg
    """
    nr  = np.sin ( alpha ) * np.sin ( long - phi0 )
    dr  = ( np.sin ( zeta ) * np.cos ( alpha ) ) - ( np.cos( zeta ) * np.sin ( alpha ) * np.cos ( long - phi0 ) )
    # pa  = pa0 - np.arctan ( nr / dr )
    pa  = pa0 + np.arctan ( nr / dr )
    ##
    pa  = np.arctan ( np.tan ( pa ) )
    return pa

# PARAM_NAMES = ['ALPHA','ZETA', 'PHI0', 'PA0'] 
# WRAPPED     = [False, False, True, False]
# PARAM_NAMES = ['ALPHA','ZETA', 'PHI0'] 
# WRAPPED     = [False, False, True ]
PARAM_NAMES = ['ALPHA','ZETA', 'PHI0'] 
WRAPPED     = [False, False, True]
def prior_transform (cube):
    """ 
    prior transform 

    """

    params      = np.zeros_like ( cube )
    # alpha
    params[0]   = np.pi * cube[0]
    # zeta
    params[1]   = np.pi * cube[1]
    # phi0
    params[2]   = 2.0 * np.pi * cube[2]
    # params[2]   = 0.5*np.pi +  np.pi * cube[2]
    # pa0
    # params[3]   = (-0.5*np.pi) + (np.pi * cube[3])
    return params

def log_likelihood ( params ):
    """
    log likelihood
    """
    model_pa    = get_rvm ( LONGS, *params )
    ####
    G_ipq, G_imq, G_ipu, G_imu = FilterResponse.get_responses ( model_pa )
    model_ipq   = DATA_III * FIPQ * G_ipq
    model_imq   = DATA_III * FIMQ * G_imq
    model_ipu   = DATA_III * FIPU * G_ipu
    model_imu   = DATA_III * FIMU * G_imu
    ll          = -0.5 * np.sum ( 
        (model_ipq - DATA_IPQ)**2 +
        (model_imq - DATA_IMQ)**2 +
        (model_ipu - DATA_IPU)**2 +
        (model_imu - DATA_IMU)**2 
    )
    return ll

sampler             = ultranest.ReactiveNestedSampler (
    # ['ALPHA','ZETA'], 
    PARAM_NAMES,
    log_likelihood, prior_transform,
    num_test_samples = 100,
    wrapped_params = WRAPPED,
    draw_multiple = True,
    num_bootstraps = 100,
    log_dir = "justfitrvm"
)
sampler.stepsampler = ultranest.stepsampler.SliceSampler (
    nsteps = 128,
    generate_direction = ultranest.stepsampler.generate_cube_oriented_differential_direction,
    adaptive_nsteps='move-distance',
)
result              = sampler.run (
    min_num_live_points = 2048,
    frac_remain = 1E-6,
    min_ess = 1024,
)
# result = dict()
###
sampler.store_tree ()
sampler.print_results ()
sampler.plot_corner ()
