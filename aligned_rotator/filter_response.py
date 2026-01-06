
import numpy as np

from scipy.interpolate import CubicSpline

class FilterResponseModel:
    """
    captures filter response
    """
    def __init__ (self, filename):
        """
        loads

        filter_pa is from [0, pi]
        it could be -0.5pi, 0.5pi

        this convention because CubicSpline needs increasing x
        """
        with np.load ( filename ) as fr:
            ##
            self.filter_pa = fr['filter_pa'] 

            self.pfilter   = fr['filter_plus']
            self.mfilter   = fr['filter_minus']
        ###
        self.pluster       = CubicSpline ( self.filter_pa, self.pfilter )
        self.minuster      = CubicSpline ( self.filter_pa, self.mfilter )

    def get_responses (self, ipa):
        """
        given a PA which is in [-0.5pi, 0.5pi]
        output of filter would be
        T0  : PA - 0 = PA
        T90 : PA - 90 
        T45 : PA - 45
        T135: PA - 135

        T0 has orthogonality at 90deg
        if PA is +85 deg
        T0 filter should be in the drop

        in our filter response formalism, the drop happens at 0deg
        so if PA is +85 deg, filter output taken at -5deg
        """

        _ipq  = self.pluster  ( np.arctan ( np.tan ( ipa ) ) )
        _imq  = self.minuster ( np.arctan ( np.tan ( ipa - 0.5*np.pi) ) )
        _ipu  = self.pluster ( np.arctan ( np.tan ( ipa + 0.25*np.pi ) ) )
        _imu  = self.minuster ( np.arctan ( np.tan ( ipa - 0.25*np.pi ) ) )
        
        return _ipq, _imq, _ipu, _imu

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    fres  = FilterResponseModel ("filter_response.npz")
    phase = np.linspace ( 0., 2.0*np.pi, 512 )
    pas   = np.arctan ( np.tan ( -phase ) )

    ipq,imq,ipu,imu = fres.get_responses ( pas )
    ######
    fig   = plt.figure ('fres')
    ax    = fig.add_subplot ()

    ax.plot ( phase, ipq, c='k', label='T0' )
    ax.plot ( phase, imq, c='orange', label='T90', marker='.' )
    ax.plot ( phase, ipu, c='b', label='T45' )
    ax.plot ( phase, imu, c='r', label='T135' )

    # ax.plot ( phase, pas, c='k' )


    plt.show ()
