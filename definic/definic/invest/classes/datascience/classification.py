import pandas as pd
import numpy as np
from sklearn import tree

if __name__ == "__main__":
    train = pd.read_csv("AllElectronics_Customer_Database.csv")
    print(train)
    
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
    
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x_train, y_train)
    pass