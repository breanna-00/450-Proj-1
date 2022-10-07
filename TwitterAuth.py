from distutils.command import clean
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import tweepy
import re
import configparser
import string
from string import digits

# everything below is from AI Spectrum on Youtube and his github

def authTwitterAPI():
    # read configs
    config = configparser.ConfigParser()
    config.read('config.ini')

    api_key = config['twitter']['api_key']
    api_key_secret = config['twitter']['api_key_secret']

    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']

    # authentication
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api

# credits:
# https://stackoverflow.com/questions/8376691/how-to-remove-hashtag-user-link-of-a-tweet-using-regular-expression
# https://www.youtube.com/watch?v=b9G78PxZtX8&t=203s
# https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python - Emoji links
# https://stackoverflow.com/questions/71591365/cleaning-up-tweets-before-sentiment-analysis-on-cryptocurrencies 
def strip_all_entities(text):
    # --Clean Text Data
    text = text.replace("@[A-Za-z0-9_]+", '', True)
    text = text.replace('http\S+', '', True)
    text = text.replace('[\+()!?:“”’"\[\]&]', '', True)
    text = text.replace('\\\\', '', True)
    ##Filter Emojis expression- Creation of the regular expresion compiler
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    text = re.sub(emoji_pattern, '', text)
    entity_prefixes = ['@']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
              # Removes RT
            if word == 'RT':
                words.remove(word)
    return ' '.join(words)

def getTweets(user, api):
    print("...Fetching Tweets From " + user + "...")
    limit=50
    tweets = tweepy.Cursor(api.user_timeline, screen_name=user, count=200, tweet_mode='extended').items(limit)
    data = []
    for tweet in tweets:
        clean_tweet = re.sub(r'http\S+', '', tweet.full_text)
        clean_tweet = re.sub(r'\d+', '', clean_tweet)
        clean_tweet = strip_all_entities(clean_tweet)
        data.append(clean_tweet)
    return data