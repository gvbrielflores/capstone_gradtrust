from flask import request
from models import issuers, accounts

def register_routes(app ,db):
    @app.route('/')
    def index():
        all_issuers = issuers.query.all()
        return str(all_issuers)
    