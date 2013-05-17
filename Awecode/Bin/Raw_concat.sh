#!/bin/bash

ffmpeg=`which ffmpeg`

if [[ "x" = "x$ffmpeg" ]]; then
    echo "ffmpeg binary is not found."
    exit 1
fi

workspace=/tmp/awecode.hoa/$RANDOM/
input1=""
input2=""
output=""

mkdir -p $workspace

function usage() {

    echo >&2 "Usage:"
    echo >&2 "    $0 -1=<input1> -2=<input2> -o=<output>"
}

while getopts 1:2:o:h opt; do
    case $opt in
        1)   input1=$OPTARG;;
        2)   input2=$OPTARG;;
        o)   output=$OPTARG;;
        h)   usage; exit 2;;
        [?]) usage; exit 2;;
    esac
done

if [[ -z "$input1" ]]; then
    echo '-1 is empty.'
    usage
    exit 3
fi

if [[ -z "$input2" ]]; then
    echo '-2 is empty.'
    usage
    exit 3
fi

if [[ -z "$output" ]]; then
    echo '-o is empty.'
    usage
    exit 3
fi

$ffmpeg -i $input1 -qscale:v 1 $workspace/intermediate1.mpg
$ffmpeg -i $input2 -qscale:v 1 $workspace/intermediate2.mpg
$ffmpeg -i concat:"$workspace/intermediate1.mpg|$workspace/intermediate2.mpg" \
        -c copy $workspace/intermediate_all.mpg
$ffmpeg -i $workspace/intermediate_all.mpg -qscale:v 2 $output

echo "[done]"
echo "    workspace: $workspace"
echo "    output file: $output"
