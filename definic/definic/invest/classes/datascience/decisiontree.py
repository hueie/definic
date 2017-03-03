import pandas as pd
import numpy as np
from sklearn import tree
from collections import Counter

class Decisiontree:
    def __init__(self):
        pass
    
    def entropy(self, x_train, y_train=None):
        ent = 0.0
        totlen = len(x_train)
        x_cnts = Counter(x_train)
        for x_word, x_count in x_cnts.items():
            #print(x_word, x_count)
            if y_train is None : #joint entropy
                x_ratio = (x_count/totlen)
                ent += -( x_ratio * np.log2( x_ratio ) )
            
            elif y_train is not None : #conditional entropy
                x_ratio = (x_count/totlen)
                subent = 0.0

                df = pd.concat([x_train, y_train], axis=1)
                y_cnts = Counter(y_train)
                for y_word, y_count in y_cnts.items():
                    #print(y_word, y_count)
                    #print(df[ df[x_train.name] == x_word ][ df[y_train.name] == y_word ])
                    
                    sublen = len(df[ df[x_train.name] == x_word ][ df[y_train.name] == y_word ])
                    if sublen == 0:
                        continue
                        
                    sub_ratio = (sublen/x_count)
                    subent += -( sub_ratio*np.log2(sub_ratio) )
                
                ent += x_ratio * subent
                            
        print('final entropy :',ent,'bits')
        return ent
    
    def prepruning(self):
        pass
    
    def postpruning(self):
        pass

    
class Id3(Decisiontree):
    def __init__(self):
        Decisiontree.__init__(self)
        gaindf = None
        treecond = None
        pass
    
    def informationgain(self, x_train, y_train):
        #print(x_train)
        #print(y_train)

        print('Gain_D')
        gain_d = self.entropy(y_train)
        
        gain_df = pd.DataFrame()
        for x_col in x_train:
            print(x_col)
            gain_sub = self.entropy(x_train[x_col], y_train )
            gain_cond = gain_d - gain_sub
            gain_df[x_col] = pd.Series(gain_cond)
        
        print('Gain_Dataframe')
        print(gain_df)
        
        maxcolname = ''
        max = 0.0
        for row in gain_df:
            if np.float(gain_df[row]) > max:
                maxcolname = row
                max = np.float(gain_df[row])
                
        print('max')
        print(max)
        
        self.gaindf = gain_df
        self.treecond = {maxcolname : max}
        return {maxcolname : max}
        
        #return {maxcolname : max}
        '''
        for cols in x_train.columns:
            lst = np.array(train[cols])
            self.entropy(lst)
        '''
    
class C45(Decisiontree):
    def __init__(self):
        Decisiontree.__init__(self)
        gaindf = None
        treecond = None
        pass    
    
    def gainratio(self, df):
        pass
        

class Cart(Decisiontree):
    def __init__(self):
        Decisiontree.__init__(self)
        gaindf = None
        treecond = None
        pass    
    
    def giniindex(self, df):
        pass
    
        
if __name__ == "__main__":
    train = pd.read_csv("AllElectronics_Customer_Database.csv")
    train = train.drop('RID', 1)
    x_train = train.drop('buys_computer',1)
    y_train = train['buys_computer']
    id3 = Id3()
    id3.informationgain(x_train, y_train)
    print(id3.gaindf)
    print(id3.treecond)
    pass
'''    
    x_train = []
    for row_idx in range(train.shape[0]):
        tmp = []
        tmp.append(train.loc[row_idx, 'age'])
        tmp.append(train.loc[row_idx, 'income'])
        tmp.append(train.loc[row_idx, 'student'])
        tmp.append(train.loc[row_idx, 'credit_rating'])
        
        x_train.append(tmp)
        
    x_train = np.array(x_train)
    y_train = np.array(train['buys_computer'])
    print(x_train) ; print(y_train)
'''    
    #clf = tree.DecisionTreeClassifier()
    # clf = clf.fit(x_train, y_train)
