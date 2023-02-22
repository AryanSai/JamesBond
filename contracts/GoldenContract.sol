//SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract GoldenContract{

    function inList(string memory input, string[] memory inputList) public pure returns (bool) {
        for (uint256 i = 0; i < inputList.length; i++) {
            bytes32 inputHash = keccak256(abi.encodePacked(input));
            if (keccak256(abi.encodePacked(inputList[i]))==inputHash) {
                return true;
            }
        }
        return false;
    } 

    function isEqual(string memory str1, string memory str2) public pure returns (bool) {
        bytes32 hashOf1 = keccak256(abi.encodePacked(str1));
        bytes32 hashOf2 = keccak256(abi.encodePacked(str2));
        return hashOf1 == hashOf2;
    }

    function isGreater(uint256 input1, uint256 input2) public pure returns (bool) {
        return input1 > input2;
    }
}