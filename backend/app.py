from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from routes import blueprints
import os
import dotenv

dotenv.load_dotenv()
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = CONNECTION_STRING
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    
    # Register all blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)