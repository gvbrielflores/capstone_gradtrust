from pymerkle import InmemoryTree as MerkleTree
import psycopg2

class IssuerVerification:
    """
    Handles Merkle tree operations for issuer verification.
    Builds Merkle tree from issuer signatures and provides proof generation.
    """

    def __init__(self):
        """Initialize database connection and build Merkle tree"""
        self.conn = psycopg2.connect(
            'postgresql://postgres:L8RTsfQAJ3wuh7y4@exactly-assured-sawfly.data-1.use1.tembo.io:5432/postgres'
        )
        self.tree = self._build_tree()

    def _build_tree(self):
        """
        Build Merkle tree from issuer signatures in database.
        Returns:
            MerkleTree: Merkle tree containing issuer signatures
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, signature FROM issuers")
        issuer_data = cursor.fetchall()
        cursor.close()

        if not issuer_data:
            raise ValueError("No issuers found in database")

        # Map issuer details to their signatures
        self.issuer_map = {}
        leaves = []

        for address, name, signature in issuer_data:
            leaves.append(signature)
            self.issuer_map[(address, name)] = signature

        tree = MerkleTree(algorithm='keccak_256', disable_security=True)
        for leaf in leaves:
            tree.append_entry(leaf)
        return tree

    def get_merkle_root(self):
        """
        Get the current Merkle root.
        Returns:
            str: Hex string of Merkle root
        """
        return self.tree.root.hex()

    def get_issuer_proof(self, issuer_address, issuer_name):
        """
        Get Merkle proof for a specific issuer.
        
        Args:
            issuer_address (str): Ethereum address of the issuer
            issuer_name (str): Name of the issuer

        Returns:
            dict: Contains proof array and leaf value
            
        Raises:
            ValueError: If issuer not found in tree
        """
        try:
            signature = self.issuer_map[(issuer_address, issuer_name)]
        except KeyError:
            raise ValueError(f"Issuer not found: {issuer_address} ({issuer_name})")

        # Get proof from tree
        proof_data = self.tree.proof(signature)
        
        # Extract proof nodes and their positions
        proof_nodes = []
        is_left = []
        
        for node in proof_data:
            # Get node value and side from proof
            side = repr(node).split('Side.')[1].strip(')')
            hex_value = repr(node).split('(')[1].split(',')[0]
            
            proof_nodes.append(hex_value)
            is_left.append(side == 'LEFT')

        return {
            'proof': proof_nodes,
            'isLeft': is_left,
            'leaf': signature
        }

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()