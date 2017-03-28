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

class DataWareHouse:
	def	__init__(self, pdata=None):
		self.dbhandler = DBHandler()
		if pdata is	not None:
			self.data =	pdata
	
	def selectInventoryFromDB(self, item_name=None):
		if(self.dbhandler.dbtype == "mysql"):
			sql = "SELECT in_out, from_to, item_id, expense, quantity, date FROM possys_inventory"
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "SELECT in_out, from_to, item_id, expense, quantity, date FROM possys_inventory"
				
		return pd.read_sql(sql, self.dbhandler.conn)

	def insertInventoryToDB(self, pIn_out, pFrom_to, pItem_id, pExpense, pQuantity, pDate):
		commonutil = CommonUtil() 
		if(self.dbhandler.dbtype == "mysql"):
			sql = "INSERT INTO possys_inventory('in_out','from_to','item_id','expense','quantity','date') "
			sql += " VALUES ( "
			sql += "%s" %  (pIn_out)
			sql += ",'%s'" % (pFrom_to)
			sql += ",'%s'" % (pItem_id)
			sql += ",%s" % (pExpense)
			sql += ",%s" % (pQuantity)
			sql += ",'%s %s'" %( commonutil.getDate() , commonutil.getTime() )
			sql += " )"
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "INSERT INTO possys_inventory('in_out','from_to','item_id','expense','quantity','date') "
			sql += " VALUES ( "
			sql += "%s" %  (pIn_out)
			sql += ",'%s'" % (pFrom_to)
			sql += ",'%s'" % (pItem_id)
			sql += ",%s" % (pExpense)
			sql += ",%s" % (pQuantity)
			sql += ",'%s %s'" %( commonutil.getDate() , commonutil.getTime() )
			sql += " )"
		else:
			pass
		
		print(sql)
		self.dbhandler.execSql(sql)
		pass
		
	
	def updateInventoryToDB(self,pIn_out,pFrom_to,pItem_id,pExpense,pQuantity,pDate):
		commonutil = CommonUtil() 
		if(self.dbhandler.dbtype == "mysql"):
			sql = " UPDATE possys_inventory SET "
			sql += "in_out=%s" %  (pIn_out)
			sql += ",from_to='%s'" % (pFrom_to)
			sql += ",item_id='%s'" % (pItem_id)
			sql += ",expense=%s" % (pExpense)
			sql += ",quantity=%s" % (pQuantity)
			sql += " WHERE date LIKE '%s' " % (pDate)
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "UPDATE possys_inventory SET "
			sql += "'in_out' = %s" %  (pIn_out)
			sql += ",'from_to' = '%s'" % (pFrom_to)
			sql += ",'item_id' = '%s'" % (pItem_id)
			sql += ",'expense' = %s" % (pExpense)
			sql += ",'quantity' = %s" % (pQuantity)
			sql += " WHERE date LIKE '%s' " % (pDate)
		else:
			pass
		
		self.dbhandler.execSql(sql)
		pass
