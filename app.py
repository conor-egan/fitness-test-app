from flask import Flask, Blueprint
from api.restplus import api
from api.endpoints.users import ns as users_namespace


application = Flask(__name__)


def initialize_app(flask_app):

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(users_namespace)
    flask_app.register_blueprint(blueprint)


def main():
    initialize_app(application)
    application.run()

if __name__ == "__main__":
    main()