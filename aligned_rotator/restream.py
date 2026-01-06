"""

"""
import numpy as np

### centers
### from fewframes
centers = {'I+Q':686, 'I-Q':637, 'I+U':625, 'I-U':600, 'I':698}

HTAKE  = 250
# TAKE   = 525

### by eye there is 500 samples between
### when phone is top aligned 

LONGS   = np.linspace ( -np.pi, np.pi, 2*HTAKE, dtype=np.float32 )

slices  = dict()
for k,v in centers.items():
    # slices[k] = slice ( v, v+TAKE )
    slices[k] = slice ( v-HTAKE, v+HTAKE )

labels = ['I','I+Q','I-Q','I+U','I-U']

files  = dict()
for l in labels:
    with np.load ( f"{l}.npz" ) as __f:
        files [ l ] = __f[l][ slices[l]  ] 

##############################################
## bring I+Q, I-Q, I+U, I-U, I into [0., 1.]
def scaler ( arr, pmin, pmax ):
    ra = arr[pmax] - arr[pmin]
    return ( arr - arr[pmin] ) / ra

# files['I']   = np.zeros_like ( files['I'] ) + 1.0
# files['I+Q'] = scaler ( files['I+Q'], pmin=128, pmax=450 )
# files['I-Q'] = scaler ( files['I-Q'], pmin=251, pmax=72 )
# files['I+U'] = scaler ( files['I+U'], pmin=314, pmax=142 )
# files['I-U'] = scaler ( files['I-U'], pmin=434, pmax=258)

##############################################

files['longs'] = LONGS

# files['iq'] = 0.5 * ( files['I+Q'] + files['I-Q'] )
# files['iu'] = 0.5 * ( files['I+U'] + files['I-U'] )

# files['qp'] = ( files['I+Q'] - files['I'] )
# files['qm'] = ( files['I'] - files['I-Q'] )
# files['qq'] = 0.5 * ( files['I+Q'] - files['I-Q'] )

# files['up'] = ( files['I+U'] - files['I'] )
# files['um'] = ( files['I'] - files['I-U'] )
# files['uu'] = 0.5 * ( files['I+U'] - files['I-U'] )

# files['pa'] = 0.5 * np.arctan2 ( files['uu'], files['qq'] )
# files['ll'] = np.sqrt ( files['qq']**2 + files['uu']**2 )

np.savez ("restream.npz", **files)
