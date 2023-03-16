from brownie import accounts,GoldenContract

def main():
    account = accounts.load("ganache")
    GoldenContract.deploy({"from": account}) #0x02c5E7ADBDaE96625d97606dEa3CEEE90A7437Ee