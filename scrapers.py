import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}

def scrape_kubii(url,local=False):
    html=""
    if local:
        with open("kubii.html","rb") as f:
            html=f.read()
    else:
        r = requests.get(url,headers=headers)
        if (r.status_code != 200):
            print(r.status_code)
            exit(100)
        # with open("kubii.html","wb") as f:
        #      f.write(r.content)
        html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    stock = soup.find("button",{"id": "availability_value"})
    print(stock)
    if stock.text.find('En rupture de stock') != -1:
        return False
    else:
        return True 

def scrape_tiendatec(url,local=False):
    html=""
    if local:
        with open("tiendatec.html","rb") as f:
            html=f.read()
    else:
        r = requests.get(url,headers=headers)
        if (r.status_code != 200):
            print(r.status_code)
            exit(100)
        # with open("kubii.html","wb") as f:
        #      f.write(r.content)
        html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    stock = soup.find("span",{"id": "availability_value"})
    if stock.text.find('Producto no disponible') == -1:
        return True
    else:
        return False 
