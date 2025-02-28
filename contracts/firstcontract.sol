// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CredentialVerification {
    struct Credential {
        bytes32 signedCredentialaHash;
        address holder;
        address issuer;
        string dataString;
        uint256 issuedAt;
    }

    // Storage mappings
    mapping(bytes32 => Credential) private credentials;
    mapping(address => bool) public verifiedIssuers;
    mapping(address => bytes32[]) private holderCredentials;

    // Events
    event CredentialStored(bytes32 indexed signedCredentialHash, address indexed issuer, address indexed holder, 
    uint256 issuedAt, string data);
    event IssuerRegistered(address indexed issuer);
    event IssuerRevoked(address indexed issuer);

    function storeSignedCredentialHash(bytes32 _signedCredentialHash, address _holder, uint256 _issuedAt, string memory _dataString) public {
        require(credentials[_signedCredentialHash].issuer == address(0), "Credential already exists");
        credentials[_signedCredentialHash] = Credential(_signedCredentialHash, msg.sender, _holder, _dataString, _issuedAt);
        emit CredentialStored(_signedCredentialHash, msg.sender, _holder, _issuedAt, _dataString);
    }

    function verifyCredential(bytes32 _diplomaHash) public view returns (bool) {
        return credentials[_diplomaHash].issuer != address(0);
    }
}