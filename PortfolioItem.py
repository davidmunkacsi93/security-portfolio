import pandas as pd
from pandas_datareader import data as wb
import numpy as np

class PortfolioItem:
    def __init__(self, ticker: str, market: str, shareCount: int):
        self.ticker = ticker
        self.market = market
        self.shareCount = shareCount
        self.securityData = pd.DataFrame()

        for t in [ticker, market]: 
            self.securityData[t] = wb.DataReader(t, data_source='yahoo', start='2017-1-1', end='2021-03-23')['Adj Close']

    def calculateBeta(self):
        securityReturns = np.log(self.securityData / self.securityData.shift(1))
        covarianceMatrix = securityReturns.cov() * 250

        covarianceWithMarket = covarianceMatrix.iloc[0,1]
        marketVariance = securityReturns[self.market].var() * 250

        return covarianceWithMarket/marketVariance

    def calculateExpectedReturnCAPM(self):
        equityRiskPremium = 0.5
        riskFree = 0.025
        beta = self.calculateBeta()

        return riskFree + equityRiskPremium * beta