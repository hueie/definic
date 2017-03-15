import pandas as pd
import numpy as np
from sklearn import tree
from collections import Counter
from scipy.spatial import distance
import copy
from astropy.wcs.docstrings import row

class Fptree:
    #Frequent Pattern Tree
    #Using Apriori (Frequent Itemsets)
    
    def __init__(self):
        self.x_train = None
        
        self.min_sup = 0.0  #minimum support threshold
        self.itr_cnt = 1
        self.L_list = []  #Apriori property ( Itemset satisfies the minimum support threshold ) how Lk-1 is used to find Lk for k >= 2
        self.C_list = []
        
        self.min_conf = 0.0 #minimum confidence threshold
        self.freqItemSubset_list = []
        self.output = []
        
        
        self.basis_order = []
        self.sorted_L_list=[]
        self.tree = None
        pass
    
    def train(self, x_train, min_sup=None, min_conf=None):
        self.apriori_joined_proned(x_train, minimum_support_threshold)
        #self.generating_associationrules(min_conf)
        self.basic_fp_growth()
        pass
    
    def basic_fp_growth(self):
        print("!!! FP Tree growth !!!")
        for rowdict in self.L_list:
            tmplist = sorted(rowdict.items() , key=lambda x: x[1], reverse=True)
            #tmplist.reverse()
            self.sorted_L_list.append(tmplist)
        
        
        basis_order = [ set(key).pop() for key, value in self.sorted_L_list[0]]
        self.basis_order = basis_order
        print(basis_order)
        
        #Preparing Empty Tree Including Null Root 
        '''
        tree = []
        for idx in range(len(basis_order)+1):
            tmplist = []
            for jdx in range(len(basis_order)+1):
                tmplist.append(0.0)
            
            tree.append(tmplist)

        tree = np.array(tree)
        '''
        tree = np.zeros( (len(basis_order)+1, len(basis_order)+1) , dtype=np.float64)
        
        #print("\t", self.L_list[0][ frozenset({'I2'}) ])
        
        print("\n!!! Failed Graph !!!\n")
        for x_dict in self.x_train:
            prev_node_num = 0
            for cur_node_num, cmp_value in enumerate(basis_order):
                for row in list(list(x_dict.values())[0]):
                    if(cmp_value == row):
                        cur_node_num += 1 #Becuase of Null Root
                        if(tree[prev_node_num][cur_node_num] == 0):
                            tree[prev_node_num][cur_node_num] = 1
                        else:
                            tree[prev_node_num][cur_node_num] += 1
                            
                        prev_node_num = cur_node_num
        
        print(tree)
        #This Graph is False, Because 0->I1->I3 and 0->I2->I1->I3 cannot be distinguished. Also Count is Accumulated in tree[I1][I3] sameplace.
        
        print("\n!!! Successful Graph Using Linked Nodes !!!\n")
        linked_node = []
        for x_dict in self.x_train:
            prev_node_num = 0
            
            tmplist = []
            for cur_node_num, cmp_value in enumerate(basis_order):
                for row in list(list(x_dict.values())[0]):
                    if(cmp_value == row):
                        tmplist.append(row)
                            
            linked_node.append(tmplist)            
        
        print(linked_node)
        pass
    
    def generating_subset(self, destset, srcset):
        if(len(destset) == 0):
            self.freqItemSubset_list = []
            
        if(destset not in self.freqItemSubset_list):
            self.freqItemSubset_list.append(destset)
            #To do Your Method
            for element in list(srcset):
                copied_srcset = copy.deepcopy(srcset)
                copied_srcset.remove(element)
                copied_destset = copy.deepcopy(destset)
                copied_destset.add(element)
                self.generating_subset(copied_destset, copied_srcset )
        else:
            pass
        
    
    def generating_associationrules(self, min_conf=None):
        if(min_conf == None):
            #70% To choose strong rules for output, unlike conventional classification rules, association rules can contain more than one conjunct
            min_conf = 0.7
            
        self.min_conf = min_conf 
        
        
        #Select the most frequent itemset
        freqItemSet = copy.deepcopy(self.L_list[-2])
        
        lineared_L_list = {}
        for x in self.L_list:
            lineared_L_list.update(x.copy())
        print(lineared_L_list)
        
        for freqItem in freqItemSet:
            #Generating Subset From The Most Frequent Itemset
            print("\n!!! Frequent Item : %s !!!\n" % freqItem)
            self.generating_subset( set({}), set(freqItem) )
            #print(associationrules.freqSubset_list)
            
            for freqItemSubset_element in self.freqItemSubset_list:
                #print("\t",freqItem, freqItemSubset_element)
                if(len(freqItem) == 0 or len(freqItemSubset_element) == 0 ):
                    #The nonempty subsets of freqItem
                    pass
                elif(freqItem == freqItemSubset_element):
                    pass
                elif( freqItemSubset_element.issubset(freqItem) ):
                    #print(element, freqItem)
                    A = copy.deepcopy(freqItemSubset_element)
                    B = copy.deepcopy(freqItem) - A
                    AB = A|B
                    sup_cnt_AB = lineared_L_list[frozenset( AB )]
                    sup_cnt_A = lineared_L_list[frozenset( A )]
                    sup_cnt_B = lineared_L_list[frozenset( B )]
                    confidence = sup_cnt_AB / sup_cnt_A
                    print("%s => %s, Confidnece = %s/%s = %s%%" % (A, set(B), sup_cnt_AB, sup_cnt_A, confidence*100 ))
                    
                    #If the confidence is larger than the minimum confidence threshold, then it is output!!.
                    if(confidence >= min_conf):
                        tmpdataset = {"A":A, "B":set(B), "sup_cnt_A":sup_cnt_A, "sup_cnt_B":sup_cnt_B, "sup_cnt_AB":sup_cnt_AB, "confidence":confidence}
                        self.output.append(tmpdataset)
                        pass
                    
        
        pass
    
    def apriori_joined_proned(self, x_train, min_sup):
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
    fptree = Fptree()
    #TID List of item IDs
    x_train=[ 
        {"T100" : {"I1", "I2", "I5"}},
        {"T200" : {"I2", "I4"}},
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
    minimum_confidence_threshold = 0.3 #Percentage
    
    fptree.train(x_train, minimum_support_threshold, minimum_confidence_threshold)

    
    pass

