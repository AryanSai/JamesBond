from brownie import accounts,GoldenContract
import time,random
import scripts.golden as gold

num_users = 20
num_iterations = 5

def get_account():
    accounts_list = [0,1,2,3,4,5,6,7,8,9]
    no = random.choice(accounts_list)
    account = accounts[no]
    return account

def get_ss():
    ss_list = ['GBO','FO Trade Capture','Murex']
    ss = random.choice(ss_list)
    return ss

def main():
    #run_load_test() only this was there
    goldenContract = GoldenContract.deploy({"from":accounts[0]})
    start_time = time.time()
    
    for i in range(num_users):
        for j in range(num_iterations):
            account = get_account()
            source_system = get_ss()
            gold.load_test(account,goldenContract,source_system)

    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"Total time: {total_time:.2f} seconds")

    print(f"Transactions per second: {(num_users*num_iterations)/total_time:.2f}")