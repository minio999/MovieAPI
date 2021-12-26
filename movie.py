from flask import Flask, request, Response
import pymongo
from bson.objectid import ObjectId
import json

class Movie:
    app = Flask(__name__)
    
    # initializing connection with mongo 
    def __init__(self):
        try:
            mongo = pymongo.MongoClient(host='movie_db', port=27017, username='root', password='pass')
            mongo.server_info() # trigger exception if not connected to db
            global db 
            db = mongo.Movie
        except: 
            print("ERROR - Cannot connect to db")

    # debug purposes
    @app.route("/")
    def hello_world():
        return "Hello World!"

    # making route for POST method to add movies
    @app.route("/movies", methods=["POST"])
    def addMovies():
        try:
            movie = request.get_json()
            movie['id'] = movie['name'] + movie['yearMade'] + movie['director'] # creating id column to get id by name tear made and diractor for example "terminator1984spielberg" if name is terminator, yearMade is 1984 etc
            dbResponse = db.movies.insert_one(movie)
            return Response(response=json.dumps({"message":"movie creaeted", "id":f"{dbResponse.inserted_id}"}), status=200, mimetype="application/json") # retruning response if we add movie sucessfully
        except Exception as ex:
            print(ex)
            return Response(response=json.dumps({"message":"cannot create movie"}), status=500, mimetype="application/json") # returning response if we dont add movie 
    
    # making route for GET method to get all movies
    @app.route("/movies", methods=["GET"]) 
    def getMovies():
        try:
            data = list(db.movies.find()) # taking all movies in db and changing it to list 
            for movie in data:
                movie["_id"] = str(movie["_id"]) # changing ObjectID type into string 
            return Response(response=json.dumps(data), status=200, mimetype="application/json") # returning data as a response
        except Exception as ex:
            print(ex)
            return Response(response=json.dumps({"message":"cannot read movies"}), status=500, mimetype="application/json") # returning message if we dont get movies

    # making routhe for DELETE to delete a movie base on their id
    @app.route("/movies/<id>", methods=["DELETE"])
    def deleteMovie(id):
        try:
            dbResponse = db.movies.delete_one({"id":id}) 
            if dbResponse.deleted_count == 1: # checking if movie was deleted 
                return Response(response=json.dumps({"message":"movie deleted", "id":f"{id}"}), status=200, mimetype="application/json") # if movie is deleted returning response 
            return Response(response=json.dumps({"message":"movie not existing", "id":f"{id}"}), status=200, mimetype="application/json") # returning response if movie not existing
        except Exception as ex:
            print(ex)
            return Response(response=json.dumps({"message":"cannot delete movie"}), status=500, mimetype="application/json")