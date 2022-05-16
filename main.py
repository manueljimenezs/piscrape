#!/usr/bin/env python3
import scrapers
import json
import re, os
from dotenv import load_dotenv
import requests

try:
    load_dotenv()
except:
    print("Need a .env variable with the following content:")
    print("\nTG_API_TOKEN=XXX:YYY - CHATID=00000")
    exit(1)

TG_API_TOKEN = os.getenv('TG_API_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

scrapers = {
    "kubii": scrapers.scrape_kubii,
    "tiendatec": scrapers.scrape_tiendatec
}

class Event:
    def __init__(self,product,title,url,inStock):
        self.product = product
        self.title = title
        self.url = url
        self.inStock = inStock
    def __str__(self):
        return (
f"""🍒  *{self.product}*
🏛  {self.title}
📦 Stock: {'In Stock ✅' if self.inStock else 'No stock available ❌'}

🌍  {self.url}""")
    def __eq__(self,other):
        return (self.url == other.url) and (self.inStock == other.inStock)

def obj_dict(obj):
    return obj.__dict__

newEvents = []
oldEvents = []

def send_telegram_message(message,disable_prevlink=False):
    msg = re.sub(r"([-.()=])", r"\\\1",str(message))
    send_text = ('https://api.telegram.org/bot' +
                  TG_API_TOKEN + 
                  '/sendMessage?chat_id=' + CHAT_ID + 
                  f'&parse_mode=MarkdownV2&disable_web_page_preview={disable_prevlink}&text=' + msg)
    return requests.get(send_text)
    
def scan():
    global oldEvents
    sources = {}
    with open('sources.json','r') as f:
        sources = json.load(f)
    if os.path.exists('latestEvents.json'):
        aux = {}
        with open("latestEvents.json","r") as f:
            aux = json.load(f)
            for i in aux:
                e = Event(i['product'],i['title'],i['url'],i['inStock'])
                oldEvents.append(e)
    for type, sources in sources.items():
        for source_name, source_url in sources.items():
            if source_name in scrapers.keys():
                inStock = False
                inStock = scrapers[source_name](source_url,local=False)
                e = Event(type,source_name,source_url,inStock)
                newEvents.append(e)
                if oldEvents:
                    if e not in oldEvents:
                        print(e)
                        send_telegram_message(e,disable_prevlink=True)
                else:
                    print(e)
                    send_telegram_message(e, disable_prevlink=True)
    if newEvents:
        with open('latestEvents.json','w') as f:
            json.dump(newEvents,f,default=obj_dict)
    print("Finished")

scan()