from __future__ import division
import cv2
import os
import numpy as np
import scipy
import h5py
import matplotlib.pyplot as plt
from itertools import islice
import tensorflow as tf
tf.compat.v1.enable_eager_execution()

def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _float_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

LIMIT = 45000
DATA_FOLDER = 'driving_dataset'
TRAIN_FILE = os.path.join(DATA_FOLDER, 'data.txt')

def preprocess(img):
    resized = cv2.resize(img[:, :, 1], (100, 100))
    return resized

def return_data():
    X = []
    y = []
    images_raw = []
    features = []
    with open(TRAIN_FILE) as fp:
        # Processing the whole dataset
        for line in islice(fp, LIMIT):
            print("Processed line:" + str(line))
            path, angle = line.strip().split()
            full_path = os.path.join(DATA_FOLDER, path)
            #full_path = str.encode(full_path)
            X.append(full_path)
            # using angles from -pi to pi to avoid rescaling the atan in the network
            new_angle = float(angle) * scipy.pi / 180
            
            int_angle = round(new_angle,1)
            print(int_angle)
            y.append(int_angle)

    for i in range(len(X)):
        print("Processing "+ str(i))
        img = plt.imread(X[i])
        features.append(preprocess(img))
    """
    for i in X:
        image_string = open(i, 'rb').read()
        images_raw.append(image_string)

    X = tf.train.BytesList(value=images_raw)
    y = tf.train.FloatList(value=y)
    main_storage = {
        'images': tf.train.Feature(bytes_list=X),
        'labels': tf.train.Feature(float_list=y)
    }
    """

    features = np.array(features).astype('float32')
    labels = np.array(y)

    np.save("features.npy", features)
    np.save("labels.npy", labels)
    """
    storage_dataset = tf.train.Features(feature=main_storage)
    example = tf.train.Example(features=storage_dataset)
    with tf.io.TFRecordWriter('dataset.tfrecord') as writer:
        writer.write(example.SerializeToString())
        writer.close()
    print("------------- Saving to to tfrecord -------------")
    """
return_data()
