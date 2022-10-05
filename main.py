from curses import raw
from TwitterAuth import authTwitterAPI, getTweets
from houserep import getArrTwitterHandles, choosePeople
import numpy as np
import pandas as pd

# Get user inputs
chosenMembers = choosePeople()
TwitterAPI = authTwitterAPI()
columns = ['User', 'Tweets']
rawTweets = []
for member in chosenMembers:
    handle = member[2]
    tweets = getTweets(handle,TwitterAPI) 
    rawTweets.append([handle, tweets])
rawTweets_df = pd.DataFrame(rawTweets, columns=columns)

print(rawTweets_df)