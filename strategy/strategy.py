import pandas as pd
import numpy as np
import talib.abstract as ta
from technical import qtpylib

class strategy:
    def __init__(self) -> None:
        self.df = pd.DataFrame()

    def populate_indicators(self) -> pd.DataFrame:
        self.df['sma'] = self.df['close'].rolling(50).mean()
        self.df['rsi'] = ta.RSI(self.df)
        
        self.df.loc[
            (
                (self.df['close'] > self.df['sma'])
            ), 'enter_long'] = True 

        self.df.loc[
            (
                (self.df['close'] < self.df['sma'])
            ), 'enter_short'] = True

        return self.df

    def get_signal(self) -> str:
        if self.df.iloc[-1]['enter_long'] == True:
            return 'ENTER LONG'

        if self.df.iloc[-1]['enter_short'] == True:
            return 'ENTER SHORT'

        if self.df.iloc[-1]['exit_long'] == True:
            return 'EXIT LONG'

        if self.df.iloc[-1]['exit_short'] == True:
            return 'EXIT SHORT'

        return 'HOLD'
