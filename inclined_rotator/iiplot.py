
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
masks   = np.ones_like ( nf['pa'] )
masks[USTART:USTOP] = False
PADATA  = np.ma.MaskedArray ( nf['pa'], mask = masks )

fig  = plt.figure ('iplot')
ax   = fig.add_subplot ()
tx   = ax.twinx()

ax.scatter ( LDEG, nf['data_iii'],  marker='.', c='k', label='Data'  )
tx.plot ( LDEG, nf['amp'],  c='b', label='Fit'  )
# ax.plot ( LDEG, np.rad2deg(TPA),c='b', label='Model')

ax.legend(loc='upper left')
tx.legend(loc='upper right')

for t in [-73, -41, 0, 41, 73]:
    ax.axvline ( t, ls=':', c='r', alpha=0.30 )

ax.set_ylabel('Response')
ax.set_xlabel('Phase / deg')

fig.savefig ('figs/iiplot.pdf', bbox_inches='tight')
# plt.show ()


