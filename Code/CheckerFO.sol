//SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract CheckerFO{
    string[] nominalCurrency = ["AUD", "CAD", "EUR", "JPY", "NZD", "NOK", "GBP", "SEK", "CHF", "USD"];
    
    struct Trade { 
        string sourceSystem;
        uint256 agreementDate;
        string nominalCurrencyBuyFee;
        string nominalCurrencyBuyInterest;
        string nominalCurrencySellFee;
        string nominalCurrencySellInterest;
        string jsonCID;
    }

    //internalID => Trade
    mapping(string => Trade) public trades;

    function store(string memory ID,uint256 _agreementDate,string memory _nominalCurrencyBuyFee,string memory _nominalCurrencyBuyInterest,string memory _nominalCurrencySellFee,string memory _nominalCurrencySellInterest,string memory _jsonCID) public {
        trades[ID].sourceSystem='FO Trade Capture';
        trades[ID].agreementDate=_agreementDate;
        trades[ID].nominalCurrencyBuyFee=_nominalCurrencyBuyFee;
        trades[ID].nominalCurrencyBuyInterest=_nominalCurrencyBuyInterest;
        trades[ID].nominalCurrencySellFee=_nominalCurrencySellFee;
        trades[ID].nominalCurrencySellInterest=_nominalCurrencySellInterest;
        trades[ID].jsonCID=_jsonCID;
    }

    function validNominalCurrency(string memory _nominalCurrency) public view returns (bool) {
        for (uint256 i = 0; i < nominalCurrency.length; i++) {
            bytes32 nominalCurrencyHash = keccak256(abi.encodePacked(_nominalCurrency));
            if (keccak256(abi.encodePacked(nominalCurrency[i]))==nominalCurrencyHash) {
                return true;
            }
        }
        return false;
    }

    function isSameDate(uint256 _date1,uint256 _date2) public pure returns (bool) {
        return _date1 == _date2;
    }
}