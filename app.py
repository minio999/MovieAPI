from flask import Flask
import pymongo
from flask_swagger_ui import get_swaggerui_blueprint
import app.movie_mod 


app = Flask(__name__)


# connecting to mongo client
try:
    mongo = pymongo.MongoClient(host='test_mongodb', port=27017, username='root', password='pass')
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

@app.route("/")
def hello_world():
    """ this function is made for debug purpose """
    return "<p>Hello, World!</p>"

#running app
if __name__ == "__main__":
    app.run(debug=True)
