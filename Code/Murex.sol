//SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract Murex{
    struct Trade { 
        uint256 timestamp;
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

    function storePaymentConvention(string memory ID,string memory _buyPC,string memory _sellPC) public{
        trades[ID].buyPaymentConvention = _buyPC; 
        trades[ID].sellPaymentConvention = _sellPC;
    }

    function storeTimestamp(string memory ID,uint256 _timestamp) public {    
        trades[ID].timestamp = _timestamp;
    }

    function store(string memory ID,string memory _nominalBuyFee,string memory _nominalBuyInterest,string memory _nominalSellFee,string memory _nominalSellInterest,uint256 _amountBuyFee,uint256 _amountBuyInterest,uint256 _amountSellFee,uint256 _amountSellInterest,string memory _jsonCID) public {
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
}