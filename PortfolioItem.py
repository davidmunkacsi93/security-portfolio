import pandas as pd
from pandas_datareader import data as wb
import numpy as np

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