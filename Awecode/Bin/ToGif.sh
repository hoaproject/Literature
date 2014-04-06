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

workspace=/tmp/awecode.hoa/$RANDOM/
input=""
output=""
frame_rate=10

mkdir -p $workspace

function usage() {

    echo >&2 "Usage:"
    echo >&2 "    $0 -i=<input> -o=<output>"
}

while getopts i:o:r:h opt; do
    case $opt in
        i)   input=$OPTARG;;
        o)   output=$OPTARG;;
        r)   frame_rate=$OPTARG;;
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

$ffmpeg -i $input -r $frame_rate $workspace/temp%03d.gif
$convert -delay 5 -loop 0 $workspace/temp*.gif $workspace/output.gif
$convert -layers Optimize $workspace/output.gif $output

echo "[done]"
echo "    workspace: $workspace"
echo "    output file: $output"
