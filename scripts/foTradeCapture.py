from datetime import datetime
import pytz

def current_timestamp():
    current_date = datetime.now(pytz.timezone('GMT'))
    return int(current_date.timestamp())

def main(goldenContract,data,ID,cid,account):
    #date from json
    ad = data['esperanto']['agreementDate']
    date = datetime.strptime(ad, '%d-%m-%Y')
    agreementdate = int(date.timestamp())
    #nominal check
    nominal_buy_fee = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][0]["nominalCurrency"]
    nominal_buy_interest= data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][1]["nominalCurrency"]
    nominal_sell_fee = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominalCurrency"]
    nominal_sell_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][1]["nominalCurrency"]

    trade=f"agreementDate:{agreementdate}, nominalCurrencyBuyFee:{nominal_buy_fee}, nominalCurrencyBuyInterest:{nominal_buy_interest}, nominalCurrencySellFee:{nominal_sell_fee}, nominalCurrencySellInterest:{nominal_sell_interest}, CID:{cid}"
    
    ts=current_timestamp()
    t = goldenContract.store(ts,ID,'FOTradeCapture',trade,{"from": account})
    t.wait(1)
    
    print("\nSuccessfully stored the data on the blockchain!!")
    print("\nThe details of the trade as stored on the blockchain:")
    print(goldenContract.trades(ts,{"from": account}))

    return 1