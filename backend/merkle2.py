from merkly.mtree import MerkleTree
import sha3

# create a Merkle Tree
mtree = MerkleTree([
'0xb740f5dc069385781027d287535c0092d3d2d8762fb3c501754710a34b827420a68073ab0b955ef5d73b8927a16e43bb0d83c54fa9eca16cdf73e67b0f3ae9bb5b996474769fa57d16150d6a19cacaab2fe7f938bafe6f041d93657667e7ff21a1c4f73d351231a1ce52d58a922ce984767fea26c435bd2a9e68de1ca68b369d', 
'0x948261ed42ef296ab681b7a2a5f0dbed656330c65c554af68ad4ef47b09d6d659324bac2bb89ff8449126bc7e94f1403f539e1c7e1b17572ed2d3e85636d5d0b3575a524217304b052baeb0fd32667f3ee2d7dfd2b03af1263369ec981b98f33bc7bc2a9a8a23974a6a0bb39beceec3235c0c79a5228a86ff6ba9d571ab0de7f',
'0x1bf0f08b020f588d341e5dd5abe69ce12173db7e7561c72861f926371e8a70e0d1023282d5e7f2382d11b73813de2a373aa95770c883f2b93d3bd62f596c6e07b0b6656304afdd15ab759d5dce941c3640b7225bee92cefd34f83abd43f16e8f075a70e078bf4328bd0bd65df79e485a609f376294de80498c84dd184d37b771',
'0x7475bc9a49133141cf2f09fff210bab8e659d429a1059b7c07f0570b8b3f6faa4c02da8ffdbfda3478c72f447e2c313f5be5021842e97eae46c945090af020cf13e1b76df7290f22e1afd0b129722ea3dcca7834e21f7461f0f577818f30fd72f2923227c861db7671ff39a69b538cf475089c7e28c04a10410388e4d25d4d3'])

# get root of tree (This is compatible with MerkleTreeJS)

print(mtree.root.hex())

def keccak256(data):
    k = sha3.keccak_256()
    k.update(data)
    return k.digest()

# Given hashes
H_a = bytes.fromhex("a432d4bbe37a060aacbb69e5071ea1ddeefc7eb2a3020a7580a4113df65b9961")
H_b = bytes.fromhex("e60d063637e26941368788fbd6f52fc02319a9ad3fd36086aea13eee72d1be5a")
H_c = bytes.fromhex("0c61cc564f1df0d0e0ddab3f2e5b280f6d914c6e9e3d00d9da43434fa57a3be8")
H_d = bytes.fromhex("13af29aa71741de1a9b72e016c778865a392b069051c995af7f8948042925a55")

# Calculate H(H(a) + H(b))
H_ab = keccak256(H_a + H_b)
print("H(H(a) + H(b)) =", H_ab.hex())

# Calculate H(H(c) + H(d))
H_cd = keccak256(H_c + H_d)
print("H(H(c) + H(d)) =", H_cd.hex())



root = keccak256(H_ab + H_cd)
print("Root =", root.hex())