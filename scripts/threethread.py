from brownie import accounts,Contract
import threading,json,time, random, scripts.threechecker as checker

num_threads = 1
num_iterations = 1

def calculate_time(start_time):
    # Calculate and print the results
    total_time = time.time() - start_time
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Trades per second: {(num_threads*num_iterations)/total_time:.2f}")

def get_account():
    accounts_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    no = random.choice(accounts_list)
    account = accounts[no]
    return account

def thread_func(goldenContract):
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
    # Create a list to hold the threads
    threads = []

    # Start the threads
    for i in range(num_threads):
        t = threading.Thread(target=thread_func, args=(goldenContract,))
        t.start()
        threads.append(t)

    # Wait for the threads to finish
    for t in threads:
        t.join()

    calculate_time(start_time)
