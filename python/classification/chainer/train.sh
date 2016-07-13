#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0);pwd)

CLASS="accordion crab pizza starfish yin_yang"
TRAIN="/tmp/train.txt"
SCALE="/tmp/scale.txt"
SCALED_TRAIN=${TRAIN:0:-4}_scaled.txt
MODEL="/tmp/my.model"

# delete old files
if [ -e $TRAIN ]
then
    rm -f $TRAIN $SCALE $SCALED_TRAIN $MODEL
fi

# generate train data
idx=0
for c in $CLASS
do
    echo "Extracting $c"
    target=$SCRIPT_DIR/data/$c/train
    img_list=`find $target -type f`
    $SCRIPT_DIR/feature.py $img_list -c $idx --output $TRAIN
    idx=$(( idx + 1 ))
done

# train SVM
svm-scale -s $SCALE $TRAIN > $SCALED_TRAIN
svm-train -c 0.03 $SCALED_TRAIN $MODEL
