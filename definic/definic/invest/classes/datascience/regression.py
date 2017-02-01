# -*- coding: utf-8 -*-
from ..common.dbhandler import DBHandler
#import sys,os
#sys.path.append((os.path.sep).join( os.getcwd().split(os.path.sep)[0:-1]))
#from common.dbhandler import DBHandler

import copy
import numpy as np
from sklearn import linear_model 
     
class Regression:
    def __init__(self ):
        self.dbhandler = DBHandler()
        self.mse = 0
        self.coef = 0
        self.score = 0
        
    def linearregression(self, data):
        print(data)
        trainToTest_Ratio = 2/3 
        train_x_arr = [] ; train_y_arr = []
        test_x_arr = [] ; test_y_arr = [] ; test_date_arr = []
        all_x_arr = [] ; all_date_arr = []
        
        tmpdata = copy.deepcopy(data)
        datalen = len(list(tmpdata))

        idx = 0
        for row in data:
            if idx < datalen*trainToTest_Ratio :
                train_x_arr.append([idx])
                train_y_arr.append( float(row['close']) )
            else :
                test_x_arr.append([idx])
                test_date_arr.append( str(row['date']) )
                test_y_arr.append( float(row['close']) )
            all_x_arr.append([idx])
            all_date_arr.append(str(row['date']))
            idx += 1
        print(train_x_arr) ; print(train_y_arr)
        print(test_x_arr) ; print(test_y_arr)
        
        data_X_train = np.array(train_x_arr) # [ val_1, val_2, ... ] multiple variables in X independent data array.
        data_y_train = np.array(train_y_arr)
        
        regr = linear_model.LinearRegression()
        regr.fit (data_X_train, data_y_train)
       
        data_X_test = np.array(test_x_arr)
        data_y_predicted = regr.predict(data_X_test) #Predicted by model
       
        data_y_test = np.array(test_y_arr)
       
        # The coefficients
        self.coef = regr.coef_
        print('Coefficients: \n', regr.coef_)
        # The mean squared error
        self.mse = np.mean((data_y_predicted - data_y_test) ** 2)
        print("Mean squared error: %.2f" % np.mean((data_y_predicted - data_y_test) ** 2))
        # Explained variance score: 1 is perfect prediction
        self.score = regr.score(data_X_test, data_y_test)
        print('Variance score: %.2f' % regr.score(data_X_test, data_y_test))

        data_X_result = test_date_arr 
        data_y_result = data_y_predicted
        #Train and Test End

        #In order to show Linear Regression Curve
        data_X_result = all_date_arr 
        data_y_result = regr.predict( np.array(all_x_arr) ) #Predicted by model
        
        #Result Part        
        result = []
        for idx in range(len(data_X_result)):
            tmp = []
            tmp.append(data_X_result[idx])
            tmp.append(data_y_result[idx])
            result.append( tuple( tmp ) )
        
        result = tuple(result)
        
        fieldlist = ['date', 'predicted_data']
        return map((lambda x: dict(zip(fieldlist, x))), result)
        
    def selectYahooDataFromDB(self, stockcode ):
        sql = "SELECT stock_code, date, lst_reg_dt, open, high, low, close, volume, adj_close FROM definic.data_stock_usa where stock_code ='%s'" % (stockcode)
        try:
            print(sql)
            cursor = self.dbhandler.execSql(sql)
        except Exception as error:
            print(error)
        
        result = cursor.fetchall()
        print(result)
        fieldlist = ['stock_code', 'date', 'lst_reg_dt', 'open', 'high', 'low', 'close', 'volume', 'adj_close']
        return map((lambda x: dict(zip(fieldlist, x))), result)
    
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

if __name__ == '__main__':
    regression = Regression()
    data = regression.selectYahooDataFromDB("GOOG")
    result = regression.linearregression(data)
    print("Predicted Over")
    for row in result:
        print("%s %s " %( row['date'], row['predicted_data']))
