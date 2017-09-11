import sys
sys.path.append('/models/')

from datetime import datetime
from flask import Flask, request
from flask_pymongo import PyMongo
from utils import jsonify
import time
from dataframes import get_dataframes
from pyspark.sql.session import SparkSession
from models import ALS_Model, AVG_Model

####################
# SPARK
####################

spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

RATINGS, MOVIES, USERS = get_dataframes(spark)
RATINGS = RATINGS.cache()

ALS = ALS_Model().load("als")
AVG = AVG_Model().load(spark, "avg")

####################
# FLASK
####################

app = Flask("recsys")

####################
# MONGO
####################

app.config["MONGO_DBNAME"] = "recsys"
app.config["MONGO_URI"] = "mongodb://mongo:27017/recsys"
mongo = PyMongo(app)


####################
# API
####################

@app.route("/predict-interests", methods = ["POST"])
def predict_interests():
    data = request.get_json()

    if "userId" not in data:
        return jsonify(error = "userId key not found in data")

    user_id = data.get("userId")
    n_preds = data.get("nPreds", 5)
    min_users = data.get("minUsers", 3)
    model = data.get("model", "als")

    if model == "als":
        model = ALS
    elif model == "avg":
        model = AVG
    else:
        return jsonify(error = "Invalid model {}".format(model))

    recomendations = model.recommend(user_id = user_id, ratings = RATINGS, n_preds = n_preds, min_users=min_users)

    return jsonify(data = recomendations)


@app.route("/add-data", methods = ["POST"])
def add_data():
    data = request.get_json()

    if "userId" not in data:
        return jsonify(error = "userId key not found in data")

    if "itemId" not in data:
        return jsonify(error = "itemId key not found in data")

    record = dict(
        user_id = data.get("userId"),
        movie_id = data.get("itemId"),
        rating = data.get("rating", 3),
        unix_timestamp = int(time.time()),
    )

    record["_id"] = mongo.db.ratings.insert(record)


    return jsonify(data = record)

@app.route("/ratings", methods = ["GET"])
def list_ratings():
    return jsonify(
        data = dict(
            ratings = mongo.db.ratings.count()
        )
    )


if __name__ == '__main__':
    app.run(
        host = "0.0.0.0",
        # debug = True
    )
