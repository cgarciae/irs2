# jupyter notebook --NotebookApp.iopub_data_rate_limit=10000000000
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from keras import backend as K
import inception_v4
import numpy as np
import cv2
import os, PIL
from PIL import Image
import tensorflow as tf
from tensorflow.python.platform import gfile
from model import get_keras_objects




def reduce_tsne(x, **kwargs):
    return TSNE(**kwargs).fit_transform(x)

sess, graph, image, embedding, keras_training = get_keras_objects()

image_name = 'cropped_panda.jpg'
image_name = 'elephant.jpg'
image

im = Image.open(image_name).resize((299,299))
img = np.asarray(im)

size = 299
folder = "imgs"
features_test = []
for name in os.listdir(folder):
    path = os.path.join(folder,name)
    im = Image.open(path)
    if (im.mode == "RGB"):
        if ( im.size[0] != size or im.size[1] != size): #reshape it
            im = im.resize((size, size,), PIL.Image.ANTIALIAS)
        features_test.append(np.array(im))

features_test =  np.stack(features_test)
features_test.shape

predictions = []
for img in features_test:
    pred = sess.run(embedding,{image: [img], keras_training:False })
    predictions.append(np.squeeze(pred))

predictions =  np.stack(predictions)
predictions.shape

features_reduced = reduce_tsne(predictions, n_components=3)
features_reduced.shape
kmeans = KMeans(n_clusters=16, random_state=0).fit(features_reduced)
kmeans.labels_.shape
