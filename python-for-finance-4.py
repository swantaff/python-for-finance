import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import mpl_finance
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

style.use ('ggplot')

#start = dt.datetime(2000,1,1)
#end = dt.datetime(2020,3,3)

#df = web.DataReader('TSLA', 'yahoo', start, end)

#df.to_csv('tsla.csv')

# read data from csv file
df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

print(df.tail()) # prints all columns

print(df[['Open', 'High']].tail()) # print specified column along with index which is date

#df['100ma'] = df['Adj Close'].rolling(window=100).mean()

df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

print(df.tail()) # prints all columns


# lets remove rows where 100ma is NaN
# df.dropna(inplace=True) 

## or we can set min periods to zero so we a an average up to 100 max for the first
# 100 values in the table
#df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()

#print(df.head()) # prints all columns

#df.plot() # shows all columns
#df['Adj Close'].plot() # shows just 'Adj Close' column
#plt.show()


#create graph template i.e. size etc.
ax1 = plt.subplot2grid((6,1), (0,0,), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0,), rowspan=1, colspan=1, sharex=ax1)

# specify x-y values for each line on the graphs above
# x-values are the date fields which is df index
# y-values are what columns we want to plot
ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
# bar chart for volume
ax2.bar(df.index, df['Volume'])

plt.show()
