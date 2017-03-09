import pandas as pd
import numpy as np
from sklearn import tree
from collections import Counter
from scipy.spatial import distance
import copy

class Fuzzyclusters:
    #Only the Coordinates of the points (x,y) about Floats Variables
    #Using Euclidean Dist
    
    def __init__(self):
        self.x_train = None
        self.clusters = []
        self.fuzzy_membership = []
        self.error_rate = 0.0
        self.error_threshold = 0.5
        self.k = None
        self.itr_cnt = 1
        pass
    
    
    def cal_fuzzy_membership(self, x_train, clusters):
        m = []
        for x_row in x_train:
            powered_distlist = []
            for cluster in clusters:
                #print("x_row : %s , cluster : %s" % (x_row, cluster))
                dist = distance.euclidean(tuple(x_row), tuple(cluster))
                powered_distlist.append(np.power(dist, 2))
                
            powered_distlist.reverse()
            sum_distlist = np.sum(powered_distlist)
            powered_distlist /= sum_distlist
            m.append(powered_distlist)
        #print(m)
        return m
    
    def train(self, x_train, k=None, error_threshold=None):
        print("\n!!! Start of Fuzzy EM Clustering !!!\n")
        
        if(len(np.array(x_train).shape) == 1):
            dimension = 0 # Simple array [1 ,2 ,3]
        elif(len(np.array(x_train).shape) > 1): # axis Array [ [1], [2] ] / [ [1,2] , [3,4] ]
            dimension = len(x_train[0])
        print("Constants : Dimension : %s, " % dimension, end="")
        
        if(error_threshold == None):
            error_threshold = 0.5
        if(k == None):
            k = 2
            
        print("Error Threshold : %s , k : %s" % (error_threshold , k) )
        self.k = k
        self.error_threshold = error_threshold
        self.x_train = x_train
        
        print("\n!!! Finish Initiating Constants !!!\n")
        
        c = []
        for idx, x_row in enumerate(x_train):
            if(idx == k):
                break
            c.append(x_row)
            
        print("1st Center : %s\n" % c)
        self.clusters.append(c)
        
        flag = True
        while(flag):
            self.itr_cnt += 1
            #Calculate Fuzzy Membership
            m = np.array(self.cal_fuzzy_membership(x_train, self.clusters[-1]))
            self.fuzzy_membership = copy.deepcopy(m)
            
            #E Step
            mT = m.T
            powered_mT = np.power(mT, 2)
            print("%sth mT : %s" % (self.itr_cnt, mT))
            #print("powered mT", powered_mT)
            #M Step
            x_trainT = np.array(x_train)
            x_trainT = x_trainT.T
            #print(x_trainT)
            
            clusters = []
            for idx in range(k):
                cluster = []
                for xy_idx in range(dimension):
                    weightedobject = powered_mT[idx] * x_trainT[xy_idx]
                    #print("weightedobject : %s" % weightedobject)
                    c_point = np.sum(weightedobject) / np.sum(powered_mT[idx])
                    cluster.append(c_point)
                
                clusters.append(tuple(cluster))    
            print("%sth Cluster : %s\n" %(self.itr_cnt, clusters) )
            self.clusters.append(clusters)
            
            # Regulation Stopping Iteration 
            for k_idx in range(k):
                error_rate =  distance.euclidean(tuple(self.clusters[-2][k_idx]) , tuple(self.clusters[-1][k_idx]) )
                
                if( np.abs(error_rate)  < error_threshold  ):
                    print("Error Rate C%s : %s" % (k_idx, error_rate), end="\t")
                    self.error_rate = error_rate
                    flag = False
        
            
        print("\n\nAll Clusters : %s" % self.clusters)    
        print("\n!!! End of Fuzzy EM Clustering !!!\n")
        pass
    
    
        
if __name__ == "__main__":
    fuzzyclusters = Fuzzyclusters()
    
    x_train=[ (3,3), (4,10), (9,6), (14,8), (18,11), (21,7)]
    #y_train=[] clustering does not have y (labels)
    x_test=[]
    k=2 #two clusters
    fuzzyclusters.train(x_train, k)
    
    pass

