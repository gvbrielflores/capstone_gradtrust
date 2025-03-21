import psycopg2
from pymerkle import InmemoryTree as MerkleTree
from ecdsa import SigningKey, SECP256k1
from web3 import Web3
import os
import dotenv

# load the .env file
dotenv.load_dotenv()

# get the database connection string
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

def fetch_issuers_from_db():
    # connect to the database
    connection = psycopg2.connect(CONNECTION_STRING)

    # create a cursor object
    cursor = connection.cursor()
    # get the addresses and names of all issuers
    cursor.execute("SELECT address, name FROM issuers")

    # fetch all the results
    issuers = cursor.fetchall()

    # close the cursor and connection
    cursor.close()
    connection.close()

    # return the addresses and names as a list of dictionaries
    return({"address": address, "name": name} for address, name in issuers)

def generate_keys():
    # generate a private key and a public key
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()

    # return the private key and the public key
    return private_key, public_key

def sign_data (private_key, data):
    # sign a piece of data using a private key
    return private_key.sign(data.encode('utf-8'))

def verify_signature(public_key, signature, data):
    # verify the signature came from the private key associated with the public key
    return public_key.verify(signature, data.encode('utf-8'))

def generate_merkle_tree(issuers):
    # create a new Merkle tree
    tree = MerkleTree(hash_type='sha256')

    for issuer in issuers:
        # generate a private key and a public key for each issuer
        private_key, public_key = generate_keys()
        # (id/address, name) pair that will be signed by the private key
        signed_pair = f"{issuer['id']},{issuer['name']}"
        # sign the pair using the private key 
        signature = sign_data(private_key, signed_pair)

        # add the public key and the signature to the issuer dictionary
        issuer['public_key'] = public_key.to_string().hex()
        issuer['signature'] = signature.hex()

        # add the signed pair to the Merkle tree
        tree.add_entry(Web3.keccak(text=signed_pair).hex())

    # return the root hash of the Merkle tree
    return tree.rootHash

def recalculate_merkle_root():
        issuers = fetch_issuers_from_db()
        return generate_merkle_tree(issuers)


if __name__ == '__main__':
    # fetch the issuers from the database
    issuers = fetch_issuers_from_db()
    # generate the merkle tree and get the root hash
    root_hash = generate_merkle_tree(issuers)
    # print the stuff
    print(f'Root hash: {root_hash}')
    for issuer in issuers:
        print(f"Address: {issuer['address']}, Name: {issuer['name']}, Public Key: {issuer['public_key']}, Signature: {issuer['signature']}")