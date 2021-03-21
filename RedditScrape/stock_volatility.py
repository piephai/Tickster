import yfinance as yf
import pandas as pd
from multiprocessing import Process
from threading import Thread
import concurrent


def check_stock_volume(csvFileName):
    df = pd.read_csv(csvFileName)
    increased_stock = []
    print(df['Symbol'])

    for stock in df['Symbol']:
        try:
            stock_info = yf.Ticker(stock)
            hist = stock_info.history(period="7d")
            previous_averaged_volume = hist['Volume'].iloc[1:6:1].mean()
            todays_volume = hist['Volume'][-1]
            previous_close = hist['Close'][-2]
            current_close = hist['Close'][-1]
            if todays_volume > previous_averaged_volume * 4 and previous_close < current_close and todays_volume > 100000:
                print(stock)
                print(previous_averaged_volume)
                print(todays_volume)
                increased_volume.append(stock)
        except:
            pass


def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


if __name__ == '__main__':
    runInParallel(check_stock_volume('tickersA-K.csv'),
                  check_stock_volume('tickersL-Z.csv'))
