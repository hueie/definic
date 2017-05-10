from ..common.dbhandler import DBHandler
from ..common.commonutil import CommonUtil

import datetime
import pandas as pd

class Login:
    def    __init__(self):
        self.dbhandler = DBHandler()
    
    def selectLoginData(self, pUser_id, pUser_pwd):
        if(self.dbhandler.dbtype == "mysql"):
            sql = "SELECT count(*) FROM possys_user WHERE user_id='" + pUser_id + "' and user_pwd ='" + pUser_pwd+"'";
                
        return pd.read_sql(sql, self.dbhandler.conn)
