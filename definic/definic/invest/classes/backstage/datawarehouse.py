# -*- coding: utf-8 -*-

import datetime
import pandas as pd
import pandas.io.data as webdata
from ..common.dbhandler import DBHandler
from ..common.commonutil import CommonUtil

class DataWareHouse:
	def	__init__(self, pdata=None):
		self.dbhandler = DBHandler()
		self.stockcode = ""
		if pdata is	not None:
			self.data =	pdata
		
	def	getYahooDataFromWeb(self, pStockCode, pStart, pEnd ):
		self.stockcode = pStockCode
		self.data =	webdata.DataReader(pStockCode, data_source='yahoo',	start=pStart, end=pEnd)
		self.data['Date'] = self.data.index.values
		return self.data
	
	def updateYahooData(self, pstockcode=None, data=None):
		if pstockcode is None:
			pstockcode = self.stockcode
		if data is None:
			data = self.data
		try:
			for row_index in range(data.shape[0]):
				sql = self.insertYahooData(pstockcode,data,row_index)
				self.dbhandler.execSql(sql)
		except Exception as error:
			print(error)
		print("finish")

	def insertYahooData(self,stockcode,data,row_index):
		commonutil = CommonUtil() 
		
		sql = "insert into data_stock_usa set "
		sql += "stock_code='%s'" %  (stockcode)
		sql += ",date='%s'" % (data['Date'][row_index])
		sql += ",lst_reg_dt='%s %s'" %( commonutil.getDate() , commonutil.getTime() )
		sql += ",open=%s" % (data['Open'][row_index])
		sql += ",high=%s" % (data['High'][row_index])
		sql += ",low=%s" % (data['Low'][row_index])
		sql += ",close=%s" % (data['Close'][row_index])
		sql += ",adj_close=%s" % (data['Adj Close'][row_index])
		sql += ",volume=%s" % (data['Volume'][row_index])

		sql += " ON DUPLICATE KEY UPDATE "

		sql += "stock_code='%s'" %  (stockcode)
		sql += ",date='%s'" % (data['Date'][row_index])
		sql += ",lst_reg_dt='%s %s'" %( commonutil.getDate() , commonutil.getTime() )
		sql += ",open=%s" % (data['Open'][row_index])
		sql += ",high=%s" % (data['High'][row_index])
		sql += ",low=%s" % (data['Low'][row_index])
		sql += ",close=%s" % (data['Close'][row_index])
		sql += ",adj_close=%s" % (data['Adj Close'][row_index])
		sql += ",volume=%s" % (data['Volume'][row_index])
		print(sql)
		return sql	
	
	def	selectYahooDataFromDB(self ):
		sql = "SELECT stock_code, min(date) as start, max(date) as end, lst_reg_dt FROM definic.data_stock_usa group by stock_code"
		try:
			print(sql)
			cursor = self.dbhandler.execSql(sql)
		except Exception as error:
			print(error)
		
		result = cursor.fetchall()
		fieldlist = ['stock_code', 'start', 'end', 'lst_reg_dt']
		return map((lambda x: dict(zip(fieldlist, x))), result)
			
'''
if __name__ == "__main__":
	datawarehouse = DataWareHouse()
	datawarehouse.getYahooDataFromWeb("GOOG", "03/03/2016", "03/04/2016")
	datawarehouse.updateYahooData()
'''