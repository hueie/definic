
import sys,os
sys.path.append((os.path.sep).join( os.getcwd().split(os.path.sep)[0:-1]))
from common.dbhandler import DBHandler
from common.const import *
from common.commonutil import CommonUtil


class Preprocessor():
    def __init__(self):
        pass
    
    def makeDataSet(self,code,start_date,end_date):
        pass

    def makeLaggedDataset(self, code,start_date,end_date, input_column, output_column, time_lags=5):
        df = self.makeDataSet(code,start_date,end_date)

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


    def splitDataset(self, df, date_column,input_column_array,output_column,split_ratio):
        first_date,last_date = df.loc[0,date_column], df.loc[df.shape[0]-1, date_column]
        commonutil = CommonUtil()
        split_date = commonutil.getDateByPerent(first_date,last_date,split_ratio)

        #print "splitDataset : date=%s" % (split_date)

        input_data = df[input_column_array]
        output_data = df[output_column]

        # Create training and test sets
        X_train = input_data[df[date_column] < split_date]
        X_test = input_data[df[date_column] >= split_date]
        Y_train = output_data[df[date_column] < split_date]
        Y_test = output_data[df[date_column] >= split_date]

        return X_train,X_test,Y_train,Y_test


    