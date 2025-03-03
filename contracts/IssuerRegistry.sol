// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract IssuerRegistry {

    // On-chain Merkle root of verified issuers
    bytes32 public merkleRoot; 
    address public admin;

    event MerkleRootUpdated(bytes32 newRoot);

    // Only called at posting of contract on chain - GradTrust address becomes admin
    constructor() {
        admin = msg.sender;
    }

    modifier onlyAdmin() {
        require(msg.sender == admin, "Not authorized");
        _;
    }

    // Function to update the Merkle root (only callable by admin - assumed to be the contract owner)
    function updateMerkleRoot(bytes32 _newMerkleRoot) external onlyAdmin {
        merkleRoot = _newMerkleRoot;
        emit MerkleRootUpdated(_newMerkleRoot);
    }

    // Verifies provided merkle proof using stored merkle root
    function verifyIssuer(
        bytes32[] calldata proof, 
        bytes32 leaf
    ) external view returns(bool) {
        bytes32 computedHash = leaf;
        for (uint256 i = 0; i < proof.length; i++) {
            bytes32 curNode = proof[i];
            if (computedHash < curNode) {
                computedHash = keccak256(
                    abi.encodePacked(computedHash, curNode)
                );
            }
            else {
                computedHash = keccak256(
                    abi.encodePacked(curNode, computedHash)
                );
            }

            return (computedHash == merkleRoot);
        }
        return false;
    }
}