import sys
sys.path.append("./flask")

import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import click
from odo import odo
from PIL import Image
import numpy as np
from model import get_keras_objects


size = 299
folder = "data/images2440"
n_clusters = "15"

@click.command()
@click.option('--size', '-s', default = "299")
@click.option('--folder', '-f', default = "/data/images2440")
@click.option('--n-clusters', '-c', default = "15")
def main(size, folder, n_clusters):
    size = int(size)
    n_clusters = int(n_clusters)

    # embeddings
    sess, graph, image, embedding, keras_training = get_keras_objects()

    features_test = []
    path_images = []

    for name in os.listdir(folder):
        path = os.path.join(folder,name)
        im = Image.open(path)
        if (im.mode == "RGB"):
            if ( im.size[0] != size or im.size[1] != size): #reshape it
                im = im.resize((size, size,), Image.ANTIALIAS)
            features_test.append(np.array(im))
            path_images.append(path)

    features_test =  np.stack(features_test)
    print("Images shape: {}".format(features_test.shape))

    embeddings = []
    for img in features_test:
        pred = sess.run(embedding,{image: [img], keras_training:False })
        embeddings.append(np.squeeze(pred))

    embeddings =  np.stack(embeddings)
    print("Embeddings shape: {}".format(embeddings.shape))


    tsne = TSNE(n_components=3, perplexity=15.0, early_exaggeration=12.0, learning_rate=200.0, n_iter=2000)
    tsne_embeddings = tsne.fit_transform(embeddings)
    tsne_embeddings.shape

    print("Tsne Embeddings shape: {}".format(tsne_embeddings.shape))


    n_clusters = 15
    kmeans = KMeans(n_clusters = n_clusters, random_state=0)
    clusters = kmeans.fit_predict(predictions_reduced)

    print("Clusters shape: {}".format(clusters.shape))




if __name__ == '__main__':
    main()
