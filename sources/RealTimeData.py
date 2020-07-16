import ib_insync as ibsy
import time
from datetime import datetime

from DBConnection import DBConnection

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

def delete_table_data(stock_symbol_list):
    for symbol in stock_symbol_list:
        query = "DELETE FROM ib_today_" + symbol + ";"
        try:
            mydb = DBConnection().db_mysql_connector()
            mycursor = mydb.cursor()
            mycursor.execute(query)
            mydb.commit()
            print("ib_today_", symbol, ": ", mycursor.rowcount, " record(s) deleted")
        except Exception as e:
            print(e)
            return None
        finally:
            mycursor.close()
            mydb.close()

def get_real_time_data(steamNum, durationStr, stock_symbol_list, host="127.0.0.1", port=7496, clientId=1):
    """
    https://interactivebrokers.github.io/tws-api/classIBApi_1_1EClient.html#aad87a15294377608e59aec1d87420594
    :param steamNum:
    :param durationStr: the amount of time for which the data needs to be retrieved:
                        " S (seconds) - " D (days)
                        " W (weeks) - " M (months)
                        " Y (years)
    :param host:
    :param port:
    :param clientId:
    :return:
    """
    ib = ibsy.IB()
    with ib.connect(host, port, clientId=clientId):
        start_time = time.time()
        for counter in range(steamNum):
            for i in stock_symbol_list:
                print("Getting " + i + " real time data...")
                contract = ibsy.Stock(i, 'SMART', 'USD', primaryExchange='NASDAQ')
                bars = ib.reqHistoricalData(contract, endDateTime='', durationStr=durationStr,
                                            barSizeSetting='1 min', whatToShow='MIDPOINT', useRTH=True)

                # convert to pandas dataframe:
                df = ibsy.util.df(bars)

                query = "INSERT IGNORE INTO IB_TODAY_" + i + " VALUES (%s, '" + i + "', %s, %s, %s, %s, %s, %s);"
                for index, row in df.iterrows():
                    insert_data = (str(row.date.strftime("%Y%m%d")),
                                   str(row.date.strftime("%H:%M:%S")),
                                   str(row.open),
                                   str(row.high),
                                   str(row.low),
                                   str(row.close),
                                   str(row.volume))
                    try:
                        mydb = DBConnection().db_mysql_connector()
                        mycursor = mydb.cursor()
                        mycursor.execute(query, insert_data)
                        mydb.commit()
                    except Exception as e:
                        print(e)
                        return None
                    finally:
                        mycursor.close()
                        mydb.close()
            print("End of getting real time data...")
        end_time = time.time()
        sleep_time = time.sleep(max(0, 60 - (end_time - start_time)))
        print("Sleep time: ", sleep_time)

if __name__ == '__main__':
    steamNum = 2
    durationStr = '120 S'
    # delete_table_data(stock_symbol_list)
    print(stock_symbol_list)
    get_real_time_data(steamNum, durationStr, stock_symbol_list)