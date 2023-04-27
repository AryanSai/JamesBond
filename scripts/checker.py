from brownie import accounts, Contract
import json, ipfsapi, os
from datetime import date, datetime
import scripts.foTradeCapture as foTradeCapture, scripts.gbo as gbo, scripts.murex as murex

nominalCurrencyList = [
    "AUD",
    "CAD",
    "EUR",
    "JPY",
    "NZD",
    "NOK",
    "GBP",
    "SEK",
    "CHF",
    "USD",
]
paymentConventionList = ["in arrears", "in advance"]
previous_file = None

# with open("/home/dmacs/Desktop/JamesBond/IRS1.json", "r") as file:
#         data = json.load(file)

def ipfs(file_path):
    api = ipfsapi.Client("127.0.0.1", 5001)
    result = api.add(file_path)
    cid = result["Hash"]
    return cid

def get_num(filename):
    return int(os.path.splitext(filename)[0])

def get_file():
    directory_path = "/home/dmacs/Desktop/JamesBond/Events"
    global previous_file
    files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
    sorted_file_list = sorted(files, key=get_num)
    
    # If previous_file exists in the directory, get its index
    if previous_file in sorted_file_list:
        index = sorted_file_list.index(previous_file)
        # If previous_file is not the last file in the directory, get the next file
        if index < len(sorted_file_list) - 1:
            file = sorted_file_list[index + 1]
        # If previous_file is the last file in the directory, get the first file
        else:
            file = sorted_file_list[0]
    # If previous_file does not exist in the directory or it's the first call to the function, get the first file
    else:
        file = sorted_file_list[0]

    previous_file = file
    path = os.path.join(directory_path, file)
    print("file path: ", path)
    return path


def getSection(sourceSytem):
    # print(sourceSytem)
    with open("/home/dmacs/Desktop/JamesBond/rules.txt", "r") as file:
        file_content = file.read()
    sections = file_content.split("\n\n")

    for section in sections:
        lines = section.split("\n")
        if len(lines) > 0:
            first_line = lines[0]
            if first_line.startswith("key:header-sourceSystem = value:FOTradeCapture"):
                # print('\nFound FO')
                fo = section

            elif first_line.startswith("key:header-sourceSystem = value:GBO"):
                # print('\nFound GBO')
                gbo = section

            elif first_line.startswith("key:header-sourceSystem = value:Murex"):
                # print('\nFound Murex')
                murex = section
            else:
                print("Unknown section:")

    if sourceSytem == "GBO":
        # print(sourceSytem)
        return gbo
    elif sourceSytem == "FOTradeCapture":
        # print(sourceSytem)
        return fo
    elif sourceSytem == "Murex":
        # print(sourceSytem)
        return murex


def get_timestamp(dt):
    date = datetime.strptime(dt, "%d-%m-%Y")
    timestamp = int(date.timestamp())
    return timestamp


def fetch_operand(data, op):
    # op = "key:esperanto-deals-deal1-legs-BUY_Fixed-flows[0]-nominal"
    # op = "value:sairam"
    if op.split(":")[0] == "key":
        path = op.split(":")[1]
        # print('key:',path)
        keys = path.split("-")
        value = data
        for key in keys:
            if "[" in key:
                key_name, index = key[:-1].split("[")
                value = value[key_name][int(index)]
            elif "Date" in key:
                value = get_timestamp(value[key])
            else:
                value = value[key]
        return value

    elif op.split(":")[0] == "value":
        if op.split(":")[1] == "Today":
            return today()
        return op.split(":")[1]


def today():
    today = date.today()
    formatted_date = today.strftime("%d-%m-%Y")
    stamp = get_timestamp(formatted_date)
    return stamp


def check(goldenContract, source_system, account,path):
    # with open("/home/dmacs/Desktop/JamesBond/IRS1.json", "r") as file:

    # open the json
    with open(path, "r") as file:
        data = json.load(file)
    # print(data)

    # upload the json and get cid
    cid = ipfs(path)

    section = getSection(source_system)
    print('\nThe Rules for ',source_system,' are :')
    print(section)
    # read rules and do checking on the contract
    section = section.split("\n")

    # find the number of rules so that you can check if all rules are satisfied
    number_of_rules = len(section)
    print("\nNumber of Rules = ", number_of_rules)
    print("------------------------------------------------")

    # list of trues
    list_of_trues = []

    for rule in section:
        words = rule.split()
        op1 = words[0]
        op = words[1]
        op2 = " ".join(words[2:])  # for special case of FO Trade Capture
        # print('\noperand1 :', op1)
        # print('operator :', op)
        # print('operand2 :', op2)

        if op == "=":
            # print("\n---Equality Operation---")
            operand1 = fetch_operand(data, op1)
            # print("operand 1:", operand1)
            operand2 = fetch_operand(data, op2)
            # print("operand 2:", operand2)
            if goldenContract.isEqual(operand1, operand2, {"from": account}):
                # print(f"\nOperation Succeeded: {operand1} = {operand2}")
                # print("------------------------------------------------")
                list_of_trues.append(True)
            else:
                print(rule)
                print(f"\nOperation Failed: {operand1} != {operand2}")
                print("------------------------------------------------")

        elif op == ">":
            # should be integer
            # print("\n---Greater than Operation---")
            operand1 = fetch_operand(data, op1)
            # print("operand 1:", operand1)
            operand2 = fetch_operand(data, op2)
            # print("operand 2:", operand2)
            if goldenContract.isGreater(operand1, operand2, {"from": account}):
                # print(f"\nOperation Succeeded: {operand1} > {operand2}")
                # print("------------------------------------------------")
                list_of_trues.append(True)
            else:
                print(rule)
                print(f"\nOperation Failed: {operand1} not greater than {operand2}")
                print("------------------------------------------------")

        elif op == "in":
            # print("\n---inList---")
            operand1 = fetch_operand(data, op1)
            # print("operand 1:", operand1)
            # should generalise this
            if op2 == "nominalCurrencyList":
                operand2 = nominalCurrencyList
            elif op2 == "paymentConventionList":
                operand2 = paymentConventionList
            # print("operand 2:", operand2)

            if goldenContract.inList(operand1, operand2, {"from": account}):
                # print(f"\nOperation Succeeded: {operand1} in {operand2}")
                # print("------------------------------------------------")
                list_of_trues.append(True)
            else:
                print(rule)
                print(f"\nOperation Failed: {operand1} not in {operand2}")
                print("------------------------------------------------")

        else:
            print("\nInvalid Operand")

    # check if all the rules are satisfied
    if len(list_of_trues) == number_of_rules:
        if source_system != "Murex":
            print("------------------------------------------------")
            print("\nAll the rules satisfied! Storing on Blockchain! ")
            print("------------------------------------------------")
            i = go_to_contract(data, cid, source_system, goldenContract, account)
            return i
        else:
            i = go_to_contract(data, cid, source_system, goldenContract, account)
            return i

    else:
        print("------------------------------------------------")
        print("\nNot all rules are satisfied!!")
        print(f"\nThe CID of the JSON is: {cid}")
        print("------------------------------------------------")


def go_to_contract(data, cid, source_system, goldenContract, account):
    ID = data["header"]["internalID"]
    # source_system = data['header']['sourceSystem']
    if source_system == "FOTradeCapture":
        #print('FO Trade Capture')
        i = foTradeCapture.main(goldenContract, data, ID, cid, account)
        return i

    elif source_system == "GBO":
        # print('GBO')
        i = gbo.main(goldenContract, data, ID, cid, account)
        return i

    elif source_system == "Murex":
        # print('Murex')
        i = murex.main(data, ID, goldenContract, cid, account)
        return i

def main():
    account = accounts.load("ganache")
    # load contract
    with open(
        "/home/dmacs/Desktop/JamesBond/build/contracts/GoldenContract.json", "r"
    ) as file:
        file_ = json.load(file)
    bytecode = file_["abi"]

    goldenContract = Contract.from_abi(
        "GoldenContract.sol", "0x3433D2D5aDDCE9db2fa78E97C8Dc4E52334568b3", bytecode
    )
    # goldenContract = GoldenContract.deploy({"from":accounts[0]})
    path = '/home/dmacs/Desktop/JamesBond/Events/8.json'
    print('\n Path of the file: ',path)
    # source_system = input("Enter the name of the Source System: ")
    source_system = 'Murex'
    print('\n---Checking if the given JSON originating from ',source_system,' satisfies all the rules---')
    check(goldenContract, source_system, account,path)
    print("\nThe End!!")


def test(goldenContract, source_system, account):
    path = get_file()
    return check(goldenContract, source_system, account,path)