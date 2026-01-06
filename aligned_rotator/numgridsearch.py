"""
numerically fit for greeks
grid search pa
find quality of fit
"""
import numpy as np

from scipy.optimize import minimize

from filter_response import FilterResponseModel
FilterResponse  = FilterResponseModel ("filter_response.npz")

################################
with np.load ("restream.npz") as rs:
    LONGS    = np.array ( rs['longs'] )
    # DATA_III = np.array ( rs['I'] )
    DATA_IPQ = np.array ( rs['I+Q'] )
    DATA_IMQ = np.array ( rs['I-Q'] )
    DATA_IPU = np.array ( rs['I+U'] )
    DATA_IMU = np.array ( rs['I-U'] )
    DATA_III = np.zeros_like ( LONGS ) + rs['I'].mean()
################################
### create grid
PGSIZE = 1024
PAG    = np.linspace ( -0.5*np.pi, 0.5*np.pi, PGSIZE )
### find responses
G_ipq, G_imq, G_ipu, G_imu = FilterResponse.get_responses ( PAG )
################################
def objective ( x ):
    """
    minimize this
    """
    fipq, fimq, fipu, fimu = x
    # fipq, fipu, fimu = x
    ipq_model, imq_model, ipu_model, imu_model = get_model ( fipq, fimq, fipu, fimu )
    # ipq_model, imq_model, ipu_model, imu_model = get_model ( fipq, fipq, fipu, fimu )
    return np.sum ( 
        (ipq_model - DATA_IPQ)**2 +
        (imq_model - DATA_IMQ)**2 +
        (ipu_model - DATA_IPU)**2 +
        (imu_model - DATA_IMU)**2 
    )
    # return np.sum ( 
        # (np.log10(ipq_model / DATA_IPQ))**2 +
        # (np.log10(imq_model / DATA_IMQ))**2 +
        # (np.log10(ipu_model / DATA_IPU))**2 +
        # (np.log10(imu_model / DATA_IMU))**2 
    # )

# pawork = np.zeros_like ( PAG )
def get_pa ( fipq, fimq, fipu, fimu ):
    """
    performs grid search pa
    """
    MPA  = np.zeros_like ( LONGS )
    FEX  = np.zeros_like ( LONGS )
    for i, long in enumerate ( LONGS ):
        #### initial
        # pawork[:] = 111_111.
        #### griding
        e1 = (DATA_III[i]*fipq*G_ipq - DATA_IPQ[i])**2 
        e2 = (DATA_III[i]*fimq*G_imq - DATA_IMQ[i])**2 
        e3 = (DATA_III[i]*fipu*G_ipu - DATA_IPU[i])**2 
        e4 = (DATA_III[i]*fimu*G_imu - DATA_IMU[i])**2 
        # for jpa in range ( PGSIZE ):
            # err = e1 + e2 + e3 + e4
            # e1 = (np.log10( DATA_III[i]*fipq*G_ipq[jpa] / DATA_IPQ[i] ))**2 
            # e2 = (np.log10( DATA_III[i]*fimq*G_imq[jpa] / DATA_IMQ[i] ))**2 
            # e3 = (np.log10( DATA_III[i]*fipu*G_ipu[jpa] / DATA_IPU[i] ))**2 
            # e4 = (np.log10( DATA_III[i]*fimu*G_imu[jpa] / DATA_IMU[i] ))**2 
        err = e1 + e2 + e3 + e4
        # pawork [ jpa ] = err
        ####
        __amin    = np.argmin ( err )
        MPA [ i ] = PAG [ __amin ]
        FEX [ i ] = err [ __amin ]
    return MPA, FEX

def get_model ( fipq, fimq, fipu, fimu ):
    """
    PA from RVM
    """
    ### RVM
    pat,_  = get_pa ( fipq, fimq, fipu, fimu )
    ### filter response
    _ipq, _imq, _ipu, _imu = FilterResponse.get_responses ( pat )
    ### get models
    ipq_model = DATA_III * fipq * _ipq
    imq_model = DATA_III * fimq * _imq
    ipu_model = DATA_III * fipu * _ipu
    imu_model = DATA_III * fimu * _imu
    ### return
    return ipq_model, imq_model, ipu_model, imu_model

def stepper(opts={}):
    """
    find those filter terms which minimize the total objective.
    """
    p0  = ( 0.5, 0.5, 0.5, 0.5 )
    # p0  = ( 0.5, 0.5, 0.5 )
    res = minimize ( 
        objective, p0, 
        bounds= ( ( 0., 3. ), (0., 3.), (0.,3.), (0., 3.) ),
        # bounds= ( ( 0., 3. ), (0.,3.), (0., 3.) ),
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
    # RET['fipu']  = res.x[1]
    # RET['fimu']  = res.x[2]
    ###
    RET['pa'], RET['fex']    = get_pa ( RET['fipq'], RET['fimq'], RET['fipu'], RET['fimu'] )
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

def tester ():
    """
    why give out nans?
    """
    p0  = ( 0.5, 0.5, 0.5 )
    out = objective ( p0 )

    print ( out )


if __name__ == "__main__":

    # tester ()
    # p0  = ( 0.5, 0.5, 0.5 )
    # out = objective ( p0 )

    ##############################
    RET = stepper (opts={'disp':True})
    np.savez ("numgridsearch.npz", **RET )
    ##############################
