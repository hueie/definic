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
        print("\n!!! Finish Initiating Constants !!!\n")
        
        x_train_arr = []
        for x_dict in x_train:
            #print(list(list(x_dict.values())[0]))
            x_train_arr = x_train_arr + list(list(x_dict.values())[0])
            
        
        print(x_train_arr)
        x_train_cnts = Counter(x_train_arr)
        
        
        print("\n!!! Start of C1 Counter !!!\n")
        C_cnts = dict()
        for word, count in x_train_cnts.items():
            C_cnts[frozenset({word})] = count
            pass

        basic_elements = list(C_cnts.keys())
        print("\n!!! End of C1 Counter !!!\n")
        
        print("\n!!! Start of C1 Min Sup !!!\n")
        L_cnts = copy.deepcopy(C_cnts)
        print("basic_elements : ", basic_elements)
        for C_word, C_count in C_cnts.items():
            if(C_count < min_sup):
                L_cnts.pop(C_word)
        
        print(L_cnts)  
        print(set(L_cnts.keys()))
        print("\n!!! End of C1 Min Sup !!!\n")
        


        # Step 1) Start of C2 Join multiple sets
        C2_list = list()
        for L_element in list(L_cnts.keys()):
            for basic_element in basic_elements:
                newSet = (L_element | basic_element)
                if (len(newSet) > len(L_element)):
                    C2_list.append(newSet)
        # End of C2 Join multiple sets
        
        # Step 2) 
        print("\n!!! Start of C2 Counter !!!\n")
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
        
        print(C2)
        print("\n!!! End of C2 Counter !!!\n")
        
        # Step 3) 
        print("\n!!! Start of C2 Min Sup !!!\n")
        L2 = copy.deepcopy(C2)
        for C2_word, C2_count in C2.items():
            if(C2_count < min_sup):
                L2.pop(C2_word)
        
        print(L2)
        print("\n!!! End of C2 Min Sup !!!\n")
        
        
        
        
        
        
        
        
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

