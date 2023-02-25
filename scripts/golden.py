from brownie import accounts,GoldenContract
import json
from datetime import date,datetime

nominalCurrencyList = ["AUD", "CAD", "EUR", "JPY", "NZD", "NOK", "GBP", "SEK", "CHF", "USD"]
paymentConventionList = ["in arrears","in advance"]

with open("/home/dmacs/Desktop/JamesBond/IRS1.json", "r") as file:
        data = json.load(file)

def get_timestamp(dt):
    date = datetime.strptime(dt, '%d-%m-%Y')
    timestamp = int(date.timestamp())
    return timestamp

def fetch_operand(op):
    #op = "key:esperanto-deals-deal1-legs-BUY_Fixed-flows[0]-nominal"
    #op = "value:sairam"
    if op.split(":")[0] == 'key':
        path = op.split(":")[1]
        print('key:',path)
        keys = path.split("-")
        value = data
        for key in keys:
            if "[" in key:
                key_name, index = key[:-1].split("[")
                value = value[key_name][int(index)]
            elif 'Date' in key:
                value =  get_timestamp(value[key])
            else:
                value = value[key]         
        return value

    elif op.split(":")[0] == 'value':
        if op.split(":")[1] == 'Today':
            return today()
        return op.split(":")[1] 

def today():
    today = date.today()
    formatted_date = today.strftime("%d-%m-%Y")
    stamp = get_timestamp(formatted_date)
    return stamp

def readRules(goldenContract):
    with open('/home/dmacs/Desktop/JamesBond/rules.txt', 'r') as file:
        for rule in file:
            words = rule.split()
            op1 = words[0]
            op = words[1]
            op2 = ' '.join(words[2:])  #for special case of FO Trade Capture
            print('operand1 :', op1)
            print('operator :', op)
            print('operand2 :', op2)

            if op == '=':
                print("Equality")
                operand1=fetch_operand(op1)
                print('operand 1:', operand1)
                operand2=fetch_operand(op2)
                print('operand 2:', operand2)
                print(goldenContract.isEqual(operand1, operand2, {"from": accounts[0]}))
            
            elif op == '>':
                #should be integer
                print("Greater")
                operand1=fetch_operand(op1)
                print('operand 1:', operand1)
                operand2=fetch_operand(op2)
                print('operand 2:', operand2)
                print(goldenContract.isGreater(operand1, operand2, {"from": accounts[0]}))

            elif op == 'in':
                print("inList")
                operand1 = fetch_operand(op1)
                print(operand1)
                #should generalise this
                if op2 == 'nominalCurrencyList':
                    operand2 = nominalCurrencyList
                elif op2 == 'paymentConventionList':
                    operand2 = paymentConventionList  
                print(operand2)
                print(goldenContract.inList(operand1,operand2, {"from": accounts[0]}))   
                 
            else:
                print("Invalid Operand")
def main():
    goldenContract = GoldenContract.deploy({"from":accounts[0]})
    readRules(goldenContract)