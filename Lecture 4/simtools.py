# simtools.py: routines for loading and pre-processing tick data

import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

# helper routing to log a message with time
def log_msg( label_string ):
    ts = time.time()
    st = datetime.datetime.fromtimestamp( ts ).strftime( '%Y-%m-%d %H:%M:%S:%f' )
    print( label_string + ' : ' + st )

# load and normalize trade file
def loadtradefile(tickfilename):
    log_msg( 'load trades' )
    trades = pd.read_csv(tickfilename, infer_datetime_format=True)
    log_msg( 'load complete' )
    log_msg( 'indexing trades' )
    format = '%Y%m%d%H:%M:%S.%f'

    # fix padding on time
    times = trades['TIME_M'].apply(lambda x: x.zfill(18))
    timestamps = trades['DATE'].astype(str) + times
    times = pd.to_datetime( timestamps, format = format )
    trades.index = times
    trades = trades.drop(columns=['DATE', 'TIME_M'])
    log_msg( "index trades done" )
    
    # standardize column names
    trades.columns = ['symbol', 'suffix', 'trade_size', 'trade_px']
    
    # return a dataframe
    return trades

# load and normalize file
def loadquotefile(tickfilename):   
    log_msg( 'load quotes' )
    quotes = pd.read_csv(tickfilename, infer_datetime_format=True)
    log_msg( 'load complete' )
    log_msg( 'indexing quotes' )
    format = '%Y%m%d%H:%M:%S.%f'

    # fix padding on time
    times = quotes['TIME_M'].apply(lambda x: x.zfill(18))
    timestamps = quotes['DATE'].astype(str) + times
    times = pd.to_datetime( timestamps, format = format )
    quotes.index = times
    quotes = quotes.drop(columns=['DATE', 'TIME_M'])
    log_msg( "index quotes done" )
    
    # standardize column names
    quotes.columns = ['exch', 'bid_px', 'bid_size', 'ask_px', 'ask_size', 'symbol', 'suffix']
    
    # return a dataframe
    return quotes

# make a merged file for simulation
# NOTE this currently doesn't support tickers with suffixes...
def makeTAQfile(trades, quotes):
    log_msg( 'start merge' )
    taq = quotes.merge( trades, how = 'outer', on = 'symbol', left_index = True, right_index = True )
    log_msg( 'end merge' )
    return taq
    
# TODO: calculate some stats on tick data
def datastats(somedataframe):
    return 1

# TODO: calculate some basic P&L
def profitandloss(somedataframe):
    return 1