//SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract GoldenContract{
    
    struct Trade {
        string ID;
        string sourceSystem;
        string details;
    }
    
    //timestamp=>Trade
    mapping(uint256 => Trade) public trades;

    //ID+SourceSystem=>timestamp
    mapping(bytes32 => uint256) private tradeIndex;
    
    function store(uint256 _timestamp,string memory _ID, string memory _sourceSystem, string memory _details) public {
        Trade memory trade = Trade(_ID, _sourceSystem, _details);
        trades[_timestamp] = trade;
        bytes32 tradeKey = keccak256(abi.encodePacked(_ID, _sourceSystem));
        tradeIndex[tradeKey] = _timestamp;
    }
    
    function findTrade(string memory _ID, string memory _sourceSystem) public view returns (Trade memory) {
        bytes32 tradeKey = keccak256(abi.encodePacked(_ID, _sourceSystem));
        uint256 timestamp = tradeIndex[tradeKey];
        if (timestamp == 0) {
            return Trade("", "", "");
        }
        return trades[timestamp];
    }

    function getTrades(uint256 _timestamp) public view returns (Trade[] memory) {
        uint256 count = 0;
        for (uint256 i = 0; i <= _timestamp; i++) {
            if (bytes(trades[i].ID).length != 0) {
                count++;
            }
        }
        Trade[] memory result = new Trade[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < _timestamp; i++) {
            if (bytes(trades[i].ID).length != 0) {
                result[index] = trades[i];
                index++;
            }
        }
        return result;
    }

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