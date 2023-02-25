from brownie import accounts,GoldenContract
import json
from datetime import date,datetime

nominalCurrencyList = ["AUD", "CAD", "EUR", "JPY", "NZD", "NOK", "GBP", "SEK", "CHF", "USD"]
paymentConventionList = ["in arrears","in advance"]

with open("/home/dmacs/Desktop/JamesBond/IRS1.json", "r") as file:
        data = json.load(file)


def getSection(sourceSytem):
    with open('/home/dmacs/Desktop/JamesBond/rules.txt', 'r') as file:
        file_content = file.read()
    sections = file_content.split('\n\n')

    for section in sections:
        lines = section.split('\n')
        if len(lines) > 0:
            first_line = lines[0]
            if first_line.startswith('key:header-sourceSystem = value:GBO'):
                print('Found GBO')
                gbo =  section
            elif first_line.startswith('key:header-sourceSystem = value:FO Trade Capture'):
                print('Found FO')
                fo = section
            elif first_line.startswith('key:header-sourceSystem = value:Murex'):
                print('Found Murex')
                murex =  section    
            else:
                print('Unknown section:')

    if sourceSytem == 'GBO':
        return gbo
    elif sourceSytem == 'FO Trade Capture':
        return fo
    elif sourceSytem == 'Murex':
        return murex                            

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
    
    section  =getSection('GBO')

    section = section.split('\n')
    for rule in section:
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