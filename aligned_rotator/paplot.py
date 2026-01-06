
import numpy as np
import matplotlib.pyplot as plt

plt.style.use ('../gmrtr3.mplstyle')
TAKES   = [-200, -100, 0, 100, 200]
HTAKE   = 250
LONGS   = np.linspace ( -np.pi, np.pi, 2*HTAKE, dtype=np.float32 )
LDEG    = np.rad2deg ( LONGS )

TPA     = np.arctan ( np.tan ( LONGS ) )

nf      = np.load ("numgridsearch.npz")

dpa     = 0.5 * np.arctan2 ( nf['data_imu'] - nf['data_ipu'], nf['data_ipq'] - nf['data_imq'] )

fig  = plt.figure ('paplot')
ax   = fig.add_subplot ()

ax.scatter ( LDEG, np.rad2deg(nf['pa']), marker='.', c='k', label='Gridsearch'  )
ax.plot ( LDEG, np.rad2deg(dpa), c='k', label='Direct' , alpha=0.2 )
ax.plot ( LDEG, np.rad2deg(TPA),c='b', label='Model')

ax.legend(loc='lower left')

for t in [-144, -72, 0, 73, 145]:
    ax.axvline ( t, ls=':', c='r', alpha=0.30 )

ax.set_ylabel('Orientation / deg')
ax.set_xlabel('Phase / deg')

fig.savefig ('figs/paplot.pdf', bbox_inches='tight')
# plt.show ()

