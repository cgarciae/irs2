import sys
sys.path.append("./flask")

import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import click
from odo import odo
from PIL import Image
import numpy as np
import os
from model import get_keras_objects
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import os



size = 299
folder = "data/images2440"
n_clusters = "7"

@click.command()
@click.option('--size', '-s', default = "299")
@click.option('--folder', '-f', default = "./data/images2440")
@click.option('--n-clusters', '-c', default = "7")
@click.option('--host', '-h', default = "localhost")
def main(size, folder, n_clusters, host):
    size = int(size)
    n_clusters = int(n_clusters)

    # embeddings
    sess, graph, image, embedding, keras_training = get_keras_objects()

    features_test = []
    images_name = os.listdir(folder)

    for name in images_name:
        path = os.path.join(folder,name)
        im = Image.open(path)
        if not (im.mode == "RGB"):
            im = im.convert("RGB")
        if ( im.size[0] != size or im.size[1] != size): #reshape it
            im = im.resize((size, size,), Image.ANTIALIAS)
        features_test.append(np.array(im))

    features_test =  np.stack(features_test)
    print("Images shape: {}".format(features_test.shape))

    embeddings = []
    for img in features_test:
        pred = sess.run(embedding,{image: [img], keras_training: False })
        embeddings.append(np.squeeze(pred))

    embeddings =  np.stack(embeddings)
    print("Embeddings shape: {}".format(embeddings.shape))


    tsne = TSNE(n_components=3, perplexity=15.0, early_exaggeration=12.0, learning_rate=200.0, n_iter=3000, init="pca")
    tsne_embeddings = tsne.fit_transform(embeddings)
    tsne_embeddings.shape

    print("Tsne Embeddings shape: {}".format(tsne_embeddings.shape))


    kmeans = KMeans(n_clusters = n_clusters, random_state=0)
    clusters = kmeans.fit_predict(tsne_embeddings)

    print("Clusters shape: {}".format(clusters.shape))


    df = pd.DataFrame(dict(
        filename = images_name,
        embeddings = embeddings.tolist(),
        tsne_embeddings = tsne_embeddings.tolist(),
        clusters = clusters
    ))




    print("Connecting to MongoDB")
    # create mongo db
    client = MongoClient(host)
    db = client.brandon

    db.images.drop()

    print("Inserting data")
    odo(df, db.images)






if __name__ == '__main__':
    main()
