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

# credit: https://stackoverflow.com/questions/8376691/how-to-remove-hashtag-user-link-of-a-tweet-using-regular-expression
def strip_all_entities(text):
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