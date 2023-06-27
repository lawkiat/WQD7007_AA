import snscrape.modules.twitter as sntwitter
import os
import json
from pymongo import MongoClient
import pandas as pd

# To request query input from user
print("Enter Twitter HashTag to search for: ")
words = input()

# To request how much tweet to be scrapped
print("Enter number of tweets to be scrapped: ")
numtweet = int(input())

tweets = []
print("Fetching tweets...")

for tweet in sntwitter.TwitterSearchScraper(words).get_items():

    if len(tweets) == numtweet:
        break
    else:
        if tweet.lang == 'en':
            tweets.append([tweet.date, tweet.id, tweet.user.username, tweet.rawContent, tweet.hashtags, tweet.replyCount, 
            tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.media])
print("Scraping has completed!")
df = pd.DataFrame(tweets, columns=['Date', 'UserId', 'User','Tweet', 'HashTags', 'ReplyCount', 'RetweetCount',
                                  'LikeCount', 'QuoteCount', 'Media'])
df.to_csv('tweetscrap.csv')

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['tweet']
collection = db['tweet_scrap']

# Open csv file to be imported
df = pd.read_csv("tweetscrap.csv")

# Transform dataframe into json format
print("Converting csv file to json format...")
data = df.to_dict(orient = "records")

# Insert transformed data into MongoDB
db.tweet_scrap.collection.insert_many(data)
print("Successfully import into MongoDB!")
