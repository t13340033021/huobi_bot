import api
from huobi.model.constant import *
import time
import datetime


def round_down(num):
    num_x, num_y = str(num).split('.')
    num = float(num_x + '.' + num_y[0:3])
    return num


# print(api.get_latest_price())
api.getloaninfo(symbol=CoinSymbol.Btcusdt)
print(api.loan_info.btc)
# print(api.loan_info.usdt)
# api.postloan(symbol=CoinSymbol.Btcusdt,CoinSymbol.Btcusdt.cash,amount=int(float(api.loan_info.cash)*0.9))
api.get_account_balance()
print(api.balance_info.cash)
# api.make_order(sell=False, amount=int(api.balance_info.cash))


price = {'up': 9500,
         'down': 9000}

sell = False
stop_loss = False




def catch_break(symbol=CoinSymbol.Btcusdt, price=999, sell=True):
    flag_sell = False
    flag_buy = False
    last_price = api.get_latest_price(symbol=symbol)
    print(str(last_price) + "    " + str(datetime.datetime.now()))
    if not sell and last_price > price:
        flag_buy = True
        currency = "cash"
        api.getloaninfo()
        amount = round_down(float(api.loan_info.cash) * 0.9)

    elif sell and last_price < price:
        flag_sell = True
        currency = "coin"
        api.getloaninfo()
        amount = round_down(float(api.loan_info.coin) * 0.9)

    if (flag_sell or flag_buy) and (amount != 0 or stop_loss):
        api.postloan(symbol=symbol, currency=currency, amount=amount)
        api.get_account_balance()
        if flag_buy:
            api.make_order(symbol=symbol, sell=False, amount=round_down(api.balance_info.cash))
        else:
            api.make_order(symbol=symbol, sell=True, amount=round_down(api.balance_info.coin))


while True:
    catch_break(symbol=CoinSymbol.Btcusdt, price=price, sell=sell)
    time.sleep(1)
