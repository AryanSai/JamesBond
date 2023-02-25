# def fetch_operand(op):
#     #op = "key:esperanto-deals-deal1-legs-BUY_Fixed-flows[0]-nominal"
#     #op = "value:sairam"
#     if op.split(":")[0] == 'key':
#         path = op.split(":")[1]
#         print('key:',path)
#         keys = path.split("-")
#         value = data
#         for key in keys:
#             if "[" in key:
#                 key_name, index = key[:-1].split("[")
#                 value = value[key_name][int(index)]
#             else:
#                 value = value[key]
#         return value

#     elif op.split(":")[0] == 'value':
#         if op.split(":")[1] == 'Today':
#             return today()
#         else:
#             return op.split(":")[1]