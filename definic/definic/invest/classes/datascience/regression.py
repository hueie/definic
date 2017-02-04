# -*- coding: utf-8 -*-
import sys,os
'''
sys.path.append((os.path.sep).join( os.getcwd().split(os.path.sep)[0:-1]))
from common.dbhandler import DBHandler
from backstage.datawarehouse import DataWareHouse
from datascience.preprocessor import Preprocessor
'''

from ..common.dbhandler import DBHandler
from ..backstage.datawarehouse import DataWareHouse
from ..datascience.preprocessor import Preprocessor

import copy
import numpy as np
from sklearn import linear_model 
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix,classification_report,roc_curve, auc
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV

     
class Regression:
    def __init__(self):
        self.dbhandler = DBHandler()
        self.model = None
    
    def train(self,x_train,y_train):
        return self.model.fit(x_train, y_train)

    def predict(self,x_test):
        return self.model.predict(x_test)
    
    def score(self,x_test,y_test):
        return self.model.score(x_test,y_test)

#Quantifying the quality of prediction

    def hitRatio(self, y_test, y_pred):
        hit_count = 0
        total_count = len(y_test)
        for idx in range(total_count):
            if (y_pred[idx]) == (y_test[idx]):
                hit_count = hit_count + 1
        
        hit_ratio = hit_count/total_count
        #print("hit_count=%s, total=%s, hit_ratio = %s" % (hit_count,total_count,hit_ratio))
        return hit_ratio

    def meanSquaredError(self, y_test, y_pred):
        return np.mean((y_pred - y_test) ** 2)
    

    def confusionMatrix(self, y_test, y_pred):
        #print(confusion_matrix(y_test, y_pred))
        return confusion_matrix(y_test, y_pred)

    def classificationReport(self, y_test, y_pred, target_names=None):
        return classification_report( y_test, y_pred, target_names=target_names)


    def rocAuc(self, y_test, y_pred):
        false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
        roc_auc = auc(false_positive_rate, true_positive_rate)
        
        plt.title('Receiver Operating Characteristic')
        plt.plot(false_positive_rate, true_positive_rate, 'b', label='AUC = %0.2f'% roc_auc)
        plt.legend(loc='lower right')
        plt.plot([0,1],[0,1],'r--')
        plt.xlim([-0.1,1.2])
        plt.ylim([-0.1,1.2])
        plt.ylabel('Sensitivity')
        plt.xlabel('Specificity')
        plt.show()
        
        return false_positive_rate, true_positive_rate, roc_auc


    def doGridSearchCV(self, x_train, y_train, param_grid):
        grid_search = GridSearchCV(self.model, param_grid=param_grid)
        grid_search.fit(x_train,y_train)

        for params, mean_score, scores in grid_search.grid_scores_:
            print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() * 2, params))
        

    def doRandomSearchCV(self, x_train, y_train, param_dist, iter_count):
        random_search =  RandomizedSearchCV(self.model, param_distributions=param_dist, n_iter=iter_count)
        random_search.fit(x_train,y_train)

        for params, mean_score, scores in random_search.grid_scores_:
            print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() * 2, params))
    
    
    
    

class LinearRegressionModel(Regression):
    def __init__(self):
        Regression.__init__(self)
        self.model = linear_model.LinearRegression()
        pass
    #Override Section

class LogisticRegressionModel(Regression):
    def __init__(self):
        Regression.__init__(self)
        self.model = LogisticRegression()
        pass
    #Override Section

class RandomForestModel(Regression):
    def __init__(self):
        Regression.__init__(self)
        self.model = RandomForestClassifier()
        pass
    #Override Section

class SVCModel(Regression):
    def __init__(self):
        Regression.__init__(self)
        self.model = SVC(probability=True)
        pass
    #Override Section




if __name__ == '__main__':
    datawarehouse = DataWareHouse()
    data = datawarehouse.selectYahooDataFromDB("GOOG")
    
    preprocessor = Preprocessor()
    train, test = preprocessor.splitDataset(data, 0.8)
    
    x_train = np.array([ [row] for row in train['open'] ])
    y_train = np.array(train['adj_close'])
    
    x_test = np.array([ [row] for row in test['open'] ])
    y_test = np.array(test['adj_close'])
    
    linearregression = LinearRegressionModel()
    print("Linear Regression Start")    
    print("Train : ", linearregression.train( x_train, y_train))
    y_pred = linearregression.predict( x_test)
    print("Y_true : ", y_test)
    print("Predicted : ", y_pred)
    print("Score : ", linearregression.score(x_test, y_test))
    print("Hit Ratio : ", linearregression.hitRatio(y_test, y_pred))
    print("meanSquaredError : ", linearregression.meanSquaredError(y_test, y_pred))
    #print("confusionMatrix : ", linearregression.confusionMatrix(y_test, y_pred))
    #print("classificationReport : ", linearregression.classificationReport(y_test, y_pred))
    #print("rocAuc : ", linearregression.rocAuc(y_test, y_pred))

    logisticregression = LogisticRegressionModel()
    print("Logistic Regression Start")    
    print("Train : ", logisticregression.train( x_train, y_train))
    y_pred = logisticregression.predict( x_test)
    print("Predicted : ", y_pred)
    print("Score : ", logisticregression.score(x_test, y_test))
    print("Hit Ratio : ", logisticregression.hitRatio(y_test, y_pred))
    print("meanSquaredError : ", logisticregression.meanSquaredError(y_test, y_pred))
    #print("confusionMatrix : ", logisticregression.confusionMatrix(y_test, y_pred))
    #print("classificationReport : ", logisticregression.classificationReport(y_test, y_pred))
    #print("rocAuc : ", logisticregression.rocAuc(y_test, y_pred))
    
    randomforest = RandomForestModel()
    print("Random Forest Start")    
    print("Train : ", randomforest.train( x_train, y_train))
    y_pred = randomforest.predict( x_test)
    print("Predicted : ", y_pred)
    print("Score : ", randomforest.score(x_test, y_test))
    print("Hit Ratio : ", randomforest.hitRatio(y_test, y_pred))
    print("meanSquaredError : ", randomforest.meanSquaredError(y_test, y_pred))
    #print("confusionMatrix : ", randomforest.confusionMatrix(y_test, y_pred))
    #print("classificationReport : ", randomforest.classificationReport(y_test, y_pred))
    #print("rocAuc : ", randomforest.rocAuc(y_test, y_pred))
        
    svc = SVCModel()
    print("SVC Start")    
    print("Train : ", svc.train( x_train, y_train))
    y_pred = svc.predict( x_test)
    print("Predicted : ", y_pred)
    print("Score : ", svc.score(x_test, y_test))
    print("Hit Ratio : ", svc.hitRatio(y_test, y_pred))
    print("meanSquaredError : ", svc.meanSquaredError(y_test, y_pred))
    #print("confusionMatrix : ", svc.confusionMatrix(y_test, y_pred))
    #print("classificationReport : ", svc.classificationReport(y_test, y_pred))
    #print("rocAuc : ", svc.rocAuc(y_test, y_pred))
        
        
    """  
    predictor = Regression()
    
    avg_hit_ratio = 0    
    for time_lags in range(1,6):
        print("- Time Lags=%s" % (time_lags))
        
        for company in ['GOOG','UWTI']:
            sql = "SELECT date, close FROM definic.data_stock_usa WHERE stock_code = '%s' order by date" % ( company )

            df_company = pd.read_sql(sql, predictor.dbhandler.conn, index_col='date')

            predictors = Predictors()
            df_dataset = predictors.make_dataset(df_company,time_lags)
            X_train,X_test,Y_train,Y_test = predictors.split_Dataset(df_dataset,["Close_Lag%s"%(time_lags),"Volume_Lag%s"%(time_lags)],"Close_Direction",0.75)
            #print X_test
            
            predictorLR = PredictorLR()
            lr_model = predictorLR.do_logistic_regression(X_train,Y_train)
            lr_hit_ratio, lr_score = test_predictor(lr_model,X_test,Y_test)
            
            predictorRF = PredictorRF()
            rf_model = predictorRF.do_random_forest(X_train,Y_train)
            rf_hit_ratio, rf_score = test_predictor(rf_model,X_test,Y_test)

            predictorSVM = PredictorSVM()
            svm_model = predictorSVM.do_svm(X_train,Y_train)
            svm_hit_ratio, svm_score = test_predictor(rf_model,X_test,Y_test)

            print("%s : Hit Ratio - Logistic Regreesion=%0.2f, RandomForest=%0.2f, SVM=%0.2f" % (company,lr_hit_ratio,rf_hit_ratio,svm_hit_ratio))
        
        
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
    """   
