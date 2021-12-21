from flask import Flask, request, render_template, redirect, Response
import pymongo
from bson.objectid import ObjectId
from flask_swagger_ui import get_swaggerui_blueprint
import json

app = Flask(__name__)


# connecting to mongo client
try:
    mongo = pymongo.MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=1000)
    mongo.server_info() # trigger exception if not connected to db
    db = mongo.Movie
except: 
    print("ERROR - Cannot connect to db")

# setting up swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/json/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name' : 'Movie Api'
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)

# making route for POST
@app.route("/movies", methods=["POST"])
def addMovies():
    try:
        movie = {"name":request.form["name"], "yearMade":request.form["yearMade"], "director": request.form["director"]}
        dbResponse = db.movies.insert_one(movie)
        return Response(response=json.dumps({"message":"user creaeted", "id":f"{dbResponse.inserted_id}"}), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message":"cannot create users"}), status=500, mimetype="application/json")

# making route for GET
@app.route("/movies", methods=["GET"])
def getMovies():
    try:
        data = list(db.movies.find())
        for movie in data:
            movie["_id"] = str(movie["_id"]) # changing ObjectID into string 
        return Response(response=json.dumps(data), status=200, mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message":"cannot read movies"}), status=500, mimetype="application/json")

#running app
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=True)