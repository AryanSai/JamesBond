//SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract CheckerGBO{  
    struct Trade { 
        string sourceSystem;
        uint256 settlementDateBuyFee;
        uint256 settlementDateBuyInterest;
        uint256 settlementDateSellFee;
        uint256 settlementDateSellInterest;
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

    // Set default values
    Trade defaultTrade = Trade({
        sourceSystem:"",
        settlementDateBuyFee:0,
        settlementDateBuyInterest:0,
        settlementDateSellFee:0,
        settlementDateSellInterest:0,
        nominalBuyFee:"",
        nominalBuyInterest:"",
        nominalSellFee:"",
        nominalSellInterest:"",
        amountBuyFee:0,
        amountBuyInterest:0,
        amountSellFee:0,
        amountSellInterest:0,
        jsonCID:""
    });

    //internalID => Trade
    mapping(string => Trade) public trades;

    function storeDates(
                string memory ID,
                uint256 _settlementDateBuyFee,
                uint256 _settlementDateBuyInterest,
                uint256 _settlementDateSellFee,
                uint256 _settlementDateSellInterest,
                string memory _nominalBuyFee,
                string memory _nominalBuyInterest,
                string memory _nominalSellFee,
                string memory _nominalSellInterest,
                uint256 _amountBuyFee,
                uint256 _amountBuyInterest,
                uint256 _amountSellFee,
                uint256 _amountSellInterest,
                string memory _jsonCID) public {
        trades[ID].sourceSystem = "GBO";
        trades[ID].settlementDateBuyFee=_settlementDateBuyFee;
        trades[ID].settlementDateBuyInterest=_settlementDateBuyInterest;
        trades[ID].settlementDateSellFee= _settlementDateSellFee;
        trades[ID].settlementDateSellInterest= _settlementDateSellInterest;
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

    function checkEquality(string memory _pfbuy, string memory _ffbuy) public pure returns (bool) {
        bytes32 hashA = keccak256(abi.encodePacked(_pfbuy));
        bytes32 hashB = keccak256(abi.encodePacked(_ffbuy));
        return hashA == hashB;
    }

    function isGreater(uint256 _dateA, uint256 _dateB) public pure returns (bool) {
        return _dateA > _dateB;
    }

    function getNominals(string memory ID) public view returns(string memory,string memory,string memory,string memory){
        return (trades[ID].nominalBuyFee,
        trades[ID].nominalBuyInterest,
        trades[ID].nominalSellFee,
        trades[ID].nominalSellInterest);
    }

    function getAmounts(string memory ID) public view returns(uint256,uint256,uint256,uint256){
        return (trades[ID].amountBuyFee,
        trades[ID].amountBuyInterest,
        trades[ID].amountSellFee,
        trades[ID].amountSellInterest);
    }
}
