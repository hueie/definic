import numpy as np
from scipy import stats
#from scipy.stats import mstats 
#import matplotlib.pylab as plb
import matplotlib.pyplot as plt

class Descriptive:
    def __init__(self):
        self.amean = 0.0,
        self.hmean = 0.0,
        self.gmean = 0.0,
        self.median = 0.0,
        self.mode = None,
        self.min = 0.0,
        self.max = 0.0,
        self.q1 = 0.0,
        self.q2 = 0.0,
        self.q3 = 0.0,
        self.var = 0.0,
        self.std = 0.0,
        self.cov = None,
        self.corr = 0.0,
        pass
    
    def calallstats(self, nparr1, nparr2=None):
        self.amean =    np.mean(nparr1)
        self.hmean = stats.hmean(nparr1)
        self.gmean = stats.gmean(nparr1)
        self.median =    np.median(nparr1)
        self.mode    = stats.mode(nparr1)
        self.min =    np.min(nparr1)
        self.max =    np.max(nparr1)
        self.q1 =    np.percentile(nparr1, 25)
        self.q2 =    np.percentile(nparr1, 50)
        self.q3 = np.percentile(nparr1, 75)
        self.var =    np.var(nparr1)
        self.std =    np.std(nparr1)
        self.cov =    np.cov(nparr1, nparr2)
        self.corr =    np.correlate(nparr1, nparr2)
        
        pass


if __name__ == "__main__":
    arr1 = [1,1,2,2,2,3,3,3,3,4,5,6,6,6,6,6,8,8,8,8,10,10]
    arr2 = [51,51,52,52,52,53,53,53,53,54,55,56,56,56,56,56,58,58,58,58,510,510]
    nparr1 = np.array(arr1)
    nparr2 = np.array(arr2)
    
    print("median : ", np.median(nparr1))
    print("arithmetic mean : ", np.mean(nparr1))
    print("harmonic mean : ", stats.hmean(nparr1))
    print("geometric mean : ", stats.gmean(nparr1))
    print("mode : ", stats.mode(nparr1))
    
    print("min : ", np.min(nparr1))
    print("percentile Q1 : ", np.percentile(nparr1, 25))
    print("percentile Q2 : ", np.percentile(nparr1, 50))
    print("percentile Q3 : ", np.percentile(nparr1, 75))
    print("max : ", np.max(nparr1))
    
    print("variance : ", np.var(nparr1))
    print("standard deviaion : ", np.std(nparr1))
    
    print("covariance : ", np.cov(nparr1, arr2))
    print("correlate : ", np.correlate(nparr1, arr2))
    
    
    stats.probplot(nparr1, dist="norm", plot=plt)
    plt.show()
    
    plt.hist(nparr1)
    plt.title("Gaussian Histogram") ; plt.xlabel("Value") ; plt.ylabel("Frequency")
    plt.show()
    
    plt.plot(nparr1, linestyle='dotted', color='k')
    plt.show()
    
    plt.plot(nparr1, linestyle='solid')
    plt.show()
    
    plt.plot(nparr1, '*', color='g')
    plt.show()
    
    pass