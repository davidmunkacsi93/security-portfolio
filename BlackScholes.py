import pandas as pd
from pandas_datareader import data as wb
import numpy as np
from scipy.stats import norm

class BlackScholes:
    def BSM(self, stockPrice, strikePrice, riskFree, standardDeviation, timeInYears):
        return (stockPrice * norm.cdf(self.d1(stockPrice, strikePrice, riskFree, standardDeviation, timeInYears))) \
            - (strikePrice * np.exp(- riskFree * timeInYears) * norm.cdf(self.d2(self, stockPrice, strikePrice, riskFree, standardDeviation, timeInYears)))  

    def d1(stockPrice, strikePrice, riskFree, standardDeviation, timeInYears):
        return (np.log(stockPrice / strikePrice) \
            +  (riskFree + standardDeviation ** 2 / 2) * timeInYears) \
            / (standardDeviation * np.sqrt(timeInYears))

    def d2(stockPrice, strikePrice, riskFree, standardDeviation, timeInYears):
        return (np.log(stockPrice / strikePrice) \
        -  (riskFree + standardDeviation ** 2 / 2) * timeInYears) \
        / (standardDeviation * np.sqrt(timeInYears))