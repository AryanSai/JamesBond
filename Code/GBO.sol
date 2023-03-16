//SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract GBO{       
    
    struct Amounts{
        uint256 amountBuyFee;
        uint256 amountBuyInterest;
        uint256 amountSellFee;
        uint256 amountSellInterest;
    }

    struct Dates{ 
        uint256 settlementDateBuyFee;
        uint256 settlementDateBuyInterest;
        uint256 settlementDateSellFee;
        uint256 settlementDateSellInterest;
    }

    struct Nominals{
        string nominalBuyFee;
        string nominalBuyInterest;
        string nominalSellFee;
        string nominalSellInterest;
    }

    struct Trade { 
        uint256 timestamp;
        string buyFixingFrequency;
        string sellFixingFrequency;
        Dates date;
        Nominals nominal;
        Amounts amount;
        string jsonCID;
    }
   
    //internalID => Trade
    mapping(string => Trade) public trades;

    function storeTimestamp(string memory ID,uint256 _timestamp) public {    
        trades[ID].timestamp = _timestamp;
    }

    function storeFrequency(string memory ID,string memory _buyFF,string memory _sellFF) public {    
        trades[ID].buyFixingFrequency=_buyFF;
        trades[ID].sellFixingFrequency= _sellFF;
    }
    
    function storeDates(
            string memory ID,
            uint256 _settlementDateBuyFee,
            uint256 _settlementDateBuyInterest,
            uint256 _settlementDateSellFee,
            uint256 _settlementDateSellInterest,
            string memory _jsonCID
        ) public {
            trades[ID].date.settlementDateBuyFee=_settlementDateBuyFee;
            trades[ID].date.settlementDateBuyInterest=_settlementDateBuyInterest;
            trades[ID].date.settlementDateSellFee= _settlementDateSellFee;
            trades[ID].date.settlementDateSellInterest= _settlementDateSellInterest;
            trades[ID].jsonCID=_jsonCID;
    }

    function storeNominals(
            string memory ID,
            string memory _nominalBuyFee,
            string memory _nominalBuyInterest,
            string memory _nominalSellFee,
            string memory _nominalSellInterest
        ) public {    
            trades[ID].nominal.nominalBuyFee=_nominalBuyFee;
            trades[ID].nominal.nominalBuyInterest= _nominalBuyInterest;
            trades[ID].nominal.nominalSellFee= _nominalSellFee;
            trades[ID].nominal.nominalSellInterest= _nominalSellInterest;
    }

    function storeAmounts(
            string memory ID,
            uint256 _amountBuyFee,
            uint256 _amountBuyInterest,
            uint256 _amountSellFee,
            uint256 _amountSellInterest
        )public {
            trades[ID].amount.amountBuyFee=_amountBuyFee;
            trades[ID].amount.amountBuyInterest= _amountBuyInterest;
            trades[ID].amount.amountSellFee= _amountSellFee;
            trades[ID].amount.amountSellInterest= _amountSellInterest;
    }

    function getNominals(string memory ID) public view returns(string memory,string memory,string memory,string memory){
        return (
            trades[ID].nominal.nominalBuyFee,
            trades[ID].nominal.nominalBuyInterest,
            trades[ID].nominal.nominalSellFee,
            trades[ID].nominal.nominalSellInterest);
    }

    function getAmounts(string memory ID) public view returns(uint256,uint256,uint256,uint256){
        return (
            trades[ID].amount.amountBuyFee,
            trades[ID].amount.amountBuyInterest,
            trades[ID].amount.amountSellFee,
            trades[ID].amount.amountSellInterest);
    }    
}