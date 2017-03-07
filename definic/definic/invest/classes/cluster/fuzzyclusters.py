import pandas as pd
import numpy as np
from sklearn import tree
from collections import Counter
from scipy.spatial import distance
import copy

class Fuzzyclusters:
    def __init__(self):
        self.x_train = None
        self.y_train = None
        self.k = None
        pass
    
    def minmaxnormalization(self, x_train):
        if(len(x_train.shape) == 1):
            dimension = 0 # Simple array [1 ,2 ,3]
        elif(len(x_train.shape) > 1): # axis Array [ [1], [2] ] / [ [1,2] , [3,4] ]
            dimension = len(x_train[0])
            
        print("dimension : %s" % dimension)
        
        if(dimension == 0):
            x_min = min(x_train)
            x_max = max(x_train)
            print("x_min : %s , x_max : %s" % (x_min, x_max) )
            
            if(x_min == x_max ):
                print("Error : Min is equal to max!!!")
                return 
            
            for idx, x in enumerate(x_train):
                x_train[idx] = (x - x_min) / (x_max - x_min)
                print("\tx_train[%s] = %s" % (idx, x_train[idx]) )
            
        elif(dimension > 0) :
            for axis in range(dimension):
                x_min = min(x_train, key = lambda item:item[axis]) [axis]
                x_max = max(x_train, key = lambda item:item[axis]) [axis]
                print("x_min : %s , x_max : %s" % (x_min, x_max) )
                
                if(x_min == x_max ):
                    print("Error : Min is equal to max!!!")
                    return 
            
                for idx, x in enumerate(x_train):
                    x_train[idx][axis] = (x[axis] - x_min) / (x_max - x_min)
                    print("\tx_train[%s][%s] = %s" % (idx, axis, x_train[idx][axis]) )
            
        return x_train
    
    
    
    def train(self, x_train, y_train, k=None):
        if(k == None):
            k = 1
        print("k : %s" % k)
        self.k = k
        self.x_train = x_train
        self.y_train = y_train
        
        print("\n!!! End of k nearest neighbors Modeling !!!\n")
        pass
    
    def test(self, x_test_row):
        tmpdict ={}
        for idx, x_row in enumerate(x_train):
            dist = distance.euclidean(tuple(x_test), tuple(x_row))
            tmpdict[idx] = dist
        
        sorted_tmpdict = copy.deepcopy( sorted(tmpdict.items(), key = lambda item:item[1]) )

        rsltdict ={} ; idx = 0
        for key, value in sorted_tmpdict:
            if( idx == self.k ):
                print("break k = %s" % idx)
                break
            else:
                if(rsltdict.get( y_train[key] ) == None ):
                    rsltdict[y_train[key]] = 1
                else:
                    rsltdict[y_train[key]] += 1
            
            idx += 1
        
        sorted_rsltdict = copy.deepcopy( sorted(rsltdict.items(), key = lambda item:item[1]) )
        sorted_rsltdict.reverse()
        print(sorted_rsltdict) ; print(sorted_rsltdict[0])
        return sorted_rsltdict
        
if __name__ == "__main__":
    fuzzyclusters = Fuzzyclusters()
    
    x_train=[]
    y_train=[]
    x_test=[[1, 0, 1]]
    
    for idx in range(10):
        x_train.append( [ float(idx), float(10-idx), float(5-idx)/2 ] )
        y_train.append( float(idx) % 3 ) #3 kinds of classes (labels) 0, 1, 2 
        
    
    
    pass

