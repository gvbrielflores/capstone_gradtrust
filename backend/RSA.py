############################################
#FOR TESTING PURPOSES
############################################
from Crypto.PublicKey import RSA
keyPair = RSA.generate(1024)
private_key = keyPair.export_key()
print(private_key.decode('utf-8'))
public_key = keyPair.publickey().export_key()
print(public_key.decode('utf-8'))

pairs = [('0x31B39c6F5E83FC03B7dd5A98047A3C75fD1dE487', 'Blake'), ('0x9DbE33e61Ca2F65118fbCAf182aC2Cdd2cAB4a42', 'Segun'), ('0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266', 'Tuser1'), ('0x70997970C51812dc3A010C7d01b50e0d17dc79C8', 'Tuser2'), ('0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC', 'Tuser3'), ('0x90F79bf6EB2c4f870365E785982E1f101E93b906', 'Tuser4')]


from hashlib import sha256
signatures=[]
for pair in pairs:
    pair_bytes = ",".join(pair).encode('utf-8')
    print(pair_bytes)
    hash = int.from_bytes(sha256(pair_bytes).digest(), byteorder='big')
    signatures.append(pow(hash, keyPair.d, keyPair.n))



for sig in signatures:
    print(f"Signature: {hex(sig)} for {pairs[signatures.index(sig)][1]}")


def verify_signature(public_key, signature, message):
    hash = int.from_bytes(sha256(message.encode('utf-8')).digest(), byteorder='big')
    hash_from_signature = pow(signature, public_key.e, public_key.n)
    return hash == hash_from_signature

for i, sig in enumerate(signatures):
    message = ",".join(pairs[i])
    if verify_signature(keyPair.publickey(), sig, message):
        print(f"Signature for {pairs[i][1]} is valid.")
    else:
        print(f"Signature for {pairs[i][1]} is invalid.")

verify_signature(keyPair.publickey(), signatures[0], ",".join(pairs[0]))

from Crypto.Hash import keccak

def keccak256(data):
    k = keccak.new(digest_bits=256)
    k.update(data)
    return k.digest()

# Convert hex strings into bytes
hash_a = bytes.fromhex("a432d4bbe37a060aacbb69e5071ea1ddeefc7eb2a3020a7580a4113df65b9961")
hash_b = bytes.fromhex("e60d063637e26941368788fbd6f52fc02319a9ad3fd36086aea13eee72d1be5a")
hash_c = bytes.fromhex("0c61cc564f1df0d0e0ddab3f2e5b280f6d914c6e9e3d00d9da43434fa57a3be8")
hash_d = bytes.fromhex("13af29aa71741de1a9b72e016c778865a392b069051c995af7f8948042925a55")

# Compute first level of Merkle tree
H_AB = keccak256(hash_a + hash_b)
H_CD = keccak256(hash_c + hash_d)

# Compute Merkle root
merkle_root = keccak256(H_AB + H_CD)

# Print results
print("H(AB):", H_AB.hex())
print("H(CD):", H_CD.hex())
print("Merkle Root:", merkle_root.hex())

