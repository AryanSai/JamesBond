import json,os

def main():    
    new_date='25-04-2023'
    folder_path='/home/dmacs/Desktop/JamesBond/Events'
    files = os.listdir(folder_path)
    for f in files:
        path = os.path.join(folder_path, f)
        with open(path, "r") as file:
            data = json.load(file)
        data['esperanto']['agreementDate'] = new_date

        f = open(path, "w")
        json.dump(data, f)
        f.close()
    print('Done')

main()