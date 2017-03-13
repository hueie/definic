import pandas as pd
import numpy as np
from sklearn import tree
from collections import Counter
from scipy.spatial import distance
import copy

class Apriori:
    
    def __init__(self):
        self.x_train = None
        self.min_sup = 0.0
        self.itr_cnt = 1
        pass
    
    
    def train(self, x_train, min_sup):
        print("\n!!! Start of Apriori Pattern !!!\n")
        if(min_sup == None):
            min_sup = 2
            
        self.min_sup = min_sup
        self.x_train = x_train
        #print("\n!!! End of Initiating Constants !!!\n")
        
        x_train_arr = []
        for x_dict in x_train:
            #print(list(list(x_dict.values())[0]))
            x_train_arr = x_train_arr + list(list(x_dict.values())[0])
        
        print(x_train_arr)
        x_train_cnts = Counter(x_train_arr)
        
        apriori_idx = 1
        print("\n!!! Start of C%s Counter !!!\n" % apriori_idx)
        C1 = dict()
        for C1_word, C1_count in x_train_cnts.items():
            C1[frozenset({C1_word})] = C1_count
            pass

        basic_elements = list(C1.keys())
        print("basic_elements : ", basic_elements)
        print("C%s : %s" % (apriori_idx , C1) ) 
        print("\n!!! End of C%s Counter !!!\n" % apriori_idx)
        
        print("\n!!! Start of L%s Min Sup !!!\n" % apriori_idx)
        L1 = copy.deepcopy(C1)
        for C_word, C_count in C1.items():
            if(C_count < min_sup):
                L1.pop(C_word)
        
        print("L%s : %s" % (apriori_idx , L1) ) 
        print("\n!!! End of L%s Min Sup !!!\n" % apriori_idx)
        
        
        while(True):
            apriori_idx += 1
            
            # Step 1) Start of C2 Join multiple sets
            C2_list = list()
            for L_element in list(L1.keys()):
                for basic_element in basic_elements:
                    newSet = (L_element | basic_element)
                    if (len(newSet) > len(L_element)):
                        C2_list.append(newSet)
            # End of C2 Join multiple sets
            
            # Step 2) 
            print("\n!!! Start of C%s Counter !!!\n" % apriori_idx)
            C2 = dict()
            for C2_list_element in set(C2_list):
                for x_row in x_train:
                    if(C2_list_element.issubset(set(list(x_row.values())[0])) ):
                        #print("%s < %s" % (C2_list_element , list(x_row.values())[0]))
                        if(C2.get(C2_list_element) == None):
                            C2[C2_list_element] = 1
                        else:
                            tmpcnt = C2[C2_list_element]
                            C2[C2_list_element] = tmpcnt + 1
            
            print("C%s : %s" % (apriori_idx , C2) ) 
            print("\n!!! End of C%s Counter !!!\n" % apriori_idx)
            
            # Step 3) 
            print("\n!!! Start of L%s Min Sup !!!\n" % apriori_idx)
            L2 = copy.deepcopy(C2)
            for C2_word, C2_count in C2.items():
                if(C2_count < min_sup):
                    L2.pop(C2_word)
            
            print("L%s : %s" % (apriori_idx , L2) ) 
            print("\n!!! End of L%s Min Sup !!!\n" % apriori_idx)
            
            
            #print("\n!!! Start of Stop Regulation !!!\n")
            if(len(L2) == 0):
                break
            
            L1 = L2
        
        
        print("\n!!! End of Apriori Pattern !!!\n")
        pass
    
    
        
if __name__ == "__main__":
    apriori = Apriori()
    #TID List of item IDs
    x_train=[ 
        {"T100" : {"I1", "I2", "I5"} },
        {"T200" : {"I2", "I4"} },
        {"T300" : {"I2", "I3"}},
        {"T400" : {"I1", "I2", "I4"}},
        {"T500" : {"I1", "I3"}},
        {"T600" : {"I2", "I3"}},
        {"T700" : {"I1", "I3"}},
        {"T800" : {"I1", "I2", "I3", "I5"}},
        {"T900" : {"I1", "I2", "I3"}}
        ]
    #y_train=[] clustering does not have y (labels)
    x_test=[]
    min_sup = 2
    apriori.train(x_train, min_sup)
    
    pass

