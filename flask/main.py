# import sys
# sys.path.append('/flask/')

# from datetime import datetime
from flask import Flask, request
from flask_pymongo import PyMongo
from utils import jsonify
# import time
from pyspark.sql.session import SparkSession
import numpy as np
import pyspark.sql.functions as F
from pyspark.sql import Row
from random import randint, shuffle
from pymongo import MongoClient
from bson.objectid import ObjectId
from scipy.spatial.distance import euclidean
import os


#### helpers

def get_random(row):

    n = len(row.filename_list)
    i = randint(0, n - 1)

    return dict(
        _id = row.id_list[i],
        clusters = row.clusters,
        filename = row.filename_list[i],
        tsne_embedding = row.tsne_embeddings_list[i]
    )

#
####################
# FLASK
####################

app = Flask("brandon")

####################
# MONGO
####################

app.config["MONGO_DBNAME"] = "brandon"
app.config["MONGO_URI"] = "mongodb://mongo:27017/brandon"
mongo = PyMongo(app)
# mongo = MongoClient("mongo")

####################
# SPARK
####################

spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

IMAGES = (
    spark.read
    .format("com.mongodb.spark.sql.DefaultSource")
    .option("uri", "mongodb://mongo/brandon.images")
    .load()
).cache()

IMAGES

print(IMAGES.count())

@app.route('/random-samples')
def random_samples():
    randoms = IMAGES.groupBy("clusters").agg(
        F.collect_list("filename").alias("filename_list"),
        F.collect_list("tsne_embeddings").alias("tsne_embeddings_list"),
        F.collect_list("_id").alias("id_list")
    ).drop("").collect()

    randoms = list(map(get_random, randoms))

    return jsonify(data = randoms)


@app.route('/images/<id>')
def get_similar(id):
    radius = float(request.args.get('radius', 80))
    n = int(request.args.get('n', 10))

    db = mongo.db

    img = db.images.find_one({'_id': ObjectId(id) })
    tsne_target = img["tsne_embeddings"]

    selected_images = (
        IMAGES.rdd.map(lambda row: Row(
            _id = row._id,
            filename = row.filename,
            distance = euclidean(row.tsne_embeddings, tsne_target)
        ))
        .toDF()
        .where(F.col("distance") <= radius )
        .orderBy("distance", ascending = True)
        .collect()
    )
    selected_images = selected_images[1:]
    shuffle(selected_images)
    selected_images = selected_images[:n]
    selected_images = sorted(selected_images, key = lambda row: row.distance)
    selected_images = [ r.asDict() for r in selected_images ]

    return jsonify(data = selected_images)

    # from IPython.display import Image
    # from IPython.core.display import HTML, display
    #
    # for row in selected_images:
    #     filename = os.path.join(os.sep, "data", "images2440", row.filename)
    #     display(Image(filename = filename))



if __name__ == '__main__':
    app.run(
        host = "0.0.0.0",
        debug = True
    )
