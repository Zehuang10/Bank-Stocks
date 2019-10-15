# Bank-Stocks
# Finance Data Project 

*Note: [You'll need to install pandas-datareader for this to work!](https://github.com/pydata/pandas-datareader) Pandas datareader allows you to [read stock information directly from the internet](http://pandas.pydata.org/pandas-docs/stable/remote_data.html) Use these links for install guidance (**pip install pandas-datareader**), or just follow along with the video lecture.*

### The Imports

    from pandas_datareader import data, wb
    import pandas as pd
    import numpy as np
    import datetime
    %matplotlib inline
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.set_style('whitegrid')

## Data

We need to get data using pandas datareader. We will get stock information for the following banks:
*  Bank of America
* CitiGroup
* Goldman Sachs
* JPMorgan Chase
* Morgan Stanley
* Wells Fargo
    
    # Bank of America
        BAC = data.DataReader("BAC", 'google', start, end)

### WARNING: MAKE SURE TO CHECK THE LINK ABOVE FOR THE LATEST WORKING API. "google" MAY NOT ALWAYS WORK.

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

    bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC],axis=1,keys=ticker)

**Set the column name levels (this is filled out for you):**

    bank_stocks.columns.names = ['Bank Ticker','Stock Info']

    bank_stocks.head()

## Since information from Yahoo and Google finance is different, we will use the dataset provided in this lecture and use read.pickle to access the information

    df = pd.read_pickle('all_banks')

**Check the head of the bank_stocks dataframe.**

    df.head()

**What is the max Close price for each bank's stock throughout the time period?**

    for i in ticker:
        print(i, '$' + str(df[i]['Close'].max().round(2)))

    df.xs(key='Close',axis=1,level ='Stock Info').max()

**Create a new empty DataFrame called returns. This dataframe will contain the returns for each bank's stock. returns are typically defined by:**

    $$r_t = \frac{p_t - p_{t-1}}{p_{t-1}} = \frac{p_t}{p_{t-1}} - 1$$

    returns = pd.DataFrame()

**We can use pandas pct_change() method on the Close column to create a column representing this return value. Create a for loop that goes and for each Bank Stock Ticker creates this returns column and set's it as a column in the returns DataFrame.**

    for i in ticker:
        returns[i+'Return'] = df[i]['Close'].pct_change()

    returns.head()

**Create a pairplot using seaborn of the returns dataframe. What stock stands out to you? Can you figure out why?** 

    sns.pairplot(returns[1:])

**Using this returns DataFrame, figure out on what dates each bank stock had the best and worst single day returns. You should notice that 4 of the banks share the same day for the worst drop, did anything significant happen that day?** 

    returns.idxmin()

    returns.idxmax()

**Take a look at the standard deviation of the returns, which stock would you classify as the riskiest over the entire time period? Which would you classify as the riskiest for the year 2015?**

    returns.std() #Citigroup is the riskiest over the entire time period

    returns.loc['2015-01-01':'2015-12-31'].std() #Morgan Stanley or BofA as riskiest for 2015

**Create a distplot using seaborn of the 2015 returns for Morgan Stanley**

    plt.figure(figsize=(12,5))
    sns.distplot(returns.loc['2015-01-01':'2015-12-31']['MSReturn'],color='green',bins=100)

**Create a distplot using seaborn of the 2008 returns for CitiGroup**

    plt.figure(figsize=(12,5))
    sns.distplot(returns.loc['2008-01-01':'2008-12-31']['CReturn'],color='red',bins=100)

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

    df.xs(key='Close',axis=1,level='Stock Info').iplot()

## Moving Averages

Let's analyze the moving averages for these stocks in the year 2008. 

**Plot the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008**

    plt.figure(figsize=(12,5))
    df['BAC']['Close'].loc['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label= '30 day Moving Average')
    df['BAC']['Close'].loc['2008-01-01':'2009-01-01'].plot(label = 'BAC Close')
    plt.legend()

**Create a heatmap of the correlation between the stocks Close Price.**

    sns.heatmap(df.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)

**Use seaborn's clustermap to cluster the correlations together:**

    sns.clustermap(df.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)

# Part 2 (Optional)

In this second part of the project we will rely on the cufflinks library to create some Technical Analysis plots. This part of the project is experimental due to its heavy reliance on the cuffinks project, so feel free to skip it if any functionality is broken in the future.

    close_date = df.xs(key='Close',axis=1,level='Stock Info').corr()

    close_date.iplot(kind='heatmap',colorscale='rdylbu')

    BAC = df.xs(key='BAC',axis=1,level='Bank Ticker')

    bac15 = BAC[['Open','High','Low','Close']].loc['2015-01-01':'2016-01-01']

    bac15.iplot(kind='candle')

**Use .ta_plot(study='sma') to create a Simple Moving Averages plot of Morgan Stanley for the year 2015.**

    df['MS']['Close'].loc['2015-01-01':'2016-01-01'].ta_plot(study='sma',periods=[13,21,55])

**Use .ta_plot(study='boll') to create a Bollinger Band Plot for Bank of America for the year 2015.**

    df['BAC']['Close'].loc['2015-01-01':'2016-01-01'].ta_plot(study='boll')
