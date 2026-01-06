"""
fit for greeks using ultranest

for every range
"""
import os
import sys
import numpy as np

import ultranest
import ultranest.stepsampler

from filter_response import FilterResponseModel
FilterResponse  = FilterResponseModel ("filter_response.npz")

tag    = sys.argv[1]
ODIR   = f"gs_unr_{tag}"

################################
FAC    = 100.
with np.load ("combvarystream.npz") as rs:
    ## further slice it
    ## ustart:ustop
    SS       = slice ( 113, 397 )
    LONGS    = np.array ( rs['longs'][SS] )
    LSIZE    = LONGS.size
    DATA_IPQ = np.array ( rs[f'I+Q_{tag}'][SS] )
    DATA_IMQ = np.array ( rs[f'I-Q_{tag}'][SS] )
    DATA_IPU = np.array ( rs[f'I+U_{tag}'][SS] )
    DATA_IMU = np.array ( rs[f'I-U_{tag}'][SS] )
################################
### create grid
def get_grids ( asize=512, psize=512 ):
    AMPG   = np.linspace ( 0., 10, asize )
    PAG    = np.linspace ( -0.5*np.pi, 0.5*np.pi, psize )
    ## make amp/pa grid
    amps, pas  = np.meshgrid ( AMPG, PAG, indexing='ij' )
    ### find filter response
    pa_ipq, pa_imq, pa_ipu, pa_imu = FilterResponse.get_responses ( pas )
    ### compute grids
    GIPQ  = amps * pa_ipq
    GIMQ  = amps * pa_imq
    GIPU  = amps * pa_ipu
    GIMU  = amps * pa_imu
    #### broadcast
    # GIPQ  = GIPQ.reshape ( (1, asize*psize) )
    # GIMQ  = GIMQ.reshape ( (1, asize*psize) )
    # GIPU  = GIPU.reshape ( (1, asize*psize) )
    # GIMU  = GIMU.reshape ( (1, asize*psize) )
    ###
    return PAG, AMPG, GIPQ, GIMQ, GIPU, GIMU

ASIZE = 64
PSIZE = 512
PAG, AMPG, GIPQ, GIMQ, GIPU, GIMU = get_grids (ASIZE, PSIZE)
################################
def get_pa ( fipq, fimq, fipu, fimu ):
    """
    performs grid search pa
    """
    MAMP = np.zeros_like ( LONGS )
    MPA  = np.zeros_like ( LONGS )
    FEX  = np.zeros_like ( LONGS )
    for i, long in enumerate ( LONGS ):
        #### griding
        # e1 = FAC * ( ( DATA_III[i] * fipq * GIPQ ) - DATA_IPQ[i] ) ** 2
        # e2 = FAC * ( ( DATA_III[i] * fimq * GIMQ ) - DATA_IMQ[i] ) ** 2
        # e3 = FAC * ( ( DATA_III[i] * fipu * GIPU ) - DATA_IPU[i] ) ** 2
        # e4 = FAC * ( ( DATA_III[i] * fimu * GIMU ) - DATA_IMU[i] ) ** 2
        e1 = FAC * ( ( fipq * GIPQ ) - DATA_IPQ[i] ) ** 2
        e2 = FAC * ( ( fimq * GIMQ ) - DATA_IMQ[i] ) ** 2
        e3 = FAC * ( ( fipu * GIPU ) - DATA_IPU[i] ) ** 2
        e4 = FAC * ( ( fimu * GIMU ) - DATA_IMU[i] ) ** 2
        #### full e
        eeee   = e1 + e2 + e3 + e4
        ####
        __amin, __pmin = np.unravel_index ( np.argmin ( eeee ), eeee.shape )
        MAMP [ i ] = AMPG [ __amin ]
        MPA [ i ]  = PAG [ __pmin ]
        FEX [ i ]  = eeee [ __amin, __pmin ]
    return MAMP, MPA, FEX

PARAM_NAMES = ['fipq','fimq','fipu','fimu'] 
WRAPPED     = [False, False, False, False]

def prior_transform (cube):
    """ 
    prior transform 

    """

    params      = np.zeros_like ( cube )
    ## ffff
    params[0]   = 5.0 * cube[0]
    params[1]   = 5.0 * cube[1]
    params[2]   = 5.0 * cube[2]
    params[3]   = 5.0 * cube[3]
    return params

def log_likelihood ( params ):
    """
    log likelihood
    """
    fipq, fimq, fipu, fimu = params
    _, _, fex         = get_pa ( fipq, fimq, fipu, fimu )
    return -1.0 * fex.sum()

sampler             = ultranest.ReactiveNestedSampler (
    # ['ALPHA','ZETA'], 
    PARAM_NAMES,
    log_likelihood, prior_transform,
    num_test_samples = 10,
    wrapped_params = WRAPPED,
    draw_multiple = True,
    num_bootstraps = 100,
    log_dir = ODIR
)
sampler.stepsampler = ultranest.stepsampler.SliceSampler (
    nsteps = 128,
    generate_direction = ultranest.stepsampler.generate_cube_oriented_differential_direction,
    adaptive_nsteps='move-distance',
)
result              = sampler.run (
    min_num_live_points = 2048,
    frac_remain = 1E-9,
    min_ess = 1024,
)
# result = dict()
###
sampler.store_tree ()
sampler.print_results ()
sampler.plot_corner ()


