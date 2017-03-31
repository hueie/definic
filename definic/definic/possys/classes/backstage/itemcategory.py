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

class Itemcategory:
	def	__init__(self, pdata=None):
		self.dbhandler = DBHandler()
	
	def selectItemcategoryFromDB(self, itemcategory_name=None):
		if(self.dbhandler.dbtype == "mysql"):
			sql = "SELECT itemcategory_id, itemcategory_name, itemcategory_content, itemcategory_date FROM possys_itemcategory"
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "SELECT itemcategory_id, itemcategory_name, itemcategory_content, itemcategory_date FROM possys_itemcategory"
		else:
			pass
		return pd.read_sql(sql, self.dbhandler.conn)
	
	def selectMaxItemcategory_idFromDB(self):
		if(self.dbhandler.dbtype == "mysql"):
			sql = "SELECT MAX(itemcategory_id) max_itemcategory_id FROM possys_itemcategory"
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "SELECT MAX(itemcategory_id) max_itemcategory_id  FROM possys_itemcategory"
		else:
			pass
		return pd.read_sql(sql, self.dbhandler.conn)

	def insertItemcategoryToDB(self, pItemcategory_id, pItemcategory_name, itemcategory_content, pItemcategory_date):
		commonutil = CommonUtil() 
		if(self.dbhandler.dbtype == "mysql"):
			sql = "INSERT INTO possys_itemcategory(itemcategory_id, itemcategory_name, itemcategory_content, itemcategory_date) "
			sql += " VALUES ( "
			sql += "%s" %  (pItemcategory_id)
			sql += ",'%s'" % (pItemcategory_name)
			sql += ",'%s'" % (itemcategory_content)
			sql += ",'%s %s'" %( commonutil.getDate() , commonutil.getTime() )
			sql += " )"
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "INSERT INTO possys_itemcategory(itemcategory_id, itemcategory_name, itemcategory_content, itemcategory_date) "
			sql += " VALUES ( "
			sql += "%s" %  (pItemcategory_id)
			sql += ",'%s'" % (pItemcategory_name)
			sql += ",'%s'" % (itemcategory_content)
			sql += ",'%s %s'" %( commonutil.getDate() , commonutil.getTime() )
			sql += " )"
		else:
			pass
		
		print(sql)
		self.dbhandler.execSql(sql)
		pass
	
	def updateItemcategoryToDB(self, pItemcategory_id, pItemcategory_name, pItemcategory_content, pItemcategory_date):
		if(self.dbhandler.dbtype == "mysql"):
			sql = "UPDATE possys_itemcategory SET "
			sql += "  itemcategory_name = '%s'" % (pItemcategory_name)
			sql += ", itemcategory_content = '%s'" % (pItemcategory_content)
			sql += ", itemcategory_date = '%s'" %( pItemcategory_date )
			sql += "  WHERE itemcategory_id = %s" %  (pItemcategory_id)
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "UPDATE possys_itemcategory SET "
			sql += "  itemcategory_name = '%s'" % (pItemcategory_name)
			sql += ", itemcategory_content = '%s'" % (pItemcategory_content)
			sql += ", itemcategory_date = '%s'" %( pItemcategory_date )
			sql += "  WHERE itemcategory_id = %s" %  (pItemcategory_id)
		else:
			pass
		
		print(sql)
		self.dbhandler.execSql(sql)
		pass
		
	def deleteItemcategoryToDB(self, pItemcategory_id):
		if(self.dbhandler.dbtype == "mysql"):
			sql = "DELETE FROM possys_itemcategory WHERE itemcategory_id = %s" %  (pItemcategory_id)
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "DELETE FROM possys_itemcategory WHERE itemcategory_id = %s" %  (pItemcategory_id)
		else:
			pass
		
		print(sql)
		self.dbhandler.execSql(sql)
		pass
