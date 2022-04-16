import numpy as np
import twitter_sa
import pandas as pd
import time
import matplotlib.pyplot as plt
import config
from binance.client import Client
import datetime
import mplfinance as mpf

client = Client(config.bin_api_key, config.bin_secret_key)
bitcoin = twitter_sa.get_tweets(twitter_sa.cryptos[0][0], twitter_sa.cryptos[0][1])
sa_value = []
tweet_time = [time.asctime()]
sentiment = 0
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC")
klines_df = pd.DataFrame(
    data=client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC"),
    columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume',
             'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore'])
klines_df['Open Time'] = pd.to_datetime(klines_df['Open Time'] / 1000, unit='s')
klines_df['Close Time'] = pd.to_datetime(klines_df['Close Time'] / 1000, unit='s')
numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'TB Base Volume', 'TB Quote Volume']

for i in range(20):
    sentiment += bitcoin.iloc[i][-1]
    i += 1
sa_value.append(sentiment)
print(sa_value)
for i in range(50):
    sentiment = 0
    bitcoin = twitter_sa.saving_tweets(bitcoin)
    for j in range(20):
        sentiment += bitcoin.iloc[j][-1]
        j += 1
    sa_value.append(sentiment)
    time.sleep(30)
    bitcoin = twitter_sa.saving_tweets(bitcoin)
    for k in range(20):
        sentiment += bitcoin.iloc[k][-1]
        k += 1
    sa_value.append(sentiment)
    time.sleep(30)
    klines1_df = pd.DataFrame(
        data=client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 minute ago UTC"),
        columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume',
                 'Number of Trades', 'TB Base Volume', 'TB Quote Volume', 'Ignore'])
    klines1_df['Open Time'] = pd.to_datetime(klines1_df['Open Time'] / 1000, unit='s')
    klines1_df['Close Time'] = pd.to_datetime(klines1_df['Close Time'] / 1000, unit='s')
    klines_df = pd.concat([klines_df, klines1_df], axis=0)
    i += 1
    tweet_time.append(time.asctime())

bitcoin.to_csv()
klines_df[numeric_columns] = klines_df[numeric_columns].apply(pd.to_numeric, axis=1)
mpf.plot(klines_df.set_index('Close Time'), sa_value,
         type='candle', style='charles')
mpf.show
plt.plot(tweet_time, sa_value)
plt.show
print('cock')
