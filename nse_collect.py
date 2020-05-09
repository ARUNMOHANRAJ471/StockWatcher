# import libraries
import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import schedule
import time
import json

toaster = ToastNotifier()


def stock_scraper(url, name, threshold, operation):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.select(
        "#div_nse_livebox_wrap > div.nsedata_bx > div.nsbs_bg > div > div.pcnsb.div_live_price_wrap > span.span_price_wrap")
    price = float(result[0].text)
    print("price is: "+str(price))
    if operation == 'gt':
        if price > threshold:
            toaster.show_toast(name+" share price", str(price), icon_path=None, duration=5)
    if operation == 'lt':
        if price < threshold:
            toaster.show_toast(name+" share price", str(price), icon_path=None, duration=5)

def get_all_stock_info():
    with open('./input.json') as f:
        data = json.load(f)

    for stock in data['stocks']:
        print(stock['name'])
        stock_scraper(stock['url'], stock['name'], stock['threshold'], stock['operation'])




schedule.every(1).minutes.do(get_all_stock_info)

while True:
    schedule.run_pending()
    time.sleep(1)

