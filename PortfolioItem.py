import pandas as pd
from pandas_datareader import data as wb
import numpy as np

class PortfolioItem:
    def __init__(self, ticker: str, shareCount: int):
        self.ticker = ticker
        self.shareCount = shareCount
        self.stockData = wb.DataReader(ticker, data_source='yahoo', start='2015-1-1', end='2021-03-23')['Adj Close']


    def calculateSecurityReturn(self):
        return np.log(self.stockData / self.stockData.shift(1))

    def calculateBeta(self):
        securityReturn = self.calculateSecurityReturn()
        covarianceMatrix = securityReturn.cov() * 250

    def calculateExpectedReturnCAPM(self):
        equityRiskPremium = 0.5
        riskFree = 0.025
        
        return