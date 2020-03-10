import bs4 as bs
import pickle
import requests
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import os
import pandas as pd
import pandas_datareader.data as web

style.use ('ggplot')

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            ticker = ticker[:-1]
            print('Found ticker {}'.format(ticker))
            tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
            pickle.dump(tickers, f)

    print('Tickers Loaded!')
    print(tickers)

    return tickers

def get_data_from_google(reload_sp500=True):

    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
         os.makedirs('stock_dfs')

    start = dt.datetime(2000,1,1)
    end = dt.datetime(2020,3,6)

    ## just try one ticker
    ticker = tickers[0]
    print ('Getting one Ticker from file : ' +ticker)
    #df = web.DataReader('{}'.format(ticker), 'yahoo', start, end)
    df = web.DataReader(ticker, 'yahoo', start, end)
    #df = web.DataReader(ticker, 'google', start, end)
    df.to_csv('stock_dfs/{}.csv'.format(ticker))
  
    for ticker in tickers[:10]:
        try:
            print('Getting Prices for ticker {}'.format(ticker))
            if not os.path.exists('stocks_dfs/{}.csv'.format(ticker)):
#                df = web.DataReader('{}'.format(ticker), 'google', start, end)
                df = web.DataReader(ticker, 'yahoo', start, end)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            else:
                print('Already have {}'.format(ticker))
        except:
            print('Cannot obtain data for ' +ticker)

def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers=pickle.load(f)

    main_df = pd.DataFrame()

    #for count, ticker in enumerate(tickers):
    for ticker in tickers[:10]:
   
        print("Loading ticker : " +ticker)
        #check csv exists for ticker
        
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)
        df.rename(columns = {'Adj Close': ticker}, inplace=True)
        df.drop(['Open','High','Low','Close', 'Volume'], 1, inplace=True)
 
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')         
        
        ##if count % 10 == 0:
        #    print(count)
    
    print(main_df.tail())
    main_df.to_csv('sp500_joined_closes.csv')

def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')
#    df['AAP'].plot()
    df_corr = df.corr()  # awsome correlation
    
    print(df_corr.tail())

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)

    fig.colorbar(heatmap)

    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns

    #print("columns are: ")
    #print(column_labels)

    row_labels = df_corr.index

    #print("rows are: ")
    #print(row_labels)

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)

    plt.xticks(rotation=90)

    heatmap.set_clim(-1,1)

    plt.tight_layout()
    
    plt.show()


def process_data_for_labels(ticker):
    hm_days = 7
    df = pd.read_csv('sp500_joined_closes.csv', index_col = 0)

    print(df.tail())

    #tickers = list (df.columns)
    # or
    #tickers = list(df.columns.values)
    # or
    #tickers = list(df.columns.values.tolist())
    # or
    tickers = (df.columns.values.tolist())

    print(tickers)
   
    df.fillna(0, inplace=True)

    for i in range (1, hm_days + 1):
        # work out percentage change per day
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker])/ df[ticker]
    
    df.fillna(0, inplace=True)
    return tickers, df 


#save_sp500_tickers()
#get_data_from_google()
#compile_data()
#visualize_data()

process_data_for_labels('MMM')



