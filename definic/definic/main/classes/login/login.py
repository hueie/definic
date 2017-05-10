from ..commonmain.dbhandler import DBHandler
import pandas as pd

class Login:
    def __init__(self):
        self.dbhandler = DBHandler()
        pass
    
    def selectLoginData(self, pUser_id, pUser_pwd):
        sql = "SELECT count(*) AS cnt FROM possys_user WHERE user_id='" + pUser_id + "' and user_pwd ='" + pUser_pwd+"'"
                
        return pd.read_sql(sql, self.dbhandler.conn)
