from flask import Flask
from routes import api

app = Flask(__name__)

@app.route('/')
def start():
    return 'this is the start'

# Register api routes root '/api'
app.register_blueprint(api)

