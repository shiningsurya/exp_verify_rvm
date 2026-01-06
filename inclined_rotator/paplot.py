
import numpy as np
import matplotlib.pyplot as plt

plt.style.use ('../gmrtr3.mplstyle')
TAKES   = [-115, -65, 0, 65, 115]
TAKE    = 500
HTAKE   = 250

USTART  = 113
USTOP   = 396
slope   = np.pi / ( USTOP - USTART )
LONGS   = np.arange ( -HTAKE, HTAKE ) * slope
LDEG    = np.rad2deg ( LONGS )



# TPA     = np.arctan ( np.tan ( LONGS ) )

# nf      = np.load ("numgridsearch.npz")
nf      = np.load ("numgridsearch_ampa_ra_fres.npz")
dpa     = 0.5 * np.arctan2 ( nf['data_imu'] - nf['data_ipu'], nf['data_ipq'] - nf['data_imq'] )

masks   = np.ones_like ( nf['pa'] )
masks[USTART:(USTOP-2)] = False
PADATA  = np.ma.MaskedArray ( nf['pa'], mask = masks )

DPADATA = np.ma.MaskedArray ( dpa, mask=masks )

lefts   = slice (113, 122)
# rights  = slice ()

rf      = np.load ("visrvm_ra_fres.npz")

gf      = np.load ('visggrvm_ra_fres.npz')

fig  = plt.figure ('paplot')
ax   = fig.add_subplot ()

ax.scatter ( LDEG, np.rad2deg(PADATA), marker='.', c='k', label='Gridsearch'  )
ax.plot ( LDEG, np.rad2deg ( DPADATA ), c='k', label='Direct', alpha=0.4 )
ax.plot ( LDEG, np.rad2deg ( rf['pa'] ), c='b', label='RVM' )
# ax.plot ( LDEG, np.rad2deg ( gf['pa'] ), c='orange', label='TRVM' )
# ax.plot ( LDEG, np.rad2deg(TPA),c='b', label='Model')
ax.scatter ( LDEG[lefts], np.rad2deg(PADATA[lefts]-np.pi), marker='.', c='r' )
# ax.scatter ( LDEG, np.rad2deg(PADATA+np.pi), marker='.', c='k' )

ax.legend(loc='lower right')

for t in [-73, -41, 0, 41, 73]:
    ax.axvline ( t, ls='--', c='k', alpha=0.30 )

ax.set_ylabel('Orientation / deg')
ax.set_xlabel('Phase / deg')

fig.savefig ('figs/paplot.pdf', bbox_inches='tight')
# plt.show ()

