from merkly.mtree import MerkleTree
import sha3

# create a Merkle Tree
mtree = MerkleTree([
'a', 
'b',
'c',
'd'])

# get root of tree (This is compatible with MerkleTreeJS)

print(mtree.root.hex())

print(mtree.proof('d'))