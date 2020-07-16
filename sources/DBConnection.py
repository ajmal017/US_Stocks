import mysql.connector
from sqlalchemy import create_engine

class DBConnection:
    def __init__(self, host="127.0.0.1", user="root", pw="Mydb!246810", db="usstockdata"):
        self.host = host
        self.user = user
        self.pw = pw
        self.db = db

    def db_mysql_connector(self):
        mydb = mysql.connector.connect(
            host=self.host,  # "localhost"
            user=self.user,  # "root"
            password=self.pw,  # "Mydb!246810"
            database=self.db  # "usstockdata"
        )
        return (mydb)

    def db_sqlalchemy(self):
        sqlEngine = create_engine('mysql+pymysql://' + self.user + ':' + self.pw + '@' + self.host + '/' + self.db)
        mydb = sqlEngine.connect()
        return mydb