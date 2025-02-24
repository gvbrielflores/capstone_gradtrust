from flask import Blueprint, request, Response, jsonify
import os
import dotenv
import json
import eth_account
from web3 import Web3

dotenv.load_dotenv()

credentials = Blueprint('credentials', __name__, url_prefix='credentials')

# TODO - FOR DEVELOPMENT PURPOSES ONLY, IN PRODUCTION/TESTNET TESTING, NEED TO IMPLEMENT PRIVATE KEY STORAGE FOR ISSUER
# (OR HAVE THEM MANUALLY INPUT - worst option)
ISSUER_KEY = os.getenv('TEST_ISSUER_PRIV_KEY')
if not ISSUER_KEY:
    raise ValueError('missing TEST_ISSUER_PRIV_KEY env var')

def sign_data(hash):
    signedData = eth_account.Account.sign_message(hash, private_key=ISSUER_KEY)
    return signedData.signature.hex()

@credentials.route('/issue', methods=['POST'])
def issue():
    try:
        data = request.json
        credentialData = json.dumps(data, sort_keys=True)
        credentialHash = Web3.keccak(text=credentialData).hex()

        signature = sign_data(credentialHash.encode())

        return jsonify({
            "credential_hash" : credentialHash,
            "signature" : signature
        }), 200

    except Exception as e:
        return jsonify({"error" : "There was an unexpected error while issuing credential"}), 500
    
@credentials.route('/verify', methods=['get'])
def verify():
    try:
        data = request.json
        return jsonify({"message": "yay"}), 200

    except Exception as e:
        return jsonify({"error": "There was an unexpected error while verifying credential"}), 500