from datetime import datetime, time
from brownie import Contract,accounts
import json,pytz

def today():
    current_date = datetime.now(pytz.timezone('GMT'))
    current_date = datetime.combine(current_date.date(), time.min)
    return int(current_date.timestamp())

def main(data,ID,cid):
    account = accounts.load("ganache")

    with open("/home/dmacs/Desktop/JamesBond/build/contracts/CheckerFO.json", "r") as file:
        file_fo = json.load(file)
    fo_bytecode=file_fo['abi']
    contract_CheckerFO = Contract.from_abi("CheckerFO.sol", '0xDfA8580e8183b6f6a353b169A04f26dab782f59b', fo_bytecode)

    #date check
    #date from json
    agreementDate = data['esperanto']['agreementDate']
    date = datetime.strptime(agreementDate, '%d-%m-%Y')
    timestamp1 = int(date.timestamp())
    #today's date
    timestamp2 = today()
    
    t=contract_CheckerFO.isSameDate(timestamp1,timestamp2,{"from": account})
    if(t):
        print("Dates match!")
        #store date on blockchain
        tr=contract_CheckerFO.store(ID,timestamp1,{"from": account})
        tr.wait(1)
        print("successfully stored date on blockchain!!")
    else:
        print("Dates do not match!")    

    #nominal check
    nominal_buy_fee = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][0]["nominalCurrency"]
    t1 = contract_CheckerFO.validNominalCurrency(nominal_buy_fee,{"from": account})
    
    nominal_buy_interest= data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][1]["nominalCurrency"]
    t2 = contract_CheckerFO.validNominalCurrency(nominal_buy_interest,{"from": account})
    
    nominal_sell_fee = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominalCurrency"]
    t3 = contract_CheckerFO.validNominalCurrency(nominal_sell_fee,{"from": account})
    
    nominal_sell_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][1]["nominalCurrency"]
    t4 = contract_CheckerFO.validNominalCurrency(nominal_sell_interest,{"from": account})
    if(t1==False or t2==False or t3==False or t4==False):
        print("Invalid Nominal Currencies!") 
    else:
        print("Valid Nominal!!!")
        #store nominal on blockchain
        tr=contract_CheckerFO.store(ID,timestamp1,nominal_buy_fee,nominal_buy_interest,nominal_sell_fee,nominal_sell_interest,cid,{"from": account})
        tr.wait(1)
        print("successfully stored data on blockchain!!")
