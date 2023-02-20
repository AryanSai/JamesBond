//SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract CheckerMurex{
    struct Trade { 
        string sourceSystem;
        string buyPaymentConvention;
        string sellPaymentConvention;
        string nominalBuyFee;
        string nominalBuyInterest;
        string nominalSellFee;
        string nominalSellInterest;
        uint256 amountBuyFee;
        uint256 amountBuyInterest;
        uint256 amountSellFee;
        uint256 amountSellInterest;
        string jsonCID;
    }

    //internalID => Trade
    mapping(string => Trade) public trades;

    function store(string memory ID,string memory _nominalBuyFee,string memory _nominalBuyInterest,string memory _nominalSellFee,string memory _nominalSellInterest,uint256 _amountBuyFee,uint256 _amountBuyInterest,uint256 _amountSellFee,uint256 _amountSellInterest,string memory _jsonCID) public {
        trades[ID].sourceSystem='Murex';
        trades[ID].nominalBuyFee=_nominalBuyFee;
        trades[ID].nominalBuyInterest= _nominalBuyInterest;
        trades[ID].nominalSellFee= _nominalSellFee;
        trades[ID].nominalSellInterest= _nominalSellInterest;
        trades[ID].amountBuyFee=_amountBuyFee;
        trades[ID].amountBuyInterest= _amountBuyInterest;
        trades[ID].amountSellFee= _amountSellFee;
        trades[ID].amountSellInterest= _amountSellInterest;
        trades[ID].jsonCID=_jsonCID;
    }

    function checkPaymentConvention(string memory _pc) public pure returns (bool) {
        bytes32 pc = keccak256(abi.encodePacked(_pc));
        if(pc==keccak256(abi.encodePacked("in arrears")) || pc==keccak256(abi.encodePacked("in advance")))
            return true;
        else
            return false;
    }

    function checkEquality(string memory _strA, string memory _strB) public pure returns (bool) {
        bytes32 hashA = keccak256(abi.encodePacked(_strA));
        bytes32 hashB = keccak256(abi.encodePacked(_strB));
        return hashA == hashB;
    }
}