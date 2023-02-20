import json,pytz
from brownie import accounts,Contract
from datetime import datetime, time

def today():
    current_date = datetime.now(pytz.timezone('GMT'))
    current_date = datetime.combine(current_date.date(), time.min)
    return int(current_date.timestamp())

def main(data,ID,cid):
    #get account
    account = accounts.load("ganache")

    #get contract
    with open("/home/dmacs/Desktop/JamesBond/build/contracts/CheckerGBO.json", "r") as file:
        file_gbo = json.load(file)
    gbo_bytecode=file_gbo['abi']
    contract_CheckerGBO = Contract.from_abi("CheckerGBO.sol", '0x040904CEE4d13b6F0Be04493909afc214763B97d', gbo_bytecode)

    #fixing frq = ff and pf = payment freq
    pf_buy = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["paymentFrequency"]
    ff_buy = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["fixingFrequency"]
    t1 = contract_CheckerGBO.checkEquality(pf_buy,ff_buy, {"from": account})

    pf_sell = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["paymentFrequency"]
    ff_sell = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["fixingFrequency"]
    t2 = contract_CheckerGBO.checkEquality(pf_sell,ff_sell, {"from": account})
    
    if(t1 == False or t2 == False):
        print("Payment and fixing frequencies do not match!!")
    else:
        print("Payment and fixing frequencies match!!")
        print("Exit")

    #settlement date > today
    #sd = settlement date
    sd_buy_fee = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][0]["settlementDate"]
    sd_buy_interest= data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][1]["settlementDate"]
    date = datetime.strptime(sd_buy_fee, '%d-%m-%Y')
    sd_buy_fee_timestamp = int(date.timestamp())
    date = datetime.strptime(sd_buy_interest, '%d-%m-%Y')
    sd_buy_interest_timestamp = int(date.timestamp())
    t3 = contract_CheckerGBO.isGreater(sd_buy_fee_timestamp,today(), {"from": account})
    t4 = contract_CheckerGBO.isGreater(sd_buy_interest_timestamp,today(), {"from": account})
    if(t3 == False or t4 == False):
        print("settlementDate not greater than today") 
    else:   
        print("settlementDate > today")

    sd_sell_fee = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["settlementDate"]
    sd_sell_interest = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][1]["settlementDate"]
    date = datetime.strptime(sd_sell_fee, '%d-%m-%Y')
    sd_sell_fee_timestamp = int(date.timestamp())
    date = datetime.strptime(sd_sell_interest, '%d-%m-%Y')
    sd_sell_interest_timestamp = int(date.timestamp())
    t5 = contract_CheckerGBO.isGreater(sd_sell_fee_timestamp,today(), {"from": account})
    t6 = contract_CheckerGBO.isGreater(sd_sell_interest_timestamp,today(), {"from": account})
    if(t5 == False or t6 == False):
        print("settlementDate not greater than today") 
    else:   
        print("settlementDate > today")

    nominal_buy_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]
    nominal_buy_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]
    nominal_sell_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]
    nominal_sell_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]

    amount_buy_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]
    amount_buy_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]
    amount_sell_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]
    amount_sell_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]

    if(t1 == False or t2 == False or t3 == False or t4 == False or t5 == False or t6 == False):
        print('Can\'t store!! since all checks have not met!! ')
    else:
        t1=contract_CheckerGBO.storeDates(ID,sd_buy_fee_timestamp, sd_buy_interest_timestamp,sd_sell_fee_timestamp,sd_sell_interest_timestamp,cid,{"from": account})
        t1.wait(1)
        t2=contract_CheckerGBO.storeNominals(ID,nominal_buy_fee,nominal_buy_interest,nominal_sell_fee,nominal_sell_interest,{"from": account})
        t2.wait(1)
        t3=contract_CheckerGBO.storeAmounts(ID,amount_buy_fee,amount_buy_interest,amount_sell_fee,amount_sell_interest,{"from": account})
        t3.wait(1)
        print("successfully stored data on blockchain!!")    