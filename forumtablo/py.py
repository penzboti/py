email = "test@test.test"
picture = 10

thread_number = 20

import requests
import queue
import threading
import random
import time
import json as importjson

# not working keyboard interrupt check
# import atexit # doesn't work how i want it to work
# def exit_handler():
#     print("kilépés...")
#     global logs
#     with open("logs.txt", "w") as f:
#         for elem in logs:
#             f.write(elem)
#     print("logok kiírva")
# atexit.register(exit_handler)

queue = queue.Queue()
logs = []
number = 0
names = []

def get_names():
    global names
    # https://1000randomnames.com/
    with open("names.txt") as f:
      for x in f:
        names.append(x.replace('\n', ''))
    print("names loaded")

def get_proxy_list_1():
    url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=json"
    proxiesres = requests.get(url)
    proxiesjson = proxiesres.json()
    proxylist = proxiesjson['proxies']
    for proxy in proxylist:
        if proxy['protocol'] == "http" and proxy['alive']:
            queue.put(proxy['proxy'])
    print("got proxy 1")

def get_proxy_list_2():
    # there was another proxy thing, do that
    print("got proxy 2")
    pass

def check_proxy():
    global queue
    while not queue.empty():
        # print("checking proxy")
        p1 = queue.get()
        proxies = {
            "http":p1,
            "https":p1
        }
        try:
            res = requests.get('https://ident.me/ip', proxies=proxies) 
        except:
            # print("proxy bad")
            continue
        if res.status_code == 200:
            print(p1)
            use_proxy(proxies)
    print("end of queue; thread dies")

def use_proxy(p):
    global email
    global pictures
    global names
    global number
    global logs

    name = random.choice(names)
    namestring = name.replace(' ', '_')
    named_email = email.replace("@",f"+{namestring}@")
    form_data = {"nev":name, "email": named_email, "jatekszabalyzat": "1", "kep": picture}

    try:
        res = requests.post("https://forumtablo.hu/tablo/szavazas",data=form_data, proxies=p)
    except:
        print("nem mukszik a proxy")
        return
    if res.status_code == 200:
        json = res.json()
        if json['success'] == 1:
            number = number + 1
            print(f"siker: {number}")
        else:
            n = len(logs) + 1
            print("nem siker")
            logs.append(importjson.dumps(json))
    else:
        print("csatlakozási probléma")

def clear_log_file():
    with open("logs.txt", "w") as f:
        f.write("")
    print("cleared log file")

clear_log_file()
get_names()
threading.Thread(target=get_proxy_list_1).start()
threading.Thread(target=get_proxy_list_2).start()
while True:
    # wait until some proxies appear, so we can use them
    if queue.qsize() >= thread_number:
        break
for t in range(thread_number):
    threading.Thread(target=check_proxy).start()

while True:
    time.sleep(5)
    locallogs = logs
    logs = []
    with open("logs.txt", "a") as f:
        for elem in locallogs:
            f.write(elem)
            f.write("\n")
    if queue.empty():
        print("proxy list empty")
        break
