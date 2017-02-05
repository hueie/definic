# -*- coding: utf-8 -*-
import sys,os
'''
sys.path.append((os.path.sep).join( os.getcwd().split(os.path.sep)[0:-1]))
from common.dbhandler import DBHandler
'''

from ..common.dbhandler import DBHandler
from ..common.commonutil import CommonUtil
import datetime
import pandas as pd
import pandas_datareader.data as webdata

import quandl 
import wbdata

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
	
	def	selectYahooPeriodDataFromDB(self):
		sql = "SELECT stock_code, min(date) as start, max(date) as end, lst_reg_dt FROM definic.data_stock_usa group by stock_code"
		return pd.read_sql(sql, self.dbhandler.conn)

	def selectYahooDataFromDB(self, stockcode ):
		sql = "SELECT stock_code, date, lst_reg_dt, open, high, low, close, volume, adj_close FROM definic.data_stock_usa where stock_code ='%s' " % (stockcode)
		return pd.read_sql(sql, self.dbhandler.conn)
	
	def selectAllYahooDataFromDB(self ):
		sql = "SELECT stock_code, date, lst_reg_dt, open, high, low, close, volume, adj_close FROM definic.data_stock_usa"
		return pd.read_sql(sql, self.dbhandler.conn)
		

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

	
	def	getQuandlDataFromWeb(self, pStockCode, pStart, pEnd ):
		#https://www.quandl.com/data/EIA-U-S-Energy-Information-Administration-Data/documentation/documentation
		self.stockcode = pStockCode
		self.data =	quandl.get(self.stockcode, returns="numpy")
		#mydata = quandl.get("FRED/GDP")
		#mydata = quandl.get("EIA/PET_RWTC_D")
		#mydata = quandl.get("EIA/PET_RWTC_D", returns="numpy")
		#mydata = quandl.get(["NSE/OIL.1", "WIKI/AAPL.4"])
		#mydata = quandl.get("WIKI/AAPL", rows=5)
		#print(mydata)
		self.data['Date'] = self.data.index.values
		return self.data
			
	
	def	getWBDataFromWeb(self, pStockCode, pStart, pEnd ):
		#https://wbdata.readthedocs.io/en/latest/
		wbdata.get_source()
		wbdata.get_indicator(source=1)
		wbdata.search_countries("united")
		date = (datetime.datetime(2010, 1, 1), datetime.datetime(2011, 1, 1))
		self.data = wbdata.get_data("IC.BUS.EASE.XQ", country=("USA", "GBR"), data_date=date)
		for row in self.data:
			print(row['country']['id'] , row)
			#indicators = {"IC.BUS.EASE.XQ": "doing_business", "NY.GDP.PCAP.PP.KD": "gdppc"}
			#df = wbdata.get_dataframe(indicators, country=countries, convert_date=True)
			#df.describe()   		
			
		return self.data
	
	
'''	
	def	selectAllYahooDataFromDB(self ):
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
	
		
'''
if __name__ == "__main__":
	datawarehouse = DataWareHouse()
	datawarehouse.getYahooDataFromWeb("GOOG", "03/03/2016", "03/04/2016")
	datawarehouse.updateYahooData()
'''