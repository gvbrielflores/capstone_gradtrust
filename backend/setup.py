from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes import api
from routes.root import merkle
import dotenv
import os


app = Flask(__name__)

# Register api routes root '/api'
app.register_blueprint(api)
app.register_blueprint(merkle)

# load the .env file
dotenv.load_dotenv()

# get the database connection string
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

app.config["SQLALCHEMY_DATABASE_URI"] = CONNECTION_STRING

db = SQLAlchemy(app)

class issuers(db.Model):
    #id = blockchain address
    id = db.Column(db.String(255), primary_key = True)
    name = db.Column(db.String(255))
    signature = db.Column(db.String(300))

    def __repr__(self):
        return f'Issuer with ID {self.id} and Name {self.name}'

class accounts(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.String(255), nullable = False, unique=True)
    password = db.Column(db.String(255))

    def __repr__(self):
        return f'Account with ID {self.id} and Name {self.email}'