from ecdsa import SigningKey, SECP256k1
from eth_utils import keccak, to_checksum_address

def generate_private_key():
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key().to_string()
    address = to_checksum_address(keccak(public_key)[-20:])
    return private_key.to_string().hex(), address

if __name__ == '__main__':
    pk, address = generate_private_key()
    print(f'Private Key: {pk}')
    print(f'Address: {address}')