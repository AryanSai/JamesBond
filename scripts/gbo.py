import pytz
from datetime import datetime,time

def today():
    current_date = datetime.now(pytz.timezone('GMT'))
    current_date = datetime.combine(current_date.date(), time.min)
    return int(current_date.timestamp())

def current_timestamp():
    current_date = datetime.now(pytz.timezone('GMT'))
    return int(current_date.timestamp())

def main(goldenContract,data,ID,cid,account):

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

    trade=f"buyFixingFrequency:{ff_buy}, sellFixingFrequency:{ff_sell}, settlementDateBuyFee:{sd_buy_fee_timestamp}, settlementDateBuyInterest:{sd_buy_interest_timestamp}, settlementDateSellFee:{sd_sell_fee_timestamp}, settlementDateSellInterest:{sd_sell_interest_timestamp}, nominalBuyFee:{nominal_buy_fee}, nominalBuyInterest:{nominal_buy_interest}, nominalSellFee:{nominal_sell_fee}, nominalSellInterest:{nominal_sell_interest}, amountBuyFee:{amount_buy_fee}, amountBuyInterest:{amount_buy_interest}, amountSellFee:{amount_sell_fee}, amountSellInterest:{amount_sell_interest}, CID:{cid}"
    # print(trade)
    
    ts=current_timestamp()
    t = goldenContract.store(ts,ID,'GBO',trade,{"from": account})
    t.wait(1)

    print(goldenContract.trades(ts,{"from": account}))

    print("\nSuccessfully stored the data on the blockchain!!")
    return 1
   
