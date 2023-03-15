from brownie import accounts,GoldenContract
import json,ipfsapi
from datetime import date, datetime
import scripts.foTradeCapture as foTradeCapture, scripts.gbo as gbo,scripts.murex as murex

nominalCurrencyList = ["AUD", "CAD", "EUR", "JPY", "NZD", "NOK", "GBP", "SEK", "CHF", "USD"]
paymentConventionList = ["in arrears","in advance"]

with open("/home/dmacs/Desktop/JamesBond/IRS1.json", "r") as file:
        data = json.load(file)

def ipfs(file_path):
    api = ipfsapi.Client('127.0.0.1', 5001)
    result = api.add(file_path)
    cid = result['Hash']
    return cid

def getSection(sourceSytem):
    with open('/home/dmacs/Desktop/JamesBond/rules.txt', 'r') as file:
        file_content = file.read()
    sections = file_content.split('\n\n')

    for section in sections:
        lines = section.split('\n')
        if len(lines) > 0:
            first_line = lines[0]
            if first_line.startswith('key:header-sourceSystem = value:FO Trade Capture'):
                #print('\nFound FO')
                fo = section
                
            elif first_line.startswith('key:header-sourceSystem = value:GBO'):
                #print('\nFound GBO')
                gbo =  section

            elif first_line.startswith('key:header-sourceSystem = value:Murex'):
                #print('\nFound Murex')
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

def check(goldenContract,source_system):
    #open the json
    with open("/home/dmacs/Desktop/JamesBond/IRS1.json", "r") as file:
        data = json.load(file)

    #upload the json and get cid
    cid = ipfs('/home/dmacs/Desktop/JamesBond/IRS1.json')

    section = getSection(source_system)

    #read rules and do checking on the contract
    section = section.split('\n')

    #find the number of rules so that you can check if all rules are satisfied
    number_of_rules = len(section)
    print("\nNumber of Rules = ",number_of_rules)

    #list of trues
    list_of_trues=[]

    for rule in section:
        words = rule.split()
        op1 = words[0]
        op = words[1]
        op2 = ' '.join(words[2:])  #for special case of FO Trade Capture
        print('\noperand1 :', op1)
        print('operator :', op)
        print('operand2 :', op2)

        if op == '=':
            print("Equality")
            operand1=fetch_operand(op1)
            print('operand 1:', operand1)
            operand2=fetch_operand(op2)
            print('operand 2:', operand2)
            list_of_trues.append(goldenContract.isEqual(operand1, operand2, {"from": accounts[0]}))
        
        elif op == '>':
            #should be integer
            print("Greater")
            operand1=fetch_operand(op1)
            print('operand 1:', operand1)
            operand2=fetch_operand(op2)
            print('operand 2:', operand2)
            list_of_trues.append(goldenContract.isGreater(operand1, operand2, {"from": accounts[0]}))
        
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
            list_of_trues.append(goldenContract.inList(operand1,operand2, {"from": accounts[0]}))   
             
        else:
            print("Invalid Operand")

    #check if all the rules are satisfied
    if(len(list_of_trues)==number_of_rules):
        print('\nAll the rules satisfied! Storing on Blockchain! ')
        go_to_contract(data,cid,source_system,goldenContract)
    else:
        print('\nNot all rules are satisfied!!')    

def go_to_contract(data,cid,source_system,goldenContract):
    ID = data['header']['internalID']
    #source_system = data['header']['sourceSystem']

    if source_system == 'FO Trade Capture':
        print('FO Trade Capture')
        foTradeCapture.main(data,ID,cid)

    elif source_system == 'GBO':
        print('GBO')
        gbo.main(data,ID,cid)

    elif source_system == 'Murex':
        print('Murex') 
        murex.main(data,ID,goldenContract,cid)

def main():
    goldenContract = GoldenContract.deploy({"from":accounts[0]})

    source_system = input('Enter the name of the Source System: ')
    check(goldenContract,source_system)