import ipfsapi

# Connect to the IPFS daemon running locally
api = ipfsapi.Client('127.0.0.1', 5001)

# Add the file to IPFS
file_path = '/home/dmacs/Desktop/JamesBond/IRS.json'
result = api.add(file_path)

# Get the CID of the added file
cid = result['Hash']

print("The CID of the file is:", cid)