import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import click
from odo import odo

@click.command()
@click.option('--dataset', '-d', default = "ml-100k", help='Number of greetings.')
def main(dataset):

    dataset_path = "/data/{}".format(dataset)

    print("Importing {}".format(dataset_path))

    print("Reading Data")
    if dataset == "ml-100k":
        #raings
        ratings = pd.read_csv(
            dataset_path + "/u.data",
            sep = '\t',
            names = ['user_id', 'movie_id', 'rating', 'unix_timestamp'],
            encoding = 'latin-1'
        )
        ratings
        #Reading movies file:
        movies = pd.read_csv(
            dataset_path + "/u.item",
            sep = '|',
            names = ['_id', 'title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'],
            encoding='latin-1'
        )
        movies
        #Reading users file:
        users = pd.read_csv(
            dataset_path + "/u.user",
            sep = '|',
            names = ['_id', 'age', 'sex', 'occupation', 'zip_code'],
            encoding ='latin-1'
        )

    elif dataset == "ml-1m":
        #raings
        ratings = pd.read_csv(
            dataset_path + "/ratings.dat",
            sep = '::',
            names = ['user_id', 'movie_id', 'rating', 'unix_timestamp'],
            encoding = 'latin-1'
        )
        ratings
        #Reading movies file:
        movies = pd.read_csv(
            dataset_path + "/movies.dat",
            sep = '::',
            names = ['_id', 'title', 'genres'],
            encoding='latin-1'
        )

        #Reading users file:
        users = pd.read_csv(
            dataset_path + "/users.dat",
            sep = '::',
            names = ['_id', 'age', 'sex', 'occupation', 'zip_code'],
            encoding ='latin-1'
        )

    elif dataset == "ml-20m" or dataset == "ml-latest-small" or dataset == "ml-latest":
        #raings
        ratings = odo(dataset_path + "/ratings.csv", pd.DataFrame)
        ratings.columns = ['user_id', 'movie_id', 'rating', 'unix_timestamp']

        #Reading movies file:
        movies = odo(dataset_path + "/movies.csv", pd.DataFrame)
        movies.columns = ['_id', 'title', 'genres']

        users = ratings.groupby("user_id", as_index=False).count()[["user_id"]].rename(columns={"user_id" : "_id"})

    else:
        print("Invalid dataset {}".format(dataset))
        return


    print("Connecting to MongoDB")
    # create mongo db
    client = MongoClient("mongo")
    db = client.recsys

    print("Dropping collections")
    # clean collections
    db.users.drop()
    db.movies.drop()
    db.ratings.drop()

    print("Inserting data")
    odo(users, db.users)
    odo(ratings, db.ratings)
    odo(movies, db.movies)


    print("Users: {}, Movies: {}, Ratings: {}".format(db.users.count(), db.movies.count(), db.ratings.count()))



if __name__ == '__main__':
    main()
