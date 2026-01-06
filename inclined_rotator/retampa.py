"""
takes ultranest solution and creates the model and data
"""
import sys
import numpy as np

from filter_response import FilterResponseModel
FilterResponse  = FilterResponseModel ("filter_response.npz")

import json

tag    = sys.argv[1]
ud     = f"gs_unr_{tag}/run1"
# of     = f"gs_ampa_{tag}.npz"
################################
FAC    = 100.
with np.load ("combvarystream.npz") as rs:
    ## further slice it
    ## ustart:ustop
    LONGS    = np.array ( rs['longs'] )
    LSIZE    = LONGS.size
    DATA_III = np.array ( rs[f'I_{tag}'] )
    DATA_IPQ = np.array ( rs[f'I+Q_{tag}'] )
    DATA_IMQ = np.array ( rs[f'I-Q_{tag}'] )
    DATA_IPU = np.array ( rs[f'I+U_{tag}'] )
    DATA_IMU = np.array ( rs[f'I-U_{tag}'] )
################################
### create grid
def get_grids ( asize=512, psize=512 ):
    AMPG   = np.linspace ( 0., 5, asize )
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
    # GIPQ  = GIPQ.reshape ( (1, asize, psize) )
    # GIMQ  = GIMQ.reshape ( (1, asize, psize) )
    # GIPU  = GIPU.reshape ( (1, asize, psize) )
    # GIMU  = GIMU.reshape ( (1, asize, psize) )
    ###
    return PAG, AMPG, GIPQ, GIMQ, GIPU, GIMU

ASIZE = 512
PSIZE = 2048
PAG, AMPG, GIPQ, GIMQ, GIPU, GIMU = get_grids (ASIZE, PSIZE)
################################
pp    = 1.0
def get_pa ( fipq, fimq, fipu, fimu ):
    """
    performs grid search pa
    """
    MAMP = np.zeros_like ( LONGS )
    MPA  = np.zeros_like ( LONGS )
    SAMP = np.zeros_like ( LONGS )
    SPA  = np.zeros_like ( LONGS )
    FEX  = np.zeros_like ( LONGS )
    for i, long in enumerate ( LONGS ):
        #### griding
        # e1 = FAC * ( ( DATA_III[i] * fipq * GIPQ ) - DATA_IPQ[i] ) ** 2
        # e2 = FAC * ( ( DATA_III[i] * fimq * GIMQ ) - DATA_IMQ[i] ) ** 2
        # e3 = FAC * ( ( DATA_III[i] * fipu * GIPU ) - DATA_IPU[i] ) ** 2
        # e4 = FAC * ( ( DATA_III[i] * fimu * GIMU ) - DATA_IMU[i] ) ** 2
        e1 = ( ( fipq * GIPQ ) - DATA_IPQ[i] ) ** 2
        e2 = ( ( fimq * GIMQ ) - DATA_IMQ[i] ) ** 2
        e3 = ( ( fipu * GIPU ) - DATA_IPU[i] ) ** 2
        e4 = ( ( fimu * GIMU ) - DATA_IMU[i] ) ** 2
        le1 = np.log10 ( e1 )
        le2 = np.log10 ( e2 )
        le3 = np.log10 ( e3 )
        le4 = np.log10 ( e4 )
        #### full e
        eeee   = e1 + e2 + e3 + e4
        llll   = (1.0 * (le1 < -4)) + (1.0 * (le2 < -4)) + (1.0 * (le3 < -4)) + (1.0 * (le4 < -4))
        # eeee   = e1 + e2 + e3 + e4
        # eeee   =np.sqrt ( e1 + e2 + e3 + e4 )
        # eeee     = e1 * e2 * e3 * e4
        # eeee     = np.power ( 
            # np.power ( e1, pp ) +
            # np.power ( e2, pp ) +
            # np.power ( e3, pp ) +
            # np.power ( e4, pp ) 
            # , 1.0 / pp
        # )
        ####
        # __amin, __pmin = np.unravel_index ( np.argmin ( eeee ), eeee.shape )
        __max__   = llll.max()
        if __max__ < 3: continue
        __lamin, __lpmin   = np.where ( llll == __max__ )
        __le       = eeee [ __lamin, __lpmin ]
        __ale      = np.argmin ( __le )
        __amin     = __lamin[ __ale ]
        __pmin     = __lpmin[ __ale ]

        MAMP [ i ] = AMPG [ __amin ]
        # SAMP [ i ] = AMPG [ __amin ].std()
        MPA [ i ]  = PAG [ __pmin ]
        # SPA [ i ]  = PAG [ __pmin ].std()
        FEX [ i ]  = eeee [ __amin, __pmin ]
        # FEX [ i ]  = eeee [ __amin, __pmin ].sum()
    return MAMP, MPA, FEX, SAMP, SPA

def tester(undir, opts={}):
    """
    find those filter terms which minimize the total objective.
    """
    ##
    with open (f"{undir}/info/results.json", 'r') as _f:
        js = json.load ( _f )
        ml = js['maximum_likelihood']
        FIPQ, FIMQ, FIPU, FIMU = ml['point']
    ##
    RET = dict()
    RET['longs']  = LONGS
    RET['fipq']  = FIPQ
    RET['fimq']  = FIMQ
    RET['fipu']  = FIPU
    RET['fimu']  = FIMU
    ###
    RET['amp'], RET['pa'], RET['fex'], RET['eamp'], RET['epa']  = get_pa ( RET['fipq'], RET['fimq'], RET['fipu'], RET['fimu'] )
    ### filter response
    _ipq, _imq, _ipu, _imu = FilterResponse.get_responses ( RET['pa'] )
    ### get models
    ipq_model = RET['amp'] * RET['fipq'] * _ipq
    imq_model = RET['amp'] * RET['fimq'] * _imq
    ipu_model = RET['amp'] * RET['fipu'] * _ipu
    imu_model = RET['amp'] * RET['fimu'] * _imu
    RET['model_ipq'] = ipq_model
    RET['model_imq'] = imq_model
    RET['model_ipu'] = ipu_model
    RET['model_imu'] = imu_model
    RET['data_ipq']  = DATA_IPQ
    RET['data_imq']  = DATA_IMQ
    RET['data_ipu']  = DATA_IPU
    RET['data_imu']  = DATA_IMU
    RET['data_iii']  = DATA_III
    return RET
################################

if __name__ == "__main__":
    RET = tester ( ud )
    # np.savez (of, **RET )
