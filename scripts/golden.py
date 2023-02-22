from brownie import accounts,GoldenContract
import json,datetime,time,pytz

nominalCurrencyList = ["AUD", "CAD", "EUR", "JPY", "NZD", "NOK", "GBP", "SEK", "CHF", "USD"]
paymentConventionList = ["in arrears","in advance"]

with open("/home/dmacs/Desktop/JamesBond/IRS1.json", "r") as file:
        data = json.load(file)

#take the list of rules and check on the individual rules taken from a text file

def find_attribute_in_json(attribute):
    results = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == attribute:
                results.append(value)
            else:
                results.extend(find_attribute_in_json(value, attribute))
    elif isinstance(data, list):
        for item in data:
            results.extend(find_attribute_in_json(item, attribute))
    return results

def today():
    current_date = datetime.now(pytz.timezone('GMT'))
    current_date = datetime.combine(current_date.date(), time.min)
    return int(current_date.timestamp())

def getOperand(op):
    if op == 'GBO' or op == 'FO Trade Capture' or op == 'Murex':
        return op  
    elif op == 'SourceSystem':
        return data['header']['sourceSystem']
    elif op == 'nominal':
        find_attribute_in_json(op)
    elif op == 'agreementDate':    
        return data['esperanto']['agreementDate']    
    elif op == 'nominalCurrencyList':
        return nominalCurrencyList
    elif op == 'paymentConventionList':
        return paymentConventionList   
    elif op == 'Today':
        today()

def readRules(goldenContract):
    with open('/home/dmacs/Desktop/JamesBond/rules.txt', 'r') as file:
        for rule in file:
            op1, op, op2 = rule.split()
            print('operand1 :', op1)
            print('operator :', op)
            print('operand2 :', op2)

            if op == '=':
                print("Equality")
                operand1 = getOperand(op1)
                operand2 = getOperand(op2)
                goldenContract.isEqual(operand1,operand2, {"from": accounts[0]})
            elif op == '>':
                print("Greater")
                goldenContract.isGreater(operand1,operand2, {"from": accounts[0]})
            elif op == 'in':
                print("inList")
            else:
                print("Invalid Operand")
                inputList=nominalCurrencyList
                goldenContract.inList(operand1,inputList, {"from": accounts[0]})

def main():
    goldenContract = GoldenContract.deploy({"from":accounts[0]})
    readRules(goldenContract)