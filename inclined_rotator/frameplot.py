"""
direct make plots
"""
import os
import numpy as np

import matplotlib.pyplot as plt

from skimage.io import imread

plt.style.use ('../gmrtr3.mplstyle')
TAKES   = [-115, -65, 0, 65, 115]
TAKE    = 500
HTAKE   = 250

USTART  = 113
USTOP   = 396
slope   = np.pi / ( USTOP - USTART )
LONGS   = np.arange ( -HTAKE, HTAKE ) * slope

def imreader ( f ):
    with np.load (f) as _f:
        frames = _f['frames']
    return frames

ipq = imreader ('I+Q_frames.npz')
imq = imreader ('I-Q_frames.npz')
ipu = imreader ('I+U_frames.npz')
imu = imreader ('I-U_frames.npz')

fig = plt.figure ('frame')
# axes = fig.subplot_mosaic ( [['ipq', 'imq'],['ipu', 'imu']], sharex=True, sharey=True, gridspec_kw={'hspace':0.2, 'wspace':0.2} )

## (ipq, imq, ipu, imu) x (longs)
axes = fig.subplots ( 4, 5, sharex=True, sharey=True )
# _axes = fig.subplots ( 2,2, sharex=True, sharey=True )
# axes  = {'ipq':_axes[0,0], 'imq':_axes[0,1], 'ipu':_axes[1,0], 'imu':_axes[1,1]}

imdict = {'aspect':'equal', 'cmap':'gray', 'origin':'upper', 'vmin':0., 'vmax':.8, 'interpolation':'none'}


### ipq
for i in range(5): axes[0, i].imshow ( ipq[i], **imdict )
for i in range(5): axes[1, i].imshow ( imq[i], **imdict )
for i in range(5): axes[2, i].imshow ( ipu[i], **imdict )
for i in range(5): axes[3, i].imshow ( imu[i], **imdict )

axes[0,0].set_ylabel('I+Q')
axes[1,0].set_ylabel('I-Q')
axes[2,0].set_ylabel('I+U')
axes[3,0].set_ylabel('I-U')

for i in range(5):
    axes[0,i].set_title (f"{np.rad2deg(LONGS[HTAKE + TAKES[i]]):.0f} deg")

# axes[0,0].set_title (f"{np.rad2deg(LONGS[-100]):.0f} deg")
# axes[0,1].set_title (f"{np.rad2deg(LONGS[0]):.0f} deg")
# axes[0,2].set_title (f"{np.rad2deg(LONGS[100]):.0f} deg")


# for ax in ['ipq','imq', 'ipu', 'imu']:
for i in range(4): 
    for j in range(5):
        axes[i,j].set_xticks([])
        axes[i,j].set_yticks([])
        # axes[i,j].plot ( [600, 850, 850, 600, 600],[800, 800, 1000, 1000, 800],  ls='-', c='r', alpha=0.55 )
    # axes[ax].set_xticks([])
    # axes[ax].set_yticks([])

# oox, ooy = slice (800,1000), slice(600,850)
## x is down y is left
# axes[0,2].plot ( [600, 850, 850, 600, 600],[800, 800, 1000, 1000, 800],  ls='-', c='r', alpha=0.55 )

fig.savefig ('figs/irframes.png', bbox_inches='tight', dpi=300)

# plt.show ()
