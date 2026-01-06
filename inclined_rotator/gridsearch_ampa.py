"""
numerically fit for greeks
grid search amp, pa
find quality of fit
"""
import numpy as np

from scipy.optimize import minimize

from filter_response import FilterResponseModel
FilterResponse  = FilterResponseModel ("filter_response.npz")

################################
tag    = 'ra'
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
if True:
    off = slice(20,60)
    DATA_III -= DATA_III[off].mean()
    DATA_IPQ -= DATA_IPQ[off].mean()
    DATA_IMQ -= DATA_IMQ[off].mean()
    DATA_IPU -= DATA_IPU[off].mean()
    DATA_IMU -= DATA_IMU[off].mean()
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
    # GIPQ  = GIPQ.reshape ( (1, asize, psize) )
    # GIMQ  = GIMQ.reshape ( (1, asize, psize) )
    # GIPU  = GIPU.reshape ( (1, asize, psize) )
    # GIMU  = GIMU.reshape ( (1, asize, psize) )
    ###
    return PAG, AMPG, GIPQ, GIMQ, GIPU, GIMU

ASIZE = 512
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

_d_ipq    = DATA_IPQ.reshape ((LSIZE, 1, 1))
_d_imq    = DATA_IMQ.reshape ((LSIZE, 1, 1))
_d_ipu    = DATA_IPU.reshape ((LSIZE, 1, 1))
_d_imu    = DATA_IMU.reshape ((LSIZE, 1, 1))
def mem_heavy_get_pa ( fipq, fimq, fipu, fimu ):
    """
    performs grid search pa
    """
    MAMP = np.zeros_like ( LONGS )
    MPA  = np.zeros_like ( LONGS )
    FEX  = np.zeros_like ( LONGS )
    #####
    e1 = FAC * ( ( fipq * GIPQ ) - _d_ipq ) ** 2
    e2 = FAC * ( ( fimq * GIMQ ) - _d_imq ) ** 2
    e3 = FAC * ( ( fipu * GIPU ) - _d_ipu ) ** 2
    e4 = FAC * ( ( fimu * GIMU ) - _d_imu ) ** 2
    #### full e
    eeee   = np.reshape ( e1 + e2 + e3 + e4, (LSIZE, ASIZE*PSIZE) )
    agme   = np.argmin ( eeee, axis=1 )
    ####
    __amin, __pmin = np.unravel_index ( agme, (ASIZE, PSIZE) )
    MAMP = AMPG [ __amin ]
    MPA  = PAG [ __pmin ]
    FEX  = eeee [ range(LSIZE), agme ]
    return MAMP, MPA, FEX

def objective ( x ):
    """
    minimize this
    """
    fipq, fimq, fipu, fimu = x
    _, _, fex = get_pa ( fipq, fimq, fipu, fimu )
    return fex.sum()

def get_model ( fipq, fimq, fipu, fimu ):
    """
    PA from RVM
    """
    ### RVM
    ampt, pat, _  = get_pa ( fipq, fimq, fipu, fimu )
    ### filter response
    _ipq, _imq, _ipu, _imu = FilterResponse.get_responses ( pat )
    ### get models
    ipq_model = ampt * fipq * _ipq
    imq_model = ampt * fimq * _imq
    ipu_model = ampt * fipu * _ipu
    imu_model = ampt * fimu * _imu
    ### return
    return ipq_model, imq_model, ipu_model, imu_model

def stepper(opts={}):
    """
    find those filter terms which minimize the total objective.
    """
    p0  = ( 0.5, 0.5, 0.5, 0.5 )
    # p0  = ( 0.5, 0.5, 0.5 )
    # p0  = ( 0.5,  )
    res = minimize ( 
        objective, p0, 
        # bounds= ( ( 0., 300. ), ),
        # bounds= ( ( 0., 1. ), (0., 1.), (0.,1.), (0., 1.) ),
        bounds= ( ( 0., 3. ), (0.,3.), (0., 3.), (0., 3.) ),
        jac='3-point',
        options=opts
    )
    RET = dict()
    RET['fipq']  = res.x[0]
    RET['fimq']  = res.x[1]
    RET['fipu']  = res.x[2]
    RET['fimu']  = res.x[3]
    # RET['fipq']  = res.x[0]
    # RET['fimq']  = res.x[0]
    # RET['fipu']  = res.x[0]
    # RET['fimu']  = res.x[0]
    # RET['fipq']  = res.x[0]
    # RET['fimq']  = res.x[0]
    # RET['fipu']  = res.x[1]
    # RET['fimu']  = res.x[2]
    ###
    RET['amp'], RET['pa'], RET['fex']    = get_pa ( RET['fipq'], RET['fimq'], RET['fipu'], RET['fimu'] )
    ###
    sipq, simq, sipu, simu   = get_model ( RET['fipq'], RET['fimq'], RET['fipu'], RET['fimu'] )
    RET['model_ipq'] = sipq
    RET['model_imq'] = simq
    RET['model_ipu'] = sipu
    RET['model_imu'] = simu
    RET['data_ipq']  = DATA_IPQ
    RET['data_imq']  = DATA_IMQ
    RET['data_ipu']  = DATA_IPU
    RET['data_imu']  = DATA_IMU
    RET['data_iii']  = DATA_III
    return RET

def tester(opts={}):
    """
    find those filter terms which minimize the total objective.
    """
    ## short.q run
    # FIPQ  = 0.448
    # FIMQ  = 0.284
    # FIPU  = 0.942
    # FIMU  = 0.421
    ## parallel.q run
    # FIPQ  = 0.424083
    # FIMQ  = 0.270866
    # FIPU  = 0.891753
    # FIMU  = 0.399125
    import json
    ##
    # with open ('./gridsearch_un_run/info/results.json', 'r') as _f:
    with open ('gs_unr_ra_fres/info/results.json', 'r') as _f:
        js = json.load ( _f )
        ml = js['maximum_likelihood']
        FIPQ, FIMQ, FIPU, FIMU = ml['point']
    FIPQ, FIMQ, FIPU, FIMU = 0.104, 0.104, 0.104, 0.104
    ##
    RET = dict()
    RET['longs']  = LONGS
    RET['fipq']  = FIPQ
    RET['fimq']  = FIMQ
    RET['fipu']  = FIPU
    RET['fimu']  = FIMU
    ###
    RET['amp'], RET['pa'], RET['fex']    = get_pa ( RET['fipq'], RET['fimq'], RET['fipu'], RET['fimu'] )
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

if __name__ == "__main__":

    # tester ()
    # p0  = ( 0.5, 0.5, 0.5 )
    # out = objective ( p0 )

    ##############################
    # RET = stepper (opts={'disp':True})
    RET = tester (opts={'disp':True})
    np.savez ("numgridsearch_ampa_ra_fres_uno.npz", **RET )
    ##############################
    # frange  = np.linspace ( 1., 5., 1024 )
    # sfx     = np.zeros_like ( frange )

    # for i, f in enumerate ( frange ):
        # _, fex = get_pa ( f, f, f, f )
        # sfx[i] = fex.sum()
    ##############################

