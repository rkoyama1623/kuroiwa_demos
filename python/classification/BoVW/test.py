#!/usr/bin/python
import cv2
import glob
import numpy
import sys
import sklearn.cluster
import sklearn.svm
import sklearn.cross_validation

files = glob.glob("caltech_test/*")
# files = glob.glob("test/*")
detector = cv2.FeatureDetector_create('ORB')
extractor = cv2.DescriptorExtractor_create("BRISK")
descriptors_dict = {}
float_converter = numpy.vectorize(lambda x: numpy.float32(x))

for file in files:
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    keypoints = detector.detect(img)
    _, descriptors = extractor.compute(img, keypoints)
    descriptors = descriptors.astype(numpy.float32)
    group = file.split("/")[1].split("-")[0]
    if descriptors_dict.has_key(group) is False:
        descriptors_dict[group] = [descriptors]
    else:
        descriptors_dict[group].append(descriptors)
    # descriptors_dict['hoge'] is expected like
    # [array([d11, d12, ..., d1n]),
    #  array([d21, d22, ..., d2n]),
    #  ...,
    #  array([dm1, dm2, ..., dmn])]
    # n is dimension of feature
    # m is num of keypoints
    # So, numpy.vstack(descriptors_dict['hoge']) is expected like
    # array([d11, d12, ..., d1n, d21, ..., dmn])
print "extraction done"

num = int(sys.argv[1])
k_means = sklearn.cluster.MiniBatchKMeans(n_clusters=num)
k_means.fit(numpy.vstack([numpy.vstack(x) for x in descriptors_dict.values()]))
centroid = k_means.cluster_centers_.astype(numpy.float32)
print "clustreing done"

knn = cv2.KNearest()
knn.train(centroid, numpy.arange(len(centroid)))
histograms_dict = {}
for group, descriptors_list in descriptors_dict.iteritems():
    for descriptors in descriptors_list:
        # descriptors represents one image
        histogram = numpy.zeros(len(centroid))
        _, results, _, _ = knn.find_nearest(descriptors, 1)
        for idx in [int(x) for x in results]:
            histogram[idx] = histogram[idx] + 1
        histogram = cv2.normalize(histogram, norm_type=cv2.NORM_L2)
        histogram = numpy.reshape(histogram, (1, -1))[0]
        if histograms_dict.has_key(group) is False:
            histograms_dict[group] = histogram
        else:
            histograms_dict[group] = numpy.vstack((histograms_dict[group], histogram))

data_train  = numpy.vstack(histograms_dict.values())
label_train = sum([[k] * len(d) for k, d in histograms_dict.iteritems()], [])
svc = sklearn.svm.SVC()
scores = sklearn.cross_validation.cross_val_score(svc, data_train, label_train, cv=5)
print num, numpy.mean(scores)*100
with open('aaa.log', mode = 'a') as f:
    f.write(str(num)+','+str(numpy.mean(scores)*100)+'\n')
