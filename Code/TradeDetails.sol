//SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract TradeDetails{
    
    struct Flow{
        uint256[2] buyAmount;
        uint256[2] sellAmount;
    }
    struct Trade { 
        uint256 agreementDate;
        Flow flow;
        string nominal;
        string frequency;
        string paymentConvention;
        string jsonCID;
    }

    //internalID => Trade
    mapping(string => Trade) public trades;

    function initialise(string memory ID,uint256 buyAmount0,uint256 buyAmount1,uint256 sellAmount0,uint256 sellAmount1,string memory _nominal,string memory _jsonCID) public {
        trades[ID].agreementDate=0;
        trades[ID].flow.buyAmount[0]=buyAmount0;
        trades[ID].flow.buyAmount[1]=buyAmount1;
        trades[ID].flow.sellAmount[0]=sellAmount0;
        trades[ID].flow.sellAmount[1]=sellAmount1;
        trades[ID].nominal=_nominal;
        trades[ID].frequency="";
        trades[ID].paymentConvention="";
        trades[ID].jsonCID=_jsonCID;
    }

    function getNominal(string memory ID) public view returns(string memory) {
        return trades[ID].nominal;
    }

    function getAmount(string memory ID) public view returns(uint256,uint256,uint256,uint256) {
        return (trades[ID].flow.buyAmount[0],trades[ID].flow.buyAmount[1],trades[ID].flow.sellAmount[0],trades[ID].flow.sellAmount[1]);
    }

    function setAgreementDate(string memory ID,uint256 _date) public {
        trades[ID].agreementDate=_date;
    }

    function setFrequency(string memory ID,string memory _frequency) public {
        trades[ID].nominal=_frequency;
    }

    function setConvention(string memory ID,string memory _convention) public {
        trades[ID].paymentConvention=_convention;
    }

    function getDetails(string memory ID) public view returns(uint256,string memory,string memory,string memory,string memory){
        return (trades[ID].agreementDate,trades[ID].nominal,trades[ID].frequency,trades[ID].paymentConvention,trades[ID].jsonCID);
    }
}