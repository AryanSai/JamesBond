from brownie import accounts,Contract
import datetime,json,pytz

def current_timestamp():
    current_date = datetime.now(pytz.timezone('GMT'))
    return int(current_date.timestamp())

def main(data,ID,goldenContract,cid):
    account = accounts.load("ganache")

    #load contract
    with open("/home/dmacs/Desktop/JamesBond/build/contracts/Murex.json", "r") as file:
        file_murex = json.load(file)
    murex_bytecode=file_murex['abi']
    contract_CheckerMurex = Contract.from_abi("Murex.sol", '0xE4A3e3FDd8771e7C5C02AfecE2Ba68b26bcd2df8', murex_bytecode)
    
    #check if data has changed from that of the json
    #get gbo contract for checking with prev instance of the json
    with open("/home/dmacs/Desktop/JamesBond/build/contracts/GBO.json", "r") as file:
        file_gbo = json.load(file)
    gbo_bytecode=file_gbo['abi']
    contract_CheckerGBO = Contract.from_abi("GBO.sol", '0xFfcB014A561eb93355c319B568faBe860e1c7e3A', gbo_bytecode)

    (chain_nominal_buy_fee,
        chain_nominal_buy_interest,
        chain_nominal_sell_fee,
        chain_nominal_sell_interest)=contract_CheckerGBO.getNominals(ID,{"from": account})
    print(contract_CheckerGBO.getNominals(ID,{"from": account}))

    (chain_amount_buy_fee,
        chain_amount_buy_interest,
        chain_amount_sell_fee,
        chain_amount_sell_interest)=contract_CheckerGBO.getAmounts(ID,{"from": account})    
    print(contract_CheckerGBO.getAmounts(ID,{"from": account}))

    pc_buy = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["paymentConvention"]
    pc_sell = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["paymentConvention"]

    nominal_buy_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]
    nominal_buy_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]
    nominal_sell_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]
    nominal_sell_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]

    amount_buy_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]
    amount_buy_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]
    amount_sell_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]
    amount_sell_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]

    #check equality
    t3 = goldenContract.isEqual(nominal_buy_fee, chain_nominal_buy_fee,{"from": account})
    t4 = goldenContract.isEqual(nominal_buy_interest, chain_nominal_buy_interest,{"from": account})
    t5 = goldenContract.isEqual(nominal_sell_fee, chain_nominal_sell_fee,{"from": account})
    t6 = goldenContract.isEqual(nominal_sell_interest, chain_nominal_sell_interest,{"from": account})
    t7 = goldenContract.isEqual(int(amount_buy_fee), chain_amount_buy_fee,{"from": account})
    t8 = goldenContract.isEqual(int(amount_buy_interest), chain_amount_buy_interest,{"from": account})
    t9 = goldenContract.isEqual(int(amount_sell_fee), chain_amount_sell_fee,{"from": account})
    t0 = goldenContract.isEqual(int(amount_sell_interest), chain_amount_sell_interest,{"from": account})
    
    if(t3 == False or t4 == False or t5 == False or t6 == False or t7 == False or t8 == False or t9 == False or t0 == False):
        print("All checks not matched!!")    
    else:
        print("All fine!!!")
        t=contract_CheckerMurex.storeTimestamp(ID,current_timestamp(),{"from": account})
        t.wait(1)
        t=contract_CheckerMurex.storePaymentConvention(ID,pc_buy,pc_sell,{"from": account})
        t.wait(1)
        t1=contract_CheckerMurex.store(ID,nominal_buy_fee,nominal_buy_interest,nominal_sell_fee,nominal_sell_interest,amount_buy_fee,amount_buy_interest,amount_sell_fee,amount_sell_interest,cid,{"from": account})
        t1.wait(1)
        print("Successfully stored on the blockchain")

        print(contract_CheckerMurex.trades(ID,{"from": account}))