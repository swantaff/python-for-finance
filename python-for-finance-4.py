import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

style.use ('ggplot')


# read data from csv file
df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

# resample data
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

# candlestick chat requires mdates and ohlc columns
# so we need to reset the data frame and include / convert these columns

df_ohlc.reset_index(inplace=True) # adds index (row) number to dataframe

df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num) # converts date to mdate format(think unix time buts its not)


print(df_ohlc.tail())


#create graph template i.e. size etc.
ax1 = plt.subplot2grid((6,1), (0,0,), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0,), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()

# create candlestick graph
candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
# show volume below
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

plt.show()
