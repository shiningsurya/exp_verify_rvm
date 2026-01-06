"""

"""
import numpy as np
TAKE   = 250

### re centers
### looking at streams
### I-Q minimum
# centers = {'I+Q':638, 'I-Q':625, 'I+U':593, 'I-U':623, "I":1149}

## I-Q centering
## I-U edging
# centers = {'I+Q':638, 'I-Q':629, 'I+U':593, 'I-U':613, "I":1149}
# USTART = 109
# USTOP  = 391


## visual centering
## after looking at the frames
centers = {'I+Q':632, 'I-Q':627, 'I+U':594, 'I-U':612, "I":1145}
USTART = 113
USTOP  = 396


"""
after centering
starts from 109 .. 391
so long should be 


-TAKE .... 0 .... TAKE

109-TAKE .... 391-TAKE
-pi/2    .... pi/2

slope = pi / (391-109) = pi / 282 
"""

# long   = np.linspace ( -0.5*np.pi, 0.5*np.pi, 2*TAKE )
slope   = np.pi / ( USTART - USTOP )
long    = np.arange ( -TAKE, TAKE ) * slope

slices  = dict()
for k,v in centers.items():
    slices[k] = slice ( v - TAKE, v + TAKE )

labels = ['I+Q','I-Q','I+U','I-U', 'I']

files  = dict()
sso    = slice ( 0, 15 )
for l in labels:
    with np.load ( f"{l}.npz" ) as __f:
        files [ l ] = __f[l][ slices[l]  ] 
        ### get scalings
        files [ f"s{l}" ] = __f[l][ sso ].mean()
        files [ f"f{l}" ] = files [ l ] / files [ f"s{l}" ]

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
## subtract off
off    = slice ( 40, 80 )
for l in labels:
    lvl  = files [ l ] [ off ].mean()
    files [ l ] -= lvl
##############################################

# files['iq'] = 0.5 * ( files['I+Q'] + files['I-Q'] )
# files['iu'] = 0.5 * ( files['I+U'] + files['I-U'] )
# files['ii'] = 0.5 * ( files['iu'] + files['iq'] )

# files['qp'] = ( files['I+Q'] - files['I'] )
# files['qm'] = ( files['I'] - files['I-Q'] )
# files['qq'] = 0.5 * ( files['I+Q'] - files['I-Q'] )

# files['up'] = ( files['I+U'] - files['I'] )
# files['um'] = ( files['I'] - files['I-U'] )
# files['uu'] = 0.5 * ( files['I+U'] - files['I-U'] )

# files['pa'] = 0.5 * np.arctan2 ( files['uu'], files['qq'] )
# files['ll'] = np.sqrt ( files['qq']**2 + files['uu']**2 )

files['longs'] = long

np.savez ("restream.npz", **files)
