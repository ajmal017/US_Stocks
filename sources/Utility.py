from DBConnection import DBConnection

import pandas as pd

class Utility:

    @staticmethod
    def DateTimeAsIndex(df, data_column="Date", time_column="TimeBarStart"):
        df['Date'] = df['Date'].astype(str)
        df['TimeBarStart'] = df['TimeBarStart'].astype(str).str[7:15]
        df['Date'] = pd.to_datetime(df['Date'] + ' ' + df['TimeBarStart'])
        df = df.set_index(pd.DatetimeIndex(df['Date']))
        df = df.drop(['Date', 'TimeBarStart'], axis=1)
        return df

    @staticmethod
    def as_str(s):
        if s is None:
            return ''
        return str(s)

    @staticmethod
    def query_stock_symbols():
        """
        Query the stock symbols that are active.

        Return:
            list of string: list of stock symbols that are active
        """
        try:
            mydb = DBConnection().db_mysql_connector()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT Ticker FROM active_stock WHERE IsActive = 1;")
            myresult = mycursor.fetchall()
            return [x[0] for x in myresult]
        except Exception as e:
            print(e)
            return None
        finally:
            mycursor.close()
            mydb.close()