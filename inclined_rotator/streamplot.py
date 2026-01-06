
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

nf      = np.load ("numgridsearch_ampa_ra_fres.npz")
rf      = np.load ("visrvm_ra_fres.npz")

fig  = plt.figure ('streamplot')
axes = fig.subplots ( 2, 2, sharex=True, )

lab = 'ipq'
ax  = axes[0,0]
ax.scatter ( LDEG, nf[f'data_{lab}'], c='k', marker='.'  )
ax.plot ( LDEG, nf[f'model_{lab}'], c='b' )
ax.plot ( LDEG, rf[f'model_{lab}'], c='r' )
ax.set_title ('I+Q')

for t in [-73, -41, 0, 41, 73]:
    ax.axvline ( t, ls='--', c='k', alpha=0.30 )

lab = 'imq'
ax  = axes[0,1]
ax.scatter ( LDEG, nf[f'data_{lab}'], c='k', marker='.'  )
ax.plot ( LDEG, nf[f'model_{lab}'], c='b' )
ax.plot ( LDEG, rf[f'model_{lab}'], c='r' )
ax.set_title ('I-Q')
for t in [-73, -41, 0, 41, 73]:
    ax.axvline ( t, ls='--', c='k', alpha=0.30 )

lab = 'ipu'
ax  = axes[1,0]
ax.scatter ( LDEG, nf[f'data_{lab}'], c='k', marker='.'  )
ax.plot ( LDEG, nf[f'model_{lab}'], c='b' )
ax.plot ( LDEG, rf[f'model_{lab}'], c='r' )
ax.set_title ('I+U')
for t in [-73, -41, 0, 41, 73]:
    ax.axvline ( t, ls='--', c='k', alpha=0.30 )

lab = 'imu'
ax  = axes[1,1]
ax.scatter ( LDEG, nf[f'data_{lab}'], c='k', marker='.'  )
ax.plot ( LDEG, nf[f'model_{lab}'], c='b' )
ax.plot ( LDEG, rf[f'model_{lab}'], c='r' )
ax.set_title ('I-U')
for t in [-73, -41, 0, 41, 73]:
    ax.axvline ( t, ls='--', c='k', alpha=0.30 )

axes[0,0].set_ylabel('Response')
axes[1,0].set_ylabel('Response')
axes[1,0].set_xlabel('Phase / deg')
axes[1,1].set_xlabel('Phase / deg')


fig.savefig ('figs/streamplot.pdf', bbox_inches='tight')
# plt.show ()
