#!/bin/bash


#centers = {'I+Q':686, 'I-Q':637, 'I+U':625, 'I-U':600, 'I':698}
#HTAKE  = 250

#ffmpeg -i I+Q.mp4 -i I-Q.mp4 -i I+U.mp4 -i I-U.mp4 \
#	-filter_complex "[0:v]trim=start_frame=436:end_frame=936[a];[1:v]trim=start_frame=387:end_frame=887[b];[2:v]trim=start_frame=375:end_frame=875[c];[3:v]trim=start_frame=350:end_frame=850[d];[a][b]hstack[t];[c][d]hstack[v];[t][v]vstack,scale=1440:1440[w]" \
#	-map "[w]" out.mp4

ffmpeg -i I+Q.mp4 -i I-Q.mp4 -i I+U.mp4 -i I-U.mp4 \
	-filter_complex "[0:v]trim=start_frame=436:end_frame=936,setpts=PTS-STARTPTS,drawtext=fontsize=72:text='0 deg I+Q':fontcolor=white:x=32:y=32[a];[1:v]trim=start_frame=387:end_frame=887,setpts=PTS-STARTPTS,drawtext=fontsize=72:text='90 deg I-Q':fontcolor=white:x=32:y=32[b];[2:v]trim=start_frame=375:end_frame=875,setpts=PTS-STARTPTS,drawtext=fontsize=72:text='45 deg I+U':fontcolor=white:x=32:y=32[c];[3:v]trim=start_frame=350:end_frame=850,setpts=PTS-STARTPTS,drawtext=fontsize=72:text='135 deg I-U':fontcolor=white:x=32:y=32[d];[a][b]hstack[t];[c][d]hstack[v];[t][v]vstack,scale=1440:1440[w]" \
	-map "[w]" aligned_rotator.mp4
