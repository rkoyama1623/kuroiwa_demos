#!/usr/bin/python
import glob
import numpy
import os.path
import shutil
import sys

IMAGE_DIR = "caltech101"
SUBSET_DIR = "caltech_test"

files = glob.glob(IMAGE_DIR+"/*")
name_list = []
for file in files:
    group = file.split("/")[1].split("-")[0]
    name_list.append(group)

name_list = list(numpy.unique(name_list))

num = int(sys.argv[1])
TARGET_CATEGORY = name_list[:num]
print TARGET_CATEGORY
TOP = 50

if os.path.exists(SUBSET_DIR):
    shutil.rmtree(SUBSET_DIR)

os.mkdir(SUBSET_DIR)
for file in os.listdir(IMAGE_DIR):
    try:
        cat = file.split("-")[0]
        num = int(file.split("-")[1][0:4])
    except:
        continue

    if cat in TARGET_CATEGORY and num <= TOP:
        source_image = "%s/%s" % (IMAGE_DIR, file)
        dest_image = "%s/%s" % (SUBSET_DIR, file)
        shutil.copyfile(source_image, dest_image)
