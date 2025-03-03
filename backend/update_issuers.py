import psycopg2
from web3 import Web3
from eth_account import Account
import os
import dotenv

# load the .env file
dotenv.load_dotenv()

# get the private key from said file
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
# get the database connection string too
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

if not PRIVATE_KEY:
    raise ValueError('missing PRIVATE_KEY env var')

if not CONNECTION_STRING:
    raise ValueError('missing CONNECTION_STRING env var')

def sign_data(data, private_key):
    #another way to sign if you have the private key...
    account = Account.from_key(private_key)
    message = Web3.solidityKeccak(['string'], [data])
    signed_message = account.sign_message(message)
    return signed_message.signature.hex()

def update_issuers():
    # connect to database
    connection = psycopg2.connect(CONNECTION_STRING)
    cursor = connection.cursor()

    # get the addresses and names of all issuers who do not have a signature
    cursor.execute("SELECT address, name FROM issuers WHERE signature IS NULL")
    issuers = cursor.fetchall()

    # sign the data and update the database
    for address, name in issuers:
        data_to_sign = f"{address},{name}"
        signature = sign_data(data_to_sign, PRIVATE_KEY)

        cursor.execute("UPDATE issuers SET signature = %s WHERE address = %s", (signature, address))

    # commit the changes to the database and close the cursor and connection
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    update_issuers()
