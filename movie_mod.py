from app import app
import pymongo
import json
from flask import request, Response


try:
    mongo = pymongo.MongoClient(host='test_mongodb', port=27017, username='root', password='pass')
    mongo.server_info() # trigger exception if not connected to db
    db = mongo.Movie
except:
    print("ERROR - Cannot connect to db")


@app.route("/movies", methods=["POST"])
def add_movies():
    """ if route is movies and method POST add movie to database from a json file """
    try:
        movie = request.get_json()
        # creating id column to get id by name tear made and diractor for example "terminator1984spielberg" if name is terminator, yearMade is 1984 etc
        movie['id'] = movie['name'] + movie['yearMade'] + movie['director']
        db_response = db.movies.insert_one(movie)
        return Response(response=json.dumps({"message":"movie creaeted", "id":f"{db_response.inserted_id}"}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message":"cannot create movie"}), status=500, mimetype="application/json")

@app.route("/movies", methods=["GET"])
def get_movies():
    """ on route /movies with method get, get all movies from database """
    try:
        data = list(db.movies.find())
        for movie in data:
            movie["_id"] = str(movie["_id"]) # changing ObjectID into string
        return Response(response=json.dumps(data), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message":"cannot read movies"}), status=500, mimetype="application/json")

@app.route("/movies/<id>", methods=["DELETE"])
def delete_movie(id):
    """ on route /movies/<id> with <id> as a parameter and method DELETE, delete movie with <id> from database """
    try:
        db_response = db.movies.delete_one({"id":id})
        if db_response.deleted_count == 1: # checking if movie was deleted
            return Response(response=json.dumps({"message":"movie deleted", "id":f"{id}"}), status=200, mimetype="application/json")
        return Response(response=json.dumps({"message":"movie not existing", "id":f"{id}"}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message":"cannot delete movie"}), status=500, mimetype="application/json")