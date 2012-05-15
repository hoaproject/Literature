#/bin/bash

blender=`which blender`

if [[ "x" = "x$blender" ]]; then
    echo "Blender binary is not found."
    exit 1
fi

workspace=/tmp/popcode.hoa/$RANDOM/
description="(empty)"
theme="(empty)"
out=$workspace"Final.avi"
step1=1
step2=1
step3=1

function usage() {

    echo >&2 "Usage:\n"
    echo >&2 "    $0 -d=<description.xml> -t=<theme> [-o=<out.format>]\c"
    echo >&2 " [-1] [-2] [-3]"
}

while getopts d:t:o:123h opt; do
    case $opt in
        d)   description=$OPTARG;;
        t)   theme=$OPTARG;;
        o)   out=$OPTARG;;
        1)   step1=0;;
        2)   step2=0;;
        3)   step3=0;;
        h)   usage; exit 2;;
        [?]) usage; exit 2;;
    esac
done

if [[ ! -f $description ]]; then
    echo "Description file $description is not found."
    usage
    exit 3
fi

if [[ ! -d Theme/$theme ]]; then
    echo "Theme $theme is not found."
    usage
    exit 4
fi

mkdir -p $workspace

export POPCODE_WORKSPACE=$workspace
export POPCODE_OUT=$out

cp $description $workspace

[[ 1 -eq $step1 ]] && \
$blender --background Theme/$theme/Title.blend --python Title.py

[[ 1 -eq $step2 ]] && \
$blender --background Theme/$theme/Credits.blend --python Credits.py

[[ 1 -eq $step3 ]] && \
$blender --background --python Sequencer.py

echo "\n\n---\n$workspace"
