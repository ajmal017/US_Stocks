from DBConnection import DBConnection
import time
import numpy as np
import pandas as pd

class StockMethod:
    def __init__(self, symbol="", freq=""):
        self.symbol = symbol
        self.freq = freq

    def query_stock_symbols(self):
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


    def query_data_by_table_name(self, table_name, start_date="", end_date="", within_RTH=True):
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
        if len(condition_list) >= 2: # non-empty list
            condition_string = " WHERE " + (" AND ".join(condition_list))
            print(condition_string)
        elif len(condition_list) == 1:
            condition_string = " WHERE " + condition_list[0]
            print(condition_string)

        query = "SELECT * FROM " + table_name + condition_string + ";"

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

    def query_by_conditions(self, table_name, condition_string):
        """Get anything you want"""
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

    def query_by_symbol_and_freq(self, start = "", end = ""):
        """Get resampled data by symbol and freq within the start and the end time

        Parameters:
            start (string): date or datetime
            end (string): date or datetime

        Return:
            df: stock data (DateTime, Ticker, Open, High, Low, Close, Volume, TotalTrades)
        """
        table_name = (self.symbol + '_' + self.freq).lower()

        condition_string = ""
        if bool(start) and bool(end): # if start and end are non-empty
            condition_string = " WHERE DateTime >= '" + start + "' AND DateTime <= '" + end + "'"
        elif bool(start): # if only start are non-empty
            condition_string = " WHERE DateTime >= '" + start + "'"
        elif bool(end): # if start and end are non-empty
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
        if len(self.symbol) > 0:
            query = "SELECT max(Date) FROM " + self.symbol.lower() + ";"
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

    def get_latest_date_freq(self):
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