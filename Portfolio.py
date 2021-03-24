import pandas as pd
from pandas_datareader import data as wb
import numpy as np

from PortfolioItem import *

class Portfolio:
    def __init__(self, portfolioItems: [PortfolioItem]):
        self.initializeDictionaries(portfolioItems)
        self.securityData = pd.DataFrame()
        
        for portfolioItem in portfolioItems:
            self.securityData[portfolioItem.ticker] = wb.DataReader(portfolioItem.ticker, data_source='yahoo', start='2016-1-1')['Adj Close']
            
    def initializeDictionaries(self, portfolioItems: [PortfolioItem]):
        self.portfolioCounts = dict((item.ticker, item.shareCount) for item in portfolioItems)
                                        
    def calculateReturns(self):
        securityReturns : pd.core.frame.DataFrame = np.log(self.securityData / self.securityData.shift(1))
        return securityReturns