import tkinter,json,ipfsapi,datetime
import scripts.foTradeCapture as foTradeCapture, scripts.gbo as gbo,scripts.murex as murex

def go_to_contract(data,cid):
    ID = data['header']['internalID']
    source_system = data['header']['sourceSystem']

    if source_system == 'FO Trade Capture':
        print('FO Trade Capture')
        foTradeCapture.main(data,ID,cid)

    elif source_system == 'GB':
        print('GBO')
        gbo.main(data,ID,cid)

    elif source_system == 'GBO':
        print('Murex') 
        murex.main(data,ID)

def current_timestamp():
    current_time = datetime.datetime.now(datetime.timezone.utc)
    formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+01:00"
    print(formatted_time)
    return formatted_time

def ipfs(file_path):
    api = ipfsapi.Client('127.0.0.1', 5001)
    result = api.add(file_path)
    cid = result['Hash']
    return cid

def modify_json(source):
    #upload the json and get cid
    cid = ipfs('/home/dmacs/Desktop/JamesBond/IRS1.json')

    with open("/home/dmacs/Desktop/JamesBond/IRS1.json", "r") as file:
        data = json.load(file)
    #change the source to the given argument
    data['header']['sourceSystem'] = source 
    #change event timestamp to current time
    data['header']['eventTimestamp'] = current_timestamp() 

    file = open("/home/dmacs/Desktop/JamesBond/IRS1.json", "w")
    json.dump(data, file)
    file.close()
    print(data['header']['sourceSystem'])

    go_to_contract(data,cid)

def main():
    m = tkinter.Tk() #m is the name of the mainwindow
    m.title('James Bond')
    button1 = tkinter.Button(m, text='FO Trade Capture', width=50, command=lambda: modify_json('FO Trade Capture'))
    button1.pack()  #pack organizes the qidgets in blocks 
    button2 = tkinter.Button(m, text='GBO', width=50, command=lambda: modify_json('GBO'))
    button2.pack()
    button3 = tkinter.Button(m, text='Murex', width=50, command=lambda: modify_json('Murex')) #here m is master and command to call a fn
    button3.pack()
    m.mainloop() #infinite loop to run the application
