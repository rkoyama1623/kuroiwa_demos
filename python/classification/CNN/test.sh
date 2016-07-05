#!/bin/bash -xe

CLASS="accordion crab pizza starfish yin_yang"
TRAIN="/tmp/train.txt"
TEST="/tmp/test.txt"

# delete old files
if [ -e $TRAIN ]
then
    rm -f $TRAIN
fi
if [ -e $TEST ]
then
    rm -f $TEST
fi

# generate train data
idx=0
for c in $CLASS
do
    for f in $c/train/*
    do
        ./feature.py $f -c $idx --output $TRAIN 2> /dev/null
    done
    idx=$(( idx + 1 ))
done

# generate test data
idx=0
for c in $CLASS
do
    for f in $c/test/*
    do
        ./feature.py $f -c $idx --output $TEST 2> /dev/null
    done
    idx=$(( idx + 1 ))
done

# train SVM
SCALE="/tmp/scale.txt"
SCALED_TRAIN=${TRAIN:0:-4}_scaled.txt
SCALED_TEST=${TEST:0:-4}_scaled.txt
MODEL="/tmp/my.model"
svm-scale -s $SCALE $TRAIN > $SCALED_TRAIN
svm-scale -r $SCALE $TEST > $SCALED_TEST
svm-train -c 0.03 $SCALED_TRAIN $MODEL
svm-predict $SCALED_TEST $MODEL /tmp/result.txt
