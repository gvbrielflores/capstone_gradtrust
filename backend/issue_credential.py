from merkly.mtree import MerkleTree
from web3 import Web3
import psycopg2
from hashlib import sha256
import os
from dotenv import load_dotenv

class IssuerVerification:
    def __init__(self):
        """Initialize database connection and create Merkle tree"""
        self.connection = psycopg2.connect('postgresql://postgres:L8RTsfQAJ3wuh7y4@exactly-assured-sawfly.data-1.use1.tembo.io:5432/postgres')
        self.cursor = self.connection.cursor()
        self.tree = None
        self.leaves = []
        self.issuer_map = {}  # Store issuer info for quick lookup
        self._build_tree()
    
    def _build_tree(self):
        """Build Merkle tree from issuer signatures"""
        # Get all signatures
        self.cursor.execute("SELECT id, name, signature FROM issuers")
        issuers = self.cursor.fetchall()
        
        # Store leaves and create mapping
        self.leaves = []
        self.issuer_map = {}
        
        print("\nIssuers being processed:")
        for addr, name, sig in issuers:
            print(f"Address: {addr}, Name: {name}")
            print(f"Signature: {sig}\n")
            
            # Use signatures directly as leaves
            self.leaves.append(sig)
            
            # Map address+name to signature and index
            self.issuer_map[f"{addr},{name}"] = {
                'signature': sig,
                'index': len(self.leaves) - 1
            }
        
        # Create tree
        self.tree = MerkleTree(self.leaves)
        print(f"Merkle root: {self.tree.root.hex()}")
    
    def get_merkle_root(self):
        """Get the current Merkle root"""
        if not self.tree:
            raise ValueError("Merkle tree not initialized")
        
        root = self.tree.root.hex()
        print(f"Current Merkle root: {root}")
        return root
    
    def _get_issuer_data(self, issuer_address, issuer_name):
        # Query database for issuer data
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT signature FROM issuers WHERE id = %s AND name = %s",
            (issuer_address, issuer_name)
        )
        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                'signature': result[0]
            }
        return None

    def get_issuer_proof(self, issuer_address, issuer_name):
        # Get issuer data from database
        issuer_data = self._get_issuer_data(issuer_address, issuer_name)
        if not issuer_data:
            raise ValueError("Issuer not found")

        # Get proof from Merkle tree - returns list directly
        proof_nodes = self.tree.proof(issuer_data['signature'])
        
        # Process proof data to include side information
        proof_with_sides = []
        for node in proof_nodes:  # Iterate over the list directly
            side = repr(node).split('Side.')[1].strip(')')
            hex_value = repr(node).split('(')[1].split(',')[0]
            
            proof_with_sides.append({
                'value': hex_value,
                'side': side == 'LEFT'  # Convert to boolean for the contract
            })

        return {
            'proof': [p['value'] for p in proof_with_sides],
            'isLeft': [p['side'] for p in proof_with_sides],
            'leaf': issuer_data['signature']
        }
    
    def refresh_tree(self):
        """Rebuild the tree with current database state"""
        self._build_tree()
    
    def close(self):
        """Close database connection"""
        self.cursor.close()
        self.connection.close()

# Test functions
if __name__ == "__main__":
    # Create verifier instance
    verifier = IssuerVerification()
    
    try:
        # Get the root
        print("Calculating Merkle root...")
        root = verifier.get_merkle_root()
        
        print("\nGetting proof for specific issuer...")
        result = verifier.get_issuer_proof("0x9DbE33e61Ca2F65118fbCAf182aC2Cdd2cAB4a42", "Segun")
        
        print("\nVerification Data:")
        print(f"Signed Message: {result['signed_message']}")
        print(f"Leaf (Signature): {result['leaf']}")
        print(f"Proof: {result['proof']}")
        
    finally:
        # Make sure we close the database connection
        verifier.close()