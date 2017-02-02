# -*- coding: utf-8 -*-
#from ..common.dbhandler import DBHandler
#from ..common.const import *
from . import predictor

import sys,os
sys.path.append((os.path.sep).join( os.getcwd().split(os.path.sep)[0:-1]))
from common.dbhandler import DBHandler
from common.const import *

import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts


class AlphaModel():
    def __init__(self):
        self.dbhandler = DBHandler()
        
    def determinePosition(self,code,df,column,row_index,verbose=False):
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


    def determinePosition(self,df, chk_row_idx ,verbose=False):
        priceSeries = pd.Series(df) 
        current_price = priceSeries[chk_row_idx]

        df_moving_average = priceSeries.rolling(window=self.window_size).mean()
        df_moving_average_std = priceSeries.rolling(window=self.window_size).std()

        moving_average = df_moving_average[chk_row_idx]
        moving_average_std = df_moving_average_std[chk_row_idx]

        price_arbitrage = float(current_price) - float(moving_average)

        if verbose:
            print("diff=%s, price=%s, moving_average=%s, moving_average_std=%s" % (price_arbitrage,current_price,moving_average,moving_average_std))

        if abs(price_arbitrage) > moving_average_std * self.threshold:
            
            if np.sign(price_arbitrage)>0:
                return SHORT
            else:
                return LONG

        return HOLD

'''
class MachineLearningModel(AlphaModel):
    def __init__ (self):
        AlphaModel.__init__(self)
        self.predictor = Predictor()
    
    def calcScore(self, split_ratio=0.75,time_lags=10):
        return self.predictor.trainAll(split_ratio=split_ratio,time_lags=time_lags )


    def determinePosition(self, code,df,column,row_index,verbose=False):
        if (row_index-1) < 0:
            return HOLD

        current_price = df.loc[row_index-1,column]

        prediction_result = 0
        for a_predictor in ['logistic','rf','svm']:
            
            predictor = self.predictor.get(code,a_predictor)
            pred,pred_prob = predictor.predict([current_price])

            print("predictor=%s, price=%s, pred=%s, pred_proba=%s" % (a_predictor,current_price,pred[0],pred_prob[0]))

            prediction_result += pred[0]
            print(prediction_result[a_predictor])

        print("price=%s, pred_result=%s" % (current_price,prediction_result))

        if prediction_result>1:
            return LONG
        else:
            return SHORT
'''
   
    def trainAll(self, time_lags=5, split_ratio=0.75):
        rows_code = self.dbreader.loadCodes(self.config.get('data_limit'))
        
        test_result = {'code':[], 'company':[], 'logistic':[], 'rf':[], 'svm':[]}

        index = 1
        for a_row_code in rows_code:
            code = a_row_code[0]
            company = a_row_code[1]
            
            print("... %s of %s : Training Machine Learning on %s %s" % (index,len(rows_code),code,company))

            df_dataset = self.makeLaggedDataset(code,self.config.get('start_date'),self.config.get('end_date'), self.config.get('input_column'),self.config.get('output_column'),time_lags=time_lags)

            #print df_dataset

            if df_dataset.shape[0]>0:
                
                test_result['code'].append(code)
                test_result['company'].append(company)

                #print df_dataset

                X_train,X_test,Y_train,Y_test = self.splitDataset(df_dataset,'price_date',[self.config.get('input_column')],self.config.get('output_column'),split_ratio)

                #print X_test, Y_test

                for a_clasifier in ['logistic','rf','svm']:
                    predictor = self.createPredictor(a_clasifier)
                    self.add(code,a_clasifier,predictor)

                    predictor.train(X_train,Y_train)
                    score = predictor.score(X_test,Y_test)

                    test_result[a_clasifier].append(score)

                    print("    predictor=%s, score=%s" % (a_clasifier,score))


                #print test_result

            index += 1

        df_result = pd.DataFrame(test_result)

        return df_result


    def dump(self):
        for a_code in self.items.keys():
            for a_predictor in self.items[a_code].keys():
                print("... code=%s , predictor=%s" % (a_code,a_predictor))



   
if __name__ == "__main__":
    alphamodel = MeanReversionModel()
    
    sql = "SELECT date, close FROM definic.data_stock_usa WHERE stock_code = 'GOOG' order by date"

    df = pd.read_sql(sql, alphamodel.dbhandler.conn, index_col='date')
    df2 = pd.read_sql(sql, alphamodel.dbhandler.conn)
    x = alphamodel.calcHalfLife(np.array(df['close']))
    
    y = alphamodel.calcHurstExponent(np.array(df['close']), 4)
    z = alphamodel.calcADF(np.array(df['close']))
    sign = alphamodel.determinePosition(np.array(df['close']), len(df2)-1 )
    
    print(x, y, z, sign)