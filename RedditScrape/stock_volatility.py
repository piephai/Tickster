from datetime import date, datetime
import yfinance as yf
import pandas as pd
import numpy as np
from multiprocessing import Process
from threading import Thread
import concurrent
import math


# Basically what I'm trying to do is create an account info which can provide
class AccountInfo:
    def __init__(self, available_fund, percentage_increase, percentage_decrease, percentage_to_take_profit):
        self.stock_holdings = pd.DataFrame(
            columns=['Name', 'Close', 'Quantity', 'Date'])
        self.set_percentage_decrease(percentage_decrease)
        self.set_percentage_increase(percentage_increase)
        self.set_percentage_to_take_profit(percentage_to_take_profit)
        self.available_fund = available_fund

    def get_available_fund(self):
        return self.available_fund

    def get_percentage_decrease(self):
        return self.percentage_decrease

    def get_percentage_increase(self):
        return self.percentage_increase

    def get_stock_holdings(self):
        return self.stocks_holding

    def set_available_fund(self, change_in_fund):
        self.available_fund += change_in_fund

    def get_percentage_to_take_profit(self):
        return self.percentage_to_take_profit

    def set_percentage_to_take_profit(self, percentage_to_take_profit):
        self.percentage_to_take_profit = percentage_to_take_profit / 100

    def set_percentage_increase(self, percentage_increase):
        self.percentage_increase = percentage_increase / 100

    def set_percentage_decrease(self, percentage_decrease):
        self.percentage_decrease = percentage_decrease / 100

    def add_new_holdings(self, stock_name: str, close: float, quantity: int, date: date):
        try:
            new_row = {'Name': stock_name, 'Close': close,
                       'Quantity': quantity, 'Date': date}
            self.stock_holdings = self.stock_holdings.append(
                new_row, ignore_index=True)
        except:
            print(Exception)

    def get_holdings(self):
        return self.stock_holdings

    def get_specific_holding(self, stock_name):
        return self.stock_holdings[self.stock_holdings.Name.isin([stock_name])]


class StockInfo:
    def __init__(self):
        self.stock_holdings = pd.DataFrame(
            columns=['Name', 'Close', 'Todays_Volume', 'Previous_Averaged_Volume', 'Open'])

    def update_stock_info(self, stock_name, close_price, todays_volume, previous_averaged_volume, open_price):
        if (stock_name in self.stock_holdings.values):
            index = self.stock_holdings[self.stock_holdings['Name']
                                        == stock_name].index.values
            self.stock_holdings.loc[index, ['Name', 'Close', 'Todays_Volume', 'Previous_Averaged_Volume', 'Open']] = [
                stock_name, close_price, todays_volume, previous_averaged_volume, open_price]
        else:
            try:
                new_row = {'Name': stock_name, 'Close': close_price,
                           'Todays_Volume': todays_volume, 'Previous_Averaged_Volume': previous_averaged_volume, 'Open': open_price}
                self.stock_holdings = self.stock_holdings.append(
                    new_row, ignore_index=True)
            except:
                print(Exception)

    def get_stock_info(self, stock_name):
        return self.stock_holdings[self.stock_holdings.Name.isin([stock_name])]


# For getting the current stock price


# class BasicStockInfo:
#     def __init__(self, stock_name, current_close):
#         self.stock_name = stock_name
#         self.current_close = current_close
#         self.stocks = pd.DataFrame(columns=['Name', 'Close'])

#     @property
#     def get_stock_name(self):
#         return self.stock_name

#     @property
#     def get_current_stock_price(self):
#         return self.current_close


# # TODO: THe idea is this class will be instantiate when the conditions of the stocks are met. Once done the stocks that met the condition will get added to a data structure then the best performer
# # This is more ideal for historical stock prices
# class DetailedStockInfo(BasicStockInfo):
#     def __init__(self, stock_name, previous_close, current_close, previous_averaged_volume, todays_volume):
#         super().__init__(stock_name, current_close)
#         self.previous_close = previous_close
#         self.previous_averaged_volume = previous_averaged_volume
#         self.todays_volume = todays_volume

#     @property
#     def get_previous_averaged_volume(self):
#         return self.previous_averaged_volume

#     @property
#     def get_todays_volume(self):
#         return self.get_todays_volume

#     @property
#     def get_yesterday_price(self):
#         return self.previous_close

# # TODO: Check to see if it's possible to set properties like self.total_cost = 0 within the constructor like below
# # TODO: Implement buy_order properly
# # TODO:
# # This class is first instiated when the conditions of the stocks are met


# class TradingOrder (BasicStockInfo, AccountInfo):
#     def __init__(self, stock_name, current_close, quantity, available_fund):
#         AccountInfo.__init__(self, available_fund)
#         BasicStockInfo.__init__(self, stock_name, current_close)
#         self.quantity = quantity
#         self.available_fund = available_fund
#         self.initial_stock_price = 0
#         self.total_initial_cost = 0
#         self.total_cost = 0

#     # TODO: This method should be called if the conditions have been met outside of this class

#     def buy_order(self):
#         self.quantity = math.floor(self.available_fund / self.current_close)
#         self.total_initial_cost = self.quantity * self.current_close
#         if (self.available_fund > 500):
#             self.available_fund = self.available_fund - self.total_initial_cost
#         self.initial_stock_price = self.current_close

#     def sell_order(self, current_close, quantity):
#         if (quantity > self.quantity and quantity < 0):
#             raise ValueError(
#                 "Invalid quantity. Check to see if quantity is greater than 0 and is not more than what you currently own")
#         self.quantity -= quantity
#         self.current_close = current_close
#         self.available_fund += quantity * current_close

#     def threshold_reach(self, previous_close):
#         if (self.current_close > previous_close * 1.05


#     @ current_close.setter
#     def current_close(self, current_close):
#         self.current_close=current_close

#     @ property
#     def get_total_value(self):
#         return self.quantity * self.current_close

#     @ property
#     def get_total_profit(self):
#         return self.total_cost - self.initial_stock_price


# percentage_increase = 5
# percentage_decrease = -10
# take_profits = 10
# input_period = 7


# def percentage_meet_criteria(current_close, previous_close, percentage_change):
#     if (percentage_change < 0):
#         # If percentage_change < 0 which mean we're checking for when it goes below a stop loss
#         if (percentage_change > (100((current_close - previous_close)/previous_close))):
#             return true
#     else:
#         # Checking to see if it goes above a buy in
#         if (percentage_change < (100((current_close - previous_close)/previous_close))):
#             return true


# def trigger_sell(current_close, bought_price):
#     if(percentage_meet_criteria(current_close, bought_price, percentage_decrease)):
#         return true
#         # TODO: Link the Interactive API to automatically sell. Even better use the API to set a stop loss as soon as a buy is made
#     if(percentage_meet_criteria(current_close, bought_price, take_profits)):
#         return true
#         # TODO: Link the Interactive API to automatically sell. Even better use the API to set a take profit after a buy is made


# def get_stock_information(stock_name, stockBought=false):
#     stock_info=yf.Ticker(stock_name)
#     # Check what the bought in price was
#     hist=stock_info.history(period=input_period)
#     if (stockBought):
#         return current_close=hist['Close'][-1]
#     previous_averaged_volume=hist['Volume'].iloc[1:input_period - 1:1].mean()
#     todays_volume=hist['Volume'][-1]
#     previous_close=hist['Close'][-2]
#     current_close=hist['Close'][-1]

#     return current_close, previous_close, todays_volume, previous_averaged_volume


# def send_notification(stock_name, quantity, current_close, bought=true):
#     if (bought):
#         print("You have purchased {0} of {1} at the current price of ${2} for the total value of ${3}",
#               quantity, stock_name, current_close, quantity*current_close)
#     else:
#         print("You have sold {0} of {1} at the current price of ${2} for the total value of ${3}",
#               quantity, stock_name, current_close, quantity*current_close)


# def check_stock_volume(csvFileName, available_fund, stockBought):
#     df=pd.read_csv(csvFileName)
#     increased_stock=[]
#     print(df['Symbol'])
#     bought_stock_name=None
#     bought_price=None

#     for stock in df['Symbol']:
#         try:
#             stock_information=get_stock_information(stock)
#             closing_higher_boolean=percentage_meet_criteria(
#                 stock_information[0], stock_information[1])

#             if (stock_information[2] > stock_information[3] * 4 and closing_higher_boolean and stock_information[2] > 100000):

#                 if (!stockBought):
#                     order=buy_order(available_fund, stock_information[0])
#                     bought_price=stock_information[0]
#                     bought_stock_name=stock
#                     quantity=order[1]
#                     available_fund=order[0]
#                     send_notification()
#                 print(stock)
#                 print(stock_information[3])
#                 print(stock_information[2])
#                 increased_volume.append(stock)

#             if (stockBought):
#                 bought_stock_information=get_stock_information(
#                     bought_stock_name, stockBought)
#                 if (trigger_sell(bought_stock_information[0], bought_price)):
#                     sell_order(available_fund, quantity)
#                     send_notification(bought_stock_name,
#                                       quantity, bought_stock_information[0])
#                     stockBought=False
#                     break

#         except:
#             pass

#     check_stock_volume(csvFileName, available_fund, stockBought)

# # TODO: Once something is bought break off the list and keep checking that stock in a seperate thread


# def runInParallel(*fns):
#     proc=[]
#     for fn in fns:
#         p=Process(target=fn)
#         p.start()
#         proc.append(p)
#     for p in proc:
#         p.join()


if __name__ == '__main__':
    # stockBought=false
    # available_fund=1000
    # runInParallel(check_stock_volume('tickersA-K.csv', available_fund, stockBought),
    #               check_stock_volume('tickersL-Z.csv', available_fund, stockBought))
    accountInfo = AccountInfo(1000, 5, 10, 10)

    df = pd.DataFrame(
        columns=['Name', 'Close', 'Quantity', 'Date'])
    df.loc[-1] = ['SOR', 20.0, 50, "10/02/1998"]
    accountInfo.add_new_holdings('SOR', 20.0, 50, "10/02/1998")
    print(accountInfo.get_holdings())
    accountInfo.add_new_holdings('CXO', 0.3, 50, "10/02/1998")
    print(accountInfo.get_specific_holding('CXO'))

    stockInfo = StockInfo()
    stockInfo.update_stock_info('CXO', 0.3, 100000, 10000, 0.2)
    print(stockInfo.get_stock_info('CXO'))
    stockInfo.update_stock_info('CXO', 0.6, 100000, 10000, 0.2)
    print(stockInfo.get_stock_info('CXO'))
