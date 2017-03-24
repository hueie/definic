import pandas as pd
import numpy as np
from sklearn import tree
from collections import Counter
from scipy.spatial import distance
import copy

class Apriori:
    
    def __init__(self):
        self.x_train = None
        self.min_sup = 0.0  #minimum support threshold
        self.itr_cnt = 1
        self.L_list = []  #Apriori property (  Itemset satisfies the minimum support threshold ) how Lk-1 is used to find Lk for k >= 2
        self.C_list = []
        pass
    
    
    def train(self, x_train, min_sup):
        print("\n!!! To find out frequent itemsets !!!\n")
        
        print("\n!!! Start of Apriori Pattern !!!\n")
        if(min_sup == None):
            min_sup = 2
            
        self.min_sup = min_sup
        self.x_train = x_train
        print("Minimum Support Threshold : %s" % min_sup)
        
        x_train_arr = []
        for x_dict in x_train:
            #print(list(list(x_dict.values())[0]))
            x_train_arr = x_train_arr + list(list(x_dict.values())[0])
        
        x_train_cnts = Counter(x_train_arr)
        
        basic_elements = list( [ {word} for word, count in x_train_cnts.items() ] )
        print("Basic Elements : %s" % basic_elements)
        
        
        apriori_idx = 1
        print("\n!!! Start of C%s Counter !!!\n" % apriori_idx)
        C1 = dict()
        for C1_word, C1_count in x_train_cnts.items():
            C1[frozenset({C1_word})] = C1_count
            pass

        #basic_elements2 = list(C1.keys())
        #print("basic_elements2 : ", basic_elements2)
        self.C_list.append(C1)
        print("C%s : %s" % (apriori_idx , C1) ) 
        print("\n!!! End of C%s Counter !!!\n" % apriori_idx)
        
        print("\n!!! Start of L%s Min Sup !!!\n" % apriori_idx)
        L1 = copy.deepcopy(C1)
        for C_word, C_count in C1.items():
            if(C_count < min_sup):
                L1.pop(C_word)
        
        self.L_list.append(L1)
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
            
            self.C_list.append(C2)
            print("C%s : %s" % (apriori_idx , C2) ) 
            print("\n!!! End of C%s Counter !!!\n" % apriori_idx)
            
            # Step 3) 
            print("\n!!! Start of L%s Min Sup !!!\n" % apriori_idx)
            L2 = copy.deepcopy(C2)
            for C2_word, C2_count in C2.items():
                if(C2_count < min_sup):
                    L2.pop(C2_word)
            
            self.L_list.append(L2)
            print("L%s : %s" % (apriori_idx , L2) ) 
            print("\n!!! End of L%s Min Sup !!!\n" % apriori_idx)
            
            
            #print("\n!!! Start of Stop Regulation !!!\n")
            if(len(L2) == 0):
                break
            
            L1 = L2
        
        
        print("\n!!! End of Apriori Pattern !!!\n")
        print("C List")
        for row in self.C_list:
            print("\t%s" % row)
        print("L List")
        for row in self.L_list:
            print("\t%s" % row)
        pass
    
    def train_joined_proned(self, x_train, min_sup):
        print("\n!!! Start of Apriori Pattern !!!\n")
        if(min_sup == None):
            min_sup = 2
            
        self.min_sup = min_sup
        self.x_train = x_train
        print("Minimum Support Threshold : %s" % min_sup)
        
        x_train_arr = []
        for x_dict in x_train:
            #print(list(list(x_dict.values())[0]))
            x_train_arr = x_train_arr + list(list(x_dict.values())[0])
        
        x_train_cnts = Counter(x_train_arr)
        
        basic_elements = list( [ {word} for word, count in x_train_cnts.items()] )
        print("Basic Elements : %s" % basic_elements)
        
        
        
        apriori_idx = 1
        print("\n!!! Start of C%s Counter !!!\n" % apriori_idx)
        C1 = dict()
        for C1_word, C1_count in x_train_cnts.items():
            C1[frozenset({C1_word})] = C1_count
            pass

        #basic_elements2 = list(C1.keys())
        #print("basic_elements2 : ", basic_elements2)
        self.C_list.append(C1)
        print("C%s : %s" % (apriori_idx , C1) ) 
        print("\n!!! End of C%s Counter !!!\n" % apriori_idx)
        
        print("\n!!! Start of L%s Min Sup !!!\n" % apriori_idx)
        L1 = copy.deepcopy(C1)
        for C_word, C_count in C1.items():
            if(C_count < min_sup):
                L1.pop(C_word)
        
        self.L_list.append(L1)
        print("L%s : %s" % (apriori_idx , L1) ) 
        print("\n!!! End of L%s Min Sup !!!\n" % apriori_idx)
        
        
        while(True):
            apriori_idx += 1
            
            # Step 1) Start of C2 Join multiple sets
            C2_list = list()
            # Join (Lk-1 | Lk-1) = Ck
            for L1_1_element in list(L1.keys()):
                for L1_2_element in list(L1.keys()):
                    newSet = (L1_1_element | L1_2_element)
                    if (len(newSet) == apriori_idx):
                        C2_list.append(newSet)
                        
            # Prune Lk-1 in Ck newSet
            Proned_C2_list = []
            for newSet in C2_list:
                for row in newSet:
                    tmpNewSet = set(copy.deepcopy(newSet))
                    tmpNewSet.discard(row)
                    
                    NotSubSetFlag = True
                    for compared_L1_1_element in list(L1.keys()):
                        if(tmpNewSet == compared_L1_1_element):    
                            NotSubSetFlag = False
                        
                    if(NotSubSetFlag == True):
                        break;
                    else:
                        Proned_C2_list.append(newSet)
                                                
            # End of C2 Join multiple sets
            
            # Step 2) 
            print("\n!!! Start of C%s Counter !!!\n" % apriori_idx)
            C2 = dict()
            for C2_list_element in set(Proned_C2_list):
                for x_row in x_train:
                    if(C2_list_element.issubset(set(list(x_row.values())[0])) ):
                        if(C2.get(C2_list_element) == None):
                            C2[C2_list_element] = 1
                        else:
                            tmpcnt = C2[C2_list_element]
                            C2[C2_list_element] = tmpcnt + 1
            
            self.C_list.append(C2)
            print("C%s : %s" % (apriori_idx , C2) ) 
            print("\n!!! End of C%s Counter !!!\n" % apriori_idx)
            
            # Step 3) 
            print("\n!!! Start of L%s Min Sup !!!\n" % apriori_idx)
            L2 = copy.deepcopy(C2)
            for C2_word, C2_count in C2.items():
                if(C2_count < min_sup):
                    L2.pop(C2_word)
            
            self.L_list.append(L2)
            print("L%s : %s" % (apriori_idx , L2) ) 
            print("\n!!! End of L%s Min Sup !!!\n" % apriori_idx)
            
            
            #print("\n!!! Start of Stop Regulation !!!\n")
            if(len(L2) == 0):
                break
            
            L1 = L2
        
        
        print("\n!!! End of Apriori Pattern !!!\n")
        print("C List")
        for row in self.C_list:
            print("\t%s" % row)
        print("L List")
        for row in self.L_list:
            print("\t%s" % row)
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
    minimum_support_threshold = 2
    
    #Compared Two Train about C3 ( Proned or Not Proned C3 in order to compred with min support)
    #And also the Same Result in L3
    apriori.train(x_train, minimum_support_threshold)
    #apriori.train_joined_proned(x_train, minimum_support_threshold)
    
    pass

