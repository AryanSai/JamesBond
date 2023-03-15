import datetime,pytz
from brownie import Contract,accounts
import json

def current_timestamp():
    current_date = datetime.now(pytz.timezone('GMT'))
    return int(current_date.timestamp())

def main(data,ID,cid):
    account = accounts.load("ganache")

    with open("/home/dmacs/Desktop/JamesBond/build/contracts/FO.json", "r") as file:
        file_fo = json.load(file)
    fo_bytecode=file_fo['abi']
    contract_CheckerFO = Contract.from_abi("FO.sol", '0x8393287a9b1e24297Bbce78f590e135E6982f47E', fo_bytecode)

    #date from json
    ad = data['esperanto']['agreementDate']
    date = datetime.strptime(ad, '%d-%m-%Y')
    agreementdate = int(date.timestamp())

    #nominal check
    nominal_buy_fee = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][0]["nominalCurrency"]
    nominal_buy_interest= data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][1]["nominalCurrency"]
    nominal_sell_fee = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominalCurrency"]
    nominal_sell_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][1]["nominalCurrency"]
    
    tr=contract_CheckerFO.store(ID,current_timestamp(),agreementdate,nominal_buy_fee,nominal_buy_interest,nominal_sell_fee,nominal_sell_interest,cid,{"from": account})
    tr.wait(1)
    
    print("\nSuccessfully Stored on Blockchain!!")

    print(contract_CheckerFO.trades(ID,{"from": account}))