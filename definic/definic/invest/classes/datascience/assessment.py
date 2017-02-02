
import sys,os
sys.path.append((os.path.sep).join( os.getcwd().split(os.path.sep)[0:-1]))
from common.dbhandler import DBHandler
from common.const import *
from common.commonutil import CommonUtil

class assessment():
    def __init__(self):
        pass
    
    def test_predictor(self, classifier,x_test,y_test):
        pred = classifier.predict(x_test)
    
        hit_count = 0
        total_count = len(y_test)
        for index in range(total_count):
            if (pred[index]) == (y_test[index]):
                hit_count = hit_count + 1
        
        hit_ratio = hit_count/total_count
        score = classifier.score(x_test, y_test)
        #print "hit_count=%s, total=%s, hit_ratio = %s" % (hit_count,total_count,hit_ratio)
    
        return hit_ratio, score
        # Output the hit-rate and the confusion matrix for each model
        
        #print("%s\n" % confusion_matrix(pred, y_test))