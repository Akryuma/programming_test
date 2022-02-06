import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

data = pd.read_csv ('data/data.csv')
# Logic


def check_uniqueness(lst):
    """
    Check if a list contains only unique values.
    Returns True only if all values in the list are unique, False otherwise
    """
    lst_aux = sorted(lst)
    for i in range(len(lst_aux) - 1):
        if lst_aux[i] == lst_aux[i + 1]:
            return False
    return True


def smallest_difference(array):
    """
    Code a function that takes an array and returns the smallest
    absolute difference between two elements of this array
    Please note that the array can be large and that the more
    computationally efficient the better
    """
    lst_aux = sorted(array)
    mini = np.inf
    for i in range(len(lst_aux) - 1):
        if lst_aux[i + 1] - lst_aux[i] < mini:
            mini = lst_aux[i + 1] - lst_aux[i]
    return mini


# Finance and DataFrame manipulation


def macd(prices, window_short=12, window_long=26):
    """
    Code a function that takes a DataFrame named prices and
    returns it's MACD (Moving Average Convergence Difference) as
    a DataFrame with same shape
    Assume simple moving average rather than exponential moving average
    The expected output is in the output.csv file
    """
    #we suppose the dataframe has 2 columns : date and SX5T Index
    df = prices.copy()
    n = len(df)
    sma_short = 0
    sma_long = 0
    
    for i in range(0,window_long- window_short):
        sma_long += prices.loc[i][1]
    for i in range(window_long- window_short, window_long):
        sma_long += prices.loc[i][1]
        sma_short += prices.loc[i][1]
        
    sma_short = sma_short / window_short
    sma_long = sma_long / window_long
    df.at[window_long -1,prices.columns[1]] = sma_short - sma_long
    
    
    for i in range(window_long,n):
        sma_short = (sma_short*window_short + prices.loc[i][1] - prices.loc[i-window_short][1])/window_short

        sma_long = (sma_long*window_long + prices.loc[i][1] - prices.loc[i-window_long][1])/window_long
        
        df.at[i,prices.columns[1]] = sma_short - sma_long
    return df
        
    


def sortino_ratio(prices):
    """
    Code a function that takes a DataFrame named prices and
    returns the Sortino ratio for each column
    Assume risk-free rate = 0
    On the given test set, it should yield 0.05457
    """
    #first column of prices is date
    pl = np.zeros([len(prices.columns) - 1,len(prices) - 1])
    res= np.zeros(len(prices.columns) - 1)
    for j in range(1,len(prices.columns)):
        for i in range(len(prices) - 1):
            pl[j -1][i] = prices.loc[i + 1][j] - prices.loc[i][j]
        res[j-1] = (prices.loc[len(prices)-1][j] - prices.loc[len(prices)-2][j])/ np.std(pl[j-1][pl[j-1]<0])
    return res


def expected_shortfall(prices, level=0.95):
    """
    Code a function that takes a DataFrame named prices and
    returns the expected shortfall at a given level
    On the given test set, it should yield -0.03468
    """
    #first column of prices is date
    pl = np.zeros(len(prices) - 1)
    for i in range(len(prices) - 1):
        pl[i] = prices.loc[i + 1][1] - prices.loc[i][1]
    pl = np.sort(pl)
    return np.mean(pl[0:int(len(prices) * 0.95)])


# Plot


def visualize(prices, path):
    """
    Code a function that takes a DataFrame named prices and
    saves the plot to the given path
    """
    fig, axs = plt.subplots(figsize=(12, 4))
    prices.plot.area(ax=axs)
    fig.savefig(path)
    
