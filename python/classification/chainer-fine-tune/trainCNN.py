#! /usr/bin/env python
# -*- coding: utf-8 -*-

from MyCNN import *
from copy_model import *
import cPickle as pickle
import numpy as np
import os
import datetime
import chainer
from chainer import optimizers

# config files
mean_url = 'https://github.com/BVLC/caffe/raw/master/python/caffe/imagenet/ilsvrc_2012_mean.npy'
caffemodel_url = 'http://dl.caffe.berkeleyvision.org/bvlc_reference_caffenet.caffemodel'
dir_name = os.path.abspath(os.path.dirname(__file__))
MEAN_PATH = os.path.join(dir_name, 'config/'+format(mean_url.split("/")[-1]))
CAFFEMODEL_PATH = os.path.join(dir_name, 'config/'+format(caffemodel_url.split("/")[-1]))
PICKLE_PATH = os.path.join(dir_name, 'config/bvlc_reference_caffenet.pkl')
NEW_MODEL_PATH = os.path.join(dir_name, 'config/new_model.pkl')

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
ref_model = pickle.load(open(PICKLE_PATH, "rb"))

# CNN network
print "Creating CNN"
my_model = MyCNN(MEAN_PATH, 5).to_cpu()
copy_model(ref_model, my_model)

# Training Parameters
LEARNIN_RATE    = 0.01
BATCH_SIZE      = 10
EPOCHS          = 100
DECAY_FACTOR    = 0.97
optimizer = chainer.optimizers.SGD(LEARNIN_RATE)
optimizer.setup(my_model)

# search train data and test data
img_list_train = []
cls_list_train = []
img_list_test = []
cls_list_test = []
dir_list = os.listdir(os.path.join(dir_name, 'data'))
dir_list = [os.path.join(dir_name, 'data/'+d) for d in dir_list]
dir_list = filter(lambda d: os.path.isdir(d), dir_list)
for cls, d in enumerate(dir_list):
    print d.split('/')[-1] + ' found'
    data_num = len(os.listdir(d))
    # assign 80% of all images are used as train data
    for img in os.listdir(d)[0:data_num/10*8]:
        img_list_train.append(os.path.join(d, img))
        cls_list_train.append(cls)
    # assign 20% of all images are used as test data
    for img in os.listdir(d)[data_num/10*8:]:
        img_list_test.append(os.path.join(d, img))
        cls_list_test.append(cls)

def load_image(filename, color=True):
    img = skimage.img_as_float(skimage.io.imread(filename, as_grey=not color)).astype(np.float32)
    if img.ndim == 2:
        img = img[:, :, np.newaxis]
        if color:
            img = np.tile(img, (1, 1, 3))
    elif img.shape[2] == 4:
        img = img[:, :, :3]
    return img

def test(model):
    sum_accuracy = 0.0
    sum_loss     = 0.0
    test_data_size = len(img_list_test)
    for i in range(0, test_data_size, BATCH_SIZE):
        cur_img_list = [load_image(img) for img in img_list_test[i:i+BATCH_SIZE]]
        cur_cls_list = np.array(cls_list_test[i:i+BATCH_SIZE], dtype=np.int32)
        _, loss = model(cur_img_list, cur_cls_list)
        sum_loss     += loss.data * BATCH_SIZE
        sum_accuracy += model.accuracy.data * BATCH_SIZE
    print "test mean loss {a}, accuracy {b}".format(a=sum_loss/test_data_size, b=sum_accuracy/test_data_size)
    return sum_accuracy/test_data_size

# train CNN
train_data_size = len(img_list_train)
for epoch in range(1, EPOCHS+1):
    print "[{}] epoch {}".format(datetime.datetime.now().strftime("%H:%M:%S"), epoch)
    indices = np.random.permutation(train_data_size)
    sum_accuracy = 0.0
    sum_loss     = 0.0
    for i in range(0, train_data_size, BATCH_SIZE):
        order = indices[i:i+BATCH_SIZE]
        cur_img_list = [load_image(img_list_train[idx]) for idx in order]
        cur_cls_list = np.array([cls_list_train[idx] for idx in order], dtype=np.int32)
        my_model.zerograds()
        _, loss = my_model(cur_img_list, cur_cls_list)
        loss.backward()
        optimizer.update()
        sum_loss     += loss.data * BATCH_SIZE
        sum_accuracy += my_model.accuracy.data * BATCH_SIZE
    print "train mean loss {a}, accuracy {b}".format(a=sum_loss/train_data_size, b=sum_accuracy/train_data_size)
    acc = test(my_model)
    if acc > 0.999:
        print "stop training because accuracy becomes over 99.9%"
        break
    optimizer.lr *= DECAY_FACTOR

pickle.dump(my_model, open(NEW_MODEL_PATH, "wb"))
