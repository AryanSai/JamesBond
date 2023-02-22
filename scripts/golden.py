from brownie import accounts,GoldenContract
import json,pytz
from datetime import datetime, time
nominalCurrencyList = ["AUD", "CAD", "EUR", "JPY", "NZD", "NOK", "GBP", "SEK", "CHF", "USD"]
paymentConventionList = ["in arrears","in advance"]

with open("/home/dmacs/Desktop/JamesBond/IRS1.json", "r") as file:
        data = json.load(file)

#take the list of rules and check on the individual rules taken from a text file

def find_attribute_in_json(data,attribute):
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
    if op == 'GBO' or op == 'FOTradeCapture' or op == 'Murex':
        return op  
    elif op == 'SourceSystem':
        return data['header']['sourceSystem']
    elif op == 'nominalCurrency':
        return find_attribute_in_json(data,op)
    elif op == 'paymentConvention':
        return find_attribute_in_json(data,op) 
    elif op == 'paymentConventionList':
        return paymentConventionList       
    elif op == 'fixingFrequency':
        return find_attribute_in_json(data,op) 
    elif op == 'paymentFrequency':
        return find_attribute_in_json(data,op)         
    elif op == 'settlementDate':
        sd_list =  find_attribute_in_json(data,op)
        result = []
        for i in sd_list:
            date = datetime.strptime(i, '%d-%m-%Y')
            timestamp = int(date.timestamp())
            result.append(timestamp)
        return result    
    elif op == 'agreementDate':    
        return data['esperanto']['agreementDate']    
    elif op == 'nominalCurrencyList':
        return nominalCurrencyList
    elif op == 'Today':
        return today()

def readRules(goldenContract):
    with open('/home/dmacs/Desktop/JamesBond/rules.txt', 'r') as file:
        for rule in file:
            op1, op, op2 = rule.split()
            print('operand1 :', op1)
            print('operator :', op)
            print('operand2 :', op2)
            if op == '=':
                print("Equality")
                operand1=[]
                op1 = getOperand(op1)
                operand1.append(op1)
                print(operand1)
                operand2 = getOperand(op2)
                print(operand2)
                if isinstance(operand1,list):
                    for i in operand1:
                        a=goldenContract.isEqual(i,operand2, {"from": accounts[0]})
                        print(a)
            elif op == '==':
                print("Component wise Equality")
                operand1 = getOperand(op1)
                print(operand1)
                operand2 = getOperand(op2)
                print(operand2)
                for i in range(len(operand1)):
                    print(goldenContract.isEqual(operand1[i],operand2[i], {"from": accounts[0]}))
            elif op == '>':
                print("Greater")
                operand1 = getOperand(op1)
                print(operand1)
                operand2 = getOperand(op2)
                print(operand2)
                if isinstance(operand1,list):
                    for i in operand1:
                        b=goldenContract.isGreater(i,operand2, {"from": accounts[0]})
                        print(b)
            elif op == 'in':
                print("inList")
                operand1 = getOperand(op1)
                print(operand1)
                operand2 = getOperand(op2)
                print(operand2)
                if isinstance(operand1,list):
                    for i in operand1:
                        c = goldenContract.inList(i,operand2, {"from": accounts[0]})
                        print(c)
            else:
                print("Invalid Operand")
                inputList=nominalCurrencyList
                goldenContract.inList(operand1,inputList, {"from": accounts[0]})

def main():
    goldenContract = GoldenContract.deploy({"from":accounts[0]})
    readRules(goldenContract)