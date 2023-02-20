from datetime import datetime, time
import pytz,json,ipfsapi
from brownie import accounts,CheckerGBO,CheckerFO,CheckerMurex,TradeDetails

def ipfs(file_path):
    api = ipfsapi.Client('127.0.0.1', 5001)
    result = api.add(file_path)
    cid = result['Hash']
    return cid

def deploy_FO():
    contract = CheckerFO.deploy({"from": accounts[0]})
    return contract

def deploy_TradeDetails():
    contract = TradeDetails.deploy({"from": accounts[0]})
    return contract

def deploy_GBO():
    contract = CheckerGBO.deploy({"from": accounts[0]})
    return contract   

def deploy_Murex():
    contract = CheckerMurex.deploy({"from": accounts[0]})
    return contract  


def today():
    current_date = datetime.now(pytz.timezone('GMT'))
    current_date = datetime.combine(current_date.date(), time.min)
    return int(current_date.timestamp())

def main():

    #upload the json and get cid
    cid = ipfs('/home/dmacs/Desktop/JamesBond/IRS1.json')

    with open("/home/dmacs/Desktop/JamesBond/IRS1.json", "r") as file:
        data = json.load(file)

    ID = data['header']['internalID']

    #store the data on the blockchain
    #id,nominal,amount
    contract = deploy_TradeDetails()
    amount1 = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][0]["amount"]
    amount2 = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][1]["amount"]
    amount3 = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]
    amount4 = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][1]["amount"]
    nominal = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][1]["nominal"]
    ts = contract.initialise(ID,amount1,amount2,amount3,amount4,nominal,cid,{"from": accounts[0]})
    ts.wait(1)
    print(ts)

    source_system = data['header']['sourceSystem']

    if source_system == 'FO':
        print('FO Trade Capture')
        
        #date check
        #date from json
        irsdate = data['esperanto']['agreementDate']
        date = datetime.strptime(irsdate, '%d-%m-%Y')
        timestamp1 = int(date.timestamp())

        #today's date
        timestamp2 = today()
        
        contract=deploy_FO()
        t=contract.isSameDate(timestamp1,timestamp2,{"from": accounts[0]})
        if(t):
            print("Dates match!")
            #store date on blockchaind
            details_contract = deploy_TradeDetails()
            tr=details_contract.setAgreementDate(ID,timestamp1,{"from": accounts[0]})
            tr.wait(1)
            print("successfully stored date on blockchain!!")
            stored_value = details_contract.getDetails(ID)
            print("I am stored:",stored_value)
        else:
            print("Dates do not match!")    

        #nominal check
        nominal_buy_0 = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][0]["nominalCurrency"]
        contract=deploy_FO()
        t1 = contract.validNominal(nominal_buy_0,{"from": accounts[0]})
        nominal_buy_1= data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][1]["nominalCurrency"]
        t2 = contract.validNominal(nominal_buy_1,{"from": accounts[0]})
        nominal_sell_0 = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominalCurrency"]
        t3 = contract.validNominal(nominal_sell_0,{"from": accounts[0]})
        nominal_sell_1= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][1]["nominalCurrency"]
        t4 = contract.validNominal(nominal_sell_1,{"from": accounts[0]})

        if(t1==False or t2==False or t3==False or t4==False):
            print("Invalid Nominal!") 
        else:
            print("Valid Nominal!!!")
            #store nominal on blockchain
            details_contract = deploy_TradeDetails()
            tr=details_contract.setFrequency(ID,nominal_buy_0,{"from": accounts[0]})
            tr.wait(1)
            print("successfully stored nominal on blockchain!!")

    elif source_system == 'O':
        print('GBO')
        #fixing frq = ff and pf = payment freq
        pf_buy = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["paymentFrequency"]
        ff_buy = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["fixingFrequency"]
        contract=deploy_GBO()
        t1 = contract.checkEquality(pf_buy,ff_buy, {"from": accounts[0]})

        pf_sell = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["paymentFrequency"]
        ff_sell = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["fixingFrequency"]
        t2 = contract.checkEquality(pf_sell,ff_sell, {"from": accounts[0]})
        if(t1 == False or t2 == False):
            print("Payment and fixing frequencies do not match!!")
        else:
            print("Payment and fixing frequencies match!!")
            #store nominal on blockchain
            details_contract = deploy_TradeDetails()
            tr=details_contract.setConvention(ID,pf_buy,{"from": accounts[0]})
            tr.wait(1)
            print("successfully stored nominal on blockchain!!")
            stored_value = details_contract.getDetails(ID)
            print("I am stored:",stored_value)

        #settlement date > today
        #sd = settlement date
        sd_buy_0 = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][0]["settlementDate"]
        sd_buy_1= data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][1]["settlementDate"]
        date = datetime.strptime(sd_buy_0, '%d-%m-%Y')
        timestamp1 = int(date.timestamp())
        date = datetime.strptime(sd_buy_1, '%d-%m-%Y')
        timestamp2 = int(date.timestamp())
        t1 = contract.isGreater(timestamp1,today(), {"from": accounts[0]})
        t2 = contract.isGreater(timestamp2,today(), {"from": accounts[0]})

        if(t1 == False or t2 == False):
            print("settlementDate not greater than today") 
        else:   
            print("settlementDate > today")

        sd_sell_0 = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["settlementDate"]
        sd_sell_1 = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][1]["settlementDate"]
        date = datetime.strptime(sd_sell_0, '%d-%m-%Y')
        timestamp1 = int(date.timestamp())
        date = datetime.strptime(sd_sell_1, '%d-%m-%Y')
        timestamp2 = int(date.timestamp())
        t1 = contract.isGreater(timestamp1,today(), {"from": accounts[0]})
        t2 = contract.isGreater(timestamp2,today(), {"from": accounts[0]})

        if(t1 == False or t2 == False):
            print("settlementDate not greater than today") 
        else:   
            print("settlementDate > today")


    elif source_system == 'Murex':
        print('Murex') 
        pc_buy = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["paymentConvention"]
        print(pc_buy)
        contract=deploy_Murex()
        t1 = contract.checkPaymentConvention(pc_buy, {"from": accounts[0]})
      
        pc_sell = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["paymentConvention"]
        contract=deploy_Murex()
        t2 = contract.checkPaymentConvention(pc_sell, {"from": accounts[0]})
        if(t1 == False or t2 == False):
            print("Invalid Payment Convention") 
        else:
            print("valid Payment Convention")

        #check if data has changed from that of the json
        details_contract= deploy_TradeDetails()
        nominal_from_blockchain = details_contract.getNominal(ID,{"from": accounts[0]})
        print("Hello", nominal_from_blockchain)
        nominal = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["flows"][1]["nominal"]
        print(nominal)

        if nominal == nominal_from_blockchain:
            print('Nominal has not changed!!!')
            stored_value = details_contract.getDetails(ID)
            print("I am stored:",stored_value)
