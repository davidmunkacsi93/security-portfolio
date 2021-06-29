import pandas as pd
from pandas_datareader import data as wb
import numpy as np
import matplotlib.pyplot as plt

from PortfolioItem import *

class Portfolio:
    def __init__(self, portfolioItems):
        self.initializeDictionaries(portfolioItems)
        self.securityData = pd.DataFrame()
        self.portfolioItems = portfolioItems
        
        for portfolioItem in portfolioItems:
            self.securityData[portfolioItem.ticker] = wb.DataReader(portfolioItem.ticker, data_source='yahoo', start='2016-1-1')['Adj Close']
            
    def initializeDictionaries(self, portfolioItems):
        self.portfolioCounts = dict((item.ticker, item.shareCount) for item in portfolioItems)
                                        
    def calculateReturns(self):
        securityReturns : pd.core.frame.DataFrame = np.log(self.securityData / self.securityData.shift(1))
        return securityReturns

    def listSharpeRatios(self):
        for portfolioItem in self.portfolioItems:
            print(portfolioItem.calculateSharpeRatio())

    def plotExpectedReturns(self):
        tickers = list(item.ticker for item in self.portfolioItems)
        expectedReturns = list(round(item.calculateExpectedReturnCAPM() * 100, 2) for item in self.portfolioItems)
        yPosition = np.arange(len(tickers))

        plt.bar(yPosition, expectedReturns, align='center', alpha=0.5)
        plt.xticks(yPosition, tickers)
        plt.ylabel('Expected return')
        plt.title('Portfolio expected returns')

        plt.show()
