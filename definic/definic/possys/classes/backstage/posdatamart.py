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

class Posdatamart:
    def    __init__(self, pdata=None):
        self.dbhandler = DBHandler()
    
    def selectPosdatamartFromDB(self, posdatamart_id=None):
        if(self.dbhandler.dbtype == "mysql"):
            sql = "SELECT posdatamart_id, posdatamart_atch_name FROM possys_posdatamart "
            if posdatamart_id != None:
                sql += " WHERE posdatamart_id = %s" % (posdatamart_id)
            else:
                pass
        return pd.read_sql(sql, self.dbhandler.conn)
    
    def insertPosdatamartToDB(self, pPosdatamart_id, posdatamart_atch_name):
        if(self.dbhandler.dbtype == "mysql"):
            sql = "INSERT INTO possys_posdatamart(posdatamart_id, posdatamart_atch_name) "
            sql += " VALUES ( "
            sql += "'%s'" %  (pPosdatamart_id)
            sql += ",'%s'" % (posdatamart_atch_name)
            sql += " )"
        
        print(sql)
        self.dbhandler.execSql(sql)
        pass
    
