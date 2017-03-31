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

class Inventory:
	def	__init__(self):
		self.dbhandler = DBHandler()
	
	def selectInventoryFromDB(self):
		if(self.dbhandler.dbtype == "mysql"):
			sql = "SELECT inv_id, in_out, from_to, inv_item_id, inv_expense, inv_quantity, inv_date FROM possys_inventory"
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "SELECT inv_id, in_out, from_to, inv_item_id, inv_expense, inv_quantity, inv_date FROM possys_inventory"
				
		return pd.read_sql(sql, self.dbhandler.conn)

	def selectMaxInv_idFromDB(self):
		if(self.dbhandler.dbtype == "mysql"):
			sql = "SELECT MAX(inv_id) FROM possys_inventory"
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "SELECT MAX(inv_id) FROM possys_inventory"
		else:
			pass
		return pd.read_sql(sql, self.dbhandler.conn)

	def insertInventoryToDB(self, pInv_id, pIn_out, pFrom_to, pInv_item_id, pInv_expense, pInv_quantity, pInv_date):
		commonutil = CommonUtil() 
		if(self.dbhandler.dbtype == "mysql"):
			sql = "INSERT INTO possys_inventory('in_out','from_to','inv_item_id','inv_expense','inv_quantity','inv_date') "
			sql += " VALUES ( "
			sql += "%s" %  (pIn_out)
			sql += ",'%s'" % (pFrom_to)
			sql += ",'%s'" % (pInv_item_id)
			sql += ",%s" % (pInv_expense)
			sql += ",%s" % (pInv_quantity)
			sql += ",'%s %s'" %( commonutil.getDate() , commonutil.getTime() )
			sql += " )"
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "INSERT INTO possys_inventory(inv_id, in_out, from_to, inv_item_id, inv_expense, inv_quantity, inv_date) "
			sql += " VALUES ( "
			sql += "%s" %  (pInv_id)
			sql += ",%s" %  (pIn_out)
			sql += ",'%s'" % (pFrom_to)
			sql += ",'%s'" % (pInv_item_id)
			sql += ",%s" % (pInv_expense)
			sql += ",%s" % (pInv_quantity)
			sql += ",'%s %s'" %( commonutil.getDate() , commonutil.getTime() )
			sql += " )"
		else:
			pass
		
		print(sql)
		self.dbhandler.execSql(sql)
		pass
		
	
	def updateInventoryToDB(self,pInv_id, pIn_out,pFrom_to,pInv_item_id,pInv_expense,pInv_quantity,pInv_date):
		commonutil = CommonUtil() 
		if(self.dbhandler.dbtype == "mysql"):
			sql = " UPDATE possys_inventory SET "
			sql += "in_out=%s" %  (pIn_out)
			sql += ",from_to='%s'" % (pFrom_to)
			sql += ",inv_item_id='%s'" % (pInv_item_id)
			sql += ",inv_expense=%s" % (pInv_expense)
			sql += ",inv_quantity=%s" % (pInv_quantity)
			sql += " WHERE inv_date LIKE '%s' " % (pInv_date)
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "UPDATE possys_inventory SET "
			sql += "inv_id = %s" %  (pInv_id)
			sql += ",in_out = %s" %  (pIn_out)
			sql += ",from_to = '%s'" % (pFrom_to)
			sql += ",inv_item_id = '%s'" % (pInv_item_id)
			sql += ",inv_expense = %s" % (pInv_expense)
			sql += ",inv_quantity = %s" % (pInv_quantity)
			sql += " WHERE inv_date LIKE '%s' " % (pInv_date)
		else:
			pass
		
		self.dbhandler.execSql(sql)
		pass
