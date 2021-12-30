from flask_swagger_ui import get_swaggerui_blueprint
from app import app

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