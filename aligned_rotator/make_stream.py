import numpy as np
import sys

import ffmpeg

## always arg
arg = sys.argv[1]

IN  = f"{arg}.mp4"
dkey = f"{arg}"
skey = f"s{arg}"
OUT = { dkey:[], skey:[] }
ONPZ= f"{arg}.npz"



oox, ooy = slice (800,1000), slice(600,850)

print (f" reading from {IN} and saving to {ONPZ} ... ")

"""
mp4 - rgb888 - brightness - mask means - save
"""

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
    # bright_frame = ( 0.257*read_frame[...,0] + 0.504*read_frame[...,1] + 0.098*read_frame[...,2] ) / 255.
    # bright_frame = np.sqrt ( 0.299*read_frame[...,0]**2 + 0.587*read_frame[...,1]**2 + 0.114*read_frame[...,2]**2 ) / 255.
    # bright_frame -= bright_frame[masker.off.mask].mean()
    # bright_frame = ( read_frame[...,0] + read_frame[...,1] + read_frame[...,2] ) / ( 3 * 255 )
    # if n == 504:
        # np.save (f"b5f{n:d}.npy", bright_frame)
        # adfad
    ################
    # val  = bright_frame.mean ()
    bf      = bright_frame[oox,ooy]
    val     = bf.mean()
    valstd  = bf.std()
    ################
    OUT[dkey].append ( val )
    OUT[skey].append ( valstd )

np.savez (ONPZ, **OUT)


