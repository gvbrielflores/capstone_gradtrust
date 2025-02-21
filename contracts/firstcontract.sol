// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DiplomaVerification {
    struct Diploma {
        bytes32 diplomaHash;
        address issuer;
    }

    mapping(bytes32 => Diploma) public diplomas;

    event DiplomaStored(bytes32 indexed diplomaHash, address indexed issuer);

    function storeDiplomaHash(bytes32 _diplomaHash) public {
        require(diplomas[_diplomaHash].issuer == address(0), "Diploma already exists");
        diplomas[_diplomaHash] = Diploma(_diplomaHash, msg.sender);
        emit DiplomaStored(_diplomaHash, msg.sender);
    }

    function verifyDiploma(bytes32 _diplomaHash) public view returns (bool) {
        return diplomas[_diplomaHash].issuer != address(0);
    }
}