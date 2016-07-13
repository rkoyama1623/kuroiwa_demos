#! /usr/bin/env python
# -*- coding: utf-8 -*-

from FeatureExtractor import *
import cPickle as pickle
from copy_model import *
import argparse, os, os.path, numpy

# arg option
parser = argparse.ArgumentParser(description='feature extractor by CNN')
parser.add_argument('input_image', type=str, help='input image', nargs='*')
parser.add_argument('-c', type=str, help='class index', required=True)
parser.add_argument('--output', type=str, help='output file name', required=True)
args = parser.parse_args()

# config files
mean_url = 'https://github.com/BVLC/caffe/raw/master/python/caffe/imagenet/ilsvrc_2012_mean.npy'
caffemodel_url = 'http://dl.caffe.berkeleyvision.org/bvlc_reference_caffenet.caffemodel'
dir_name = os.path.abspath(os.path.dirname(__file__))
MEAN_PATH = os.path.join(dir_name, 'config/'+format(mean_url.split("/")[-1]))
CAFFEMODEL_PATH = os.path.join(dir_name, 'config/'+format(caffemodel_url.split("/")[-1]))
PICKLE_PATH = os.path.join(dir_name, 'config/bvlc_reference_caffenet.pkl')

if not os.path.exists(MEAN_PATH):
    import urllib
    print "Downloading {}".format(mean_url.split("/")[-1])
    urllib.urlretrieve(mean_url, MEAN_PATH)

if not os.path.exists(PICKLE_PATH):
    if not os.path.exists(CAFFEMODEL_PATH):
        import urllib
        print "Downloading {}".format(caffemodel_url.split("/")[-1])
        urllib.urlretrieve(caffemodel_url, CAFFEMODEL_PATH)
    print "Converting {} to {}".format(caffemodel_url.split("/")[-1], PICKLE_PATH.split("/")[-1])
    import chainer.links.caffe
    model = chainer.links.caffe.caffe_function.CaffeFunction(CAFFEMODEL_PATH)
    pickle.dump(model, open(PICKLE_PATH, "wb"))

print "Loading {}".format(PICKLE_PATH.split("/")[-1])
model = pickle.load(open(PICKLE_PATH, "rb"))

# CNN network
print "Creating CNN"
extractor = FeatureExtractor(MEAN_PATH).to_cpu()
copy_model(model, extractor)

def load_image(filename, color=True):
    img = skimage.img_as_float(skimage.io.imread(filename, as_grey=not color)).astype(np.float32)
    if img.ndim == 2:
        img = img[:, :, np.newaxis]
        if color:
            img = np.tile(img, (1, 1, 3))
    elif img.shape[2] == 4:
        img = img[:, :, :3]
    return img

img_list = [load_image(f) for f in args.input_image]
for feat in extractor(img_list).tolist():
    with open(args.output, mode='a') as fh:
        fh.write(args.c + " ")
        for i, f in enumerate(feat):
            fh.write(str(i+1) + ":" + str(f))
            if i != len(feat) - 1:
                fh.write(" ")
        fh.write("\n")
