from harvester import Harvester             # need captch-harverst import
import requests
import json
import sys
import time
from termcolor import colored
#from .get_params import get_params
#from .get_params import get_params
import logging
import threading


item_name = "Supreme®/Hanes® Tagless Tees (3 Pack)"
category = "Accessories"
item_color = "White"
item_size = "Medium"

item_id = 0
item_id_color = 0
item_id_size = 0

profile = {
}

def get_stock():
    url = "https://www.supremenewyork.com/mobile_stock.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "close",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "Trailers"
    }

    stock = requests.get(url , headers = headers).json()
    return stock

def get_item_variants(item_id):

    item_url = f"https://www.supremenewyork.com/shop/{item_id}.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "close",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "Trailers"
    }
    item_variants = requests.get(item_url, headers=headers).json()

    return item_variants

def add_to_cart(item_id, size_id, style_id):                                        # cart 함수
    s = requests.Session()
    atc_url = f"https://www.supremenewyork.com/shop/{item_id}/add.json"
    '''headers = {
        'Host':                 'www.supremenewyork.com',
        'Accept':               'application/json',
        'Proxy-connection':     'keep-alive',
        'X-Requested-Width':    'XMLHttpRequest',
        'Accept-Encoding':      'gzip, deflate',
        'Accept-Language':      'en-us',
        'Content-Type':         'application/x-www-form-urlencoded',
        'Origin':               'http://www.supremenewyork.com',
        'Connection':           'keep-alive',
        'User-Agent':           'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
        'Referrer':             'http://www.supremenewyork.com/mobile'
    }'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.supremenewyork.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.supremenewyork.com/mobile/',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }
    data = {
        "size": size_id,                    #일본 서버는 data 값 size,style
        "style": style_id,                  #미국 서버는 s,st 영국은 잘모름
        "qty": "1"
    }

    atc_post = s.post(atc_url, headers = headers, data = data)

    if atc_post.json():
        print(atc_post.json()[0]['in_stock'])
        if atc_post.json()[0]['in_stock']:
            print(colored(f"{style_id}: Added to Cart", "blue"))
            return s

'''def make_checkout_parameters(s,profile,headers):
    checkout_page_content=s.get("https://www.supremenewyork.com/mobile/#checkout", headers=headers)

    cookie_sub = s.cookies.get_dict()["pure_cart"]
    checkout_params = get_params(checkout_page_content.content, profile, cookie_sub)

    if not checkout_params:
        print("Error with parsing checkout parameters")
    else:
        return checkout_params'''      #open_supreme 소스 주석
#def send_checkout_request(s, profile):

def fetch_captcha(session):

    print(colored("Waiting for Captcha...", "cyan"))

    while True:
        try:
            captcha_response = session.get("http://127.0.0.1:5000/www.supremenewyork.com/token", timeout=0.1)
            print(captcha_response.status_code)
            if captcha_response.status_code == 200:
                print(captcha_response.text)
                return captcha_response.text
        except requests.exceptions.Timeout:
            pass


def checkout(s,item_id):
    checkoutUrl = "https://www.supremenewyork.com/checkout.json"

    # made by 정훈
    '''checkoutHeaders={
        'Host': 'www.supremenewyork.com',
        'If-None-Match': '"*"',
        'Accept': 'application/json',
        'Proxy-Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-us',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://www.supremenewyork.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257',
        'Referrer': 'http://www.supremenewyork.com/mobile'
    }'''
    # made by openSupremebot
    checkoutHeaders= {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.8',
        'x-requested-with': 'XMLHttpRequest',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.supremenewyork.com',
        #'DNT': '1',
        #'Connection': 'keep-alive',
        'referer': 'https://www.supremenewyork.com/mobile/',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin'
        #'Pragma': 'no-cache',
        #'Cache-Control': 'no-cache',
        #'TE': 'Trailers',
    }
    checkout_page_content = s.get("https://www.supremenewyork.com/mobile/#checkout", headers=checkoutHeaders)   # get information var parse to html
    cookie_sub = s.cookies.get_dict()["pure_cart"]

    checkoutPayload = {
        'store_credit_id':'',
        'from_mobile':'1',
        'cookie-sub':cookie_sub,
        'same_as_billing_address':'1',
        'order[billing_name]':'aa',
        'order[email]':'bb@test.com',
        'order[tel]':'cc',
        'order[billing_zip]':'60056',
        'order[billing_state]':'富山県',
        'order[billing_city]':'ee',
        'order[billing_address]':'ff',
        'store_address' : '1',
        'credit_card[type]':'visa',
        'credit_card[cnb]':'1111 2222 3333 4444',
        'credit_card[month]' : '01',
        'credit_card[year]' : '2020',
        'credit_card[vval]' : '555',
        'order[terms]' :'0',
        'order[terms]' :'1',
        'g-recaptcha-response': fetch_captcha((s))
    }

    checkout_request = s.post("https://www.supremenewyork.com/checkout.json", headers=checkoutHeaders, data=checkoutPayload)
    print(checkout_request.json())
    if checkout_request.json():
        print("Success send")
    else:
        print("Send Failed...")
    return checkout_request

def get_order_status(s,checkout_request):                   #임시로 만듦 ,openSupreme 에서 가져옴
    checkout_response = checkout_request.json()
    if checkout_response["status"] == "failed":
        print("failed...")
    elif checkout_response["status"] == "queued":
        print("Successed")
        display_slug_status(s, checkout_response)

def display_slug_status(session, checkout_response):
    slug = checkout_response["slug"]

    while True:
        slug_status = get_slug_status(session, slug)
        if slug_status == "queued":
            print(colored(f": Getting Order Status", "yellow"))
        elif slug_status == "paid":
            print(colored(f": Check Email!", "green"))
            break
        elif slug_status == "failed":
            print(colored(f": Checkout Failed", "red"))
            return "failed"
    session.event.wait(timeout=1)   # 기존 timeout=10 에서 timeout=1로 변경

def get_slug_status(session, slug):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://www.supremenewyork.com/mobile/',
        'TE': 'Trailers'
    }
    status_url = f"https://www.supremenewyork.com/checkout/{slug}/status.json"

    slug_content = session.get(status_url, headers=headers).json()
    slug_status = slug_content["status"]
    print(slug_status)
    return slug_status

#--------------------------Main start--------------------------------#


def start_captcha_server():
    logging.getLogger('harvester').setLevel(logging.CRITICAL)
    harvester= Harvester()
    tokens=harvester.intercept_recaptcha_v2(
        domain='www.supremenewyork.com',
        sitekey='6LeWwRkUAAAAAOBsau7KpuC9AV-6J8mhw4AjC3Xz'
    )

    server_thread = threading.Thread(target=harvester.serve,daemon=True)
    server_thread.start()
    harvester.launch_browser()


start_captcha_server()                                                  ## 캡챠 harvest 실행 first

max_retry = 0
while True:
    breaker = True
    for item_name_stock in get_stock()['products_and_categories'][category]:
        if item_name_stock["name"] == item_name:
            item_id = item_name_stock["id"]                                #첫번째 id 값 가져오기
            breaker = False
            break
    if breaker == False:
        break
    max_retry = max_retry + 1
    print("waiting... "+str(max_retry))


for item_name_stock_detail in get_item_variants(item_id)['styles']:
    if item_name_stock_detail['name'] == item_color:
        item_id_color = item_name_stock_detail['id']                 #style(color) 일치하는 상품 id 가져
        for item_name_stock_detail2 in item_name_stock_detail['sizes']:
            if item_name_stock_detail2["name"] == item_size:
                item_id_size = item_name_stock_detail2["id"]         #size 일치하는 상품 id 가져옴

print(item_id, item_id_color, item_id_size)

ses = add_to_cart(item_id, item_id_size, item_id_color)         #add_to_cart 에서 return 한 세션값 s를 ses로 return

checkout_request = checkout(ses,item_id_size)                                    #Checkout 하기 위해 세션,상품id 파라미터로 전달

get_order_status(ses,checkout_request)



