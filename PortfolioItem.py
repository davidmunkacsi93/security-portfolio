import pandas as pd
from pandas_datareader import data as wb
import numpy as np

class PortfolioItem:
    def __init__(self, ticker: str, market: str, shareCount: int):
        self.ticker = ticker
        self.market = market
        self.shareCount = shareCount

        for t in [ticker, market]: 
            self.securityData[t] = wb.DataReader(t, data_source='yahoo', start='2015-1-1', end='2021-03-23')['Adj Close']


    def calculateSecurityReturns(self):
        securityReturns : pd.core.frame.DataFrame = np.log(self.securityData / self.securityData.shift(1))
        return securityReturns

    def calculateBeta(self):
        securityReturns = self.calculateSecurityReturn()
        covarianceMatrix = securityReturns.cov() * 250
        covarianceWithMarket = covarianceMatrix.iloc[0,1]
        marketVariance = self.securityData[self.market].var() * 250

        return covarianceWithMarket/marketVariance

    def calculateExpectedReturnCAPM(self):
        equityRiskPremium = 0.5
        riskFree = 0.025
        beta = self.calculateBeta()

        return riskFree + equityRiskPremium * beta