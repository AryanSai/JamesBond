from brownie import accounts,GBO,FO,Murex

def main():
    account = accounts.load("ganache")
    FO.deploy({"from": account}) #0x8393287a9b1e24297Bbce78f590e135E6982f47E
    GBO.deploy({"from": account}) #0xFfcB014A561eb93355c319B568faBe860e1c7e3A
    Murex.deploy({"from": account}) #0xE4A3e3FDd8771e7C5C02AfecE2Ba68b26bcd2df8