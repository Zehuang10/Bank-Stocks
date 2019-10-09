>>> # Finance Data Project
>>> from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('whitegrid')

## Data

    # Bank of America
    BAC = data.DataReader("BAC", 'google', start, end)

start = datetime.datetime(2006,1,1)
end = datetime.datetime(2016,1,1)
# BOFA
BAC = data.DataReader('BAC', 'yahoo', start,end)
#Citi
C = data.DataReader('C', 'yahoo', start,end)
# Goldman Sachs
GS = data.DataReader('GS', 'yahoo', start,end)
# JP Morgan
JPM = data.DataReader('JPM', 'yahoo', start,end)
# Morgan Stanley
MS = data.DataReader('MS', 'yahoo', start,end)
# Wells Fargo
WFC = data.DataReader('WFC', 'yahoo', start,end)

# Could also do this for a Panel Object
df = data.DataReader(['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC'],'yahoo', start, end)

df.head()

**Create a list of the ticker symbols (as strings) in alphabetical order. Call this list: tickers**

ticker = 'BAC C GS JPM MS WFC'.split()

**Use pd.concat to concatenate the bank dataframes together to a single data frame called bank_stocks. Set the keys argument equal to the tickers list. Also pay attention to what axis you concatenate on.**

Here axis =1 to concatenate each stock columns and our keys help us create multilevels for each stock

bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC],axis=1,keys=ticker)

**Set the column name levels (this is filled out for you):**

bank_stocks.columns.names = ['Bank Ticker','Stock Info']

bank_stocks.head()

## Since information from Yahoo and Google finance is different, we will use the dataset provided in this lecture and use read.pickle to access the information

df = pd.read_pickle('all_banks')

**Check the head of the bank_stocks dataframe.**

df.head()

# EDA

**What is the max Close price for each bank's stock throughout the time period?**

for i in ticker:
    print(i, '$' + str(df[i]['Close'].max().round(2)))

df.xs(key='Close',axis=1,level ='Stock Info').max()

**Create a new empty DataFrame called returns. This dataframe will contain the returns for each bank's stock. returns are typically defined by:**

$$r_t = \frac{p_t - p_{t-1}}{p_{t-1}} = \frac{p_t}{p_{t-1}} - 1$$

returns = pd.DataFrame()

for i in ticker:
    returns[i+'Return'] = df[i]['Close'].pct_change()

returns.head()

**Create a pairplot using seaborn of the returns dataframe. What stock stands out to you? Can you figure out why?** 

Here since row 0 is NA, we start from 1st row

sns.pairplot(returns[1:])

returns.idxmin()

** You should have noticed that Citigroup's largest drop and biggest gain were very close to one another, did anythign significant happen in that time frame? **

returns.idxmax()

**Take a look at the standard deviation of the returns, which stock would you classify as the riskiest over the entire time period? Which would you classify as the riskiest for the year 2015?**

returns.std() #Citigroup is the riskiest over the entire time period

Here we can use loc to slice a portion of what we need or index slicing, loc for strings 

returns.loc['2015-01-01':'2015-12-31'].std() #Morgan Stanley or BofA as riskiest for 2015

**Create a distplot using seaborn of the 2015 returns for Morgan Stanley**

plt.figure(figsize=(12,5))
sns.distplot(returns.loc['2015-01-01':'2015-12-31']['MSReturn'],color='green',bins=100)

**Create a distplot using seaborn of the 2008 returns for CitiGroup**

plt.figure(figsize=(12,5))
sns.distplot(returns.loc['2008-01-01':'2008-12-31']['CReturn'],color='red',bins=100)

____
# More Visualization

A lot of this project will focus on visualizations. Feel free to use any of your preferred visualization libraries to try to recreate the described plots below, seaborn, matplotlib, plotly and cufflinks, or just pandas.

### Imports

import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# Optional Plotly Method Imports
import plotly
import cufflinks as cf
cf.go_offline()

**Create a line plot showing Close price for each bank for the entire index of time. (Hint: Try using a for loop, or use [.xs](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.xs.html) to get a cross section of the data.)**

for i in ticker:
    df[i]['Close'].plot(label=i,figsize = (12,5))
plt.legend()

Another method is to use .xs for a cross section of the data

df.xs(key='Close',axis=1,level='Stock Info').plot(figsize=(12,5))

Here we use plotly to graph the same chart but more interactive

df.xs(key='Close',axis=1,level='Stock Info').iplot()

## Moving Averages

Let's analyze the moving averages for these stocks in the year 2008. 

**Plot the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008**

Pandas allow to use rolling for moving average, and window is for how many days in this case 30

plt.figure(figsize=(12,5))
df['BAC']['Close'].loc['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label= '30 day Moving Average')
df['BAC']['Close'].loc['2008-01-01':'2009-01-01'].plot(label = 'BAC Close')
plt.legend()

**Create a heatmap of the correlation between the stocks Close Price.**

Use annot=True to display values or numbers in the boxes

sns.heatmap(df.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)

**Use seaborn's clustermap to cluster the correlations together:**

sns.clustermap(df.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)

# Part 2 (Optional)

In this second part of the project we will rely on the cufflinks library to create some Technical Analysis plots. This part of the project is experimental due to its heavy reliance on the cuffinks project, so feel free to skip it if any functionality is broken in the future.

**Use .iplot(kind='candle) to create a candle plot of Bank of America's stock from Jan 1st 2015 to Jan 1st 2016.**

close_date = df.xs(key='Close',axis=1,level='Stock Info').corr()

seaborn heatmap graph has a better representation

close_date.iplot(kind='heatmap',colorscale='rdylbu')

BAC = df.xs(key='BAC',axis=1,level='Bank Ticker')

bac15 = BAC[['Open','High','Low','Close']].loc['2015-01-01':'2016-01-01']

Candle very interesting to see if stock close higher or lower that day

bac15.iplot(kind='candle')

**Use .ta_plot(study='sma') to create a Simple Moving Averages plot of Morgan Stanley for the year 2015.**

Here ta_plot() is for technical analysis, and we specifiy sma for simple moving average and periods for days

df['MS']['Close'].loc['2015-01-01':'2016-01-01'].ta_plot(study='sma',periods=[13,21,55])

**Use .ta_plot(study='boll') to create a Bollinger Band Plot for Bank of America for the year 2015.**

This analysis boll is for the standard deviation of stock price through time 

df['BAC']['Close'].loc['2015-01-01':'2016-01-01'].ta_plot(study='boll')
