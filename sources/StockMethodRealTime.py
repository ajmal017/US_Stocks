from StockMethod import StockMethod
from DBConnection import DBConnection
from Utility import Utility
import pandas as pd
import numpy as np

class StockMethodRealTime:
    def __init__(self, p_symbol="", p_freq=""):
        self.symbol = p_symbol.lower()
        self.freq = p_freq.lower()

    def get_real_time_data(self):
        """Get today real time data from table IB_TODAY_<stock>"""
        query = "SELECT * FROM IB_TODAY_" + self.symbol + ";"
        try:
            db_con = DBConnection().db_sqlalchemy()
            result = pd.read_sql(query, db_con)
            return result
        except Exception as e:
            print(e)
            return None
        finally:
            db_con.close()

    def get_resample_rt_data(self, resample_rule="default"):
        data = Utility().DateTimeAsIndex(self.get_real_time_data())

        if "default" == resample_rule:
            resample_rule = {'Ticker': lambda x: x.head(1),
                             'Open': lambda x: x.head(1),
                             'High': np.max,
                             'Low': np.min,
                             'Close': lambda x: x.tail(1),
                             # 'Volume': np.sum}
                             'Volume': lambda x: np.sum(x)*100}

        resampled_data = data.resample(self.freq).apply(resample_rule).dropna()

        # index as column
        resampled_data = resampled_data.reset_index(drop=False)

        return resampled_data

    def join_real_time_data(self, p_start = "", p_end = ""):
        # get non-real-time data with specified freq
        non_rt_stock = StockMethod(symbol=self.symbol, freq=self.freq)
        non_rt_data = non_rt_stock.query_by_symbol_and_freq(start=p_start, end=p_end)
        non_rt_data = non_rt_data.loc[:,['DateTime', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']]

        print(non_rt_data)

        # get real-time data
        resampled_rt_data = self.get_resample_rt_data()
        resampled_rt_data.columns = ['DateTime', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']

        print(resampled_rt_data)

        print(non_rt_data.append(resampled_rt_data))

if __name__ == '__main__':
    aapl_1h = StockMethodRealTime('aapl', '1h')
    aapl_1h.join_real_time_data(p_start = "2020-07-05", p_end = "2020-07-10")



