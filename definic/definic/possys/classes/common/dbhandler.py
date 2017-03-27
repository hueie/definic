# -*- coding: utf-8 -*-
import MySQLdb as mdb
import sqlite3 as sq3

class DBHandler():
    def __init__(self):
        try:
            self.dbtype = "mysql"
            self.conn = mdb.connect('127.0.0.1', 'root', '1234', 'definic', port=3306, charset='utf8')
            self.conn.autocommit(False)
            self.initdb()
        except Exception as error:
            print(">>> Unexpected error in Connection to Mysql : ", error)
            try:
                self.dbtype = "sqlite3"
                self.conn = sq3.connect("definic/definic.sqlite3") #, isolation_level=exclusive
            except Exception as error:
                print(">>> Unexpected error in Connection to Sqlite3 : ", error)
                
    def initdb(self):
        if(self.dbtype == "mysql"):
            pass
        elif(self.dbtype == "sqlite3"):
            #sql = "DROP TABLE data_stock_usa" ; self.execSql(sql)
            #sql = "CREATE TABLE data_stock_usa (stock_code TEXT NOT NULL , date TEXT NOT NULL , lst_reg_dt TEXT, open INTEGER, high INTEGER, low INTEGER, close INTEGER, volume INTEGER, adj_close INTEGER, PRIMARY KEY(stock_code, date))"
            #self.execSql(sql)
            pass
        pass
        
    def execSql(self,sql,db_commit=True):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            
            if db_commit:
                self.conn.commit()
            return cursor

        except Exception as error:
            print(">>> Unexpected error in Execution SQL : ", error)
            print("\t%s" % (sql))
            self.conn.rollback()
            cursor.close()
            #self.conn.close()
            #raise

'''  
if __name__ == "__main__":
    dbhandler = DBHandler()
    
    sql = "SELECT min(date) as start, max(date) as end,  stock_code FROM data_stock_usa group by stock_code"
        
    for rows in dbhandler.execSql(sql, False):
        print(rows['start']) #(x)
    
    for rows in dbhandler.execSql("SELECT 'HI' ", False):
        print(rows[0])
    
    #for rows in dbhandler.execSql("SELECT 'HI' FROM DUAL", False):
    #   print(rows[0])
       
     
        

    cursor = dbhandler.execSql("SELECT 'HI' FROM DUAL", False)
    if cursor is not None :
        print("Rows produced by statement '{}':".format(cursor.statement))
        print(cursor.fetchall())
    else:
        print("Number of rows affected by statement '{}': {}".format(cursor.statement, cursor.rowcount))
    '''