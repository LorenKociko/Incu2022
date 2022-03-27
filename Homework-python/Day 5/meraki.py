import requests
import pandas as pd
from IPython.display import display

headers = {'X-Cisco-Meraki-API-Key': '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'}

def apiCall(url):
    res = requests.get(url, headers=headers)  
    data = res.json()
    return data

def getIndex(data,selected = ''):
    df = pd.DataFrame(data)
    if not selected:
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame(data,columns=selected)
    display(df)
    
    while True:
        index = input(f"\nSelect the index that you are interested from {0} to {len(data)-1}.\n")
        if index.isnumeric():
            index = int(index)
            if index>-1 and index<len(data):
                break
            else:
                print(f"(!) Error! Out of range. The index needs to be between {0} and {len(data)-1}")
        else:
            print(f"(!) Error! Please give a number between {0} to {len(data)-1}")
    return index

organizations = []
data = apiCall("https://api.meraki.com/api/v1/organizations")
for line in data:
    organizations.append({'name':line['name'],'id':line['id']})
    
print("The avaiable organizations are:")
index = getIndex(organizations)
organization = organizations[index]

print('Loading...')
data = apiCall(f"https://api.meraki.com/api/v1/organizations/{organization['id']}/networks")

organization['networks'] = []
for line in data:
    organization['networks'].append({'network_id':line['id'],'network_name':line['name']})

for network in organization['networks']:
    data = apiCall(f"https://api.meraki.com/api/v1/organizations/{organization['id']}/networks/{network['network_id']}/clients")
    network['client'] = []
    for client in data:
        network['client'].append(client)
    network['client_number'] = len(network['client'])
print(f"\nThe {organization['name']} organization has {len(organization['networks'])} networks, please choose one from the list.")
net_index = getIndex(organization['networks'],selected=['network_name','network_id','client_number'])

if organization['networks'][net_index]['client']:
    try:
        df = pd.DataFrame(organization['networks'][net_index]['client'],columns=['status','description','recentDeviceConnection','ssid','mac','ip'])
        display(df)
    except:
        print("Unexpected error!")
else: 
    print("No clients on the network")