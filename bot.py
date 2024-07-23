from settings import settings
from enum import Enum
import pandas

class action(Enum):
    ENTER_LONG=1
    ENTER_SHORT=2
    EXIT_LONG=3
    EXIT_SHORT=4

class bot: 
    tickers = []
    tickers_df = {}

    def __init__() -> None:
        self.tickers = settings['tickers']

    # def update(df: pd.Dataframe) -> str:

