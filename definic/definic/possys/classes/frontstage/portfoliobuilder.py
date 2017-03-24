# -*- coding: utf-8 -*-
from ..common.dbhandler import DBHandler
from ..common.commonutil import CommonUtil
from ..common.const import *
from ..datascience.regression import Regression, LinearRegressionModel, LogisticRegressionModel, RandomForestModel, SVCModel
from ..datascience.preprocessor import Preprocessor
from ..backstage.datawarehouse import DataWareHouse
from ..middlestage.alphamodel import MeanReversionModel, MachineLearningModel
'''
import sys,os
sys.path.append((os.path.sep).join( os.getcwd().split(os.path.sep)[0:-1]))
from common.dbhandler import DBHandler
from common.commonutil import CommonUtil
from common.const import *
from datascience.regression import Regression, LinearRegressionModel, LogisticRegressionModel, RandomForestModel, SVCModel
from datascience.preprocessor import Preprocessor
from backstage.datawarehouse import DataWareHouse
from middlestage.alphamodel import MeanReversionModel, MachineLearningModel
'''
import numpy as np
import pandas as pd


class PortfolioBuilder:
    def __init__(self):
        self.mean_reversion_model = MeanReversionModel()
        self.machine_learning_model = MachineLearningModel()
        pass

    def assessADF(self,test_stat,adf_1,adf_5,adf_10):
        if test_stat<adf_10:
            return 3
        elif test_stat<adf_5:
            return 2
        elif test_stat<adf_1:
            return 1

        return 0


    def assessHurst(self,hurst):
        if hurst>0.4:
            return 0

        if hurst<0.1:
            return 3
        elif hurst<0.2:
            return 2
        
        return 1


    def assessHalflife(self,percentile,halflife):
        for index in range(len(percentile)):
            print("assessHalflife : %s , half=%s : percentile=%s" % (index, halflife, percentile[index]))
            if halflife<=percentile[index]:
                print("assessHalflife : %s , half=%s : percentile=%s" % (index, halflife, percentile[index]))

                if index<2:
                    return 3
                elif index<3:
                    return 2
                elif index<4:
                    return 1

        return 0


    def assessMachineLearning(self,percentile,halflife):
        for index in range(len(percentile)):
            print("assessHalflife : %s , half=%s : percentile=%s" % (index, halflife, percentile[index]))
            if halflife<=percentile[index]:
                print("assessHalflife : %s , half=%s : percentile=%s" % (index, halflife, percentile[index]))

                if index<2:
                    return 3
                elif index<3:
                    return 2
                elif index<4:
                    return 1

        return 0

    def rankStationarity(self,df_stationarity):
        df_stationarity['rank_adf'] = 0
        df_stationarity['rank_hurst'] = 0
        df_stationarity['rank_halflife'] = 0
        halflife_percentile = np.percentile(df_stationarity['halflife'], np.arange(0, 100, 10)) # quartiles
        print(halflife_percentile)

        for row_index in range(df_stationarity.shape[0]):
            df_stationarity.loc[row_index,'rank_adf'] = self.assessADF(df_stationarity.loc[row_index,'adf_statistic'],df_stationarity.loc[row_index,'adf_1'],df_stationarity.loc[row_index,'adf_5'],df_stationarity.loc[row_index,'adf_10'])
            df_stationarity.loc[row_index,'rank_hurst'] = self.assessHurst(df_stationarity.loc[row_index,'hurst'])
            df_stationarity.loc[row_index,'rank_halflife'] = self.assessHalflife(halflife_percentile, df_stationarity.loc[row_index,'halflife'])

        df_stationarity['rank'] = df_stationarity['rank_adf'] + df_stationarity['rank_hurst'] + df_stationarity['rank_halflife']

        return df_stationarity


    def buildUniverse(self,df_stationarity,column,ratio):
        commonutil = CommonUtil()
        percentile_column = np.percentile(df_stationarity[column], np.arange(0, 100, 10))
        ratio_index = np.trunc(ratio * len(percentile_column))

        universe = {}

        for row_index in range(df_stationarity.shape[0]):        
            percentile_index = commonutil.getPercentileIndex(percentile_column, df_stationarity.loc[row_index,column])
            if percentile_index >= ratio_index:
                universe[df_stationarity.loc[row_index,'code']] = df_stationarity.loc[row_index,'company']

        return universe

    def doStationarityTest(self, df, codelist, col_name,lags_count=100):
        if lags_count <= 3 or len(df) < lags_count :
            return "Lags_count is Out of Data Size"
        
        test_result = {'code':[], 'adf_statistic':[], 'adf_1':[],'adf_5':[],'adf_10':[], 'hurst':[],'halflife':[]}

        for idx, code in enumerate(codelist):
            subdf = df[df['stock_code'] == code][col_name]
            print("... %s : Testing Stationarity on %s" % ( idx, code))
            
            if subdf.shape[0]>0:
                test_result['code'].append(code)
                test_result['hurst'].append(self.mean_reversion_model.calcHurstExponent(subdf, lags_count))
                test_result['halflife'].append(self.mean_reversion_model.calcHalfLife(subdf))
    
                test_stat, adf_1,adf_5,adf_10 = self.mean_reversion_model.calcADF(subdf)
                test_result['adf_statistic'].append(test_stat)
                test_result['adf_1'].append(adf_1)
                test_result['adf_5'].append(adf_5)
                test_result['adf_10'].append(adf_10)
                print(test_result)
            else:
                pass
                

        df_result = pd.DataFrame(test_result)
        return df_result

    def doMachineLearningTest(self, df, codelist, col_name, split_ratio=0.75,lags_count=10):
        if lags_count <= 3 or len(df) < lags_count :
            return "Lags_count is Out of Data Size"
        
        test_result = {'code':[], 'linear':[], 'logistic':[], 'randomforest':[], 'svc':[]}

        for idx, code in enumerate(codelist):
            subdf = df[df['stock_code'] == code]
            print("... %s : Testing Stationarity on %s" % ( idx, code))

            preprocessor = Preprocessor()
            train, test = preprocessor.splitDataset(df, split_ratio)
            
            x_train = np.array([ [row] for row in train['open'] ])
            y_train = np.array(train[col_name])
            
            x_test = np.array([ [row] for row in test['open'] ])
            y_test = np.array(test[col_name])
            
            #df_dataset = self.predictor.makeLaggedDataset(code,self.config.get('start_date'),self.config.get('end_date'), self.config.get('input_column'),self.config.get('output_column'),time_lags=lags_count)

            if subdf.shape[0]>0:
                test_result['code'].append(code)

                selectedRegressionList =  ['linear','logistic', 'randomforest','svc']
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
                    score = regression.score(x_test, y_test) 
                    test_result[arr_regression].append(score)
                    print("    regression=%s, score=%s" % (arr_regression, score))
                
                print('test_result : %s' , test_result)

        df_result = pd.DataFrame(test_result)
        return df_result


    def rankMachineLearning(self,df_machine_learning):
        def listed_columns(arr,prefix):
            result = []
            for a_item in arr:
                result.append( prefix % (a_item) )
            return result

        mr_models = ['linear','logistic', 'randomforest','svc']

        for a_predictor in mr_models:
            df_machine_learning['rank_%s' % (a_predictor)] = 0

        percentiles = {}
        for a_predictor in mr_models:
            percentiles[a_predictor] = np.percentile(df_machine_learning[a_predictor], np.arange(0, 100, 10))

            for row_index in range(df_machine_learning.shape[0]):
                df_machine_learning.loc[row_index,'rank_%s' % (a_predictor)] = self.assessMachineLearning(percentiles[a_predictor],df_machine_learning.loc[row_index,a_predictor])

        df_machine_learning['total_score'] = df_machine_learning[mr_models].sum(axis=1)
        df_machine_learning['rank'] = df_machine_learning[ listed_columns(mr_models,'rank_%s') ].sum(axis=1)

        return df_machine_learning


if __name__ == "__main__":
    
    datawarehouse = DataWareHouse()
    codelist = ["GOOG"]
    data = datawarehouse.selectYahooDataFromDB("GOOG")
    preprocessor = Preprocessor()
    train, test = preprocessor.splitDataset(data, 0.9)
    
    portfoliobuilder = PortfolioBuilder()
    df_stationarity = portfoliobuilder.doStationarityTest(data, codelist, 'close', 5)    
    df_rank = portfoliobuilder.rankStationarity(df_stationarity)
    stationarity_codes = portfoliobuilder.buildUniverse(df_rank,'rank',0.8)
    print(stationarity_codes)

    
    df_machine_result = portfoliobuilder.doMachineLearningTest(data, codelist, 'close', split_ratio=0.75,lags_count=5 )
    df_machine_rank = portfoliobuilder.rankMachineLearning(df_machine_result)
    machine_codes = portfoliobuilder.buildUniverse(df_machine_rank,'rank',0.8)
    print(machine_codes)
    pass
