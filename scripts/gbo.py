import json,pytz
from brownie import accounts,Contract
from datetime import datetime,time

def today():
    current_date = datetime.now(pytz.timezone('GMT'))
    current_date = datetime.combine(current_date.date(), time.min)
    return int(current_date.timestamp())

def current_timestamp():
    current_date = datetime.now(pytz.timezone('GMT'))
    return int(current_date.timestamp())

def main(data,ID,cid):
    #get account
    account = accounts.load("ganache")

    #get contract
    with open("/home/dmacs/Desktop/JamesBond/build/contracts/GBO.json", "r") as file:
        file_gbo = json.load(file)
    gbo_bytecode=file_gbo['abi']
    contract_CheckerGBO = Contract.from_abi("GBO.sol", '0xFfcB014A561eb93355c319B568faBe860e1c7e3A', gbo_bytecode)

    ff_buy = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["fixingFrequency"]
    ff_sell = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["fixingFrequency"]

    sd_buy_fee = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][0]["settlementDate"]
    sd_buy_interest= data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][1]["settlementDate"]
    date = datetime.strptime(sd_buy_fee, '%d-%m-%Y')
    sd_buy_fee_timestamp = int(date.timestamp())
    date = datetime.strptime(sd_buy_interest, '%d-%m-%Y')
    sd_buy_interest_timestamp = int(date.timestamp())

    sd_sell_fee = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["settlementDate"]
    sd_sell_interest = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][1]["settlementDate"]
    date = datetime.strptime(sd_sell_fee, '%d-%m-%Y')
    sd_sell_fee_timestamp = int(date.timestamp())
    date = datetime.strptime(sd_sell_interest, '%d-%m-%Y')
    sd_sell_interest_timestamp = int(date.timestamp())

    nominal_buy_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]
    nominal_buy_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]
    nominal_sell_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]
    nominal_sell_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]

    amount_buy_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]
    amount_buy_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]
    amount_sell_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]
    amount_sell_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]

    t=contract_CheckerGBO.storeTimestamp(ID,current_timestamp(),{"from": account})
    t.wait(1)
    t11=contract_CheckerGBO.storeFrequency(ID,ff_buy,ff_sell,{"from": account})
    t11.wait(1)
    t1=contract_CheckerGBO.storeDates(ID,sd_buy_fee_timestamp, sd_buy_interest_timestamp,sd_sell_fee_timestamp,sd_sell_interest_timestamp,cid,{"from": account})
    t1.wait(1)
    t2=contract_CheckerGBO.storeNominals(ID,nominal_buy_fee,nominal_buy_interest,nominal_sell_fee,nominal_sell_interest,{"from": account})
    t2.wait(1)
    t3=contract_CheckerGBO.storeAmounts(ID,amount_buy_fee,amount_buy_interest,amount_sell_fee,amount_sell_interest,{"from": account})
    t3.wait(1)
    print("successfully stored data on blockchain!!")    

    print(contract_CheckerGBO.trades(ID,{"from": account}))