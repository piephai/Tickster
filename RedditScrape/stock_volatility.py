import yfinance as yf
import pandas as pd
from multiprocessing import Process
from threading import Thread
import concurrent
import math


# Basically what I'm trying to do is create an account info which can provide
class AccountInfo:
    def __init__(self, available_fund)
    self.available_fund = available_fund


class BasicStockInfo:
    def __init__(self, stock_name, current_close):
        self.stock_name = stock_name
        self.current_close = current_close


class DetailedStockInfo(BasicStockInfo):
    def __init__(self, stock_name, current_close, previous_close, previous_averaged_volume, todays_volume):
        super().__init__(stock_name, current_close)
        self.previous_close = previous_close
        self.previous_averaged_volume = previous_averaged_volume
        self.todays_volume = todays_volume


class TradingOrder (BasicStockInfo, AccountInfo):
    def __init__(self, stock_name, current_close, quantity):
        super(TradingOrder, self).__init__()
        self.quantity = quantity
        self.available_fund = available_fund

    def buy_order(self):
        # TODO: Make a way to simulating trading. Current fund should be "static" and keep its value. Send notification that a trade was made
        self.quantity = math.floor(self.available_fund / self.current_close)
        if (self.available_fund > 500):
            available_fund = - available_fund/quantity

        return available_fund, quantity

    def initial_cost(self):

    def sell_order(available_fund, quantity, current_close):
        available_fund += quantity * current_close

        return available_fund, false


percentage_increase = 5
percentage_decrease = -10
take_profits = 10
input_period = 7


def percentage_meet_criteria(current_close, previous_close, percentage_change):
    if (percentage_change < 0):
        # If percentage_change < 0 which mean we're checking for when it goes below a stop loss
        if (percentage_change > (100((current_close - previous_close)/previous_close))):
            return true
    else:
        # Checking to see if it goes above a buy in
        if (percentage_change < (100((current_close - previous_close)/previous_close))):
            return true


def trigger_sell(current_close, bought_price):
    if(percentage_meet_criteria(current_close, bought_price, percentage_decrease)):
        return true
        # TODO: Link the Interactive API to automatically sell. Even better use the API to set a stop loss as soon as a buy is made
    if(percentage_meet_criteria(current_close, bought_price, take_profits)):
        return true
        # TODO: Link the Interactive API to automatically sell. Even better use the API to set a take profit after a buy is made


def get_stock_information(stock_name, stockBought=false):
    stock_info = yf.Ticker(stock)
    # Check what the bought in price was
    hist = stock_info.history(period=input_period)
    if (stockBought):
        return current_close = hist['Close'][-1]
    previous_averaged_volume = hist['Volume'].iloc[1:input_period - 1:1].mean()
    todays_volume = hist['Volume'][-1]
    previous_close = hist['Close'][-2]
    current_close = hist['Close'][-1]

    return current_close, previous_close, todays_volume, previous_averaged_volume


def send_notification(stock_name, quantity, current_close, bought=true):
    if (bought):
        print("You have purchased {0} of {1} at the current price of ${2} for the total value of ${3}",
              quantity, stock_name, current_close, quantity*current_close)
    else:
        print("You have sold {0} of {1} at the current price of ${2} for the total value of ${3}",
              quantity, stock_name, current_close, quantity*current_close)


def check_stock_volume(csvFileName, available_fund, stockBought):
    df = pd.read_csv(csvFileName)
    increased_stock = []
    print(df['Symbol'])
    bought_stock_name = None
    bought_price = None

    for stock in df['Symbol']:
        try:
            stock_information = get_stock_information(stock)
            closing_higher_boolean = percentage_meet_criteria(
                stock_information[0], stock_information[1])

            if (stock_information[2] > stock_information[3] * 4 and closing_higher_boolean and stock_information[2] > 100000):

                if (!stockBought):
                    order = buy_order(available_fund, stock_information[0])
                    bought_price = stock_information[0]
                    bought_stock_name = stock
                    quantity = order[1]
                    available_fund = order[0]
                    send_notification()
                print(stock)
                print(stock_information[3])
                print(stock_information[2])
                increased_volume.append(stock)

            if (stockBought):
                bought_stock_information = get_stock_information(
                    bought_stock_name, stockBought)
                if (trigger_sell(bought_stock_information[0], bought_price)):
                    sell_order(available_fund, quantity)
                    send_notification(bought_stock_name,
                                      quantity, bought_stock_information[0])
                    stockBought = False
                    break

        except:
            pass

    check_stock_volume(csvFileName, available_fund, stockBought)

# TODO: Once something is bought break off the list and keep checking that stock in a seperate thread


def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


if __name__ == '__main__':
    stockBought = false
    available_fund = 1000
    runInParallel(check_stock_volume('tickersA-K.csv', available_fund, stockBought),
                  check_stock_volume('tickersL-Z.csv', available_fund, stockBought))
