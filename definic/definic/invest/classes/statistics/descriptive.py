import numpy as np
from scipy.stats import hmean, gmean
#from scipy.stats.mstats import *

class Descriptive:
    def __init__(self):
        pass
    
    
if __name__ == "__main__":
    #http://www.marsja.se/pandas-python-descriptive-statistics/
    arr = np.array([1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 9, 9, 9, 9, 9, 9, 17])
    print( np.min(arr) )
    print( np.mean(arr) )
    print( np.median(arr) )
    
    print( np.max(arr) )
    np.mean(arr)
    gmean(arr)


    stats.hmean(arr)    #Arithmetic mean (“average”) of data.
    hmean(arr)    #Harmonic mean of data.
    median()    #Median (middle value) of data.
    median_low()    #Low median of data.
    median_high()    #High median of data.
    median_grouped()    #Median, or 50th percentile, of grouped data.
    mode()
    
    print("out")
    pass