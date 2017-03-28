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

class Item:
	def	__init__(self, pdata=None):
		self.dbhandler = DBHandler()
	
	def selectItemFromDB(self, item_name=None):
		if(self.dbhandler.dbtype == "mysql"):
			sql = "SELECT item_id, item_name, barcode, cur_price, cur_quantity, cur_place, item_date FROM possys_item"
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "SELECT item_id, item_name, barcode, cur_price, cur_quantity, cur_place, item_date FROM possys_item"
		else:
			pass
		return pd.read_sql(sql, self.dbhandler.conn)
	
	def selectMaxItem_idFromDB(self):
		if(self.dbhandler.dbtype == "mysql"):
			sql = "SELECT MAX(item_id) FROM possys_item"
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "SELECT MAX(item_id) FROM possys_item"
		else:
			pass
		return pd.read_sql(sql, self.dbhandler.conn)

	def insertItemToDB(self, pItem_id, pItem_name, pBarcode, pCur_price, pCur_quantity, pCur_place, pItem_date):
		commonutil = CommonUtil() 
		if(self.dbhandler.dbtype == "mysql"):
			sql = "INSERT INTO possys_item('item_id','item_name','barcode','cur_price','cur_quantity','cur_place','item_date') "
			sql += " VALUES ( "
			sql += "'%s'" %  (pItem_id)
			sql += ",'%s'" % (pItem_name)
			sql += ",%s" % (pBarcode)
			sql += ",%s" % (pCur_price)
			sql += ",%s" % (pCur_quantity)
			sql += ",'%s'" % (pCur_place)
			sql += ",'%s %s'" %( commonutil.getDate() , commonutil.getTime() )
			sql += " )"
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "INSERT INTO possys_item(item_id,item_name,barcode,cur_price,cur_quantity,cur_place,item_date) "
			sql += " VALUES ( "
			sql += "'%s'" %  (pItem_id)
			sql += ",'%s'" % (pItem_name)
			sql += ",%s" % (pBarcode)
			sql += ",%s" % (pCur_price)
			sql += ",%s" % (pCur_quantity)
			sql += ",'%s'" % (pCur_place)
			sql += ",'%s %s'" %( commonutil.getDate() , commonutil.getTime() )
			sql += " )"
		else:
			pass
		
		print(sql)
		self.dbhandler.execSql(sql)
		pass
	
	def updateItemToDB(self, pItem_id, pItem_name, pBarcode, pCur_price, pCur_quantity, pCur_place, pItem_date):
		if(self.dbhandler.dbtype == "mysql"):
			sql = "UPDATE possys_item SET "
			sql += "  item_name = '%s'" % (pItem_name)
			sql += ", barcode = %s" % (pBarcode)
			sql += ", cur_price = %s" % (pCur_price)
			sql += ", cur_quantity = %s" % (pCur_quantity)
			sql += ", cur_place = '%s'" % (pCur_place)
			sql += ", item_date = '%s'" %( pItem_date )
			sql += "  WHERE item_id = '%s'" %  (pItem_id)
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "UPDATE possys_item SET "
			sql += "  item_name = '%s'" % (pItem_name)
			sql += ", barcode = %s" % (pBarcode)
			sql += ", cur_price = %s" % (pCur_price)
			sql += ", cur_quantity = %s" % (pCur_quantity)
			sql += ", cur_place = '%s'" % (pCur_place)
			sql += ", item_date = '%s'" % (pItem_date)
			sql += "  WHERE item_id = '%s'" %  (pItem_id)
		else:
			pass
		
		print(sql)
		self.dbhandler.execSql(sql)
		pass
		
	def deleteItemToDB(self, pItem_id):
		if(self.dbhandler.dbtype == "mysql"):
			sql = "DELETE FROM possys_item WHERE item_id = %s" %  (pItem_id)
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "DELETE FROM possys_item WHERE item_id = %s" %  (pItem_id)
		else:
			pass
		
		print(sql)
		self.dbhandler.execSql(sql)
		pass
