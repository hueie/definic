# -*- coding: utf-8 -*-
import sys,os

'''
sys.path.append((os.path.sep).join( os.getcwd().split(os.path.sep)[0:-1]))
from backstage.datawarehouse import DataWareHouse
from datascience.preprocessor import Preprocessor
'''

from ..backstage.datawarehouse import DataWareHouse
from ..datascience.preprocessor import Preprocessor

import copy
import numpy as np

from sklearn.neural_network import MLPClassifier

from sklearn.metrics import confusion_matrix,classification_report,roc_curve, auc
import matplotlib.pyplot as plt
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
   
     
class Neuralnetwork:
    def __init__(self):
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
    
    
 
class MLPClassifierModel(Neuralnetwork):
    def __init__(self):
        Neuralnetwork.__init__(self)
        self.model = MLPClassifier(hidden_layer_sizes=(15,), activation='tanh', solver='sgd', learning_rate='constant', \
                                alpha=1e-4,  random_state=1, batch_size=1,verbose= True, max_iter=1, warm_start=True)
   
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
    
    mlpclassifiermodel = MLPClassifierModel()
    print("Linear Regression Start")    
    print("Train : ", mlpclassifiermodel.train( x_train, y_train))
    y_pred = mlpclassifiermodel.predict( x_test)
    print("Y_true : ", y_test)
    print("Predicted : ", y_pred)
    print("Score : ", mlpclassifiermodel.score(x_test, y_test))
    print("Hit Ratio : ", mlpclassifiermodel.hitRatio(y_test, y_pred))
    print("meanSquaredError : ", mlpclassifiermodel.meanSquaredError(y_test, y_pred))
    
    print('Print nodes of Weight')
    print( [mynode.shape for mynode in mlpclassifiermodel.model.coefs_] )
    pass
