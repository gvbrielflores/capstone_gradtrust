// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import './IssuerRegistry.sol';

contract CredentialVerification {

    // Use to access members/call functions from IssuerRegistry
    IssuerRegistry public issuerRegistry; 

    // Credential data structure holds info on holder's cert
    struct Credential { 
        bytes32 credentialHash;
        address issuer;
        address holder;
        uint256 issuedAt;
        string data;
    }

    // Storage mapping for credentials
    mapping(bytes32 => Credential) public credentials;
    mapping(address => bytes32[]) public holderCredentials;

    // Events
    event CredentialStored(
        bytes32 indexed credentialHash,
        address indexed issuer,
        address indexed holder,
        uint256 issuedAt,
        string data
    );

    event CredentialDeleted(bytes32 indexed credentialHash);

    
    // WORRY ABOUT THIS LATER
    // // function to delete a credential
    // function deleteCredential(bytes32 _credentialHash) external {
    //     // Check if the credential exists
    //     require(credentials[_credentialHash].issuer != address(0), "Credential does not exist");

    //     // delete the credential
    //     delete credentials[_credentialHash];
    //     // let external world know that the credential has been deleted
    //     emit CredentialDeleted(_credentialHash);
    // }

    // Modifier to check if an issuer is valid (only verifies Merkle proof)
    modifier onlyVerifiedIssuer(
        bytes32[] memory proof,
        bytes32 signedPairHash
    ) {
        require(issuerRegistry.verifyIssuer(proof, signedPairHash), "Invalid issuer: Merkle proof failed");
        _;
    }

    constructor(address _issuerRegistry) {
        issuerRegistry = IssuerRegistry(_issuerRegistry);
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
        require(credentials[_credentialHash].issuer == address(0), "Credential already exists");

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


    // Function to check if a credential exists
    function verifyCredential(bytes32 _credentialHash) public view returns (bool) {
        return credentials[_credentialHash].issuer != address(0);
    }
}
