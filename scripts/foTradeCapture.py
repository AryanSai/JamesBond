from datetime import datetime
from brownie import Contract,accounts
import json

def main(data,ID,cid):
    account = accounts.load("ganache")

    with open("/home/dmacs/Desktop/JamesBond/build/contracts/CheckerFO.json", "r") as file:
        file_fo = json.load(file)
    fo_bytecode=file_fo['abi']
    contract_CheckerFO = Contract.from_abi("CheckerFO.sol", '0xDfA8580e8183b6f6a353b169A04f26dab782f59b', fo_bytecode)

    #date from json
    agreementDate = data['esperanto']['agreementDate']
    date = datetime.strptime(agreementDate, '%d-%m-%Y')
    timestamp = int(date.timestamp())

    #nominal check
    nominal_buy_fee = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][0]["nominalCurrency"]
    nominal_buy_interest= data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][1]["nominalCurrency"]
    nominal_sell_fee = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominalCurrency"]
    nominal_sell_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][1]["nominalCurrency"]
    
    tr=contract_CheckerFO.store(ID,timestamp,nominal_buy_fee,nominal_buy_interest,nominal_sell_fee,nominal_sell_interest,cid,{"from": account})
    tr.wait(1)
    
    print("\nSuccessfully Stored on Blockchain!!")