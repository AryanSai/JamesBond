from brownie import accounts,CheckerGBO,CheckerFO,CheckerMurex

def main():
    account = accounts.load("ganache")
    CheckerFO.deploy({"from": account}) #0xDfA8580e8183b6f6a353b169A04f26dab782f59b
    CheckerGBO.deploy({"from": account}) #0x040904CEE4d13b6F0Be04493909afc214763B97d
    CheckerMurex.deploy({"from": account}) #0x715fa7C970C72803fac0488B107Ec6adB5345d11