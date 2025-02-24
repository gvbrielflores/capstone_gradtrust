from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

# Register api routes
from .credentials import credentials

api.register_blueprint(credentials)