import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd
import numpy as np
import json


def create_fig(data, ticker):
    if isinstance(data.columns, pd.MultiIndex):
        close_series = data["Close"][ticker]
    else:
        close_series = data["Close"]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(close_series.index, close_series.values, label=ticker)
    ax.set_title(f"{ticker} - 5 Days 15m Close Prices")
    ax.set_xlabel("Datetime (UTC)")
    ax.set_ylabel("Close Price (USD)")
    ax.legend()
    ax.grid(True)
    
    plt.close(fig)

    return fig, ax


def load_json() -> dict:
    try:
        with open('stocks.json', 'r') as file:
             file_data= json.load(file)
             return file_data
    except json.decoder.JSONDecodeError:
        file_data = {}
        return file_data
    

class PandasJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.to_json(orient="columns")


def write_json(tickers_dict, filename = 'stocks.json'):
    with open('stocks.json', 'w') as file:
        file_data = load_json()
        for key in tickers_dict:
            if key in file_data:
                file_data[key]['price_history'].append(tickers_dict[key]['price_history'])
                file_data[key]['recommendations'] = tickers_dict[key]['recommendations']
                file_data[key]['news'] = tickers_dict[key]['news']
            else:
                file_data[key] = tickers_dict[ticker]
        file.seek(0)
        json.dump(file_data, file, indent=4, cls=PandasJSONEncoder)


def retrieve_info(tickers:list[str], tickers_dict = {}):
    for ticker in tickers:
        company = yf.Ticker(ticker)
        
        data = yf.download(tickers, period="5d", interval="15m")
        
        recommendations = company.recommendations
        
        info = yf.Search(ticker, news_count=8)
        
        tickers_dict[ticker] = {
        'price_history':data,
        'recommendations':recommendations,
        'news':info.news,
        }

    write_json(tickers_dict)






        












