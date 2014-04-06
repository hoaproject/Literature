#!/bin/bash

ffmpeg=`which ffmpeg`

if [[ "x" = "x$ffmpeg" ]]; then
    echo "ffmpeg binary is not found."
    exit 1
fi

convert=`which convert`

if [[ "x" = "x$convert" ]]; then
    echo "convert binary is not found."
    exit 1
fi

gifsicle=`which gifsicle`

if [[ "x" = "x$gifsicle" ]]; then
    echo "gifsicle binary is not found."
    exit 1
fi

workspace=/tmp/awecode.hoa/$RANDOM/
input=""
output=""
frame_rate=10
delay=5
colors=16

mkdir -p $workspace

function usage() {

    echo >&2 "Usage:"
    echo >&2 "    $0 -i=<input> -o=<output>"
    echo >&2 "Options:"
    echo >&2 "    (input)"
    echo >&2 "    -i  input file"
    echo >&2 "    -r  frame rate (default: $frame_rate)"
    echo >&2 "    (output)"
    echo >&2 "    -o  output file"
    echo >&2 "    -d  delay between each frame (default: $delay)"
    echo >&2 "    -c  number of colors (default: $colors)"
}

while getopts i:o:r:d:c:h opt; do
    case $opt in
        i)   input=$OPTARG;;
        o)   output=$OPTARG;;
        r)   frame_rate=$OPTARG;;
        d)   delay=$OPTARG;;
        c)   colors=$OPTARG;;
        h)   usage; exit 2;;
        [?]) usage; exit 2;;
    esac
done

if [[ -z "$input" ]]; then
    echo '-i is empty.'
    usage
    exit 3
fi

if [[ -z "$output" ]]; then
    echo '-o is empty.'
    usage
    exit 3
fi

$ffmpeg -i $input -r $frame_rate $workspace/temp%03d.png
$convert -fuzz 1% -delay $delay -loop 0 $workspace/temp*.png \
         +dither -layers Optimize -colors $colors $output
$gifsicle -O9 $output -o $output

echo "[done]"
echo "    workspace: $workspace"
echo "    output file: $output"
