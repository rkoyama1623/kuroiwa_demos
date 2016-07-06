#!/bin/bash -xe

CLASS="accordion crab pizza starfish yin_yang"
TRAIN="train.txt"
SCALE="scale.txt"
SCALED_TRAIN=${TRAIN:0:-4}_scaled.txt
MODEL="my.model"

# delete old files
if [ -e $TRAIN ]
then
    rm -f $TRAIN $SCALE $SCALED_TRAIN $MODEL
fi

# generate train data
idx=0
for c in $CLASS
do
    num=0
    for f in $c/*
    do
        if [ $num -gt 10 ]
        then
            continue
        fi
        ./feature.py $f -c $idx --output $TRAIN 2> /dev/null
        num=$(( num + 1 ))
    done
    idx=$(( idx + 1 ))
done

# train SVM
svm-scale -s $SCALE $TRAIN > $SCALED_TRAIN
svm-train -c 0.03 $SCALED_TRAIN $MODEL
