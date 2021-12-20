from flask import Flask, request, render_template, redirect
import pymongo
from bson.objectid import ObjectId
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(host="localhost", port=27017)
    mongo.server_info()
    db = mongo.Movie
except: 
    print("ERROR - Cannot connect to db")


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

@app.route("/", methods=["POST", "GET"])
def mainpage():
    if request.method == "POST":
        try:
            movie_name = {"name": request.form['movie_content']}
            db.movies.insert_one(movie_name)
            return redirect('/')
        except Exception as ex:
            print(ex)
            return 'There was an issue'
    else:
        movies = list(db.movies.find())
        return render_template('index.html', movies=movies)

@app.route("/delete/<id>")
def delete(id):
    try:
        db.movies.delete_one({'_id':ObjectId(id)})
        return redirect('/')
    except:
        return 'there was a problem with deleting'

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    movie_id = db.movies.find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        try:
            db.movies.update_one({"_id": ObjectId(id)}, {"$set":{"name": request.form["movie_content"]}})
            print(":DDDDDDD")
            return redirect('/')
        except Exception as ex:
            print(ex)
            return "there's issue updating task"
    else:
        return render_template('update.html', movie=movie_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)