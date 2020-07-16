import mysql.connector
import os
import zipfile

from DBConnection import DBConnection

# stock_symbol_list = [x[:-4] for x in os.listdir('NDX100_data/2020/20200622/20200622')]
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

def sql_load_data(stock_symbol_list, data_location):
    directory = os.getcwd().replace('\\', '/')
    sql_insert_table_list = []
    for stock_sumbol in stock_symbol_list:
        sql_insert_table_list.append("LOAD DATA INFILE '" +
                                     directory + "/" + data_location + "/" + stock_sumbol + ".csv' IGNORE INTO TABLE " +
                                     stock_sumbol + " FIELDS TERMINATED BY ',' IGNORE 1 LINES;")
    return (sql_insert_table_list)


def db_insert_latest_data(data_dir, zip_data_dir):
    """unzip the data from "zip_data_dir" to "data_dir" and then create "LOAD DATA" sql for each stock"""
    try:
        mydb = DBConnection().db_mysql_connector()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(Date) FROM AAPL;")  # get the latest date in db
        myresult = mycursor.fetchall()
        db_latest_date = myresult[0][0].strftime("%Y%m%d")
    except Exception as e:
        print(e)
        return None
    finally:
        mycursor.close()
        mydb.close()

    years = [year for year in os.listdir(data_dir) if int(year) >= myresult[0][0].year]
    for year in years:
        yyyymmdds = os.listdir(zip_data_dir + '/' + year)
        # get data that is not in db
        filenames = [yyyymmdd for yyyymmdd in yyyymmdds if int(yyyymmdd[:-4]) > int(db_latest_date)]
        if not filenames:
            print("DB is already the most updated.")
        for filename in filenames:
            zip_location = zip_data_dir + '/' + year + '/' + filename
            unzip_location = data_dir + '/' + year + '/' + filename[:-4]

            print('zip location: ' + zip_location)
            print('unzip location: ' + unzip_location)

            if not os.path.exists(unzip_location):
                with zipfile.ZipFile(zip_location, 'r') as zip_ref:
                    zip_ref.extractall(unzip_location)
            else:
                print("Zip exists.")

            # export .sql files
            sql_export_dir = 'SQL/' + filename[:-4] + '_sql_insert_table.sql'
            with open(sql_export_dir, 'w') as f:
                print("Export Dir: " + sql_export_dir)
                for sql_insert_table in sql_load_data(stock_symbol_list, unzip_location + '/' + filename[:-4]):
                    f.write("%s\n" % sql_insert_table)

if __name__ == '__main__':
    # step 1: use aws command to update zip file

    # step 2: unzip the data from "zip_data_dir" to "data_dir"
    # step 3: create "LOAD DATA" sql for each stock
    unzip_data_dir = 'data/NDX100_data'
    zip_data_dir = 'data/NDX100_zip_data'
    db_insert_latest_data(data_dir=unzip_data_dir, zip_data_dir=zip_data_dir)

    # step 4: check integrity of stock symbols
    latest_folder = str(max([int(x[:-4]) for x in os.listdir(zip_data_dir + '/2020/')]))
    latest_stock_symbol_list = [x[:-4] for x in os.listdir(unzip_data_dir + '/2020/' + latest_folder + '/' + latest_folder + '/')]
    if latest_stock_symbol_list == stock_symbol_list:
        print("Stock symbols are same as 20200622. No further action should be made.")
    else:
        print("Stock symbols are not the same as 20200622. Further action should be made.")

    # step 5: run the .sql file in MySQL Workbench