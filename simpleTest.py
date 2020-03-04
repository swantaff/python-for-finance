import pandas as pd
import pandas_datareader.data as web
import datetime
pd.set_option('display.width', 200) # Displaying more columns in one row

# Data date range, Google provides up to 4000 entries in one call
start = datetime.datetime(2016, 3, 2) 
end = datetime.datetime(2020, 3, 2)

spy = web.DataReader("MSFT", "yahoo", start, end)

print(spy.tail()) # See last few rows
