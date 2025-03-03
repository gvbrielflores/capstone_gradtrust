import psycopg2
from web3 import Web3
from eth_account import Account
import os
import dotenv

dotenv.load_dotenv()

PRIVATE_KEY = os.getenv('PRIVATE_KEY')
if not PRIVATE_KEY:
    raise ValueError('missing PRIVATE_KEY env var')

def sign_data(data, private_key):
    account = Account.from_key(private_key)
    message = Web3.solidityKeccak(['string'], [data])
    signed_message = account.sign_message(message)
    return signed_message.signature.hex()

def update_issuers():
    connection = psycopg2.connect("postgresql://postgres:L8RTsfQAJ3wuh7y4@exactly-assured-sawfly.data-1.use1.tembo.io:5432/postgres")
    cursor = connection.cursor()

    cursor.execute("SELECT address, name FROM issuers WHERE signature IS NULL")
    issuers = cursor.fetchall()

    for address, name in issuers:
        data_to_sign = f"{address},{name}"
        signature = sign_data(data_to_sign, PRIVATE_KEY)

        cursor.execute("UPDATE issuers SET signature = %s WHERE address = %s", (signature, address))

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    update_issuers()
