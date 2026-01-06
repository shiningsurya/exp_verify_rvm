import numpy as np
import sys

import ffmpeg

## always arg
arg = sys.argv[1]

IN  = f"{arg}.mp4"
dkey = f"{arg}"
OUT = { dkey:[] }
ONPZ= f"{arg}.npz"


print (f" reading from {IN} and saving to {ONPZ} ... ")

"""
mp4 - rgb888 - brightness - mask means - save
"""
def stolin ( v ):
    """
    sRGBtoLin
    """
    mm = v <= 0.04045
    um = ~mm
    vv = np.zeros_like (v)
    vv [ mm ] = v [ mm ] / 12.92
    vv [ um ]= np.power ( ( v [ um ] + 0.055 ) / 1.055, 2.4 )
    return vv

def make_bright_frame ( rgb ):
    """
    https://stackoverflow.com/questions/596216/formula-to-determine-perceived-brightness-of-rgb-color
    """
    rr, gg, bb = rgb[...,0], rgb[...,1], rgb[...,2]
    ##
    vr = stolin ( rr / 255. )
    vg = stolin ( gg / 255. )
    vb = stolin ( bb / 255. )
    ##
    yy = 0.2126*vr + 0.7152*vg + 0.0722*vb
    return yy


height, width = 1440, 1440
chan   = 3 

reader = (
    ffmpeg
    .input(IN)
    .output('pipe:', format='rawvideo', pix_fmt='rgb24')
    .run_async(pipe_stdout=True)
)

## read loop
# https://kkroening.github.io/ffmpeg-python/
n  = 0
while True:
    print (f" read {n:d} frames ... ", end='\r')
    read_bytes = reader.stdout.read ( width * height * 3 )
    n += 1
    if not read_bytes:
    # if n >= 128:
        break
    ################
    read_frame   = np.float32 ( np.frombuffer ( read_bytes, np.uint8 ).reshape ( ( height, width, chan ) ) )
    bright_frame = ( 0.299*read_frame[...,0] + .587*read_frame[...,1] + .114*read_frame[...,2] ) / 255.
    # bright_frame = make_bright_frame ( read_frame )
    # bright_frame = ( 0.257*read_frame[...,0] + 0.504*read_frame[...,1] + 0.098*read_frame[...,2] ) / 255.
    # bright_frame = np.sqrt ( 0.299*read_frame[...,0]**2 + 0.587*read_frame[...,1]**2 + 0.114*read_frame[...,2]**2 ) / 255.
    # bright_frame -= bright_frame[masker.off.mask].mean()
    # bright_frame = ( read_frame[...,0] + read_frame[...,1] + read_frame[...,2] ) / ( 3 * 255 )
    # if n == 504:
        # np.save (f"b5f{n:d}.npy", bright_frame)
        # adfad
    ################
    val  = bright_frame.mean ()
    ################
    OUT[dkey].append ( val )

np.savez (ONPZ, **OUT)


