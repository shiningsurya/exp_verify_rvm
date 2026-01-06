"""
make restream-like timeseries
but splitting y-axis into 4 equal ranges
"""
import numpy as np
import sys

import ffmpeg

HTAKE   = 250

centers = {'I+Q':632, 'I-Q':627, 'I+U':594, 'I-U':612, "I":1145}
"""
split on the 1D into four ranges
"""
ox   = slice ( 500, 1400 )
oy   = slice ( 355, 1075 )

# 500...725...950...1175...1400
# r1   = slice (500, 725) 
# r2   = slice (725, 950)
# r3   = slice (950,1175)
# r4   = slice (1175, 1400)

#  500,  650,  800,  950, 1100, 1250
r1   = slice ( 500, 650 )
r2   = slice ( 650, 800 )
r3   = slice ( 800, 950 )
r4   = slice ( 950, 1100 )
r5   = slice ( 1100, 1250 )
r6   = slice ( 1250, 1400 )

def get_args ():
    import argparse
    agp = argparse.ArgumentParser('varystream')
    add = agp.add_argument
    add ('arg', help="argument")
    return agp.parse_args()

if __name__ == "__main__":
    ## get args
    args = get_args ()

    ## setup
    arg = args.arg

    ## files
    IN  = f"{arg}.mp4"
    ONPZ= f"{arg}_vary.npz"

    ## output setup
    keys = [f"{arg}_ra", f"{arg}_r1", f"{arg}_r2", f"{arg}_r3", f"{arg}_r4", f"{arg}_r5", f"{arg}_r6"]
    dkey = keys[0]
    key1 = keys[1]
    key2 = keys[2]
    key3 = keys[3]
    key4 = keys[4]
    key5 = keys[5]
    key6 = keys[6]
    OUT = {k:[] for k in keys}

    OUT['split_into'] = [6]

    ### find start and stop frames
    cen = centers[arg]
    NSTART = cen - HTAKE
    NSTOP  = cen + HTAKE
    NN     = NSTOP - NSTART

    OUT['nstart'] = NSTART
    OUT['nstop']  = NSTOP

    print (f" reading {NN:d} frames ({NSTART:d} ... {NSTOP:d}) from {IN} and saving to {ONPZ} ... ")

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
        if not read_bytes or n > NSTOP:
        # if n >= 128:
            break
        ################
        read_frame   = np.float32 ( np.frombuffer ( read_bytes, np.uint8 ).reshape ( ( height, width, chan ) ) )
        bright_frame = ( 0.299*read_frame[...,0] + .587*read_frame[...,1] + .114*read_frame[...,2] ) / 255.
        ################
        if n >= NSTART and n < NSTOP:
            OUT[dkey].append ( bright_frame.mean() )
            OUT[key1].append ( bright_frame[r1].mean() )
            OUT[key2].append ( bright_frame[r2].mean() )
            OUT[key3].append ( bright_frame[r3].mean() )
            OUT[key4].append ( bright_frame[r4].mean() )
            OUT[key5].append ( bright_frame[r5].mean() )
            OUT[key6].append ( bright_frame[r6].mean() )
        ################

    np.savez (ONPZ, **OUT)


