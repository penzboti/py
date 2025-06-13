# https://youtu.be/FbtCl9jJyyc?si=C3D-GhplBQZmLxBW
import requests
import queue
import threading

thread_number = 20

queue = queue.Queue()
def get_1proxy_list():
    url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=json"
    proxiesres = requests.get(url)
    proxiesjson = proxiesres.json()
    proxylist = proxiesjson['proxies']
    for proxy in proxylist:
        if proxy['protocol'] == "http" and proxy['alive']:
            queue.put(proxy['proxy'])


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
            continue
        if res.status_code == 200:
            print(p1)
            use_proxy(proxies)

def use_proxy(p):
    nev = "johndoe"
    kep = "10"
    email = "aaaa@aaaa.aaaa"
    form_data = {"nev":nev, "email": email, "jatekszabalyzat": "1", "kep": kep}
    try:
        res = requests.post("https://forumtablo.hu/tablo/szavazas",data=form_data, proxies=p)
    except:
        print("nem mukszik a proxy")
        return
    if res.status_code == 200:
        json = res.json()
        if json['success'] == 1:
            print("siker")
        else:
            print("nem siker, mert:")
            print(json)
    else:
        print("nem 200as")
    
get_1proxy_list()
for t in range(thread_number):
    threading.Thread(target=check_proxy).start()
