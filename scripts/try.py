import json
from datetime import date,datetime

with open("/home/dmacs/Desktop/JamesBond/IRS1.json", "r") as file:
    data = json.load(file)

# op = "key:esperanto-deals-deal1-legs-BUY_Fixed-flows[0]-settlementDate"
op = "key:esperanto-deals-deal1-legs-BUY_Fixed-flows[0]-settlementDate"
# op = "value:sairam"

def get_timestamp(dt):
    date = datetime.strptime(dt, '%d-%m-%Y')
    timestamp = int(date.timestamp())
    return timestamp

if op.split(":")[0] == 'key':
    path = op.split(":")[1]
    print('key:',path)
    keys = path.split("-")
    value = data
    for key in keys:
        if "[" in key:
            key_name, index = key[:-1].split("[")
            value = value[key_name][int(index)]
        elif 'Date' in key:
            value =  get_timestamp(value[key])
        else:
            value = value[key]         
    print(value)

elif op.split(":")[0] == 'value':
    print(op.split(":")[1])    