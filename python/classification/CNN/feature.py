#! /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, os, os.path, numpy, caffe

HEDA = "/home/eisoku/myrepo/caffe/"
MEAN_FILE = HEDA + 'python/caffe/imagenet/ilsvrc_2012_mean.npy'
MODEL_FILE = HEDA + 'examples/imagenet/imagenet_feature.prototxt'
PRETRAINED = HEDA + 'examples/imagenet/caffe_reference_imagenet_model'
LAYER = 'fc6wi'
INDEX = 4

parser = argparse.ArgumentParser(description='feature extractor by CNN')
parser.add_argument('input_image', type=file, help='input image')
parser.add_argument('-c', type=str, help='class index', required=True)
parser.add_argument('--output', type=str, help='output file name', required=True)
args = parser.parse_args()

net = caffe.Classifier(MODEL_FILE, PRETRAINED)
caffe.set_mode_cpu()
net.transformer.set_mean('data', numpy.load(MEAN_FILE))
net.transformer.set_raw_scale('data', 255)
net.transformer.set_channel_swap('data', (2,1,0))

image = caffe.io.load_image(args.input_image)
net.predict([image])
feat = net.blobs[LAYER].data[INDEX].flatten().tolist()

with open(args.output, mode='a') as fh:
    fh.write(args.c + " ")
    for i, f in enumerate(feat):
        fh.write(str(i+1) + ":" + str(f))
        if i != len(feat) - 1:
            fh.write(" ")
    fh.write("\n")
