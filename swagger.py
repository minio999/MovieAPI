from flask_swagger_ui import get_swaggerui_blueprint


class swagger:
    # setting app swagger setting on init and returning blueprint
    def __init__(self):
        SWAGGER_URL = '/swagger'
        API_URL = '/static/json/swagger.json'
        SWAGGER_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config = {'app_name' : 'Movie Api'})