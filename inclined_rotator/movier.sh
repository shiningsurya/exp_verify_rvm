#!/bin/bash


#HTAKE  = 250
#centers = {'I+Q':632, 'I-Q':627, 'I+U':594, 'I-U':612, "I":1145}

ffmpeg -i I+Q.mp4 -i I-Q.mp4 -i I+U.mp4 -i I-U.mp4 \
	-filter_complex "[0:v]trim=start_frame=382:end_frame=882,setpts=PTS-STARTPTS,drawtext=fontsize=72:text='0 deg I+Q':fontcolor=white:x=32:y=32[a];[1:v]trim=start_frame=377:end_frame=877,setpts=PTS-STARTPTS,drawtext=fontsize=72:text='90 deg I-Q':fontcolor=white:x=32:y=32[b];[2:v]trim=start_frame=344:end_frame=844,setpts=PTS-STARTPTS,drawtext=fontsize=72:text='45 deg I+U':fontcolor=white:x=32:y=32[c];[3:v]trim=start_frame=362:end_frame=862,setpts=PTS-STARTPTS,drawtext=fontsize=72:text='135 deg I-U':fontcolor=white:x=32:y=32[d];[a][b]hstack[t];[c][d]hstack[v];[t][v]vstack,scale=1440:1440[w]" \
	-map "[w]" inclined_rotator.mp4
