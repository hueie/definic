# -*- coding: utf-8 -*-
import MySQLdb as mdb
import sqlite3 as sq3

class DBHandler():
    def __init__(self):
        try:
            self.dbtype = "mysql"
            self.conn = mdb.connect('192.168.1.129', 'alpha', '1234', 'definic', port=3306, charset='utf8')
            self.conn.autocommit(False)
            self.initdb()
        except Exception as error:
            print(">>> Unexpected error in Connection to Mysql : ", error)
            try:
                self.dbtype = "sqlite3"
                self.conn = sq3.connect("definic/possys.sqlite3") #, isolation_level=exclusive
            except Exception as error:
                print(">>> Unexpected error in Connection to Sqlite3 : ", error)
                
    def initdb(self):
        if(self.dbtype == "mysql"):
            
            sql = "CREATE TABLE possys_user ( user_id VARCHAR(20), user_pwd VARCHAR(20), user_date VARCHAR(20) )"
            self.execSql(sql)
            
            sql = "CREATE TABLE possys_item ( item_id VARCHAR(20), barcode INTEGER, item_name VARCHAR(20), cur_price INTEGER, cur_place VARCHAR(20), cur_quantity INTEGER, item_date VARCHAR(20), itemcategory_id INTEGER )"
            self.execSql(sql)
            sql = "CREATE TABLE possys_transaction ( tr_id VARCHAR(20), pos_num INTEGER, item_id VARCHAR(20), tr_price INTEGER, tr_quantity INTEGER, tr_date VARCHAR(20) )"
            self.execSql(sql)
            sql = "CREATE TABLE possys_bill ( tr_id VARCHAR(20), total_cost INTEGER , tax INTEGER , card INTEGER , bill_date VARCHAR(20) )"
            self.execSql(sql)
            sql = "CREATE TABLE possys_inventory ( inv_id INTEGER, in_out INTEGER , from_to VARCHAR(20), inv_item_id VARCHAR(20), inv_expense INTEGER , inv_quantity INTEGER , inv_date VARCHAR(20) )"
            self.execSql(sql)
            sql = "CREATE TABLE possys_itemcategory ( itemcategory_id INTEGER , itemcategory_name VARCHAR(20), itemcategory_content VARCHAR(20), itemcategory_date VARCHAR(20) )"
            self.execSql(sql)
     
            pass
        elif(self.dbtype == "sqlite3"):
            #sql = "DROP TABLE data_stock_usa" ; self.execSql(sql)
            sql = "CREATE TABLE 'possys_item' ( 'item_id' TEXT, 'barcode' INTEGER, 'item_name' TEXT, 'cur_price' INTEGER, 'cur_place' TEXT, 'cur_quantity' INTEGER, 'item_date' TEXT )"
            self.execSql(sql)
            sql = "CREATE TABLE 'possys_transaction' ( 'tr_id' TEXT, 'pos_num' INTEGER, 'item_id' TEXT, 'tr_price' INTEGER, 'tr_quantity' INTEGER, 'tr_date' TEXT )"
            self.execSql(sql)
            sql = "CREATE TABLE 'possys_bill' ( 'tr_id' TEXT, 'total_cost' INTEGER, 'tax' INTEGER, 'card' INTEGER, 'bill_date' TEXT )"
            self.execSql(sql)
            sql = "CREATE TABLE 'possys_inventory' ( 'in_out' INTEGER, 'from_to' TEXT, 'item_id' TEXT, 'expense' INTEGER, 'quantity' INTEGER, 'date' TEXT )"
            self.execSql(sql)
            
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