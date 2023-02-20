import json
from brownie import Contract

def main():
    with open("/home/dmacs/Desktop/JamesBond/build/contracts/CheckerFO.json", "r") as file:
            file_fo = json.load(file)
    fo_bytecode=file_fo['abi']

    MyContract = Contract.from_abi("CheckerFO.sol", '0x0d64fFfaDf3bd63f8892200ACDDA1D1FB22E9825', fo_bytecode)
    result = MyContract.validNominalCurrency('CHF')
    print(result)

main()