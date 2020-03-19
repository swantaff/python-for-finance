import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use ('ggplot')

start = dt.datetime(2000,1,1)
end = dt.datetime(2020,3,13)

df = web.DataReader('0P0000KSPA.L', 'yahoo', start, end)

df.to_csv('vanguard.csv')

# read data from csv file
df = pd.read_csv('vanguard.csv', parse_dates=True, index_col=0)

print(df.tail()) # prints all columns

print(df[['Open', 'High']].tail()) # print specified column along with index which is date

#df.plot() # shows all columns
df['Adj Close'].plot() # shows just 'Adj Close' column
plt.show()
