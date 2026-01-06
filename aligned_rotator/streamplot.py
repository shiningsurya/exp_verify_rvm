
import numpy as np
import matplotlib.pyplot as plt

plt.style.use ('../gmrtr3.mplstyle')
TAKES   = [-200, -100, 0, 100, 200]
HTAKE   = 250
LONGS   = np.linspace ( -np.pi, np.pi, 2*HTAKE, dtype=np.float32 )
LDEG    = np.rad2deg ( LONGS )

nf      = np.load ("numgridsearch.npz")

fig  = plt.figure ('streamplot')
axes = fig.subplots ( 2, 2, sharex=True, sharey=True )

lab = 'ipq'
ax  = axes[0,0]
ax.scatter ( LDEG, nf[f'data_{lab}'], c='k', marker='.'  )
ax.plot ( LDEG, nf[f'model_{lab}'], c='b' )
ax.set_title ('I+Q')

for t in [-144, -72, 0, 73, 145]:
    ax.axvline ( t, ls=':', c='r', alpha=0.30 )

lab = 'imq'
ax  = axes[0,1]
ax.scatter ( LDEG, nf[f'data_{lab}'], c='k', marker='.'  )
ax.plot ( LDEG, nf[f'model_{lab}'], c='b' )
ax.set_title ('I-Q')
for t in [-144, -72, 0, 73, 145]:
    ax.axvline ( t, ls=':', c='r', alpha=0.30 )

lab = 'ipu'
ax  = axes[1,0]
ax.scatter ( LDEG, nf[f'data_{lab}'], c='k', marker='.'  )
ax.plot ( LDEG, nf[f'model_{lab}'], c='b' )
ax.set_title ('I+U')
for t in [-144, -72, 0, 73, 145]:
    ax.axvline ( t, ls=':', c='r', alpha=0.30 )

lab = 'imu'
ax  = axes[1,1]
ax.scatter ( LDEG, nf[f'data_{lab}'], c='k', marker='.'  )
ax.plot ( LDEG, nf[f'model_{lab}'], c='b' )
ax.set_title ('I-U')
for t in [-144, -72, 0, 73, 145]:
    ax.axvline ( t, ls=':', c='r', alpha=0.30 )

axes[0,0].set_ylabel('Response')
axes[1,0].set_ylabel('Response')
axes[1,0].set_xlabel('Phase / deg')
axes[1,1].set_xlabel('Phase / deg')


fig.savefig ('figs/streamplot.pdf', bbox_inches='tight')
# plt.show ()
