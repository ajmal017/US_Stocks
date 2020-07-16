from DBConnection import DBConnection
from StockMethod import StockMethod

import bt

import pandas as pd

def above_sd(tickers, period=50, start='2010-01-01', name='above_sma'):
    """
    Long securities that are above their n period sd with equal weights.
    """
    # download data
    data = bt.get(tickers, start=start)
    # calc sma
    sma = data.rolling(period).sd()

    # create strategy
    s = bt.Strategy(name, [SelectWhere(data > sma),
                           bt.algos.WeighEqually(),
                           bt.algos.Rebalance()])

    # now we create the backtest
    return bt.Backtest(s, data)

if __name__ == '__main__':
    start_date = '2016-01-01'
    aapl_1h = StockMethod("aapl", "1h").query_by_symbol_and_freq(start=start_date)

    data = pd.DataFrame()
    data['aapl'] = aapl_1h['Close']

    above_sd('aapl', )



