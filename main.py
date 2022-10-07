##from curses import raw
from os import remove
import re
from opcode import hasjabs
from TwitterAuth import authTwitterAPI, getTweets
from houserep import getArrTwitterHandles, choosePeople, getFilterWord
import numpy as np
import pandas as pd
from wordcloud import STOPWORDS

# Get user inputs @nikki
chosenMembers = choosePeople()
TwitterAPI = authTwitterAPI()
columns = ['User', 'Tweets']
rawTweets = []


# Get raw tweet data @githel @breanna
for member in chosenMembers:
    handle = member[2]
    print(handle)
    tweets = getTweets(handle,TwitterAPI) 
    rawTweets.append([handle, tweets])
rawTweets_df = pd.DataFrame(rawTweets, columns=columns)


# Clean raw tweet data @Katherine

fillerWords = getFilterWord()
# Function to just take the words that are not in the list of filler words
def remove_word(text):
    
    textFilter = [word for word in text.split() if word not in fillerWords] 

    return " ".join(textFilter)
##deletes Stopwords
rawTweets_df['Tweets'] = rawTweets_df.Tweets.map(lambda x: remove_word(x.to_string().lower()))  
## delete Non text data
rawTweets_df["Tweets"] = rawTweets_df["Tweets"].str.replace("@[A-Za-z0-9_]+", '', regex=True)
rawTweets_df["Tweets"] = rawTweets_df["Tweets"].str.replace("#[A-Za-z0-9_]+", '', regex=True) 
rawTweets_df["Tweets"] = rawTweets_df["Tweets"].str.replace('http\S+', '', regex=True)
rawTweets_df["Tweets"] = rawTweets_df["Tweets"].str.replace('[\+()!?:“”’"\[\]&]', '', regex=True)
rawTweets_df["Tweets"] = rawTweets_df["Tweets"].str.replace('\\\\', '', regex=True)

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

## execute the filter emojis expression
rawTweets_df["Tweets"] = rawTweets_df["Tweets"].str.replace(emoji_pattern, "", regex=True)


#If we want an X representative we can use print(rawTweets_df['Tweets'].iloc[X]) where X is the # of the representative
print(rawTweets_df['Tweets']) # prints all the tweets filtered

# Credits
# https://www.youtube.com/watch?v=b9G78PxZtX8&t=203s
# https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python - Emoji links
# https://stackoverflow.com/questions/71591365/cleaning-up-tweets-before-sentiment-analysis-on-cryptocurrencies 







# use rawTweets_df 

# Send clean tweet data to Natural Language API @githel