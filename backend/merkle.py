import psycopg2
from pymerkle import MerkleTree
from hashlib import sha256
from ecdsa import SigningKey, SECP256k1
from web3 import Web3

def fetch_issuers_from_db():
    connection = psycopg2.connect("postgresql://postgres:L8RTsfQAJ3wuh7y4@exactly-assured-sawfly.data-1.use1.tembo.io:5432/postgres")
    cursor = connection.cursor()
    
    cursor.execute("SELECT address, name FROM issuers")

    issuers = cursor.fetchall()

    cursor.close()
    connection.close()

    return({"address": address, "name": name} for address, name in issuers)

def generate_keys():
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    return private_key, public_key

def sign_data (private_key, data):
    return private_key.sign(data.encode('utf-8'))

def verify_signature(public_key, signature, data):
    return public_key.verify(signature, data.encode('utf-8'))

def generate_merkle_tree(issuers):
    tree = MerkleTree(hash_type='sha256')

    for issuer in issuers:
        private_key, public_key = generate_keys()
        signed_pair = f"{issuer['address']},{issuer['name']}"
        signature = sign_data(private_key, signed_pair)

        issuer['public_key'] = public_key.to_string().hex()
        issuer['signature'] = signature.hex()

        tree.encrypt(Web3.keccak(text=signed_pair).hex())
    return tree.rootHash


if __name__ == '__main__':
    issuers = fetch_issuers_from_db()
    root_hash = generate_merkle_tree(issuers)
    print(f'Root hash: {root_hash}')
    for issuer in issuers:
        print(f"Address: {issuer['address']}, Name: {issuer['name']}, Public Key: {issuer['public_key']}, Signature: {issuer['signature']}")