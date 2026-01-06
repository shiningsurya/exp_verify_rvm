"""

combines all the varystream outputs

they are already centered

"""
import numpy as np

USTART = 113
USTOP  = 396
TAKE   = 250

# long   = np.linspace ( -0.5*np.pi, 0.5*np.pi, 2*TAKE )
slope   = np.pi / ( USTART - USTOP )
long    = np.arange ( -TAKE, TAKE ) * slope

labels  = ['I+Q','I-Q','I+U','I-U', 'I']

files  = dict()
for l in labels:
    with np.load ( f"{l}_vary.npz" ) as __f:
        for lk, lv in __f.items():
            files [ lk ] = lv

files['longs'] = long

np.savez ("combvarystream.npz", **files)
