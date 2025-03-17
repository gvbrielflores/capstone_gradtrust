from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from routes import api
from routes.root import merkle
import dotenv
import os
from eth_account.messages import encode_defunct
from eth_account import Account
from web3 import Web3
from issue_verification import IssuerVerification
import json
import psycopg2
from flask_cors import CORS

# Create the SQLAlchemy instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS

    # # Register api routes root '/api'
    # app.register_blueprint(api)
    # app.register_blueprint(merkle)

    # # load the .env file
    # dotenv.load_dotenv()

    # Either use os.getenv with a key
    # CONNECTION_STRING = os.getenv('DATABASE_URL', 'postgresql://postgres:L8RTsfQAJ3wuh7y4@exactly-assured-sawfly.data-1.use1.tembo.io:5432/postgres')

    # Or just use the string directly since you're not using environment variables
    CONNECTION_STRING = 'postgresql://postgres:L8RTsfQAJ3wuh7y4@exactly-assured-sawfly.data-1.use1.tembo.io:5432/postgres'

    # Uncomment these lines
    app.config["SQLALCHEMY_DATABASE_URI"] = CONNECTION_STRING
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Create application context
    with app.app_context():
        # Web3 setup (Hardhat local node)
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

        # Contract addresses (convert to checksum format)
        ISSUER_REGISTRY_ADDRESS = Web3.to_checksum_address("0x5fbdb2315678afecb367f032d93f642f64180aa3")
        CREDENTIAL_VERIFICATION_ADDRESS = Web3.to_checksum_address("0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512")  # Your deployed address

        # Load contract ABI
        def load_contract_abi(contract_name):
            artifact_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'artifacts',
                'contracts',
                f'{contract_name}.sol',
                f'{contract_name}.json'
            )
            with open(artifact_path) as f:
                return json.load(f)['abi']

        # Initialize contracts
        issuer_registry = w3.eth.contract(
            address=ISSUER_REGISTRY_ADDRESS,
            abi=load_contract_abi('IssuerRegistry')
        )
        
        credential_verification = w3.eth.contract(
            address=CREDENTIAL_VERIFICATION_ADDRESS,
            abi=load_contract_abi('CredentialVerification')
        )

        @app.route('/api/register-issuer', methods=['POST'])
        def register_issuer():
            """Register a new issuer with their signature"""
            data = request.json
            issuer_address = data.get('address')
            issuer_name = data.get('name')
            private_key = data.get('private_key')

            if not all([issuer_address, issuer_name, private_key]):
                return jsonify({'error': 'Missing required fields'}), 400

            try:
                # Create and sign message
                message = f"{issuer_address},{issuer_name}"
                message_hash = encode_defunct(text=message)
                signed_message = Account.sign_message(message_hash, private_key=private_key)
                signature = '0x' + signed_message.signature.hex()

                # Store in database
                with psycopg2.connect(CONNECTION_STRING) as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            INSERT INTO issuers (id, name, signature) 
                            VALUES (%s, %s, %s)
                            ON CONFLICT (id) 
                            DO UPDATE SET 
                                name = EXCLUDED.name,
                                signature = EXCLUDED.signature
                            """,
                            (issuer_address, issuer_name, signature)
                        )
                    conn.commit()

                return jsonify({
                    'success': True,
                    'address': issuer_address,
                    'name': issuer_name,
                    'signature': signature
                })

            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/test', methods=['GET'])
        def test():
            return jsonify({'status': 'Server is running'})

        @app.route('/api/issue-credential', methods=['POST'])
        def issue_credential():
            """Issue a new credential to a holder"""
            try:
                # Get request data
                credential_hash = request.form.get('credentialHash')
                holder_address = request.form.get('holderAddress')
                issuer_address = request.form.get('issuerAddress')
                issuer_name = request.form.get('issuerName')

                # Get issuer's Merkle proof
                verifier = IssuerVerification()
                try:
                    proof_data = verifier.get_issuer_proof(issuer_address, issuer_name)
                    
                    # Prepare contract call data
                    proof = [Web3.to_bytes(hexstr=p) for p in proof_data['proof']]
                    leaf_hash = Web3.keccak(text=proof_data['leaf'])
                    
                    # Store credential on chain
                    tx = credential_verification.functions.storeCredential(
                        Web3.to_bytes(hexstr=credential_hash),
                        Web3.to_checksum_address(holder_address),
                        w3.eth.get_block('latest').timestamp,
                        "Credential",
                        proof,
                        proof_data['isLeft'],
                        leaf_hash
                    ).transact({'from': issuer_address})
                    
                    receipt = w3.eth.wait_for_transaction_receipt(tx)
                    
                    return jsonify({
                        'success': True,
                        'transactionHash': receipt.transactionHash.hex(),
                        'credentialHash': credential_hash
                    })
                finally:
                    verifier.close()
                    
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/api/update-merkle-root', methods=['POST'])
        def update_merkle_root():
            """Update the Merkle root in the smart contract"""
            try:
                verifier = IssuerVerification()
                try:
                    new_root = verifier.get_merkle_root()
                    root_bytes = Web3.to_bytes(hexstr=new_root)
                    
                    # Update root using admin account
                    admin = w3.eth.accounts[0]
                    tx = issuer_registry.functions.updateMerkleRoot(
                        root_bytes
                    ).transact({'from': admin})
                    
                    receipt = w3.eth.wait_for_transaction_receipt(tx)
                    
                    return jsonify({
                        'success': True,
                        'merkleRoot': new_root,
                        'transactionHash': receipt.transactionHash.hex()
                    })
                finally:
                    verifier.close()
                    
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/api/verify-credential', methods=['GET'])
        def verify_credential():
            """Verify a credential's authenticity"""
            try:
                credential_hash = request.args.get('hash')
                if not credential_hash:
                    return jsonify({'error': 'Missing credential hash'}), 400

                # Convert hash to bytes32
                hash_bytes = Web3.to_bytes(hexstr=credential_hash)
                
                # Check credential on chain
                is_valid = credential_verification.functions.verifyCredential(
                    hash_bytes
                ).call()
                
                return jsonify({
                    'success': True,
                    'isValid': is_valid
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        root = issuer_registry.functions.merkleRoot().call()
        print(f"Updated root: {root.hex()}")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)


