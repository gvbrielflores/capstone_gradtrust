// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract IssuerRegistry {
    // On-chain Merkle root of verified issuers
    bytes32 public merkleRoot;
    address public admin;

    event MerkleRootUpdated(bytes32 newRoot);
    event ComputedHashUpdate(
        uint256 step,
        bytes32 computedHash,
        bytes32 proofElement
    );

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
    // Modified to match how we built the tree
    function verifyIssuer(
        bytes32[] memory proof,
        bool[] memory isLeft, // Array indicating if each proof element is a left sibling
        bytes32 leaf
    ) public view returns (bool) {
        bytes32 computedHash = leaf;

        for (uint256 i = 0; i < proof.length; i++) {
            bytes32 proofElement = proof[i];
            if (isLeft[i]) {
                // Left sibling: proofElement is on left, computedHash on right
                computedHash = keccak256(
                    abi.encodePacked(proofElement, computedHash)
                );
            } else {
                // Right sibling: computedHash is on left, proofElement on right
                computedHash = keccak256(
                    abi.encodePacked(computedHash, proofElement)
                );
            }
        }

        return computedHash == merkleRoot;
    }

    // Helper function to convert bytes32 to hex string
    function toHexString(uint256 value) internal pure returns (string memory) {
        bytes memory buffer = new bytes(64);
        for (uint256 i = 63; i >= 0; i--) {
            buffer[63 - i] = bytes1(
                uint8((value % 16) + (value % 16 < 10 ? 48 : 87))
            );
            value /= 16;
        }
        return string(buffer);
    }

    // Event for debugging
    event Debug(string message);

    function debugVerifyIssuer(
        bytes32[] memory proof,
        bytes32 leaf
    ) public returns (bool) {
        bytes32 computedHash = leaf;
        emit ComputedHashUpdate(0, computedHash, bytes32(0));

        for (uint256 i = 0; i < proof.length; i++) {
            bytes32 proofElement = proof[i];
            if (i == 0) {
                computedHash = keccak256(
                    abi.encodePacked(proofElement, computedHash)
                );
            } else {
                computedHash = keccak256(
                    abi.encodePacked(computedHash, proofElement)
                );
            }
            emit ComputedHashUpdate(i + 1, computedHash, proofElement);
        }

        emit ComputedHashUpdate(proof.length + 1, computedHash, merkleRoot);
        return computedHash == merkleRoot;
    }
}
