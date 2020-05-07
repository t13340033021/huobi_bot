from huobi import RequestClient
from huobi.constant.test import *
from huobi.base.printobject import *
from huobi.model import *

import time
test_flag = False



class loan_info:
    def __init__(self):
        self.coin = 0
        self.cash = 0
        self.min_coin=0
        self.min_cash=0

class order_info:
    def __init__(self):
        self.order_id = 0


class balance_info:
    def __init__(self):
        self.coin = 0
        self.cash = 0


class market_info:
    def __init__(self):
        self.bid = 0
        self.ask = 0


def get_latest_price(symbol=CoinSymbol.Btcusdt):
    try:
        request_client = RequestClient()
        depth = request_client.get_price_depth(symbol.symbol, 1)
        market_info.bid = depth.bids[0].price
        market_info.ask = depth.asks[0].price
        average_price = (depth.bids[0].price + depth.asks[0].price) / 2
        return average_price
    except Exception as e:
        print(e)
        print("retrying in 1s")
        time.sleep(1)
        return get_latest_price()


def getloaninfo(symbol=CoinSymbol.Btcusdt):
    request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
    try:
        result_list = request_client.get_margin_loan_info(symbol.symbol)
        if result_list and len(result_list):
            for loan_item in result_list:
                for item_info in loan_item.currencies:

                    if item_info.currency == symbol.coin:
                        loan_info.coin = item_info.loanable_amt
                        loan_info.min_coin = item_info.min_loan_amt
                    if item_info.currency == symbol.cash:
                        loan_info.cash = item_info.loanable_amt
                        loan_info.min_cash = item_info.min_loan_amt
        return loan_info
    except Exception as e:
        print(e)
        print("retrying in 1s")
        time.sleep(1)
        return getloaninfo()

def postloan(symbol=CoinSymbol.Btcusdt, currency="coin", amount=0.02):
    if currency== "coin" :
        currency=symbol.coin
        if loan_info.min_coin> amount or amount > loan_info.coin:
            return False
    if currency== "cash":
        currency=symbol.cash or amount > loan_info.cash
        if loan_info.min_cash> amount:
            return False
    try:
        request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
        loan_order_id = request_client.apply_loan(symbol=symbol.symbol, currency=currency, amount=amount)
        PrintBasic.print_basic(loan_order_id, "Loan Order Id")
    except Exception as e:
        print(e)
        print("retrying in 1s")
        time.sleep(1)
        return postloan()

def get_account_balance(symbol=CoinSymbol.Btcusdt):
    try:
        request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
        account_balance_list = request_client.get_account_balance()
        if account_balance_list and len(account_balance_list):
            for account in account_balance_list:
                if account.account_type == AccountType.MARGIN and account.subtype == symbol.symbol:
                    if account.balances and len(account.balances):
                        for balance in account.balances:
                            if balance.currency == CoinSymbol.Btcusdt.coin and balance.balance_type == "trade":
                                balance_info.coin = balance.balance
                            if balance.currency == CoinSymbol.Btcusdt.cash and balance.balance_type == "trade":
                                balance_info.cash = balance.balance
    except Exception as e:
        print(e)
        print("retrying in 1s")
        time.sleep(1)
        return get_account_balance()

def make_order(symbol=CoinSymbol.Btcusdt, sell=True, amount=0):
    try:
        request_client = RequestClient(api_key=g_api_key,
                                       secret_key=g_secret_key)
        if not test_flag:
            if sell:
                order_id = request_client.create_order(symbol.symbol, AccountType.MARGIN, OrderType.SELL_MARKET, amount,
                                                       price=0)
            else:
                order_id = request_client.create_order(symbol.symbol, AccountType.MARGIN, OrderType.BUY_MARKET, amount,
                                                       price=0)
        else:
            print("test mode on")
        order_info.order_id = order_id
    except Exception as e:
        print(e)
        print("retrying in 1s")
        time.sleep(1)
        return make_order()