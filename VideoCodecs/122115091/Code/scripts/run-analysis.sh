#!/bin/sh
ffmpeg -hide_banner -i $2 -i $1 -lavfi "[0:v][1:v]ssim=ssim.log;[0:v][1:v]psnr=psnr.log" -f null -
ffprobe -hide_banner -v quiet -select_streams v:0 -print_format csv -show_frames $2 > $3