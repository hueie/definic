# -*- coding: utf-8 -*-
from ..common.dbhandler import DBHandler

class LinearGraph:
    def __init__(self ):
        self.dbhandler = DBHandler()
            
    def selectYahooDataFromDB(self, stockcode ):
        sql = "SELECT stock_code, date, lst_reg_dt, open, high, low, close, volume, adj_close FROM definic.data_stock_usa where stock_code ='%s'" % (stockcode)
        try:
            print(sql)
            cursor = self.dbhandler.execSql(sql)
        except Exception as error:
            print(error)
        
        result = cursor.fetchall()
        fieldlist = ['stock_code', 'date', 'lst_reg_dt', 'open', 'high', 'low', 'close', 'volume', 'adj_close']
        return map((lambda x: dict(zip(fieldlist, x))), result)
    
    def selectAllStockCodeFromDB(self ):
        sql = "SELECT stock_code FROM definic.data_stock_usa GROUP BY stock_code"
        try:
            print(sql)
            cursor = self.dbhandler.execSql(sql)
        except Exception as error:
            print(error)
        
        result = cursor.fetchall()
        fieldlist = ['stock_code']
        return map((lambda x: dict(zip(fieldlist, x))), result)

    def selectTopStockCodeFromDB(self ):
        sql = "SELECT stock_code FROM definic.data_stock_usa GROUP BY stock_code LIMIT 1"
        try:
            print(sql)
            cursor = self.dbhandler.execSql(sql)
        except Exception as error:
            print(error)
        
        result = cursor.fetchall()
        fieldlist = ['stock_code']
        return map((lambda x: dict(zip(fieldlist, x))), result)
