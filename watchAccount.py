import requests
import time
import threading


def getAccounts():
    with open('users.txt', 'r') as f:
        users = f.read().splitlines()
    return users


def accountStatus(user, token):
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'X-Auth-User': user,
        'X-Auth-Token': token
    }
    r = requests.get(f'https://api.sliver.tv/v1/user/{user}/inventory/list?number=10&status=unclaimed',
                     headers=head)
    return r.json()['body']


def start(user, token):
    addedIDs = []
    while True:
        m = accountStatus(user, token)
        if m != []:
            for item in m:
                if item['id'] not in addedIDs:
                    print(f'|ACCOUNT {user} | YOU HAVE A NEW ITEM IN YOUR INVENTORY WITH THE ID: {item["id"]}')
                    try:
                        print(f"|ACCOUNT {user} | The item is: {item['subject']['name']}\n")
                    except:
                        print(f"|ACCOUNT {user} | The item is: {item['item']['name']}\n")
                    addedIDs.append(item["id"])


users = getAccounts()

for accountm in users:
    account = accountm.split(":")
    token = account[0]
    user = account[1]
    print(token)
    print(user)
    threading.Thread(target=start, args=(user, token,)).start()
