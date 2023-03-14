from brownie import accounts,Contract
import json

def main(data,ID,goldenContract):
    account = accounts.load("ganache")

    #load contract
    with open("/home/dmacs/Desktop/JamesBond/build/contracts/CheckerMurex.json", "r") as file:
        file_murex = json.load(file)
    murex_bytecode=file_murex['abi']
    contract_CheckerMurex = Contract.from_abi("CheckerMurex.sol", '0x715fa7C970C72803fac0488B107Ec6adB5345d11', murex_bytecode)

    pc_buy = data["esperanto"]["deals"]["deal1"]["legs"]["BUY_Fixed"]["paymentConvention"]
    pc_sell = data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["paymentConvention"]
    
    #check if data has changed from that of the json
    #get gbo contract for checking with prev instance of the json
    with open("/home/dmacs/Desktop/JamesBond/build/contracts/CheckerGBO.json", "r") as file:
        file_gbo = json.load(file)
    gbo_bytecode=file_gbo['abi']
    contract_CheckerGBO = Contract.from_abi("CheckerGBO.sol", '0x040904CEE4d13b6F0Be04493909afc214763B97d', gbo_bytecode)

    (chain_nominal_buy_fee,
        chain_nominal_buy_interest,
        chain_nominal_sell_fee,
        chain_nominal_sell_interest)=contract_CheckerGBO.getNominals(ID,{"from": account})

    (chain_amount_buy_fee,
        chain_amount_buy_interest,
        chain_amount_sell_fee,
        chain_amount_sell_interest)=contract_CheckerGBO.getAmounts(ID,{"from": account})    

    nominal_buy_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]
    nominal_buy_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]
    nominal_sell_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]
    nominal_sell_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["nominal"]

    amount_buy_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]
    amount_buy_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]
    amount_sell_fee= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]
    amount_sell_interest= data["esperanto"]["deals"]["deal1"]["legs"]["SELL_Floating"]["flows"][0]["amount"]

    #check equality
    t3 = goldenContract.isEqual(nominal_buy_fee, chain_nominal_buy_fee,{"from": accounts[0]})
    t4 = goldenContract.isEqual(nominal_buy_interest, chain_nominal_buy_interest,{"from": accounts[0]})
    t5 = goldenContract.isEqual(nominal_sell_fee, chain_nominal_sell_fee,{"from": accounts[0]})
    t6 = goldenContract.isEqual(nominal_sell_interest, chain_nominal_sell_interest,{"from": accounts[0]})
    t7 = goldenContract.isEqual(amount_buy_fee, chain_amount_buy_fee,{"from": accounts[0]})
    t8 = goldenContract.isEqual(amount_buy_interest, chain_amount_buy_interest,{"from": accounts[0]})
    t9 = goldenContract.isEqual(amount_sell_fee, chain_amount_sell_fee,{"from": accounts[0]})
    t0 = goldenContract.isEqual(amount_sell_interest, chain_amount_sell_interest,{"from": accounts[0]})
    
    if(t3 == False or t4 == False or t5 == False or t6 == False or t7 == False or t8 == False or t9 == False or t0 == False):
        print("All checks not matched!!")    
    else:
        print("All fine!!!")
        tr=contract_CheckerMurex.store(nominal_buy_fee,nominal_buy_interest,nominal_sell_fee,nominal_sell_interest,amount_buy_fee,amount_buy_interest,amount_sell_fee,amount_sell_interest,{"from": account})
        tr.wait(1)
        print("Successfully stored on the blockchain")