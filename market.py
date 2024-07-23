import requests, asyncio, pandas as pd, numpy as np, os, re
from typing import Optional
from datetime import datetime, timedelta
import ccxt

exchange = ccxt.phemex({
        'apiKey': os.environ.get('API_KEY'),
        'secret': os.environ.get('API_SECRET'),
        'options': {
            'defaultType': 'swap',
        }
    })
exchange.set_sandbox_mode(True)

print('Init Client')

def resample(old_df: pd.DataFrame, timeframe: Optional[str] = os.environ.get('TIMEFRAME')):
    df = old_df.copy()

    resampled = df.resample("15min") # 15T TODO: Change later to dynamically read from $TIMEFRAME
    df = resampled.agg({ 
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'baseTokenVolume': 'sum',
        'usdVolume': 'sum',
        'startingOpenInterest': 'first',
        'trades': 'sum',
        'startedAt': 'first',
        'resolution': 'first'
    })
    timeframe = ''.join(filter(lambda x: x.isdigit(), timeframe))
    
    # Clean up dataframe from incomplete bars
    counts = resampled.size()
    completed_candles = counts[counts == 15].index # TODO: change the verification to dynamically read from $TIMEFRAME
    df = df.loc[completed_candles]

    # Fix naming
    df.rename(columns={"resolution": "timeframe"}, inplace=True)

    return df

def get_candles(ticker: str, timeframe: str):
    ohlcv = exchange.fetch_ohlcv(ticker, timeframe)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    return df

def prepare_df(df: pd.DataFrame):
    for i in range(len(df)):
        df['enter_long'][i] = False 
        df['enter_short'][i] = False
        df['exit_long'][i] = False
        df['exit_short'][i] = False

    return df

def buy(ticker: str, side: str):
    order = exchange.create_order(symbol, 'market', 'buy', amount)

# def stoploss(ticker: str, side: str):

