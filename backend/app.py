from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import api
from routes.root import merkle
import dotenv
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Register api routes root '/api'
    app.register_blueprint(api)
    app.register_blueprint(merkle)

    # load the .env file
    dotenv.load_dotenv()

    # get the database connection string
    CONNECTION_STRING = os.getenv('CONNECTION_STRING')

    app.config["SQLALCHEMY_DATABASE_URI"] = CONNECTION_STRING
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from route import register_routes
    register_routes(app, db)

    return app


