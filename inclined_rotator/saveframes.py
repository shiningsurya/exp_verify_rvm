import numpy as np
import sys

import ffmpeg

## from restream
centers = {'I+Q':632, 'I-Q':627, 'I+U':594, 'I-U':612, "I":1145}

## wrt centers
TAKES = [-115, -65, 0, 65, 115]

def get_args ():
    import argparse
    agp = argparse.ArgumentParser('fewframes')
    add = agp.add_argument
    add ('arg', help="argument")
    return agp.parse_args()

if __name__ == "__main__":
    args = get_args ()
    arg  = args.arg
    CEN  = centers [ arg ]
    frames = [t + CEN for t in TAKES]
    NSTOP  = max ( frames )


    IN  = f"{arg}.mp4"
    dkey = "frames"
    OUT = { dkey:[],}

    ONPZ= f"{arg}_frames.npz"

    OUT['saved_frames'] = frames


# masker.divide_by ( N )

    print (f" reading {len(frames):d} frames from {IN} and saving to {ONPZ} ... ")


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
        # mmask  = masker.mask
        # val    = bright_frame [ masker.mask ].mean()
        # if n >= NSTART and n < NSTOP:
        if n in frames:
            val    = bright_frame
            OUT[dkey].append ( val )
        # for imm in range ( N ):
            # __mm = masker.mm[imm]
            # val  = bright_frame[ __mm ].mean()
            # OUT[ mkeys[imm] ].append ( val )
        ################

    np.savez (ONPZ, **OUT)


