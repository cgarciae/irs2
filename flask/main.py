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
        embedding = row.embeddings_list[i]
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

IMAGES_DESIGNERS = (
    spark.read
    .format("com.mongodb.spark.sql.DefaultSource")
    .option("uri", "mongodb://mongo/brandon.designers")
    .load()
).cache()


@app.route('/random-samples')
def random_samples():
    randoms = IMAGES.groupBy("clusters").agg(
        F.collect_list("filename").alias("filename_list"),
        F.collect_list("embeddings").alias("embeddings_list"),
        F.collect_list("_id").alias("id_list")
    ).collect()

    randoms = list(map(get_random, randoms))

    return jsonify(data = randoms)


@app.route('/images/<id>')
def get_similar(id):
    intial_radius = float(request.args.get('initial-radius', 100))
    radius = float(request.args.get('radius', 80))
    n = int(request.args.get('n', 10))

    db = mongo.db

    img = db.images.find_one({'_id': ObjectId(id) })
    target = img["embeddings"]

    selected_images = (
        IMAGES.rdd.map(lambda row: Row(
            _id = row._id,
            filename = row.filename,
            distance = euclidean(row.embeddings, target)
        ))
        .toDF()
        .where(F.col("distance") <= radius )
        .orderBy("distance", ascending = True)
        .withColumn("similarity", (F.lit(1.0) - (F.col("distance") / F.lit(intial_radius))) * F.lit(100.0) )
        .collect()
    )
    selected_images = selected_images[1:]
    shuffle(selected_images)
    selected_images = selected_images[:n]
    selected_images = sorted(selected_images, key = lambda row: row.distance)
    selected_images = [ r.asDict() for r in selected_images ]

    return jsonify(data = selected_images)


@app.route('/designers/<id>')
def get_similar_designer(id):
    intial_radius = float(request.args.get('initial-radius', 100))
    radius = float(request.args.get('radius', 80))
    n = int(request.args.get('n', 10))

    db = mongo.db

    img = db.images.find_one({'_id': ObjectId(id) })
    target = img["embeddings"]

    selected_images = (
        IMAGES_DESIGNERS.rdd.map(lambda row: Row(
            _id = row._id,
            filename = row.filename,
            distance = euclidean(row.embeddings, target)
        ))
        .toDF()
        .where(F.col("distance") <= radius )
        .orderBy("distance", ascending = True)
        .withColumn("similarity", (F.lit(1.0) - (F.col("distance") / F.lit(intial_radius))) * F.lit(100.0) )
        .collect()
    )
    selected_images = selected_images[1:]
    shuffle(selected_images)
    selected_images = selected_images[:n]
    selected_images = sorted(selected_images, key = lambda row: row.distance)
    selected_images = [ r.asDict() for r in selected_images ]

    return jsonify(data = selected_images)


if __name__ == '__main__':
    app.run(
        host = "0.0.0.0",
        debug = False
    )
