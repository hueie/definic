# -*- coding: utf-8 -*-
import sys,os
'''
sys.path.append((os.path.sep).join( os.getcwd().split(os.path.sep)[0:-1]))
from common.dbhandler import DBHandler
from common.const import *
from common.commonutil import CommonUtil
'''
from ..common.dbhandler import DBHandler
from ..common.const import *
from ..common.commonutil import CommonUtil

import numpy as np
import pandas as pd


class Preprocessor:
    def __init__(self):
        pass
    
    def makeDataSet(self, start_date, end_date):
        pass

    def makeLaggedDataset(self, start_date, end_date, input_column, output_column, time_lags=5):
        df = self.makeDataSet(start_date, end_date)

        df_lag = df
        df_lag[input_column] = df[input_column]
        df_lag["volume"] = df["volume"]

        df_lag["%s_Lag%s" % (input_column,time_lags)] = df[input_column].shift(time_lags)
        df_lag["%s_Lag%s_Change" % (input_column,time_lags)] = df_lag["%s_Lag%s" % (input_column,time_lags)].pct_change()*100.0

        df_lag["volume_Lag%s" % (time_lags)] = df["volume"].shift(time_lags)
        df_lag["volume_Lag%s_Change" % (time_lags)] = df_lag["volume_Lag%s" % (time_lags)].pct_change()*100.0

        #df_lag[output_column] = np.sign(df_lag["%s_Lag%s_Change" % (input_column,time_lags)])
        df_lag[output_column] = np.where(df_lag["%s_Lag%s_Change" % (input_column,time_lags)]>0,1,0)
            
        df_lag["volume_indicator"] = np.sign(df_lag["volume_Lag%s_Change" % (time_lags)])

        return df_lag.dropna(how='any').reset_index()


    def splitDataset(self, df, split_ratio, reindex=True):
        split_index = len(df)*split_ratio # ; print("splitDataset : date=%s" % (split_index))
        train = df[df.index < split_index]
        train = train.copy(deep=True)
        test = df[df.index >= split_index]
        test = test.copy(deep=True)
        if reindex is True:
            test = test.reset_index(drop=True)
            
        return train, test

    def adjustSeasonalData(self, df):
        pass
    
if __name__ == '__main__':
    pass
    
    