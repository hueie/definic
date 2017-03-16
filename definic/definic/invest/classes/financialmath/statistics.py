import numpy as np
np.random.seed(1000)
import scipy.stats as scs
import statsmodels.api as sm
import matplotlib as mpl
import matplotlib.pyplot as plt

def gen_paths(S0, r, sigma, T, M, I):
    """ Generates Monte Carlo paths for geometric Brownian motion.
    Parameters
    ==========
    S0 : float
    initial stock/index value
    r : float
    constant short rate
    sigma : float
    constant volatility
    T : float
    final time horizon
    M : int
    number of time steps/intervals
    I : int
    number of paths to be simulated
    Returns
    =======
    paths : ndarray, shape (M + 1, I)
    simulated paths given the parameters
    """
    dt = float(T) / M
    paths = np.zeros((M + 1, I), np.float64)
    paths[0] = S0
    for t in range(1, M + 1):
        rand = np.random.standard_normal(I)
        rand = (rand - rand.mean()) / rand.std()
        paths[t] = paths[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt +
        sigma * np.sqrt(dt) * rand)
    return paths
def Monte_Carlo_paths():
    S0 = 100.
    r = 0.05
    sigma = 0.2
    T = 1.0
    M = 50
    I = 250000
    paths = gen_paths(S0, r, sigma, T, M, I)
    
    plt.plot(paths[:, :10])
    plt.grid(True)
    plt.xlabel("time steps")
    plt.ylabel("index level")

    log_returns = np.log(paths[1:] / paths[0:-1])
    paths[:, 0].round(4)
    log_returns[:, 0].round(4)
    
    print_statistics(log_returns.flatten())
    plt.hist(log_returns.flatten(), bins=70, normed=True, label="frequency")
    plt.grid(True)
    plt.xlabel("log-return")
    plt.ylabel("frequency")
    x = np.linspace(plt.axis()[0], plt.axis()[1])
    plt.plot(x, scs.norm.pdf(x, loc=r / M, scale=sigma / np.sqrt(M)),
    "r", lw=2.0, label="pdf")
    plt.legend()
    
    sm.qqplot(log_returns.flatten()[::500], line="s")
    plt.grid(True)
    plt.xlabel("theoretical quantiles")
    plt.ylabel("sample quantiles")
    
    
    normality_tests(log_returns.flatten())
    
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
    ax1.hist(paths[-1], bins=30)
    ax1.grid(True)
    ax1.set_xlabel("index level")
    ax1.set_ylabel("frequency")
    ax1.set_title("regular data")
    ax2.hist(np.log(paths[-1]), bins=30)
    ax2.grid(True)
    ax2.set_xlabel("log index level")
    ax2.set_title("log data")
    
    print_statistics(paths[-1])
    print_statistics(np.log(paths[-1]))
    normality_tests(np.log(paths[-1]))
    
    log_data = np.log(paths[-1])
    plt.hist(log_data, bins=70, normed=True, label="observed")
    plt.grid(True)
    plt.xlabel("index levels")
    plt.ylabel("frequency")
    x = np.linspace(plt.axis()[0], plt.axis()[1])
    plt.plot(x, scs.norm.pdf(x, log_data.mean(), log_data.std()),
    "r", lw=2.0, label="pdf")
    plt.legend()
    
    sm.qqplot(log_data, line="s")
    plt.grid(True)
    plt.xlabel("theoretical quantiles")
    plt.ylabel("sample quantiles")
    pass

def normality_tests(arr):
    """ "Tests for normality distribution of given data set.
    Parameters
    ==========
    array: ndarray
    object to generate statistics on
    """
    print "Skew of data set %14.3f" % scs.skew(arr)
    print "Skew test p-value %14.3f" % scs.skewtest(arr)[1]
    print "Kurt of data set %14.3f" % scs.kurtosis(arr)
    print "Kurt test p-value %14.3f" % scs.kurtosistest(arr)[1]
    print "Norm test p-value %14.3f" % scs.normaltest(arr)[1]
    pass

def print_statistics(array):
    """ Prints selected statistics.
    Parameters
    ==========
    array: ndarray
    object to generate statistics on
    """
    sta = scs.describe(array)
    print "%14s %15s" % ("statistic", "value")
    print 30 * "-"
    print "%14s %15.5f" % ("size", sta[0])
    print "%14s %15.5f" % ("min", sta[1][0])
    print "%14s %15.5f" % ("max", sta[1][1])
    print "%14s %15.5f" % ("mean", sta[2])
    print "%14s %15.5f" % ("std", np.sqrt(sta[3]))
    print "%14s %15.5f" % ("skew", sta[4])
    print "%14s %15.5f" % ("kurtosis", sta[5])
    pass

import pandas as pd
import pandas.io.data as web   
    
def realworld():
     
    symbols = ["^GDAXI", "^GSPC", "YHOO", "MSFT"]
    data = pd.DataFrame()
    for sym in symbols:
        data[sym] = web.DataReader(sym, data_source="yahoo", start="1/1/2006")["Adj Close"]
    data = data.dropna()
    data.info()
    data.head()
    
    (data / data.ix[0] * 100).plot(figsize=(8, 6))
    log_returns = np.log(data / data.shift(1))
    log_returns.head()
    log_returns.hist(bins=50, figsize=(9, 6))
    
    for sym in symbols:
        print "\nResults for symbol %s" % sym
        print 30 * "-"
        log_data = np.array(log_returns[sym].dropna())
        print_statistics(log_data)
    
    sm.qqplot(log_returns["^GSPC"].dropna(), line="s")
    plt.grid(True)
    plt.xlabel("theoretical quantiles")
    plt.ylabel("sample quantiles")
    
    sm.qqplot(log_returns["MSFT"].dropna(), line="s")
    plt.grid(True)
    plt.xlabel("theoretical quantiles")
    plt.ylabel("sample quantiles")
    
    for sym in symbols:
        print "\nResults for symbol %s" % sym
        print 32 * "-"
        log_data = np.array(log_returns[sym].dropna())
        normality_tests(log_data)
    
    pass
def basictheory():
    import numpy as np
    import pandas as pd
    import pandas.io.data as web
    import matplotlib.pyplot as plt
    %matplotlib inline    
        
    symbols = ["AAPL", "MSFT", "YHOO", "DB", "GLD"]
    noa = len(symbols)    
        
    data = pd.DataFrame()
    for sym in symbols:
        data[sym] = web.DataReader(sym, data_source="yahoo",
        end="2014-09-12")["Adj Close"]
    data.columns = symbols    
    
    (data / data.ix[0] * 100).plot(figsize=(8, 5))
    rets = np.log(data / data.shift(1))
    rets.mean() * 252
    rets.cov() * 252
    
    #The Basic Theory
    weights = np.random.random(noa)
    weights /= np.sum(weights)
    weights

    np.sum(rets.mean() * weights) * 252
    np.dot(weights.T, np.dot(rets.cov() * 252, weights))
    np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights)))
    
    prets = []
    pvols = []
    for p in range (2500):
        weights = np.random.random(noa)
        weights /= np.sum(weights)
        prets.append(np.sum(rets.mean() * weights) * 252)
        pvols.append(np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights))))
    prets = np.array(prets)
    pvols = np.array(pvols)
    
    plt.figure(figsize=(8, 4))
    plt.scatter(pvols, prets, c=prets / pvols, marker="o")
    plt.grid(True)
    plt.xlabel("expected volatility")
    plt.ylabel("expected return")
    plt.colorbar(label="Sharpe ratio")
    
    pass

def portfolio_optimization():
    
    cons = ({"type": "eq", "fun": lambda x: np.sum(x) - 1})
    bnds = tuple((0, 1) for x in range(noa))
    noa * [1. / noa,]
    %%time
    opts = sco.minimize(min_func_sharpe, noa * [1. / noa,], method="SLSQP", bounds=bnds, constraints=cons)
    opts
    opts["x"].round(3)
    statistics(opts["x"]).round(3)
    
    optv = sco.minimize(min_func_variance, noa * [1. / noa,],
    method="SLSQP", bounds=bnds,
    constraints=cons)
    optv
    
    optv["x"].round(3)
    statistics(optv["x"]).round(3)
    
    pass

def efficient_frontier():
    cons = ({"type": "eq", "fun": lambda x: statistics(x)[0] - tret},
    {"type": "eq", "fun": lambda x: np.sum(x) - 1})
    bnds = tuple((0, 1) for x in weights)
    
    %%time
    trets = np.linspace(0.0, 0.25, 50)
    tvols = []
    for tret in trets:
        cons = ({"type": "eq", "fun": lambda x: statistics(x)[0] - tret},
        {"type": "eq", "fun": lambda x: np.sum(x) - 1})
        res = sco.minimize(min_func_port, noa * [1. / noa,], method="SLSQP",
        bounds=bnds, constraints=cons)
        tvols.append(res["fun"])
    tvols = np.array(tvols)
    
    
    plt.figure(figsize=(8, 4))
    plt.scatter(pvols, prets,
    c=prets / pvols, marker="o")
    # random portfolio composition
    plt.scatter(tvols, trets,
    c=trets / tvols, marker="x")
    # efficient frontier
    plt.plot(statistics(opts["x"])[1], statistics(opts["x"])[0],
    "r*", markersize=15.0)
    # portfolio with highest Sharpe ratio
    plt.plot(statistics(optv["x"])[1], statistics(optv["x"])[0],
    "y*", markersize=15.0)
    # minimum variance portfolio
    plt.grid(True)
    plt.xlabel("expected volatility")
    plt.ylabel("expected return")
    plt.colorbar(label="Sharpe ratio")
    
    
    pass

def min_func_port(weights):
    return statistics(weights)[1]


def min_func_variance(weights):
    return statistics(weights)[1] ** 2

    
def statistics(weights):
    "" Returns portfolio statistics.
    Parameters
    ==========
    weights : array-like
    weights for different securities in portfolio
    Returns
    =======
    pret : float
    expected portfolio return
    pvol : float
    expected portfolio volatility
    pret / pvol : float
    Sharpe ratio for rf=0
    ""
    weights = np.array(weights)
    pret = np.sum(rets.mean() * weights) * 252
    pvol = np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights)))
    return np.array([pret, pvol, pret / pvol])    
    
import scipy.optimize as sco
def min_func_sharpe(weights):
    return -statistics(weights)[2]


import scipy.interpolate as sci
def Capital_Market_Line():
    ind = np.argmin(tvols)
    evols = tvols[ind:]
    erets = trets[ind:]

    opt = sco.fsolve(equations, [0.01, 0.5, 0.15])
    opt
    np.round(equations(opt), 6)
    
    plt.figure(figsize=(8, 4))
    plt.scatter(pvols, prets,
    c=(prets - 0.01) / pvols, marker="o")
    # random portfolio composition
    plt.plot(evols, erets, "g", lw=4.0)
    # efficient frontier
    cx = np.linspace(0.0, 0.3)
    plt.plot(cx, opt[0] + opt[1] * cx, lw=1.5)
    # capital market line
    plt.plot(opt[2], f(opt[2]), "r*", markersize=15.0)
    plt.grid(True)
    plt.axhline(0, color="k", ls="—", lw=2.0)
    plt.axvline(0, color="k", ls="—", lw=2.0)
    plt.xlabel("expected volatility")
    plt.ylabel("expected return")
    plt.colorbar(label="Sharpe ratio")
    
    
    cons = ({"type": "eq", "fun": lambda x: statistics(x)[0] - f(opt[2])},
    {"type": "eq", "fun": lambda x: np.sum(x) - 1})
    res = sco.minimize(min_func_port, noa * [1. / noa,], method="SLSQP",
    bounds=bnds, constraints=cons)
    res["x"].round(3)

    pass

def f(x):
    "" Efficient frontier function (splines approximation). ""
    return sci.splev(x, tck, der=0)
def df(x):
    "" First derivative of efficient frontier function. ""
    return sci.splev(x, tck, der=1)
def equations(p, rf=0.01):
    eq1 = rf - p[0]
    eq2 = rf + p[1] * p[2] - f(p[2])
    eq3 = p[1] - df(p[2])
    return eq1, eq2, eq3


def principal_component_analysis():
    import numpy as np
    import pandas as pd
    import pandas.io.data as web
    from sklearn.decomposition import KernelPCA
    
    symbols = ["ADS.DE", "ALV.DE", "BAS.DE", "BAYN.DE", "BEI.DE",
        "BMW.DE", "CBK.DE", "CON.DE", "DAI.DE", "DB1.DE",
        "DBK.DE", "DPW.DE", "DTE.DE", "EOAN.DE", "FME.DE",
        "FRE.DE", "HEI.DE", "HEN3.DE", "IFX.DE", "LHA.DE",
        "LIN.DE", "LXS.DE", "MRK.DE", "MUV2.DE", "RWE.DE",
        "SAP.DE", "SDF.DE", "SIE.DE", "TKA.DE", "VOW3.DE",
        "^GDAXI"]
    
    %%time
    data = pd.DataFrame()
    for sym in symbols:
        data[sym] = web.DataReader(sym, data_source="yahoo")["Close"]
    data = data.dropna()
    
    dax = pd.DataFrame(data.pop("^GDAXI"))
    data[data.columns[:6]].head()
    
    #Applying PCA
    scale_function = lambda x: (x - x.mean()) / x.std()
    pca = KernelPCA().fit(data.apply(scale_function))
    len(pca.lambdas_)
    pca.lambdas_[:10].round()
    get_we = lambda x: x / x.sum()
    get_we(pca.lambdas_)[:10]
    get_we(pca.lambdas_)[:5].sum()
    
    
    #Constructing a PCA Index
    pca = KernelPCA(n_components=1).fit(data.apply(scale_function))
    dax["PCA_1"] = pca.transform(-data)
    
    import matplotlib.pyplot as plt
    %matplotlib inline
    dax.apply(scale_function).plot(figsize=(8, 4))
    
    pca = KernelPCA(n_components=5).fit(data.apply(scale_function))
    pca_components = pca.transform(-data)
    weights = get_we(pca.lambdas_)
    dax["PCA_5"] = np.dot(pca_components, weights)
    
    import matplotlib.pyplot as plt
    %matplotlib inline
    dax.apply(scale_function).plot(figsize=(8, 4))
    
    import matplotlib as mpl
    mpl_dates = mpl.dates.date2num(data.index)
    mpl_dates
    plt.figure(figsize=(8, 4))
    plt.scatter(dax["PCA_5"], dax["^GDAXI"], c=mpl_dates)
    lin_reg = np.polyval(np.polyfit(dax["PCA_5"],
    dax["^GDAXI"], 1),
    dax["PCA_5"])
    plt.plot(dax["PCA_5"], lin_reg, "r", lw=3)
    plt.grid(True)
    plt.xlabel("PCA_5")
    plt.ylabel("^GDAXI")
    plt.colorbar(ticks=mpl.dates.DayLocator(interval=250),
    format=mpl.dates.DateFormatter("%d %b %y"))
    
    cut_date = "2011/7/1"
    early_pca = dax[dax.index < cut_date]["PCA_5"]
    early_reg = np.polyval(np.polyfit(early_pca,
    dax["^GDAXI"][dax.index < cut_date], 1),
    early_pca)
    
    late_pca = dax[dax.index >= cut_date]["PCA_5"]
    late_reg = np.polyval(np.polyfit(late_pca,
    dax["^GDAXI"][dax.index >= cut_date], 1),
    late_pca)
    
    plt.figure(figsize=(8, 4))
    plt.scatter(dax["PCA_5"], dax["^GDAXI"], c=mpl_dates)
    plt.plot(early_pca, early_reg, "r", lw=3)
    plt.plot(late_pca, late_reg, "r", lw=3)
    plt.grid(True)
    plt.xlabel("PCA_5")
    plt.ylabel("^GDAXI")
    plt.colorbar(ticks=mpl.dates.DayLocator(interval=250),
    format=mpl.dates.DateFormatter("%d %b %y"))
    

    pass


def bayesian_regression():
    import warnings
    warnings.simplefilter("ignore")
    import pymc as pm
    import numpy as np
    np.random.seed(1000)
    import matplotlib.pyplot as plt
    %matplotlib inline
    
    #PYMC3
    x = np.linspace(0, 10, 500)
    y = 4 + 2 * x + np.random.standard_normal(len(x)) * 2
    reg = np.polyfit(x, y, 1)
    
    plt.figure(figsize=(8, 4))
    plt.scatter(x, y, c=y, marker="v")
    plt.plot(x, reg[1] + reg[0] * x, lw=2.0)
    plt.colorbar()
    plt.grid(True)
    plt.xlabel("x")
    plt.ylabel("y")
    
    reg
    
    with pm.Model() as model:
        # model specifications in PyMC3
        # are wrapped in a with statement
        # define priors
        alpha = pm.Normal("alpha", mu=0, sd=20)
        beta = pm.Normal("beta", mu=0, sd=20)
        sigma = pm.Uniform("sigma", lower=0, upper=10)
        # define linear regression
        y_est = alpha + beta * x
        # define likelihood
        likelihood = pm.Normal("y", mu=y_est, sd=sigma, observed=y)
        # inference
        start = pm.find_MAP()
        # find starting value by optimization
        step = pm.NUTS(state=start)
        # instantiate MCMC sampling algorithm
        trace = pm.sample(100, step, start=start, progressbar=False)
        # draw 100 posterior samples using NUTS sampling
    
    trace[0]
    
    fig = pm.traceplot(trace, lines={"alpha": 4, "beta": 2, "sigma": 2})
    plt.figure(figsize=(8, 8))
    plt.figure(figsize=(8, 4))
    plt.scatter(x, y, c=y, marker="v")
    plt.colorbar()
    plt.grid(True)
    plt.xlabel("x")
    plt.ylabel("y")
    for i in range(len(trace)):
        plt.plot(x, trace["alpha"][i] + trace["beta"][i] * x)
        
    pass

def realdata():
    import warnings
    warnings.simplefilter("ignore")
    import zipline
    import pytz
    import datetime as dt
    
    data = zipline.data.load_from_yahoo(stocks=["GLD", "GDX"],
    end=dt.datetime(2014, 3, 15, 0, 0, 0, 0, pytz.utc)).dropna()
    data.info()
    data.plot(figsize=(8, 4))
    
    data.ix[-1] / data.ix[0] - 1
    data.corr()
    data.index
    
    
    import matplotlib as mpl
    mpl_dates = mpl.dates.date2num(data.index)
    mpl_dates
    plt.figure(figsize=(8, 4))
    plt.scatter(data["GDX"], data["GLD"], c=mpl_dates, marker="o")
    plt.grid(True)
    plt.xlabel("GDX")
    plt.ylabel("GLD")
    plt.colorbar(ticks=mpl.dates.DayLocator(interval=250),
                 format=mpl.dates.DateFormatter("%d %b %y"))
    
    with pm.Model() as model:
        alpha = pm.Normal("alpha", mu=0, sd=20)
        beta = pm.Normal("beta", mu=0, sd=20)
        sigma = pm.Uniform("sigma", lower=0, upper=50)
        y_est = alpha + beta * data["GDX"].values
        likelihood = pm.Normal("GLD", mu=y_est, sd=sigma,
        observed=data["GLD"].values)
        start = pm.find_MAP()
        step = pm.NUTS(state=start)
        trace = pm.sample(100, step, start=start, progressbar=False)
        
    fig = pm.traceplot(trace)
    plt.figure(figsize=(8, 8))    
        
    plt.figure(figsize=(8, 4))
    plt.scatter(data["GDX"], data["GLD"], c=mpl_dates, marker="o")
    plt.grid(True)
    plt.xlabel("GDX")
    plt.ylabel("GLD")
    for i in range(len(trace)):
        plt.plot(data["GDX"], trace["alpha"][i] + trace["beta"][i] * data
        ["GDX"])
    plt.colorbar(ticks=mpl.dates.DayLocator(interval=250),
    format=mpl.dates.DateFormatter("%d %b %y"))    
        
    model_randomwalk = pm.Model()
    with model_randomwalk:
        # std of random walk best sampled in log space
        sigma_alpha, log_sigma_alpha = \
            model_randomwalk.TransformedVar("sigma_alpha",
            pm.Exponential.dist(1. / .02, testval=.1),
        pm.logtransform)
        sigma_beta, log_sigma_beta = \
            model_randomwalk.TransformedVar("sigma_beta",
            pm.Exponential.dist(1. / .02, testval=.1),
            pm.logtransform)    
    
    
    from pymc.distributions.timeseries import GaussianRandomWalk
    # to make the model simpler, we will apply the same coefficients
    # to 50 data points at a time
    subsample_alpha = 50
    subsample_beta = 50
    with model_randomwalk:
        alpha = GaussianRandomWalk("alpha", sigma_alpha**-2,
        shape=len(data) / subsample_alpha)
        beta = GaussianRandomWalk("beta", sigma_beta**-2,
        shape=len(data) / subsample_beta)
        # make coefficients have the same length as prices
        alpha_r = np.repeat(alpha, subsample_alpha)
        beta_r = np.repeat(beta, subsample_beta)
    
    len(data.dropna().GDX.values)
        
        
    with model_randomwalk:
        # define regression
        regression = alpha_r + beta_r * data.GDX.values[:1950]
        # assume prices are normally distributed
        # the mean comes from the regression
        sd = pm.Uniform("sd", 0, 20)
        likelihood = pm.Normal("GLD",
        mu=regression,
        sd=sd,
        observed=data.GLD.values[:1950])
    
    import scipy.optimize as sco
    with model_randomwalk:
        # first optimize random walk
        start = pm.find_MAP(vars=[alpha, beta], fmin=sco.fmin_l_bfgs_b)
        # sampling
        step = pm.NUTS(scaling=start)
        trace_rw = pm.sample(100, step, start=start, progressbar=False)
    
    np.shape(trace_rw["alpha"])
    part_dates = np.linspace(min(mpl_dates), max(mpl_dates), 39)
    
    fig, ax1 = plt.subplots(figsize=(10, 5))
    plt.plot(part_dates, np.mean(trace_rw["alpha"], axis=0), "b", lw=2.5, label="alpha")
    for i in range(45, 55):
        plt.plot(part_dates, trace_rw["alpha"][i], "b-.", lw=0.75)
    plt.xlabel("date")
    plt.ylabel("alpha")
    plt.axis("tight")
    plt.grid(True)
    plt.legend(loc=2)
    ax1.xaxis.set_major_formatter(mpl.dates.DateFormatter("%d %b %y") )
    ax2 = ax1.twinx()
    plt.plot(part_dates, np.mean(trace_rw["beta"], axis=0), "r", lw=2.5, label="beta")
    for i in range(45, 55):
        plt.plot(part_dates, trace_rw["beta"][i], "r-.", lw=0.75)
    plt.ylabel("beta")
    plt.legend(loc=4)
    fig.autofmt_xdate()
    
    
    
    plt.figure(figsize=(10, 5))
    plt.scatter(data["GDX"], data["GLD"], c=mpl_dates, marker="o")
    plt.colorbar(ticks=mpl.dates.DayLocator(interval=250),
    format=mpl.dates.DateFormatter("%d %b %y"))
    plt.grid(True)
    plt.xlabel("GDX")
    plt.ylabel("GLD")
    x = np.linspace(min(data["GDX"]), max(data["GDX"]))
    for i in range(39):
        alpha_rw = np.mean(trace_rw["alpha"].T[i])
        beta_rw = np.mean(trace_rw["beta"].T[i])
        plt.plot(x, alpha_rw + beta_rw * x, color=plt.cm.jet(256 * i / 39))
    
    
        
    pass


class Statistics:
    def __init__(self):
        pass
    
    
if __name__=="__main__":
    

    pass