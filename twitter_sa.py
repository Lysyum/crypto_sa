import re
import pandas as pd
import tweepy
from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np
import config

finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

client = tweepy.Client(config.bearer_token)
cryptos = [['Bitcoin', 'BTC'], ['Ethereum', 'ETH'], ['Tether', 'USDT'], ['BNB', 'BNB'], ['USD Coin', 'USDC'],
           ['XRP', 'XRP'], ['Terra', 'LUNA'], ['Solana', 'SOL'], ['Avalanche', 'AVAX']]
labels = {0: 0, 1: 1, 2: -1}


def cleanTxt(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)  # removed @mentions
    text = re.sub(r'#', '', text)  # removing the '#' symbol
    text = re.sub(r'RT[\s]+', '', text)  # removing RT
    text = re.sub(r'https?:\/\/\S+', '', text)  # remove the hyper link
    text = re.sub(r'\n', '', text)  # remove \n
    RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    text = RE_EMOJI.sub(r'', text)  # emoji clearing
    return text


def get_tweets(crypto, ticker):
    query = 'lang:en #' + crypto + ' -is:retweet -has:media OR lang:en #' + ticker + ' -is:retweet -has:media'
    response = client.search_recent_tweets(query=query, max_results=20, tweet_fields=['created_at'])
    tweet_list = []
    for tweet in response.data:
        tweet_list.append(tweet)
    df = pd.DataFrame(data=tweet_list)
    df['text'] = df['text'].apply(cleanTxt)
    df = df.drop(['id'], axis=1)
    marvin = list(df['text'])
    inputs = tokenizer(marvin, return_tensors="pt", padding=True)
    outputs = finbert(**inputs)[0]
    sentiment = []
    for i in range(20):
        sentiment.append(labels[np.argmax(outputs.detach().numpy()[i])])
    sentiment_df = pd.DataFrame(data=sentiment, columns=['sentiment'])
    df = pd.concat([df, sentiment_df], axis=1)
    return df


def saving_tweets(spot):
    x = get_tweets(cryptos[0][0], cryptos[0][1])
    merge = pd.concat([spot, x], axis=1)
    return merge
