// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CredentialVerification {
    bytes32 public merkleRoot; // On-chain Merkle root for verified issuers

    struct Credential {
        bytes32 credentialHash;
        address issuer;
        address holder;
        uint256 issuedAt;
        string data;
    }

    // Storage mapping for credentials
    mapping(bytes32 => Credential) private credentials;

    // Events
    event CredentialStored(
        bytes32 indexed credentialHash,
        address indexed issuer,
        address indexed holder,
        uint256 issuedAt,
        string data
    );
    event MerkleRootUpdated(bytes32 newMerkleRoot);
    event CredentialDeleted(bytes32 indexed credentialHash);

    // Modifier to check if an issuer is valid (only verifies Merkle proof)
    modifier onlyVerifiedIssuer(
        bytes32[] memory proof,
        bytes32 signedPairHash
    ) {
        require(
            verifyIssuer(proof, signedPairHash),
            "Invalid issuer: Merkle proof failed"
        );
        _;
    }

    // Function to store a new credential (Issuer must be verified via Merkle proof)
    function storeCredential(
        bytes32 _credentialHash,
        address _holder,
        uint256 _issuedAt,
        string calldata _data,
        bytes32[] calldata _merkleProof,
        bytes32 signedPairHash
    ) external onlyVerifiedIssuer(_merkleProof, signedPairHash) {
        require(
            credentials[_credentialHash].issuer == address(0),
            "Credential already exists"
        );

        credentials[_credentialHash] = Credential(
            _credentialHash,
            msg.sender,
            _holder,
            _issuedAt,
            _data
        );
        emit CredentialStored(
            _credentialHash,
            msg.sender,
            _holder,
            _issuedAt,
            _data
        );
    }

    // Function to verify if an address is a registered issuer using a Merkle proof
    function verifyIssuer(
        bytes32[] memory proof,
        bytes32 signedPairHash
    ) public view returns (bool) {
        bytes32 computedHash = signedPairHash;

        // Process the Merkle proof
        for (uint256 i = 0; i < proof.length; i++) {
            bytes32 proofElement = proof[i];
            if (computedHash < proofElement) {
                computedHash = keccak256(
                    abi.encodePacked(computedHash, proofElement)
                );
            } else {
                computedHash = keccak256(
                    abi.encodePacked(proofElement, computedHash)
                );
            }
        }

        return computedHash == merkleRoot; // Compare with the stored Merkle root
    }

    // Function to update the Merkle root (only callable by admin - assumed to be the contract owner)
    //changed this to internal so deleteCredential can call it
    function updateMerkleRoot(bytes32 _newMerkleRoot) internal {
        merkleRoot = _newMerkleRoot;
        emit MerkleRootUpdated(_newMerkleRoot);
    }

    // Function to check if a credential exists
    function verifyCredential(
        bytes32 _credentialHash
    ) public view returns (bool) {
        return credentials[_credentialHash].issuer != address(0);
    }

    // function to delete a credential
    function deleteCredential(bytes32 _credentialHash, bytes32 _newMerkleRoot) external {
        // Check if the credential exists
        require(credentials[_credentialHash].issuer != address(0), "Credential does not exist");

        // delete the credential
        delete credentials[_credentialHash];
        // let external world know that the credential has been deleted
        emit CredentialDeleted(_credentialHash);

        // update the merkle root
        updateMerkleRoot(_newMerkleRoot);
    }
}
