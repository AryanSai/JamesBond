import ipfsapi, os
import scripts.checker as checker

previous_third_file = None

def get_ss():
    ss_list = ["GBO", "FOTradeCapture", "Murex"]
    if not hasattr(get_ss, "index"):
        get_ss.index = 0
    ss = ss_list[get_ss.index]
    get_ss.index = (get_ss.index + 1) % len(ss_list)
    return ss

def ipfs(file_path):
    api = ipfsapi.Client("127.0.0.1", 5001)
    result = api.add(file_path)
    cid = result["Hash"]
    return cid

def get_num(filename):
    return int(os.path.splitext(filename)[0])

def get_files():
    directory_path = "/home/dmacs/Desktop/JamesBond/Events"
    global previous_third_file

    # Get a list of all JSON files in the directory
    files = [f for f in os.listdir(directory_path) if f.endswith(".json")]

    # Sort the files based on a numerical value extracted from their filenames
    sorted_file_list = sorted(files, key=get_num)

    # Select the next three files that come after the previously selected third file
    selected_files = []
    if previous_third_file is None or previous_third_file not in sorted_file_list:
        selected_files = sorted_file_list[0:3]
    else:
        index = sorted_file_list.index(previous_third_file)
        if index < len(sorted_file_list) - 3:
            selected_files = sorted_file_list[index + 1 : index + 4]
        else:
            selected_files = sorted_file_list[0:3]

    # Store the third file from the selected set for future use
    previous_third_file = selected_files[2]

    # Create a list of absolute file paths for the selected files
    file_paths = [os.path.join(directory_path, file) for file in selected_files]

    # Print the file paths for debugging purposes
    print("file paths: ", file_paths)

    # Return the list of file paths
    return file_paths


def test(goldenContract, account):
    files = get_files()
    truth = 0
    for file in files:
        source_system = get_ss()
        if checker.check(goldenContract, source_system, account,file):
            truth+=1     
    if truth == 3:
        print('This thread finished sucessfully!!')
        print("###########################################################################################")