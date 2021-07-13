import pandas as pd
from pandas_datareader import data as wb
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from BlackScholes import BlackScholes

class PortfolioItem:
    def __init__(self, ticker: str, market: str, shareCount: int):
        self.ticker = ticker
        self.market = market
        self.shareCount = shareCount
        self.securityData = pd.DataFrame()

        # Yield of 10 year US goverment bonds as an expectation of risk free return.
        self.riskFree = 0.025
        self.equityRiskPremium = 0.5
        self.annualMarketYears = 250

        self.blackScholes = BlackScholes()

        for t in [ticker, market]: 
            self.securityData[t] = wb.DataReader(t, data_source='yahoo', start='2017-1-1', end='2021-03-23')['Adj Close']

    def calculateBeta(self):
        securityReturns = np.log(self.securityData / self.securityData.shift(1))
        covarianceMatrix = securityReturns.cov() * self.annualMarketYears

        covarianceWithMarket = covarianceMatrix.iloc[0,1]
        marketVariance = securityReturns[self.market].var() * self.annualMarketYears

        return covarianceWithMarket/marketVariance

    def calculateStandardDeviation(self):
        securityReturns = np.log(self.securityData / self.securityData.shift(1))
        return securityReturns[self.market].std() * self.annualMarketYears ** 0.5

    def calculateExpectedReturnCAPM(self):
        beta = self.calculateBeta()

        return self.riskFree + self.equityRiskPremium * beta

    def calculateSharpeRatio(self):
        expectedReturn = self.calculateExpectedReturnCAPM()
        standardDeviation = self.calculateStandardDeviation()

        return (expectedReturn - self.riskFree) / standardDeviation

    def forecastFuturePrice(self):
        data = pd.DataFrame()
        data[self.ticker] = self.securityData[self.ticker]
        logReturns = np.log(1 + data.pct_change())
        mean = logReturns.mean()
        variance = logReturns.var()

        drift = mean - (0.5 * variance)
        standardDeviation = logReturns.std()

        timeIntervals = 1000
        iterations = 10
        simulation = norm.ppf(np.random.rand(timeIntervals, iterations))
        dailyReturns = np.exp(drift.values + standardDeviation.values * simulation)
        
        # Market price day zero.
        currentMarketPrice = data.iloc[-1]
        pricesList = np.zeros_like(dailyReturns)
        pricesList[0] = currentMarketPrice

        for t in range(1, timeIntervals):
            pricesList[t] = pricesList[t - 1] * dailyReturns[t]

        plt.figure(figsize=(10,6))
        plt.plot(pricesList)
        plt.title(self.ticker + ' expected price')

        plt.show()

    def BSM(self):
        data = pd.DataFrame()
        data[self.ticker] = self.securityData[self.ticker]

        stockPrice = data.iloc[-1]
        print(stockPrice)

        logReturns = np.log(1 - data.pct_change())
        standardDeviation = logReturns.std() * 250 ** 0.5
        riskFree = 0.025
        strikePrice = 110.0
        timeInYears = 1

        bsm = self.blackScholes.BSM(stockPrice, strikePrice, riskFree, standardDeviation, timeInYears)
        print(bsm)