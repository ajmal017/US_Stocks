# from StockMethod import StockMethod
from DBConnection import DBConnection
from Utility import Utility
from StockMethodFreq import StockMethodFreq
from StockMethodAS import StockMethodAS

import numpy as np
import time

def resample_data(symbol, freqs, resample_method='default',
                  new_col_names=['Ticker','Open','High','Low','Close','Volume','TotalTrades']):
    if 'default' == resample_method:
        resample_rule = {'Ticker': lambda x: x.head(1),
                         'FirstTradePrice': lambda x: x.head(1),
                         'HighTradePrice': np.max,
                         'LowTradePrice': np.min,
                         'LastTradePrice': lambda x: x.tail(1),
                         'Volume': np.sum,
                         'TotalTrades': np.sum}

    astype_dict = {'FirstTradePrice': 'str',
                   'HighTradePrice': 'str',
                   'LowTradePrice': 'str',
                   'LastTradePrice': 'str',
                   'Volume': 'str',
                   'TotalTrades': 'str'}

    start_time = time.time()
    print('Updating ' + symbol + '...')
    for freq in freqs:
        print(symbol + ' ' + freq)

        # get latest date in stock_freq table
        sm_f = StockMethodFreq(symbol, freq)
        latest_date_freq = Utility().as_str(sm_f.get_latest_date())
        print('latest_date_freq: ' + latest_date_freq)

        # get latest date in algoseek table
        sm_as = StockMethodAS(symbol)
        latest_date_as = Utility().as_str(sm_as.get_latest_date())
        print('latest_date_as: ' + latest_date_as)

        if not latest_date_freq or latest_date_freq != latest_date_as:
            sm = StockMethodAS(symbol)
            if latest_date_freq: # if not None
                stock_data = sm.query_by_symbol(start_date=latest_date_freq)
            else:
                stock_data = sm.query_by_symbol()

            stock_data = Utility().DateTimeAsIndex(stock_data)
            res = stock_data.resample(freq).apply(resample_rule).dropna()
            res = res.astype(astype_dict)
            res.columns = new_col_names
            try:
                db_con = DBConnection().db_sqlalchemy()
                res.to_sql(name=(symbol + '_' + freq).lower(), con=db_con, if_exists='replace', index=True, index_label='DateTime')
            except Exception as e:
                print(e)
            finally:
                db_con.close()
        else:
            print(symbol + ' ' + freq + ' is skipped.')

    end_time = time.time()
    print('End of updating ' + symbol + '...')
    print(end_time - start_time)

if __name__ == '__main__':
    stock_symbol_list = ['AAPL', 'ADBE', 'ADI', 'ADP', 'ADSK', 'ALGN', 'ALXN', 'AMAT', 'AMD', 'AMGN',
                         'AMZN', 'ANSS', 'ASML', 'ATVI', 'AVGO', 'BIDU', 'BIIB', 'BKNG', 'BMRN', 'CDNS',
                         'CDW', 'CERN', 'CHKP', 'CHTR', 'CMCSA', 'COST', 'CPRT', 'CSCO', 'CSGP', 'CSX',
                         'CTAS', 'CTSH', 'CTXS', 'DLTR', 'DXCM', 'EA', 'EBAY', 'EXC', 'EXPE', 'FAST',
                         'FB', 'FISV', 'FOX', 'FOXA', 'GILD', 'GOOG', 'GOOGL', 'IDXX', 'ILMN', 'INCY',
                         'INTC', 'INTU', 'ISRG', 'JD', 'KHC', 'KLAC', 'LBTYA', 'LBTYK', 'LRCX', 'LULU',
                         'MAR', 'MCHP', 'MDLZ', 'MELI', 'MNST', 'MSFT', 'MU', 'MXIM', 'NFLX', 'NTAP',
                         'NTES', 'NVDA', 'NXPI', 'ORLY', 'PAYX', 'PCAR', 'PEP', 'PYPL', 'QCOM', 'REGN',
                         'ROST', 'SBUX', 'SGEN', 'SIRI', 'SNPS', 'SPLK', 'SWKS', 'TCOM', 'TMUS', 'TSLA',
                         'TTWO', 'TXN', 'UAL', 'ULTA', 'VRSK', 'VRSN', 'VRTX', 'WBA', 'WDAY', 'WDC',
                         'XEL', 'XLNX', 'ZM']

    freqs = ['5min', '15min', '1H', '4H', '1D', '1W', '1M']
    # freqs = ['1D']

    for symbol in stock_symbol_list[:51]:
        resample_data(symbol=symbol, freqs=freqs)