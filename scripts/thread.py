from brownie import accounts, GoldenContract
import threading
import time
import random
import scripts.checker as checker

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

def get_ss():
    ss_list = ["GBO", "FO Trade Capture", "Murex"]
    if not hasattr(get_ss, "index"):
        get_ss.index = 0
    ss = ss_list[get_ss.index]
    get_ss.index = (get_ss.index + 1) % len(ss_list)
    return ss

def thread_func(goldenContract):
    for j in range(num_iterations):
        account = get_account()
        source_system = get_ss()
        checker.test(goldenContract, source_system, account)


def main():
    goldenContract = GoldenContract.deploy({"from": accounts[0]})
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
