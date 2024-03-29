from brownie import accounts, Contract
import multiprocessing as mp,time,random,json
import scripts.threechecker as checker

num_processes = 2
num_iterations = 1

def calculate_time(start_time):
    # Calculate and print the results
    total_time = time.time() - start_time
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Trades per second: {(num_processes*num_iterations)/total_time:.2f}")


def get_account():
    accounts_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    no = random.choice(accounts_list)
    account = accounts[no]
    return account


def process_func(goldenContract):
    for j in range(num_iterations):
        account = get_account()
        checker.test(goldenContract, account)

def main():
    # goldenContract = GoldenContract.deploy({"from": accounts[0]})
    with open(
        "/home/dmacs/Desktop/JamesBond/build/contracts/GoldenContract.json", "r"
    ) as file:
        file_ = json.load(file)
    bytecode = file_["abi"]

    goldenContract = Contract.from_abi(
        "GoldenContract.sol", "0x3433D2D5aDDCE9db2fa78E97C8Dc4E52334568b3", bytecode
    )
    start_time = time.time()
    # Create a list to hold the processes
    processes = []

    # Start the processes
    for i in range(num_processes):
        p = mp.Process(target=process_func, args=(goldenContract,))
        p.start()
        processes.append(p)

    # Wait for the processes to finish
    for p in processes:
        p.join()

    calculate_time(start_time)