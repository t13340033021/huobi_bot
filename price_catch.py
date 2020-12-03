import api
from huobi.model.constant import *
import time
from datetime import datetime
import csv

while True:
    with open("test.csv","a+",newline='') as csvfile:
        writer = csv.writer(csvfile)


        last_price = api.get_latest_price(symbol=CoinSymbol.Btcusdt)
        if last_price:
            now=datetime.now()
            writer.writerow([datetime.timestamp(now),api.market_info.bid,api.market_info.ask])
            time.sleep(0.5)
