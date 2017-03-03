import pandas as pd
import numpy as np
from sklearn import tree
from collections import Counter
import math
import copy

class Backpropagation:
    def __init__(self):
        self.weight = None
        self.bias = None
        self.learning_rate = None
        self.each_layer_unit = None
        pass
    
    def train(self, x_train, y_train, w, b, elu, l_r=None):
        num_of_train = len(x_train)
        print("num_of_train :", num_of_train)
        
        learning_rate = l_r
        if(learning_rate == None):
            if(num_of_train == 1):
                learning_rate = 0.9 # In Example
            else:
                learning_rate = 1/num_of_train # arule of thumb
            print("learning_rate : None, ", learning_rate)
        else:        
            print("learning_rate :", learning_rate)
        
        
        #Initialize all weights and biases in network;
        each_layer_unit = elu
        total_layer_len = len(each_layer_unit)
        total_unit_cnt = np.sum(each_layer_unit)
        
        terminating_condition = False;
        
        while terminating_condition is not True:
            for x_train_idx, row in enumerate(x_train):
                print("\n!!! Start of %s x train : %s , y train : %s !!!\n" % (x_train_idx, row, y_train[x_train_idx]) ) 
                print("\n!!! Start of Train Input and Output Calculations !!!\n")   
                #!!! Start of Net Input and Output Calculations
                O = np.array([0.0]*total_unit_cnt) # Must use 0.0 float
                I = np.array([0.0]*total_unit_cnt)
                Err = np.array([0.0]*total_unit_cnt)
                
                prev_layer_unit_cnt = 0
                for idx, current_layer_unit_cnt in enumerate(each_layer_unit):
                    print("\n[%s Layer]" % (idx) , end="")
                    print(" Output of Units %s ~ %s" % (prev_layer_unit_cnt, prev_layer_unit_cnt + current_layer_unit_cnt - 1))
                        
                    if (idx == 0): #Stating at Input layer
                        for i in range(0,len(row)):
                            I[i] = copy.deepcopy(row[i])

                        O = copy.deepcopy(I)  # output of an input unit is its actual input value
                        prev_layer_unit_cnt = current_layer_unit_cnt
                    else: #Propagate the inputs forward:
                        for j_unit in range(prev_layer_unit_cnt, prev_layer_unit_cnt + current_layer_unit_cnt):
                            print("Output of Unit %s : " % j_unit)
                            for i_unit in range(0, prev_layer_unit_cnt):
                                if(w[i_unit][j_unit] == 0):
                                    continue
                                
                                weighted_output = w[i_unit][j_unit] * O[i_unit]
                                print("\tWeighted Output %s -> %s : Weight * Output = %s * %s = %s" % (i_unit, j_unit, w[i_unit][j_unit], O[i_unit], weighted_output))
                                I[j_unit] = I[j_unit] + weighted_output# compute the net input of unit j with respect to the previous layer, i
                                
                                
                            print("Adding Bias : Integraged Weighted Output + Bias[%s] = %s + %s" % (j_unit, I[j_unit], b[j_unit]) , end="")
                            I[j_unit] = I[j_unit] + b[j_unit]  #Add Bias
                            print(" = %s" % I[j_unit])
                            O[j_unit] = 1 / ( 1 + math.exp(-I[j_unit]) ) # compute the output of each unit j
                            print("\nProcessed Input : %s \nProcessed Output : %s \n" % (I, O) )
                                    
                        prev_layer_unit_cnt = prev_layer_unit_cnt + current_layer_unit_cnt
                #!!! End of Train Input and Output Calculations
                
                
                print("\n!!! Start of Backpropagate the errors !!!\n")    
                #!!! Start of Backpropagate the errors:
                each_layer_unit.reverse() #; print(each_layer_unit)
                prev_layer_unit_cnt = 0
                for idx, current_layer_unit_cnt in enumerate(each_layer_unit):
                    print("\n[%s Layer]" % (total_layer_len - idx -1) , end="")
                    print(" Error of Units %s ~ %s" % (total_unit_cnt - prev_layer_unit_cnt - current_layer_unit_cnt, total_unit_cnt - prev_layer_unit_cnt - 1))
                    
                    if (idx == 0): #Stating at Output layer
                        print("Error of Unit %s : " % (total_unit_cnt-1) )
                        Err[-1] = O[-1] * (1 - O[-1]) * ( y_train[x_train_idx] - O[-1] )# compute the error
                        print("\tError[%s] : %s" % (j_unit, Err[-1]) )
                        prev_layer_unit_cnt = current_layer_unit_cnt
                    
                    else :
                        for j_unit in range(total_unit_cnt - prev_layer_unit_cnt - current_layer_unit_cnt  , total_unit_cnt - prev_layer_unit_cnt):
                            print("Error of Unit %s : " % j_unit)
                            for k_unit in range(prev_layer_unit_cnt, total_unit_cnt):
                                if(w[j_unit][k_unit] == 0):
                                    continue

                                weighted_error = w[j_unit][k_unit] * Err[k_unit]
                                print("\tWeighted Error %s <- %s : Weight * Err[%s] = %s * %s = %s" % (j_unit, k_unit, k_unit, Err[k_unit], w[j_unit][k_unit], weighted_error))
                                Err[j_unit] = Err[j_unit] + weighted_error # compute the error with respect to the next higher layer, k
                            
                            print("Using the derivative of the logistic func : O * (1-O) * Err[%s] = %s * %s * %s" % (j_unit, O[j_unit], (1 - O[j_unit]), Err[j_unit]) , end="")
                            Err[j_unit] = O[j_unit] * (1 - O[j_unit]) * Err[j_unit]
                            print(" = %s" % Err[j_unit])
                            
                        prev_layer_unit_cnt = prev_layer_unit_cnt + current_layer_unit_cnt
                #!!! End of Backpropagate the errors:    
                
                
                print("\n!!! Start of Updating Weight or Bias !!!\n")
                #!!! Start of Adjusting Backpropagation Algorithm
                each_layer_unit.reverse()
                prev_layer_unit_cnt=0
                for idx, current_layer_unit_cnt in enumerate(each_layer_unit):
                    print("\n[%s Layer]" % (idx) , end="")
                    print(" Update of Units %s ~ %s" % (prev_layer_unit_cnt, prev_layer_unit_cnt + current_layer_unit_cnt - 1))
                    
                    if (idx == 0): #Stating at Input layer
                        prev_layer_unit_cnt = current_layer_unit_cnt
                    
                    else :
                        for j_unit in range(prev_layer_unit_cnt, prev_layer_unit_cnt + current_layer_unit_cnt ):
                            print("Update of Unit %s : " % j_unit)
                            for i_unit in range(prev_layer_unit_cnt):
                                if(w[i_unit][j_unit] == 0):
                                    #print("A Unit From %s To %s : These Two Units are not connected!!!" % (i_unit, j_unit))
                                    continue
                                    
                                delta_w = learning_rate * Err[j_unit] * O[i_unit] # weight increment
                                print("\tDelta Weight %s -> %s : learning_rate * O[%s] * Err[%s] = %s * %s * %s = %s" % (i_unit, j_unit, i_unit, j_unit, learning_rate, Err[j_unit], O[i_unit], delta_w))
                                w[i_unit][j_unit] = w[i_unit][j_unit] +  delta_w # weight update
                            
                            print("Weight Update : Integraged Delta Weighted + Weight[%s] = %s" % (j_unit, w[i_unit][j_unit]))
                            
                            delta_b = learning_rate * Err[j_unit] # bias increment
                            print("\tDelta Bias %s : learning_rate * Error[%s] = %s * %s = %s" % (j_unit, j_unit, learning_rate, Err[j_unit], delta_b))
                            print("Delta Bias Update : Bias[%s] + Delta Bias = %s * %s" % (j_unit, b[j_unit], delta_b), end="")
                            b[j_unit] = b[j_unit] + delta_b # bias update
                            print(" = %s" % b[j_unit])
                                                    
                        prev_layer_unit_cnt = prev_layer_unit_cnt + current_layer_unit_cnt
                
                #!!! End of Adjusting Backpropagation Algorithm
                print("\n!!! End of %s x train : %s , y train : %s !!!\n" % (x_train_idx, row, y_train[x_train_idx]) ) 
                
                          
            print("\n!!! Start of Terminating condition !!!\n")
            #!!! Start of Terminating condition
            if(True):
                terminating_condition = True
                '''
                1) All delta_w[i][j] in the previous epoch are so small as to be below some specified threshold
                2) The percentage of tuples misclassified in the previous epoch is below some threshold
                3) A prespecified number of epochs has expired.
                '''
            #!!! End of Terminating condition
        
        print("\n!!! Start of Modeling Assessment !!!\n")
        #!!! Start of Modeling Assessment
        print("Learning Rate", learning_rate)
        print("Weight Graph", w)
        print("Bias", b)
        #!! End of Modeling Assessment    
        
        self.learning_rate = learning_rate
        self.weight = w
        self.bias = b
        self.each_layer_unit = each_layer_unit
        
        print("\n!!! End of Propagation Modeling !!!\n")
        pass
    
    def test(self, x_train):
        total_unit_cnt = np.sum(self.each_layer_unit)
        print("\n!!! Start of Test Input and Output Calculations !!!\n")   
        #!!! Start of Net Input and Output Calculations
        O = np.array([0.0]*total_unit_cnt) # Must use 0.0 float
        I = np.array([0.0]*total_unit_cnt)
        
        prev_layer_unit_cnt = 0        
        for d_idx, row in enumerate(x_train):        
            for idx, current_layer_unit_cnt in enumerate(self.each_layer_unit):
                if (idx == 0): #Stating at Input layer
                    for i in range(0,len(row)):
                        I[i] = copy.deepcopy(row[i])
                        
                    O = copy.deepcopy(I)  # output of an input unit is its actual input value
                    prev_layer_unit_cnt = current_layer_unit_cnt
    
                else: #Propagate the inputs forward:
                    for j_unit in range(prev_layer_unit_cnt, prev_layer_unit_cnt + current_layer_unit_cnt):
                        for i_unit in range(0, prev_layer_unit_cnt):
                            I[j_unit] = I[j_unit] + self.weight[i_unit][j_unit] * O[i_unit]# compute the net input of unit j with respect to the previous layer, i
                                    
                        I[j_unit] = I[j_unit] + self.bias[j_unit]  #Add Bias
                        O[j_unit] = 1 / ( 1 + math.exp(-I[j_unit]) ) # compute the output of each unit j
                                
                    prev_layer_unit_cnt = prev_layer_unit_cnt + current_layer_unit_cnt
            #!!! End of Test Input and Output Calculations
        
        print("Processed Input : ", I)
        print("Processed Output : ", O)
        print("Classified Result : ", O[-1])   
        print("\n!!! End of Test Input and Output Calculations !!!\n")   
        
        pass
    
    
    def train_example(self):
        x1=1; x2=0; x3=1; y=1; 
        D=[ [x1, x2, x3] ]
        
        num_of_train = len(D)
        print("num_of_train : %s", num_of_train)
        if(num_of_train == 1):
            l_r = 0.9 # In Example
        else:
            l_r = 1/num_of_train # arule of thumb
        print("learning_rate : %s", l_r)
        
        
        #Initialize all weights and biases in network;
        w14=0.2; w15=-0.3; w24=0.4; w25=0.1; 
        w34=-0.5; w35=0.2; w46=-0.3; w56=-0.2
        b4=-0.4; b5=0.2; b6=0.1
        
        w = [ [0, 0, 0, w14, w15, 0],
              [0, 0, 0, w24, w25, 0],
              [0, 0, 0, w34, w35, 0],
              [0, 0, 0,  0,  0, w46],
              [0, 0, 0,  0,  0, w56],
              [0, 0, 0,  0,  0,   0] ]
        b = [0, 0, 0, b4, b5, b6]
        
        each_layer_unit = [3, 2, 1]
        total_unit_cnt = np.sum(each_layer_unit)
        
        terminating_condition = False;
        
        while terminating_condition is not True:
            for d_idx, row in enumerate(D):
                
                print("\n!!! Start of Train Input and Output Calculations !!!\n")   
                #!!! Start of Net Input and Output Calculations
                O = np.array([0.0]*total_unit_cnt) # Must use 0.0 float
                I = np.array([0.0]*total_unit_cnt)
                Err = np.array([0.0]*total_unit_cnt)
                
                
                for idx, current_layer_unit_cnt in enumerate(each_layer_unit):
                    print("current_layer_unit_cnt : ", current_layer_unit_cnt)
                    if (idx == 0): #Stating at Input layer
                        for i in range(0,len(row)):
                            I[i] = copy.deepcopy(row[i])

                        O = copy.deepcopy(I)  # output of an input unit is its actual input value
                        prev_layer_unit_cnt = current_layer_unit_cnt

                    else:#Propagate the inputs forward:
                        print("Units From :", prev_layer_unit_cnt, "To :", prev_layer_unit_cnt + current_layer_unit_cnt)
                        for j_unit in range(prev_layer_unit_cnt, prev_layer_unit_cnt + current_layer_unit_cnt):
                            for i_unit in range(0, prev_layer_unit_cnt):
                                print("A Unit From %s To %s : Weight %s * Output %s" % (i_unit, j_unit, w[i_unit][j_unit], O[i_unit]))
                                I[j_unit] = I[j_unit] + w[i_unit][j_unit] * O[i_unit]# compute the net input of unit j with respect to the previous layer, i
                                
                            print("Add Bias to Unit : %s + %s =" % (I[j_unit], b[j_unit]) , end="")
                            I[j_unit] = I[j_unit] + b[j_unit]  #Add Bias
                            print("", I[j_unit])
                            O[j_unit] = 1 / ( 1 + math.exp(-I[j_unit]) ) # compute the output of each unit j
                            
                            print("Processed Input : ", I)
                            print("Processed Output : ", O)
                                    
                        prev_layer_unit_cnt = prev_layer_unit_cnt + current_layer_unit_cnt
                #!!! End of Train Input and Output Calculations
                
                
                print("\n!!! Start of Backpropagate the errors !!!\n")    
                #!!! Start of Backpropagate the errors:
                each_layer_unit.reverse() #; print(each_layer_unit)
                for idx, current_layer_unit_cnt in enumerate(each_layer_unit):
                    if (idx == 0): #Stating at Output layer
                        Err[j_unit] = O[j_unit] * (1 - O[j_unit]) * (y - O[j_unit])# compute the error
                        print("Err[%s] = %s" % (j_unit, Err[j_unit]) )
                        prev_layer_unit_cnt = current_layer_unit_cnt
                    
                    else :
                        print("Units From :", total_unit_cnt - prev_layer_unit_cnt - current_layer_unit_cnt, "To :", total_unit_cnt - prev_layer_unit_cnt)
                        for j_unit in range(total_unit_cnt - prev_layer_unit_cnt - current_layer_unit_cnt  , total_unit_cnt - prev_layer_unit_cnt):
                            for k_unit in range(prev_layer_unit_cnt, total_unit_cnt):
                                print("A Unit From %s To %s : Err[%s] %s * Weight %s" % (j_unit, k_unit, k_unit, Err[k_unit], w[j_unit][k_unit]))
                                Err[j_unit] = Err[j_unit] + Err[k_unit] * w[j_unit][k_unit] # compute the error with respect to the next higher layer, k
                            
                            print("Err[%s] = O*(1-O)*Err = %s * %s * %s = " % (j_unit, O[j_unit], (1 - O[j_unit]), Err[j_unit]) , end="")
                            Err[j_unit] = O[j_unit] * (1 - O[j_unit]) * Err[j_unit]
                            print("", Err[j_unit])
                            
                        prev_layer_unit_cnt = prev_layer_unit_cnt + current_layer_unit_cnt
                #!!! End of Backpropagate the errors:    
                
                
                print("\n!!! Start of Adjusting Backpropagation Algorithm !!!\n")
                #!!! Start of Adjusting Backpropagation Algorithm
                each_layer_unit.reverse()
                for idx, current_layer_unit_cnt in enumerate(each_layer_unit):
                    if (idx == 0): #Stating at Input layer
                        prev_layer_unit_cnt = current_layer_unit_cnt
                    
                    else :
                        print("Units From :", prev_layer_unit_cnt, "To :", prev_layer_unit_cnt + current_layer_unit_cnt)
                        for j_unit in range(prev_layer_unit_cnt, prev_layer_unit_cnt + current_layer_unit_cnt ):
                            for i_unit in range(prev_layer_unit_cnt):
                                if(w[i_unit][j_unit] == 0):
                                    print("A Unit From %s To %s : These Two Units are not connected!!!" % (i_unit, j_unit))
                                    continue
                                    
                                print("A Unit From %s To %s : delta_w[%s][%s] = " % (i_unit, j_unit, i_unit, j_unit), end="")
                                delta_w = l_r * Err[j_unit] * O[i_unit] # weight increment
                                print("learning_rate * Err[%s] * O[%s] = %s * %s * %s" % (j_unit, i_unit, l_r, Err[j_unit], O[i_unit]))
                                print("w[%s][%s] = w[%s][%s] + delta_w = %s + %s" % (i_unit, j_unit, i_unit, j_unit, w[i_unit][j_unit], delta_w), end="")
                                w[i_unit][j_unit] = w[i_unit][j_unit] +  delta_w # weight update
                                print(" = %s" % (w[i_unit][j_unit]))
                            
                            print()       
                            delta_b = l_r * Err[j_unit] # bias increment
                            print("delta_b[%s] = learning_rate * Err[%s] = %s * %s = %s" % (j_unit, j_unit, l_r, Err[j_unit], delta_b))
                            print("b[%s] = b[%s] * delta_b[%s] = %s * %s" % (j_unit, j_unit, j_unit, b[j_unit], delta_b), end="")
                            b[j_unit] = b[j_unit] + delta_b # bias update
                            print(" =", b[j_unit])
                            print()
                                                    
                        prev_layer_unit_cnt = prev_layer_unit_cnt + current_layer_unit_cnt
                
                #!!! End of Adjusting Backpropagation Algorithm
                
                          
            print("\n!!! Start of Terminating condition !!!\n")
            #!!! Start of Terminating condition
            if(True):
                terminating_condition = True
                '''
                1) All delta_w[i][j] in the previous epoch are so small as to be below some specified threshold
                2) The percentage of tuples misclassified in the previous epoch is below some threshold
                3) A prespecified number of epochs has expired.
                '''
            #!!! End of Terminating condition
        
        print("\n!!! Start of Modeling Assessment !!!\n")
        #!!! Start of Modeling Assessment
        print("Learning Rate", l_r)
        print("Weight Graph", w)
        print("Bias", b)
        #!! End of Modeling Assessment    
        
        self.learning_rate = l_r
        self.weight = w
        self.bias = b
        self.each_layer_unit = each_layer_unit
        
        print("\n!!! End of Propagation Modeling !!!\n")
        
        pass
    
    def test_example(self):
        x1=1; x2=0; x3=1; 
        D=[ [x1, x2, x3] ]
        
        total_unit_cnt = np.sum(self.each_layer_unit)
        
        print("\n!!! Start of Test Input and Output Calculations !!!\n")   
        #!!! Start of Net Input and Output Calculations
        O = np.array([0.0]*total_unit_cnt) # Must use 0.0 float
        I = np.array([0.0]*total_unit_cnt)
                
        for d_idx, row in enumerate(D):        
            for idx, current_layer_unit_cnt in enumerate(self.each_layer_unit):
                if (idx == 0): #Stating at Input layer
                    for i in range(0,len(row)):
                        I[i] = copy.deepcopy(row[i])
                        
                    O = copy.deepcopy(I)  # output of an input unit is its actual input value
                    prev_layer_unit_cnt = current_layer_unit_cnt
    
                else: #Propagate the inputs forward:
                    for j_unit in range(prev_layer_unit_cnt, prev_layer_unit_cnt + current_layer_unit_cnt):
                        for i_unit in range(0, prev_layer_unit_cnt):
                            I[j_unit] = I[j_unit] + self.weight[i_unit][j_unit] * O[i_unit]# compute the net input of unit j with respect to the previous layer, i
                                    
                        I[j_unit] = I[j_unit] + self.bias[j_unit]  #Add Bias
                        O[j_unit] = 1 / ( 1 + math.exp(-I[j_unit]) ) # compute the output of each unit j
                                
                    prev_layer_unit_cnt = prev_layer_unit_cnt + current_layer_unit_cnt
            #!!! End of Test Input and Output Calculations
        
        print("Processed Input : ", I)
        print("Processed Output : ", O)
        print("Classified Result : ", O[-1])   
        
        pass

    
        
if __name__ == "__main__":
    backpropagation = Backpropagation()
    #backpropagation.train_example()
    #backpropagation.test_example()
    
    x1=1; x2=0; x3=1; y=1
    x_train=[]
    y_train=[]
    x_test=[[x1, x2, x3]]
    
    for idx in range(100):
        x_train.append([x1, x2, x3])
        y_train.append(y)
        
    print(x_train)
    print(y_train)
    
    
    
    w14=0.2; w15=-0.3; w24=0.4; w25=0.1; 
    w34=-0.5; w35=0.2; w46=-0.3; w56=-0.2
    b4=-0.4; b5=0.2; b6=0.1
        
    w = [ [0, 0, 0, w14, w15, 0],
          [0, 0, 0, w24, w25, 0],
          [0, 0, 0, w34, w35, 0],
          [0, 0, 0,  0,  0, w46],
          [0, 0, 0,  0,  0, w56],
          [0, 0, 0,  0,  0,   0] ]
    b = [0, 0, 0, b4, b5, b6]
    elu = [3, 2, 1]    
        
    backpropagation.train(x_train, y_train, w, b, elu)
    backpropagation.test(x_test)
    
    pass

