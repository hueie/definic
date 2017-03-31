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

class Transaction:
	def	__init__(self, pdata=None):
		self.dbhandler = DBHandler()
	
	def selectTransactionFromDB(self, item_name=None):
		if(self.dbhandler.dbtype == "mysql"):
			sql = "SELECT tr_id, pos_num, item_id, tr_price, tr_quantity, tr_date FROM possys_transaction"
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "SELECT tr_id, pos_num, item_id, tr_price, tr_quantity, tr_date FROM possys_transaction"
		else:
			pass
		return pd.read_sql(sql, self.dbhandler.conn)

	def selectMaxTransaction_idFromDB(self):
		if(self.dbhandler.dbtype == "mysql"):
			sql = "SELECT MAX(tr_id) FROM possys_transaction"
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "SELECT MAX(tr_id) FROM possys_transaction"
		else:
			pass
		return pd.read_sql(sql, self.dbhandler.conn)

	def insertTransactionToDB(self, pTr_id, pPos_num, pItem_id, pTr_price, pTr_quantity, pTr_Date):
		commonutil = CommonUtil() 
		if(self.dbhandler.dbtype == "mysql"):
			sql = "INSERT INTO possys_transaction('tr_id','pos_num','item_id','tr_price','tr_quantity','tr_date') "
			sql += " VALUES ( "
			sql += "'%s'" %  (pTr_id)
			sql += ",%s" % (pPos_num)
			sql += ",'%s'" % (pItem_id)
			sql += ",%s" % (pTr_price)
			sql += ",%s" % (pTr_quantity)
			sql += ",'%s %s'" %( commonutil.getDate() , commonutil.getTime() )
			sql += " )"
		elif(self.dbhandler.dbtype == "sqlite3"):
			sql = "INSERT INTO possys_transaction('tr_id','pos_num','item_id','tr_price','tr_quantity','tr_date') "
			sql += " VALUES ( "
			sql += "'%s'" %  (pTr_id)
			sql += ",%s" % (pPos_num)
			sql += ",'%s'" % (pItem_id)
			sql += ",%s" % (pTr_price)
			sql += ",%s" % (pTr_quantity)
			sql += ",'%s %s'" %( commonutil.getDate() , commonutil.getTime() )
			sql += " )"
		else:
			pass
		
		print(sql)
		self.dbhandler.execSql(sql)
		pass
		
	
