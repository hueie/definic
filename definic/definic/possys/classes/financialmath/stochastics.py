import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt

import scipy.stats as scs

def random_numbers():
    print(npr.rand(10))
    print(npr.rand(5,5))
    #interval a to b, 5 to 10
    a = 5; b=10
    print(npr.rand(10)*(b-a) + a)
    
    sample_size = 500
    rn1 = npr.rand(sample_size, 3)
    rn2 = npr.randint(0, 10, sample_size)
    rn3 = npr.sample(size = sample_size)
    a = [0, 25, 50, 75, 100]
    rn4 = npr.choice(a, size = sample_size)
    
    print("rn1 : %s" % rn1)
    print("rn2 : %s" % rn2)
    print("rn3 : %s" % rn3)
    print("rn4 : %s" % rn4)
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(7, 7))
    
    ax1.hist(rn1, bins=25, stacked=True) ; ax1.set_title("rand") ; ax1.set_ylabel("frequency") ; ax1.grid(False)
    ax2.hist(rn2, bins=25) ; ax2.set_title("randint") ; ax2.grid(True)
    ax3.hist(rn3, bins=25) ; ax3.set_title("sample") ; ax3.set_ylabel("frequency")
    ax4.hist(rn4, bins=25) ; ax4.set_title("choice") ; ax4.grid(True)
    plt.show()
    
    #distributions
    sample_size = 500
    rn1 = npr.standard_normal(sample_size)
    rn2 = npr.normal(100, 20, sample_size)
    rn3 = npr.chisquare(df=0.5, size=sample_size)
    rn4 = npr.poisson(lam=1.0, size=sample_size)
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(10,10))
    ax1.hist(rn1, bins=25) ; ax1.set_title("standard normal") ; ax1.set_ylabel("frequency") ; ax1.grid(True)
    ax2.hist(rn2, bins=25) ; ax2.set_title("normal(100, 20)") ; ax2.set_xlabel("hi") ; ax2.grid(True)
    ax3.hist(rn3) ; ax3.set_title("chi square") ; ax3.set_ylabel("frequency") ; ax3.grid(True)
    ax4.hist(rn4, bins=100) ; ax4.set_title("Poisson")
    plt.show()
    pass

class Stochastics:
    def __init__(self):
        pass
    
    def bsm_call_value(self, S0, K, T, r, sigma):
        """ 
        Valuation of European call option in BSM model.
        Analytical formula.
        Parameters
        ==========
        S0 : float
        initial stock/index level
        K : float
        strike price
        T : float
        maturity date (in year fractions)
        r : float
        constant risk-free short rate
        sigma : float
        volatility factor in diffusion term
        Returns
        =======
        value : float
        present value of the European call option
        """
        from math import log, sqrt, exp
        from scipy import stats
        S0 = float(S0)
        d1 = (log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
        d2 = (log(S0 / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
        value = (S0 * stats.norm.cdf(d1, 0.0, 1.0)
        - K * exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0))
        # stats.norm.cdf —> cumulative distribution function
        # for normal distribution
        return value
    
    # Vega function
    def bsm_vega(self, S0, K, T, r, sigma):
        """ Vega of European option in BSM model.
        Parameters
        ==========
        S0 : float
        initial stock/index level
        K : float
        strike price
        T : float
        maturity date (in year fractions)
        r : float
        constant risk-free short rate
        sigma : float
        volatility factor in diffusion term
        Returns
        =======
        vega : float
        partial derivative of BSM formula with respect
        to sigma, i.e. Vega
        """
        from math import log, sqrt
        from scipy import stats
        S0 = float(S0)
        d1 = (log(S0 / K) + (r + 0.5 * sigma ** 2) * T / (sigma * sqrt(T)))
        vega = S0 * stats.norm.cdf(d1, 0.0, 1.0) * sqrt(T)
        return vega   
    
    def bsm_call_imp_vol(self, S0, K, T, r, C0, sigma_est, it=100):
        """ 
        Implied volatility of European call option in BSM model.
        Parameters
        ==========
        S0 : float
        initial stock/index level
        K : float
        strike price
        T : float
        maturity date (in year fractions)
        r : float
        constant risk-free short rate
        sigma_est : float
        estimate of impl. volatility
        it : integer
        number of iterations
        Returns
        =======
        simga_est : float
        numerically estimated implied volatility
        """
        for i in range(it):
            sigma_est -= ((self.bsm_call_value(S0, K, T, r, sigma_est) - C0) / self.bsm_vega(S0, K, T, r, sigma_est))
        return sigma_est
    
    def example_VSTOXX_index(self):
        V0 = 17.6639
        r = 0.01
        import pandas as pd
        h5 = pd.HDFStore("./vstoxx_data_31032014.h5", "r")
        futures_data = h5["futures_data"] # VSTOXX futures data
        options_data = h5["options_data"] # VSTOXX call option data
        h5.close()
        
        print(futures_data)
        options_data.info()
        options_data[["DATE", "MATURITY", "TTM", "STRIKE", "PRICE"]].head()
        
        options_data["IMP_VOL"] = 0.0
        # new column for implied volatilities
        # from bsm_functions import *
        tol = 0.5 # tolerance level for moneyness
        for option in options_data.index:
            # iterating over all option quotes
            forward = futures_data[ futures_data["MATURITY"] == options_data.loc[option]["MATURITY"] ] ["PRICE"].values[0]
            # picking the right futures value
            if (forward * (1 - tol) < options_data.loc[option]["STRIKE"] < forward * (1 + tol)):
            # only for options with moneyness within tolerance
                imp_vol = self.bsm_call_imp_vol(
                    V0, # VSTOXX value
                    options_data.loc[option]["STRIKE"],
                    options_data.loc[option]["TTM"],
                    r, # short rate
                    options_data.loc[option]["PRICE"],
                    sigma_est=2., # estimate for implied volatility
                    it=100)
                options_data["IMP_VOL"].loc[option] = imp_vol
        
        futures_data["MATURITY"]    
        options_data.loc[46170]
        options_data.loc[46170]["STRIKE"]
        plot_data = options_data[options_data["IMP_VOL"] > 0]
        maturities = sorted(set(options_data["MATURITY"]))
        print(maturities)
        
        plt.figure(figsize=(8, 6))
        for maturity in maturities:
            data = plot_data[options_data.MATURITY == maturity]
            # select data for this maturity
            plt.plot(data["STRIKE"], data["IMP_VOL"], label=maturity.timestamp(), lw=1.5)
            plt.plot(data["STRIKE"], data["IMP_VOL"], "r.")
        plt.grid(True)
        plt.xlabel("strike")
        plt.ylabel("implied volatility of volatility")
        plt.legend()
        plt.show()
        
        
        keep = ["PRICE", "IMP_VOL"]
        group_data = plot_data.groupby(["MATURITY", "STRIKE"])[keep]
        print(group_data)
        group_data = group_data.sum()
        group_data.head()
        group_data.index.levels
        
        pass
    
    
    
    def print_statistics(self, a1, a2):
        sta1 = scs.describe(a1)
        sta2 = scs.describe(a2)
        print("%14s %14s %14s" % ("statistic", "data set 1", "data set 2") )
        print(45 * "-")
        print("%14s %14.3f %14.3f" % ("size", sta1[0], sta2[0]))
        print("%14s %14.3f %14.3f" % ("min", sta1[1][0], sta2[1][0]))
        print("%14s %14.3f %14.3f" % ("max", sta1[1][1], sta2[1][1]))
        print("%14s %14.3f %14.3f" % ("mean", sta1[2], sta2[2]))
        print("%14s %14.3f %14.3f" % ("std", np.sqrt(sta1[3]), np.sqrt(sta2[3])) )
        print("%14s %14.3f %14.3f" % ("skew", sta1[4], sta2[4]) )
        print("%14s %14.3f %14.3f" % ("kurtosis", sta1[5], sta2[5]) )
        pass
    
    #Stochastic Processes
    def black_scholes_merton_simulation(self):
        #Simulating future index level in Black-Scholes-Merton setup
        
        S0 = 100 #initial value
        r = 0.05 # constant short rate
        sigma = 0.25 # constant volatility
        T = 2.0 # in years
        I = 10000 # number of random draws
        z = npr.standard_normal(I)
        
        delta_S = r-(1/2)*np.power(sigma,2)*T  +  sigma*np.power(T,1/2) * z
        ST1 = S0 * np.exp( delta_S )
        
        #plt.hist(ST1, bins = 50) ; plt.xlabel("index level") ; plt.ylabel("frequency") ; plt.grid(True)
        #plt.show()
        
        ST2 = S0 * npr.lognormal( (r-0.5*sigma**2)*T, sigma*np.sqrt(T), size = I)
        
        z = npr.normal( (r-0.5*sigma**2)*T, sigma*np.sqrt(T), size = I )
        delta_S = r-(1/2)*np.power(sigma,2)*T  +  sigma*np.power(T,1/2) * z
        ST3 = S0 * np.exp( delta_S )
        
        z = npr.normal( (r-0.5*sigma**2)*T, sigma*np.sqrt(T), size = I )
        delta_S = z
        ST4 = S0 * np.exp( delta_S )
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(10,10))
        ax1.hist(ST1, bins=25) ; ax1.set_title("exp ** standard normal") ; ax1.set_xlabel("index level") ; ax1.set_ylabel("frequency") ; ax1.grid(True)
        ax2.hist(ST2, bins=25) ; ax2.set_title("log normal") ; ax2.set_xlabel("index level") ; ax2.set_ylabel("frequency") ; ax2.grid(True)
        ax3.hist(ST3, bins=25) ; ax3.set_title("exp ** normal") ; ax3.set_xlabel("index level") ; ax3.set_ylabel("frequency") ; ax3.grid(True)
        ax4.hist(ST4, bins=25) ; ax4.set_title("normal") ; ax4.set_xlabel("index level") ; ax4.set_ylabel("frequency") ; ax4.grid(True)
        plt.show()
        
        self.print_statistics(ST1, ST2)
        self.print_statistics(ST3, ST4)
        pass
    
    def black_scholes_merton_dynamically_simulation(self):
        #Simulating future index levels !!!dynamically!!! in Black-Scholes-Merton setup
        
        S0 = 100 #initial value
        r = 0.05 # constant short rate
        sigma = 0.25 # constant volatility
        T = 2.0 # in years
        
        I = 10000
        M = 50
        dt = T / M
        S = np.zeros((M + 1, I))
        S[0] = S0
        for t in range(1, M + 1):
            S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt 
                    + sigma * np.sqrt(dt) * npr.standard_normal(I))
        
        plt.hist(S[-1], bins=50) ; plt.xlabel("index level") ; plt.ylabel("frequency") ; plt.grid(True)
        plt.show()
        self.print_statistics(S[-1], S[-1])
        plt.plot(S[:, :10], lw=1.5) ; plt.xlabel("time") ; plt.ylabel("index level") ; plt.grid(True)
        plt.show()
        pass
    
    
    #mean-reverting processes
    def square_root_diffusion(self):
    #Stochastic differential equation for square-root diffusion
        x0 = 0.05 # Process level at date t
        kappa = 3.0 # Mean-reversion factor
        theta = 0.02 # Long-term mean of the process
        sigma = 0.1 # Constant volatility parameter
        T = 2.0 # in years
        I = 10000
        z = npr.standard_normal(I) # Standard Brownian motion
        M = 50
        dt = T / M
        
        # Euler discretization for square-root diffusion
        def srd_euler():
            xh = np.zeros((M + 1, I))
            x1 = np.zeros_like(xh)
            xh[0] = x0
            x1[0] = x0
            for t in range(1, M + 1):
                xh[t] = (xh[t - 1]
                + kappa * (theta - np.maximum(xh[t - 1], 0)) * dt
                + sigma * np.sqrt(np.maximum(xh[t - 1], 0)) * np.sqrt(dt)
                * z)
            x1 = np.maximum(xh, 0)
            return x1
        x1 = srd_euler()
        
        plt.hist(x1[-1], bins=50) ; plt.xlabel("value") ; plt.ylabel("frequency") ; plt.grid(True)
        plt.plot(x1[:, :10], lw=1.5) ; plt.xlabel("time") ; plt.ylabel("index level") ; plt.grid(True)
        plt.show()
        # Exact discretization for square-root diffusion 
        def srd_exact():
            x2 = np.zeros((M + 1, I))
            x2[0] = x0
            for t in range(1, M + 1):
                df = 4 * theta * kappa / sigma ** 2
                c = (sigma ** 2 * (1 - np.exp(-kappa * dt))) / (4 * kappa)
                nc = np.exp(-kappa * dt) / c * x2[t - 1]
                x2[t] = c * npr.noncentral_chisquare(df, nc, size=I)
            return x2
        x2 = srd_exact()
        
        plt.hist(x2[-1], bins=50) ; plt.xlabel("value") ; plt.ylabel("frequency") ; plt.grid(True)
        plt.plot(x2[:, :10], lw=1.5) ; plt.xlabel("time") ; plt.ylabel("index level") ; plt.grid(True)
        plt.show()
        
        self.print_statistics(x1[-1], x2[-1])
        I = 250000
        # %time x1 = srd_euler()
        # %time x2 = srd_exact()
        self.print_statistics(x1[-1], x2[-1])
        x1 = 0.0; x2 = 0.0
        pass
    
    def heston_stochastic_volatility_model(self):
        #Stochastic differential equations for Heston stochastic volatility model
        S0 = 100.
        r = 0.05
        v0 = 0.1
        kappa = 3.0
        theta = 0.25
        sigma = 0.1
        rho = 0.6
        T = 1.0
        
        corr_mat = np.zeros((2, 2))
        corr_mat[0, :] = [1.0, rho]
        corr_mat[1, :] = [rho, 1.0]
        cho_mat = np.linalg.cholesky(corr_mat)
        print(cho_mat)
        
        M = 50
        I = 10000
        ran_num = npr.standard_normal((2, M + 1, I))

        dt = T / M
        v = np.zeros_like(ran_num[0])
        vh = np.zeros_like(v)
        v[0] = v0
        vh[0] = v0
        for t in range(1, M + 1):
            ran = np.dot(cho_mat, ran_num[:, t, :])
            vh[t] = (vh[t - 1] + kappa * (theta - np.maximum(vh[t - 1], 0)) * dt
                    + sigma * np.sqrt(np.maximum(vh[t - 1], 0)) * np.sqrt(dt)
                    * ran[1])
        v = np.maximum(vh, 0)

        S = np.zeros_like(ran_num[0])
        S[0] = S0
        for t in range(1, M + 1):
            ran = np.dot(cho_mat, ran_num[:, t, :])
            S[t] = S[t - 1] * np.exp((r - 0.5 * v[t]) * dt + np.sqrt(v[t]) * ran[0] * np.sqrt(dt))


        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5))
        ax1.hist(S[-1], bins=50) ; ax1.set_xlabel("index level") ; ax1.set_ylabel("frequency") ; ax1.grid(True)
        ax2.hist(v[-1], bins=50) ; ax2.set_xlabel("volatility") ; ax2.grid(True)
        plt.show()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(7, 6)) ; ax1.plot(S[:, :10], lw=1.5)
        ax1.set_ylabel("index level") ; ax1.grid(True)
        ax2.plot(v[:, :10], lw=1.5) ; ax2.set_xlabel("time") ; ax2.set_ylabel("volatility") ; ax2.grid(True)
        plt.show()
        self.print_statistics(S[-1], v[-1])
        pass
    
    def jump_diffusion(self):
        #Stochastic differential equation for Merton jump diffusion model
        S0 = 100.
        r = 0.05
        sigma = 0.2
        lamb = 0.75
        mu = -0.6
        delta = 0.25
        T = 1.0
        
        M = 50
        I = 10000
        dt = T / M
        rj = lamb * (np.exp(mu + 0.5 * delta ** 2) - 1)
        S = np.zeros((M + 1, I))
        S[0] = S0
        sn1 = npr.standard_normal((M + 1, I))
        sn2 = npr.standard_normal((M + 1, I))
        poi = npr.poisson(lamb * dt, (M + 1, I))
        for t in range(1, M + 1, 1):
            S[t] = S[t - 1] * (np.exp((r - rj - 0.5 * sigma ** 2) * dt
                + sigma * np.sqrt(dt) * sn1[t])
                + (np.exp(mu + delta * sn2[t]) - 1)
                * poi[t])
        S[t] = np.maximum(S[t], 0)

        plt.hist(S[-1], bins=50) ; plt.xlabel("value") ; plt.ylabel("frequency") ; plt.grid(True)
        plt.show()
        plt.plot(S[:, :10], lw=1.5) ; plt.xlabel("time") ; plt.ylabel("index level") ; plt.grid(True)
        plt.show()
        pass
    
    def variance_reduction(self):
        print("%15s %15s" % ("Mean", "Std. Deviation"))
        print(31 * "-")
        for i in range(1, 31, 2):
            npr.seed(1000)
            sn = npr.standard_normal(i ** 2 * 10000)
            print( "%15.12f %15.12f" % (sn.mean(), sn.std()) )
            
        print(i ** 2 * 10000)
        sn = npr.standard_normal(10000 / 2)
        sn = np.concatenate((sn, -sn))
        print(np.shape(sn))
        
        print("%15s %15s" % ("Mean", "Std. Deviation"))
        print(31 * "-")
        for i in range(1, 31, 2):
            npr.seed(1000)
            sn = npr.standard_normal(i ** 2 * 10000 / 2)
            sn = np.concatenate((sn, -sn))
            print("%15.12f %15.12f" % (sn.mean(), sn.std()) )
            
            
        # variance reduction : moment matching  
        sn = npr.standard_normal(10000)
        print(sn.mean())
        print(sn.std())
        
        sn_new = (sn - sn.mean()) / sn.std()
        print(sn_new.mean())
        print(sn_new.std())
        

        sn_new_gen = self.gen_sn(M = 50, I = 10000)
        print(sn_new_gen.mean())
        print(sn_new_gen.std())
        pass
    
    def gen_sn(self, M, I, anti_paths=True, mo_match=True):
        ''' 
        Function to generate random numbers for simulation.
        Parameters
        ==========
        M : int
        number of time intervals for discretization
        I : int
        number of paths to be simulated
        anti_paths: Boolean
        use of antithetic variates
        mo_math : Boolean
        use of moment matching
        '''
        if anti_paths is True:
            sn = npr.standard_normal((M + 1, I / 2))
            sn = np.concatenate((sn, -sn), axis=1)
        else:
            sn = npr.standard_normal((M + 1, I))
        if mo_match is True:
            sn = (sn - sn.mean()) / sn.std()
        return sn
    
    
    def european_options_valuation(self):
        #Risk-neutral Monte Carlo estimator
        print(self.gbm_mcs_stat(K=105.))
        print(self.gbm_mcs_dyna(K=110., option="call"))
        print(self.gbm_mcs_dyna(K=110., option="put"))

        S0 = 100.
        r = 0.05
        sigma = 0.2
        T = 1.0
        
        stat_res = []
        dyna_res = []
        anal_res = []
        k_list = np.arange(80., 120.1, 5.)
        np.random.seed(200000)
        for K in k_list:
            stat_res.append(self.gbm_mcs_stat(K))
            dyna_res.append(self.gbm_mcs_dyna(K))
            anal_res.append(self.bsm_call_value(S0, K, T, r, sigma))
        stat_res = np.array(stat_res)
        dyna_res = np.array(dyna_res)
        anal_res = np.array(anal_res)

        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
        ax1.plot(k_list, anal_res, "b", label="analytical")
        ax1.plot(k_list, stat_res, "ro", label="static")
        ax1.set_ylabel("European call option value")
        ax1.grid(True)
        ax1.legend(loc=0)
        ax1.set_ylim(ymin=0)
        wi = 1.0
        ax2.bar(k_list - wi / 2, (anal_res - stat_res) / anal_res * 100, wi)
        ax2.set_xlabel("strike")
        ax2.set_ylabel("difference in %")
        ax2.set_xlim(left=75, right=125)
        ax2.grid(True)
        plt.show()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
        ax1.plot(k_list, anal_res, "b", label="analytical")
        ax1.plot(k_list, dyna_res, "ro", label="dynamic")
        ax1.set_ylabel("European call option value")
        ax1.grid(True)
        ax1.legend(loc=0)
        ax1.set_ylim(ymin=0)
        wi = 1.0
        ax2.bar(k_list - wi / 2, (anal_res - dyna_res) / anal_res * 100, wi)
        ax2.set_xlabel("strike")
        ax2.set_ylabel("difference in %")
        ax2.set_xlim(left=75, right=125)
        ax2.grid(True)
        plt.show()
        pass
    
    def gbm_mcs_stat(self, K):
        S0 = 100.
        r = 0.05
        sigma = 0.25
        T = 1.0
        I = 50000
        
        ''' Valuation of European call option in Black-Scholes-Merton
        by Monte Carlo simulation (of index level at maturity)
        Parameters
        ==========
        K : float
        (positive) strike price of the option
        Returns
        =======
        C0 : float
        estimated present value of European call option
        '''
        sn = self.gen_sn(1, I)
        # simulate index level at maturity
        ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T
        + sigma * np.sqrt(T) * sn[1])
        # calculate payoff at maturity
        hT = np.maximum(ST - K, 0)
        # calculate MCS estimator
        C0 = np.exp(-r * T) * 1 / I * np.sum(hT)
        return C0
    
    def gbm_mcs_dyna(self, K, option="call"):
        S0 = 100.
        r = 0.05
        sigma = 0.25
        T = 1.0
        I = 50000
        M = 50
        ''' Valuation of European options in Black-Scholes-Merton
        by Monte Carlo simulation (of index level paths)
        Parameters
        ==========
        K : float
        (positive) strike price of the option
        option : string
        type of the option to be valued ("call", "put")
        Returns
        =======
        C0 : float
        estimated present value of European call option
        '''
        dt = T / M
        # simulation of index level paths
        S = np.zeros((M + 1, I))
        S[0] = S0
        sn = self.gen_sn(M, I)
        for t in range(1, M + 1):
            S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt
            + sigma * np.sqrt(dt) * sn[t])
        # case-based calculation of payoff
        if option == "call":
            hT = np.maximum(S[-1] - K, 0)
        else:
            hT = np.maximum(K - S[-1], 0)
        # calculation of MCS estimator
        C0 = np.exp(-r * T) * 1 / I * np.sum(hT)
        return C0
    
    def american_options_valuation(self):
        print(self.gbm_mcs_amer(110., option="call"))
        print(self.gbm_mcs_amer(110., option="put"))
        
        euro_res = []
        amer_res = []
        k_list = np.arange(80., 120.1, 5.)
        for K in k_list:
            euro_res.append(self.gbm_mcs_dyna(K, "put"))
            amer_res.append(self.gbm_mcs_amer(K, "put"))
        euro_res = np.array(euro_res)
        amer_res = np.array(amer_res)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
        ax1.plot(k_list, euro_res, "b", label="European put")
        ax1.plot(k_list, amer_res, "ro", label="American put")
        ax1.set_ylabel("call option value")
        ax1.grid(True)
        ax1.legend(loc=0)
        wi = 1.0
        ax2.bar(k_list - wi / 2, (amer_res - euro_res) / euro_res * 100, wi)
        ax2.set_xlabel("strike")
        ax2.set_ylabel("early exercise premium in %")
        ax2.set_xlim(left=75, right=125)
        ax2.grid(True)
        plt.show()
        pass
    
    def gbm_mcs_amer(self, K, option="call"):
        ''' Valuation of American option in Black-Scholes-Merton
        by Monte Carlo simulation by LSM algorithm
        Parameters
        ==========
        K : float
        (positive) strike price of the option
        option : string
        type of the option to be valued ("call", "put")
        Returns
        =======
        C0 : float
        estimated present value of European call option
        '''
        S0 = 100.
        r = 0.05
        sigma = 0.25
        T = 1.0
        I = 50000
        M = 50
        
        dt = T / M
        df = np.exp(-r * dt)
        # simulation of index levels
        S = np.zeros((M + 1, I))
        S[0] = S0
        sn = self.gen_sn(M, I)
        for t in range(1, M + 1):
            S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt
            + sigma * np.sqrt(dt) * sn[t])
        # case-based calculation of payoff
        if option == "call":
            h = np.maximum(S - K, 0)
        else:
            h = np.maximum(K - S, 0)
        # LSM algorithm
        V = np.copy(h)
        for t in range(M - 1, 0, -1):
            reg = np.polyfit(S[t], V[t + 1] * df, 7)
            C = np.polyval(reg, S[t])
            V[t] = np.where(C > h[t], V[t + 1] * df, h[t])
        # MCS estimator
        C0 = df * 1 / I * np.sum(V[1])
        return C0
    
    #Risk Measures
    def value_at_risk(self):
        #Value-at-Risk
        lamb = 0.75
        mu = -0.6
        delta = 0.25
        M = 50
        
        
        S0 = 100
        r = 0.05
        sigma = 0.25
        T = 30 / 365.
        I = 10000
        ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T
            + sigma * np.sqrt(T) * npr.standard_normal(I))
        
        R_gbm = np.sort(ST - S0)
        plt.hist(R_gbm, bins=50)
        plt.xlabel("absolute return")
        plt.ylabel("frequency")
        plt.grid(True)
        
        percs = [0.01, 0.1, 1., 2.5, 5.0, 10.0]
        var = scs.scoreatpercentile(R_gbm, percs)
        print("%16s %16s" % ("Confidence Level", "Value-at-Risk"))
        print(33 * "-")
        for pair in zip(percs, var):
            print("%16.2f %16.3f" % (100 - pair[0], -pair[1]))

        dt = 30. / 365 / M
        rj = lamb * (np.exp(mu + 0.5 * delta ** 2) - 1)
        S = np.zeros((M + 1, I))
        S[0] = S0
        sn1 = npr.standard_normal((M + 1, I))
        sn2 = npr.standard_normal((M + 1, I))
        poi = npr.poisson(lamb * dt, (M + 1, I))
        for t in range(1, M + 1, 1):
            S[t] = S[t - 1] * (np.exp((r - rj - 0.5 * sigma ** 2) * dt
            + sigma * np.sqrt(dt) * sn1[t])
            + (np.exp(mu + delta * sn2[t]) - 1)
            * poi[t])
            S[t] = np.maximum(S[t], 0)
            
        R_jd = np.sort(S[-1] - S0)

        plt.hist(R_jd, bins=50)
        plt.xlabel("absolute return")
        plt.ylabel("frequency")
        plt.grid(True)
                
        percs = [0.01, 0.1, 1., 2.5, 5.0, 10.0]
        var = scs.scoreatpercentile(R_jd, percs)
        print("%16s %16s" % ("Confidence Level", "Value-at-Risk"))
        print(33 * "-")
        for pair in zip(percs, var):
            print("%16.2f %16.3f" % (100 - pair[0], -pair[1]))
        
        percs = list(np.arange(0.0, 10.1, 0.1))
        gbm_var = scs.scoreatpercentile(R_gbm, percs)
        jd_var = scs.scoreatpercentile(R_jd, percs)
        
        plt.plot(percs, gbm_var, "b", lw=1.5, label="GBM")
        plt.plot(percs, jd_var, "r", lw=1.5, label="JD")
        plt.legend(loc=4)
        plt.xlabel("100 - confidence level [%]")
        plt.ylabel("value-at-risk")
        plt.grid(True)
        plt.ylim(ymax=0.0)
        pass
    
    def credit_value_adjustments(self):
        #Credit Value Adjustments
        S0 = 100.
        r = 0.05
        sigma = 0.2
        T = 1.
        I = 100000
        ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * npr.standard_normal(I))
        
        L = 0.5
        p = 0.01
        
        D = npr.poisson(p * T, I)
        D = np.where(D > 1, 1, D)
        
        print(np.exp(-r * T) * 1 / I * np.sum(ST))
        CVaR = np.exp(-r * T) * 1 / I * np.sum(L * D * ST)
        print(CVaR)
        S0_CVA = np.exp(-r * T) * 1 / I * np.sum((1 - L * D) * ST)
        print(S0_CVA)
        S0_adj = S0 - CVaR
        print(S0_adj)
        print(np.count_nonzero(L * D * ST))
        
        plt.hist(L * D * ST, bins=50)
        plt.xlabel("loss")
        plt.ylabel("frequency")
        plt.grid(True)
        plt.ylim(ymax=175)
        
        
        K = 100.
        hT = np.maximum(ST - K, 0)
        C0 = np.exp(-r * T) * 1 / I * np.sum(hT)
        print(C0)
        
        CVaR = np.exp(-r * T) * 1 / I * np.sum(L * D * hT)
        print(CVaR)
        C0_CVA = np.exp(-r * T) * 1 / I * np.sum((1 - L * D) * hT)
        print(C0_CVA)
        print(np.count_nonzero(L * D * hT))
        print(np.count_nonzero(D))
        print(I - np.count_nonzero(hT))
        
        plt.hist(L * D * hT, bins=50)
        plt.xlabel("loss")
        plt.ylabel("frequency")
        plt.grid(True)
        plt.ylim(ymax=350)
        pass
    
    
if __name__=="__main__":
    stochastics = Stochastics()
#    stochastics.random_numbers()
#    stochastics.black_scholes_merton_simulation()
#    stochastics.black_scholes_merton_dynamically_simulation()
#    stochastics.heston_stochastic_volatility_model()
#    stochastics.jump_diffusion()
#    stochastics.variance_reduction()
#    stochastics.european_options_valuation()
#    stochastics.american_options_valuation()
#    stochastics.value_at_risk()
#    stochastics.credit_value_adjustments()
    stochastics.example_VSTOXX_index()
    
    pass