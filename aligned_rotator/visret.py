"""
visualize RET
"""

import numpy as np
import matplotlib.pyplot as plt


def get_args ():
    import argparse 
    agp = argparse.ArgumentParser("visret")
    add = agp.add_argument
    add('npz_file', help='RET output file')
    return agp.parse_args ()

if __name__ == "__main__":
    args = get_args()

    nf   = np.load ( args.npz_file )

    for pkey in ['fipq', 'fimq', 'fipu', 'fimu', 'tpq', 'tmq', 'tpu', 'tmu']:
        if pkey in nf.keys():
            print (f" {pkey} -- {nf[pkey]:.2f}")

    fig  = plt.figure ('visret')
    axes = fig.subplots ( 3, 2, sharex=True, )


    axes[0,0].plot ( nf['data_iii'], c='k')
    axes[0,1].plot ( nf['pa'], c='k', marker='.')

    lab = 'ipq'
    ax  = axes[1,0]
    ax.plot ( nf[f'data_{lab}'], c='k'  )
    ax.plot ( nf[f'model_{lab}'], c='b' )

    lab = 'imq'
    ax  = axes[1,1]
    ax.plot ( nf[f'data_{lab}'], c='k'  )
    ax.plot ( nf[f'model_{lab}'], c='b' )

    lab = 'ipu'
    ax  = axes[2,0]
    ax.plot ( nf[f'data_{lab}'], c='k'  )
    ax.plot ( nf[f'model_{lab}'], c='b' )

    lab = 'imu'
    ax  = axes[2,1]
    ax.plot ( nf[f'data_{lab}'], c='k'  )
    ax.plot ( nf[f'model_{lab}'], c='b' )

    plt.show ()

