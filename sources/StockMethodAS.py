from AbstractStockMethod import AbstractStockMethod
from DBConnection import DBConnection

import pandas as pd

class StockMethodAS(AbstractStockMethod):
    """Related to algoseek tables"""
    def __init__(self, symbol=''):
        self.symbol = symbol.lower()

    def query_by_symbol(self, start_date="", end_date="", within_RTH=True):
        """
        Get algoseek original data

        Parameters:
            within_RTH (boolean): True if within regular trading hour
            start_date (string): start date
            end_date (string): end date

        Return:
            df: stock data
        """
        condition_list = []
        if within_RTH:
            trading_hour_condition = "TimeBarStart >= '09:30:00' AND TimeBarStart < '16:00:00'"
            condition_list.append(trading_hour_condition)
        else:
            trading_hour_condition = ""

        if not start_date:
            start_date_condition = ""
        else:
            start_date_condition = "Date >= '" + start_date + "'"
            condition_list.append(start_date_condition)

        if not end_date:
            end_date_condition = ""
        else:
            end_date_condition = "Date <= '" + end_date + "'"
            condition_list.append(end_date_condition)

        condition_string = ""
        if len(condition_list) >= 2:  # non-empty list
            condition_string = " WHERE " + (" AND ".join(condition_list))
            print(condition_string)
        elif len(condition_list) == 1:
            condition_string = " WHERE " + condition_list[0]
            print(condition_string)

        query = "SELECT * FROM " + self.symbol.lower() + condition_string + ";"

        print(query)
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
        if len(self.symbol) > 0:
            query = "SELECT max(Date) FROM " + self.symbol.lower() + ";"
        else:
            return None

        try:
            mydb = DBConnection().db_mysql_connector()
            mycursor = mydb.cursor()
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            return [x[0] for x in myresult][0].strftime("%Y-%m-%d")
        except Exception as e:
            print(e)
            return None
        finally:
            mycursor.close()
            mydb.close()
