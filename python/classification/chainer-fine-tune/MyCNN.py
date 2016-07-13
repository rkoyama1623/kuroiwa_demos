#! /usr/bin/env python
# -*- coding: utf-8 -*-

import chainer
# from chainer import optimizers
import chainer.functions as F
import chainer.links as L
import numpy as np
import skimage.io
from skimage.transform import resize

class MyCNN(chainer.Chain):
    def __init__(self, mean_path, class_num):
        super(MyCNN, self).__init__(
            conv1=L.Convolution2D(  3,  96, 11, pad=0, stride=4),
            conv2=L.Convolution2D( 96, 256,  5, pad=2, stride=1),
            conv3=L.Convolution2D(256, 384,  3, pad=1, stride=1),
            conv4=L.Convolution2D(384, 384,  3, pad=1, stride=1),
            conv5=L.Convolution2D(384, 256,  3, pad=1, stride=1),
            fc6=L.Linear(9216, 4096), # 9216=6x6x256
            fc7=L.Linear(4096, 4096),
            scene_fc8=L.Linear(4096, class_num)
        )
        self.ref_len = 227      # the size of input image should be (227, 227)
        mean = np.load(mean_path)
        m_min, m_max = mean.min(), mean.max()
        normal_mean = (mean - m_min) / (m_max - m_min)
        self.mean = self.resize_image(normal_mean.transpose((1, 2, 0)), np.array([self.ref_len, self.ref_len])).transpose((2, 0, 1)) * (m_max - m_min) + m_min
        self.train = True

    def clear(self):
        self.loss = None
        self.accuracy = None

    def resize_image(self, im, new_dims, interp_order=1):
        im_min, im_max = im.min(), im.max()
        if im_max > im_min:
            # skimage is fast but only understands {1,3} channel images in [0, 1].
            im_std = (im - im_min) / (im_max - im_min)
            resized_std = resize(im_std, new_dims, order=interp_order)
            resized_im = resized_std * (im_max - im_min) + im_min
            ret = resized_im.astype(np.float32)
        else:
            # the image is a constant -- avoid divide by 0
            ret = np.empty((new_dims[0], new_dims[1], im.shape[-1]), dtype=np.float32)
            ret.fill(im_min)
        return ret

    def preprocess(self, img):
        input_ = self.resize_image(img, np.array([self.ref_len, self.ref_len]))
        chainer_in = input_.astype(np.float32, copy=False)
        # transpose
        chainer_in = chainer_in.transpose((2, 0, 1))
        # channel swap
        chainer_in = chainer_in[(2,1,0), :, :]
        # raw scale
        chainer_in *= 255
        # mean
        chainer_in -= self.mean
        return chainer_in

    def __call__(self, img_list, answer):
        self.clear()
        xs = np.zeros((len(img_list), 3, self.ref_len, self.ref_len)).astype(np.float32)
        for i, img in enumerate(img_list):
            xs[i] = self.preprocess(img)

        # conv1->relu1->pool1->norm1
        h = F.local_response_normalization(
                F.max_pooling_2d(
                    F.relu(
                        self.conv1(xs)
                    ),
                    ksize=3,
                    stride=2
                    # pad=0
                )
                # n(local_size)=5
                # alpha=0.0001
                # beta=0.75
            )
        # conv2->relu2->pool2->norm2
        h = F.local_response_normalization(
                F.max_pooling_2d(
                    F.relu(
                        self.conv2(h)
                    ),
                    ksize=3,
                    stride=2
                )
            )
        # conv3->relu3
        h = F.relu(
            self.conv3(h)
        )
        # conv4->relu4
        h = F.relu(
            self.conv4(h)
        )
        # conv5->relu5->pooling5
        h = F.max_pooling_2d(
                F.relu(
                    self.conv5(h)
                ),
                ksize=3,
                stride=2
            )
        # fc6->relu6->drop6
        h = F.dropout(
            F.relu(
                self.fc6(h)
            ),
            train=self.train
            # ratio=0.5
        )

        # fc7->relu7->drop7
        h = F.dropout(
            F.relu(
                self.fc7(h)
            ),
            train=self.train
        )

        # scene_fc8
        h = self.scene_fc8(h)

        self.loss = F.softmax_cross_entropy(h, answer)
        self.accuracy = F.accuracy(h, answer)
        return (h, self.loss)
