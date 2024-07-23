import requests, time
import ntfy, market
from strategy.strategy_trendline_breakout import strategy_trendline_breakout
from datetime import datetime
import pandas as pd
import os
from settings import *

# TESTING 
import mplfinance as mpf

# TODO: Pretty bad fix this later
while True:
    print('Connecting to gluetun!')
    time.sleep(1)

    try:
        response = requests.get('https://api.ipify.org?format=json').json()
        break

    except:
        print('Connection Failed')

print(f'{datetime.now()} - Running as IP {response["ip"]}')
print(f'{datetime.now()} - Trading Bot Initiated!')

trader = strategy_trendline_breakout()

# Trade loop
while True:
    for pair in pairs:
        print(f'{datetime.now()} - Populating Indicators on {pair}')

        df = market.get_candles(
            ticker = pair,
            timeframe = '15m',
        )
        trader.df = df 

        trader.df['enter_long'] = False 
        trader.df['enter_short'] = False
        trader.df['exit_long'] = False
        trader.df['exit_short'] = False
    
        trader.populate_indicators()

        match trader.get_signal():
            case 'ENTER LONG':
                print(f'{datetime.now()} - Signal -> ENTER LONG')
            case 'ENTER SHORT':
                print(f'{datetime.now()} - Signal -> ENTER SHORT')
            case 'EXIT LONG':
                print(f'{datetime.now()} - Signal -> EXIT LONG')
            case 'EXIT SHORT': 
                print(f'{datetime.now()} - Signal -> EXIT SHORT')
            case _:
                print(f'{datetime.now()} - No Signal -> HOLD')

        print(f'{datetime.now()} - Sleeping')
        time.sleep(int(sleep_time/5))

    time.sleep(sleep_time)
