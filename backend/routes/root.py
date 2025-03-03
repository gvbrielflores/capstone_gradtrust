from flask import Blueprint, jsonify, request
from merkle import fetch_issuers_from_db, generate_merkle_tree

merkle = Blueprint('merkle', __name__, url_prefix='/merkle')

@merkle.route('/generate', methods=['POST'])
def generate():
    try:
        issuers = fetch_issuers_from_db()
        
        if not issuers:
            return jsonify({'error': 'No issuers provided'}), 400
        
        merkle_root = generate_merkle_tree(issuers)
        return jsonify({'merkle_root': merkle_root}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
