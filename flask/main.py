import sys
sys.path.append('/flask/')

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
        id = row.id_list[i]
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
    randoms = [ r.asDict() for r in randoms ]

    return jsonify(data = randoms)


@app.route('/images/<id:string>')
def get_similar(i):
    radius = request.args.get('user', 80)
    n = request.args.get('n', 10)+++++++++++++++++++++++++++++
    db = mongo.db

    img = db.images.find_one({'_id': ObjectId('59b61548a0931d451bb392d3') })
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


    # from IPython.display import Image
    # from IPython.core.display import HTML, display
    #
    for row in selected_images:
        filename = os.path.join(os.sep, "data", "images2440", row.filename)
        display(Image(filename = filename))




#
#
# ####################
# # API
# ####################
#
# @app.route("/predict-interests", methods = ["POST"])
# def predict_interests():
#     data = request.get_json()
#
#     if "userId" not in data:
#         return jsonify(error = "userId key not found in data")
#
#     user_id = data.get("userId")
#     n_preds = data.get("nPreds", 5)
#     min_users = data.get("minUsers", 3)
#     model = data.get("model", "als")
#
#     if model == "als":
#         model = ALS
#     elif model == "avg":
#         model = AVG
#     else:
#         return jsonify(error = "Invalid model {}".format(model))
#
#     recomendations = model.recommend(user_id = user_id, ratings = RATINGS, n_preds = n_preds, min_users=min_users)
#
#     return jsonify(data = recomendations)
#
#
# @app.route("/add-data", methods = ["POST"])
# def add_data():
#     data = request.get_json()
#
#     if "userId" not in data:
#         return jsonify(error = "userId key not found in data")
#
#     if "itemId" not in data:
#         return jsonify(error = "itemId key not found in data")
#
#     record = dict(
#         user_id = data.get("userId"),
#         movie_id = data.get("itemId"),
#         rating = data.get("rating", 3),
#         unix_timestamp = int(time.time()),
#     )
#
#     record["_id"] = mongo.db.ratings.insert(record)
#
#
#     return jsonify(data = record)
#
# @app.route("/ratings", methods = ["GET"])
# def list_ratings():
#     return jsonify(
#         data = dict(
#             ratings = mongo.db.ratings.count()
#         )
#     )
#
#
# if __name__ == '__main__':
#     app.run(
#         host = "0.0.0.0",
#         # debug = True
#     )
