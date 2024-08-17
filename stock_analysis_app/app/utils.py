import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import json

def get_stock_price(ticker):
    data = yf.Ticker(ticker).history(period='1y')
    if data.empty:
        return "No data available for this ticker."
    return str(data.iloc[-1].Close)

def calculate_SMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    if data.empty:
        return "No data available for this ticker."
    if len(data) < window:
        return f"Not enough data to calculate {window}-day SMA."
    return str(data.rolling(window=window).mean().iloc[-1])

def calculate_EMA(ticker, window):
    data = yf.Ticker(ticker).history(period='1y').Close
    if data.empty:
        return "No data available for this ticker."
    if len(data) < window:
        return f"Not enough data to calculate {window}-day EMA."
    return str(data.ewm(span=window, adjust=False).mean().iloc[-1])

def calculate_RSI(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    if data.empty:
        return "No data available for this ticker."
    delta = data.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    if len(data) < 14:  # Typically, RSI uses a 14-day period
        return "Not enough data to calculate RSI."
    ema_up = up.ewm(com=14-1, adjust=False).mean()
    ema_down = down.ewm(com=14-1, adjust=False).mean()
    rs = ema_up / ema_down
    return str(100 - (100 / (1 + rs)).iloc[-1])

def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period='1y').Close
    if data.empty:
        return "No data available for this ticker."
    short_EMA = data.ewm(span=12, adjust=False).mean()
    long_EMA = data.ewm(span=26, adjust=False).mean()
    MACD = short_EMA - long_EMA
    signal = MACD.ewm(span=9, adjust=False).mean()
    MACD_histogram = MACD - signal
    return f'{MACD.iloc[-1]}, {signal.iloc[-1]}, {MACD_histogram.iloc[-1]}'

def plot_stock_price(ticker):
    data = yf.Ticker(ticker).history(period='1y')
    if data.empty:
        return "No data available for this ticker."
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data.Close)
    plt.title(f'{ticker} Stock Price Over Last Year')
    plt.xlabel('Date')
    plt.ylabel('Stock Price ($)')
    plt.grid(True)
    plt.savefig('stock.png')
    plt.close()
    return "Plot saved as stock.png"

def get_latest_news(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news
    if not news:
        return "No news available for this ticker."
    
    news_list = []
    for article in news[:5]:  # Limit to the 5 latest news articles
        news_list.append({
            'Title': article.get('title', 'N/A'),
            'Publisher': article.get('publisher', 'N/A'),
            'Link': article.get('link', 'N/A')
        })
    return json.dumps(news_list, indent=4)

# Define the functions list
functions = [
    {
        'name': 'get_stock_price',
        'description': 'Gets the latest stock price given the ticker symbol of a company.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (for example AAPL for Apple).'
                }
            },
            'required': ['ticker']
        }
    },
    {
        'name': 'calculate_SMA',
        'description': 'Calculate the simple moving average for a given stock ticker and a window.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple)',
                },
                'window': {
                    'type': 'integer',
                    'description': 'The timeframe to consider when calculating the SMA'
                }
            },
            'required': ['ticker', 'window']
        }
    },
    {
        'name': 'calculate_EMA',
        'description': 'Calculate the exponential moving average for a given stock ticker and a window.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple)',
                },
                'window': {
                    'type': 'integer',
                    'description': 'The timeframe to consider when calculating the EMA'
                }
            },
            'required': ['ticker', 'window']
        }
    },
    {
        'name': 'calculate_RSI',
        'description': 'Calculate the RSI for a given stock ticker.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple)',
                }
            },
            'required': ['ticker']
        }
    },
    {
        'name': 'calculate_MACD',
        'description': 'Calculate the MACD for a given stock ticker.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple)',
                }
            },
            'required': ['ticker']
        }
    },
    {
        'name': 'plot_stock_price',
        'description': 'Plot the stock price for the last year given the ticker symbol of a company.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple)',
                }
            },
            'required': ['ticker'],
        }
    },
    {
        'name': 'get_latest_news',
        'description': 'Retrieves the latest news articles related to the company, providing insights into recent developments.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (e.g., AAPL for Apple).'
                }
            },
            'required': ['ticker']
        }
    },
]
