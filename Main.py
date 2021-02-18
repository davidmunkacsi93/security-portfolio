from PortfolioItem import *
from Portfolio import *

portfolioItems = [PortfolioItem('AAPL', 24), PortfolioItem('HFG.DE', 11)]
portfolio = Portfolio(portfolioItems)

portfolio.getReturnsCorrelation()