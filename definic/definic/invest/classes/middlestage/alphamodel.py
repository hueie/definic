# -*- coding: utf-8 -*-
#from ..common.dbhandler import DBHandler
#from ..common.const import *

import sys,os
sys.path.append((os.path.sep).join( os.getcwd().split(os.path.sep)[0:-1]))
from common.dbhandler import DBHandler
from common.const import *
from datascience.regression import Regression, LinearRegressionModel, LogisticRegressionModel, RandomForestModel, SVCModel
from datascience.preprocessor import Preprocessor
from backstage.datawarehouse import DataWareHouse

import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts


class AlphaModel():
    def __init__(self):
        self.dbhandler = DBHandler()
        
    def determinePosition(self, x_train, y_train, x_test, verbose=False):
        pass


class MeanReversionModel(AlphaModel):
    def __init__(self):
        AlphaModel.__init__(self)
        self.window_size = 3 # Alpha Constant
        self.threshold = 1.5 # Alpha Constant
    
    def calcADF(self,df):
        adf_result = ts.adfuller(df)
        ciritical_values = adf_result[4]
        print(ciritical_values)

        return adf_result[0], ciritical_values['1%'],ciritical_values['5%'], ciritical_values['10%']

    def calcHurstExponent(self,df,lags_count=100):
        if lags_count <= 3 or len(df) < lags_count :
            return "Lags_count is Out of Data Size"
        
        lags = range(2, lags_count)
        ts = np.log(df)

        tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]
        poly = np.polyfit(np.log(lags), np.log(tau), 1)
        result = poly[0]*2.0
        return result

    def calcHalfLife(self,df):
        price = pd.Series(df) 
        lagged_price = price.shift(1).fillna(method="bfill")  
        delta = price - lagged_price  
        beta = np.polyfit(lagged_price, delta, 1)[0] 
        half_life = (-1*np.log(2)/beta) 

        return half_life


    def determinePosition(self, x_train, y_train, x_test, verbose=False):
        priceSeries = pd.Series(y_train) 

        df_moving_average = priceSeries.rolling(window=self.window_size).mean()
        df_moving_average_std = priceSeries.rolling(window=self.window_size).std()

        moving_average = df_moving_average[len(priceSeries)-1]
        moving_average_std = df_moving_average_std[len(priceSeries)-1]

        price_arbitrage = float(x_test) - float(moving_average)

        if verbose:
            print("diff=%s, price=%s, moving_average=%s, moving_average_std=%s" % (price_arbitrage, x_test, moving_average, moving_average_std))
            pass
        
        if abs(price_arbitrage) > moving_average_std * self.threshold:
            if np.sign(price_arbitrage)>0:
                return SHORT
            else:
                return LONG

        return HOLD

class MachineLearningModel(AlphaModel):
    def __init__ (self):
        AlphaModel.__init__(self)
        pass

    def determinePosition(self, x_train, y_train, x_test, verbose=False):
        if (len(x_test)-1) < 0:
            return HOLD
        
        selectedRegressionList =  ['linear','logistic', 'randomforest','svc']
        prediction_result = 0
        for arr_regression in selectedRegressionList:
            
            regression = Regression()
            if(arr_regression == 'linear'):
                regression = LinearRegressionModel()
            elif(arr_regression == 'logistic'):
                regression = LogisticRegressionModel()
            elif(arr_regression == 'randomforest'):
                regression = RandomForestModel()
            elif(arr_regression == 'svc'):
                regression = SVCModel()
            else:
                pass
            
            regression.train(x_train, y_train)
            y_predicted = regression.predict( x_test )
            print("predictor=%s, x_test=%s, y_predicted=%s" % (arr_regression, x_test, y_predicted) )
            prediction_result += y_predicted[0]
            
        
        prediction_result /= len(selectedRegressionList)
        print("price=%s, pred_result=%s" % (x_test, prediction_result))

        if prediction_result - x_test > 0:
            return LONG, prediction_result
        elif prediction_result - x_test < 0:
            return SHORT, prediction_result
   
        return HOLD, prediction_result

   
if __name__ == "__main__":
    datawarehouse = DataWareHouse()
    data = datawarehouse.selectYahooDataFromDB("GOOG")
    preprocessor = Preprocessor()
    train, test = preprocessor.splitDataset(data, 0.9)
    
    x_train = np.array([ [row] for row in train['open'] ])
    y_train = np.array(train['adj_close'])
    
    x_test = np.array([ [row] for row in test['open'] ])
    y_test = np.array(test['adj_close'])
    
    alphamodel = MeanReversionModel()
    x = alphamodel.calcHalfLife(y_train)
    y = alphamodel.calcHurstExponent(y_train, 4)
    z = alphamodel.calcADF(y_train)
    print(x, y, z)
    print(alphamodel.determinePosition(x_train, y_train, x_test ))

    alphamodel2 = MachineLearningModel()
    print( alphamodel2.determinePosition(x_train, y_train, x_test) )
    
    pass
