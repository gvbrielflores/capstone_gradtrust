// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CredentialVerification {
    struct Credential {
        bytes32 signedCredentialaHash;
        address holder;
        address issuer;
        uint256 issuedAt;
    }

    mapping(bytes32 => Credential) public credentials;

    event CredentialStored(bytes32 indexed signedCredentialHash, address indexed issuer, address indexed holder, 
    uint256 issuedAt);

    function storeSignedCredentialHash(bytes32 _signedCredentialHash, address _holder, uint256 _issuedAt) public {
        require(credentials[_signedCredentialHash].issuer == address(0), "Diploma already exists");
        credentials[_signedCredentialHash] = Credential(_signedCredentialHash, msg.sender, _holder, _issuedAt);
        emit CredentialStored(_signedCredentialHash, msg.sender, _holder, _issuedAt);
    }

    function verifyCredential(bytes32 _diplomaHash) public view returns (bool) {
        return credentials[_diplomaHash].issuer != address(0);
    }
}