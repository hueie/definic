# -*- coding: utf-8 -*-
from ..common.dbhandler import DBHandler
#import sys,os
#sys.path.append((os.path.sep).join( os.getcwd().split(os.path.sep)[0:-1]))
#from common.dbhandler import DBHandler

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
    def __init__(self ):
        self.dbhandler = DBHandler()
        self.mse = 0
        self.coef = 0
        self.score = 0
        self.model = None
    
    def train(self,x_train,y_train):
        self.classifier.fit(x_train, y_train)
        return self.classifier.score(x_train, y_train)

    def predict(self,x_test,with_probability=True):
        pred = self.classifier.predict(x_test)
        pred_proba = self.classifier.predict_proba(x_test)
        return pred,pred_proba


    def score(self,x_test,y_test):
        return self.classifier.score(x_test,y_test)

    def confusionMatrix(self,y_true,y_pred):
        print(confusion_matrix(y_true, y_pred))

    def classificationReport(self,y_true,y_pred,target_names):
        print(classification_report(y_true, y_pred, target_names=target_names))


    def drawROC(self,y_true,y_pred):
        false_positive_rate, true_positive_rate, thresholds = roc_curve(y_true, y_pred)
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


    def doGridSearch(self,x_train,y_train,param_grid):
        grid_search = GridSearchCV(self.classifier, param_grid=param_grid)
        grid_search.fit(x_train,y_train)

        for params, mean_score, scores in grid_search.grid_scores_:
            print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() * 2, params))
        

    def doRandomSearch(self,x_train,y_train,param_dist,iter_count):
        random_search =  RandomizedSearchCV(self.classifier, param_distributions=param_dist, n_iter=iter_count)
        random_search.fit(x_train,y_train)

        for params, mean_score, scores in random_search.grid_scores_:
            print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() * 2, params))
    
    
    
    
    
        
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


class LinearRegressionModel(Regression):
    def __init__(self,name):
        Regression.__init__(self,name)
        self.classifier = linear_model.LinearRegression()
    
    def do_logistic_regression(self, X_train,Y_train):
        return self.classifier

class LogisticRegressionModel(Regression):
    def __init__(self,name):
        Regression.__init__(self,name)
        self.classifier = LogisticRegression()
    
    def do_logistic_regression(self, X_train,Y_train):
        return self.classifier


class RandomForestClassifierModel(Regression):
    def __init__(self,name):
        Regression.__init__(self,name)
        self.classifier = RandomForestClassifier()

    def do_random_forest(self, X_train,Y_train):
        return self.classifier


class PredictorSVMModel(Regression):
    def __init__(self,name):
        Regression.__init__(self,name)
        self.classifier = SVC(probability=True)

    def do_svm(self, X_train,Y_train):
        return self.classifier











if __name__ == '__main__':
    regression = Regression()
    data = regression.selectYahooDataFromDB("GOOG")
    result = regression.linearregression(data)
    print("Predicted Over")
    for row in result:
        print("%s %s " %( row['date'], row['predicted_data']))
        
        
        
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
            lr_classifier = predictorLR.do_logistic_regression(X_train,Y_train)
            lr_hit_ratio, lr_score = test_predictor(lr_classifier,X_test,Y_test)
            
            predictorRF = PredictorRF()
            rf_classifier = predictorRF.do_random_forest(X_train,Y_train)
            rf_hit_ratio, rf_score = test_predictor(rf_classifier,X_test,Y_test)

            predictorSVM = PredictorSVM()
            svm_classifier = predictorSVM.do_svm(X_train,Y_train)
            svm_hit_ratio, svm_score = test_predictor(rf_classifier,X_test,Y_test)

            print("%s : Hit Ratio - Logistic Regreesion=%0.2f, RandomForest=%0.2f, SVM=%0.2f" % (company,lr_hit_ratio,rf_hit_ratio,svm_hit_ratio))
        
        
        
