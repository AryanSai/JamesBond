# import json
# from time import hello
# 
# print(hello)
# with open("/home/dmacs/Desktop/JamesBond/temp.json", "r") as file:
#     data = json.load(file)
 
# ID = data['header']['internalID']
# print(ID)
 
# data['header']['internalID']='Aryan' 
# file = open("/home/dmacs/Desktop/JamesBond/temp.json", "w")
# json.dump(data, file)
# file.close()

# print(data['header']['internalID'])

import json

def find_attribute_in_json(obj, attribute):
    results = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == attribute:
                results.append(value)
            else:
                results.extend(find_attribute_in_json(value, attribute))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(find_attribute_in_json(item, attribute))
    return results

# Example usage
with open("/home/dmacs/Desktop/JamesBond/IRS1.json", "r") as file:
        data = json.load(file)

results = find_attribute_in_json(data, 'nominalCurrency')
print(results)
