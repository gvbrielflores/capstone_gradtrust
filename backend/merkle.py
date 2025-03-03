import psycopg2
from pymerkle import MerkleTree
from hashlib import sha256

def keccak256(data):
    return sha256(data.encode('utf-8')).hexdigest()

def fetch_issuers_from_db():
    connection = psycopg2.connect("postgresql://postgres:L8RTsfQAJ3wuh7y4@exactly-assured-sawfly.data-1.use1.tembo.io:5432/postgres")
    
    cursor = connection.cursor()
    cursor.execute("SELECT address, name FROM issuers")

    issuers = cursor.fetchall()

    cursor.close()
    connection.close()

    return({"address": address, "name": name} for address, name in issuers)

def generate_merkle_tree(issuers):
    tree = MerkleTree(hash_type='sha256')

    for issuer in issuers:
        signed_pair = f"{issuer['address']},{issuer['name']}"
        tree.encrypt(keccak256(signed_pair))
    return tree.rootHash


