from pymerkle import InmemoryTree as MerkleTree
from pymerkle.hasher import MerkleHasher

algo = 'keccak_256'

#disabling security for testing purposes as it prepends to hash and makes it harder to manually compute hashes
tree = MerkleTree(algorithm=algo, disable_security=True)\
#can use the hasher functionality in pymerkle to manually check hash pairs
hasher = MerkleHasher(tree.algorithm, tree.security)

index = tree.append_entry(b"foo")
index2 = tree.append_entry(b"bar")
index3 = tree.append_entry(b"baz")

#getting the hash of the data for each leaf node (returns bytes)
value_byte = tree.get_leaf(index)
value2_byte = tree.get_leaf(index2)
value3_byte = tree.get_leaf(index3)

#in the case of odd number of leaves, last leaf is hashed with parent node on the left
hash_pair1 = hasher.hash_pair(value_byte, value2_byte)
hash_pair2 = hasher.hash_pair(hash_pair1, value3_byte)

print(f'Root hash should be: {hash_pair2.hex()}')

#this is how you get the merkle root (also returns bytes)
#hexify everything for easy comparison
state = tree.get_state().hex()
value = value_byte.hex()
value2 = value2_byte.hex()
value3 = value3_byte.hex()

print(f'Using hash function: {algo}')
print(f'Root hash: {state}')
print(f'1st leaf value: {value}')
print(f'2nd leaf value: {value2}')
print(f'3rd leaf value: {value3}')
print(f'Size of tree: {tree.get_size()}')