from curses import raw
from TwitterAuth import authTwitterAPI, getTweets
from houserep import getArrTwitterHandles, choosePeople
import numpy as np
import pandas as pd

# Get user inputs @nikki
chosenMembers = choosePeople()
TwitterAPI = authTwitterAPI()
columns = ['User', 'Tweets']
rawTweets = []

# Get raw tweet data @githel @breanna
for member in chosenMembers:
    handle = member[2]
    tweets = getTweets(handle,TwitterAPI) 
    rawTweets.append([handle, tweets])
rawTweets_df = pd.DataFrame(rawTweets, columns=columns)

print(rawTweets_df)

# Clean raw tweet data @katrina

# use rawTweets_df 

# Send clean tweet data to Natural Language API @githel