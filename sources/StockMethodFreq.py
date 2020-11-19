from AbstractStockMethod import AbstractStockMethod
from DBConnection import DBConnection

import pandas as pd

class StockMethodFreq(AbstractStockMethod):
    """Related to stock freq tables i.e. table name like aapl_1h, etc"""
    def __init__(self, symbol="", freq=""):
        self.symbol = symbol.lower()
        self.freq = freq.lower()

    def query_by_symbol(self, start = "", end = ""):
        """Get resampled data by symbol and freq within the start and the end time

        Parameters:
            start (string): date or datetime
            end (string): date or datetime

        Return:
            df: stock data (DateTime, Ticker, Open, High, Low, Close, Volume, TotalTrades)
        """
        table_name = (self.symbol + '_' + self.freq).lower()

        condition_string = ""
        if bool(start) and bool(end):  # if start and end are non-empty
            condition_string = " WHERE DateTime >= '" + start + "' AND DateTime <= '" + end + "'"
        elif bool(start):  # if only start are non-empty
            condition_string = " WHERE DateTime >= '" + start + "'"
        elif bool(end):  # if start and end are non-empty
            condition_string = " WHERE DateTime <= '" + end + "'"

        query = "SELECT * FROM " + table_name + condition_string + ";"

        try:
            db_con = DBConnection().db_sqlalchemy()
            result = pd.read_sql(query, db_con)
            return result
        except Exception as e:
            print(e)
            return None
        finally:
            db_con.close()

    def get_latest_date(self):
        """
        Get the latest date in table

        Return:
            Str: the latest date
        """
        if len(self.symbol) > 0 and len(self.freq) > 0:
            query = "SELECT max(Date(DateTime)) FROM " + (self.symbol + '_' + self.freq).lower() + ";"
        else:
            return None

        try:
            mydb = DBConnection().db_mysql_connector()
            mycursor = mydb.cursor()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            return [x[0] for x in myresult][0]
        except Exception as e:
            print(e)
            return None
        finally:
            mycursor.close()
            mydb.close()