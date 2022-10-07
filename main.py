from os import remove
import re
from opcode import hasjabs
from curses import raw
from TwitterAuth import authTwitterAPI, getTweets
from houserep import choosePeople
import numpy as np
import pandas as pd
from google.cloud import language_v1
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist

# --- User Interaction: Get user inputs @nikki ---
chosenMembers = choosePeople()
TwitterAPI = authTwitterAPI()
rawTweets = []
print(str(chosenMembers))

# --- Fetch Data: Get tweet data @githel @breanna ---
for member in chosenMembers:
    handle = member[2]
    tweets = getTweets(handle,TwitterAPI) 
    # extend tweets array to rawTweets
    rawTweets += tweets

# --- Entity Analysis: Send clean tweet data to Natural Language API @githel ---
# Save phrases as entire words
# 1. run entity analysis to separate phrases with NLP API
# 2. get frequency per phrase with nltk 
phrases = []
print("...Running Entity Analysis on All Tweets...")
for tweet in rawTweets:
    LangAPI = language_v1.LanguageServiceClient()
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": tweet, "type_": type_, "language": language}
    encoding_type = language_v1.EncodingType.UTF8
    response = LangAPI.analyze_entities(request = {'document': document, 'encoding_type': encoding_type})

    for entity in response.entities:
        # Loop over the mentions of this entity in the input document to grab individual phrases
        for mention in entity.mentions:
            phrase = mention.text.content
            phrases.append(phrase)
# Count frequencies per phrase
phrase_freqs = nltk.FreqDist(phrases)
top_words = dict(sorted(phrase_freqs.items(), key=lambda item: item[1]))
# --- Output for User ---
print("--- Top 50 Words with Frequencies from House of Rep Member Tweets ---")
members_str = '-- Members: '
for member in chosenMembers:
    members_str += member[2] + ", "
print(members_str + " --\n")
for phrase, freq in top_words.items():
    print(phrase + ": " + str(freq))

# --- WordCloud: Create WordCloud based on Phrase Frequencies ---
word_cloud = WordCloud(background_color='white',width=900,height=500, max_words=1628,relative_scaling=1,normalize_plurals=False).generate_from_frequencies(top_words)
plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
plt.show()

