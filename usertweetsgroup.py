'''
Created on Dec 7, 2015
@author: kzaman
'''


import tweepy
from tweepy import OAuthHandler
from time import sleep
import sqlite3
from credentials import *

sleeptime = (15 * 60)
numbertweets = 10

print("Connecting to Twitter API via Tweepy")
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

print("Setting up the database")
# Setting Up the Database
conn = sqlite3.connect(database_location) # Enter directory to save database here
c = conn.cursor()
# Setting up the table
c.execute(
    '''CREATE TABLE IF NOT EXISTS grouptweets (name, username, description, location, followers, numberstatuses, time, tweets)''')

def user_info():
    print('. . . Name: ' + str(user.name.encode('utf-8')))
    print('. . . Username: ' + str(user.screen_name.encode('utf-8')))
    print('. . . Description: ' + str(user.description.encode('utf-8')))
    print('. . . Location: ' + str(user.location.encode('utf-8')))
    print('. . . Followers: ' + str(user.followers_count))
    print('. . . Statuses: ' + str(user.statuses_count))
    return()

def pull_user_tweets():
    print("Storing user's tweets")
    for tweet in tweepy.Cursor(api.user_timeline, id = user.screen_name).items(numbertweets):
        print(tweet.created_at, tweet.text.encode('utf-8'), tweet.lang.encode('utf-8'))
        c.execute(
            "INSERT INTO grouptweets (name, username, description, location, followers, numberstatuses, time, tweets) values(?, ?, ?, ?, ?, ?, ?, ?)",
            (user.name, user.screen_name, user.description, user.location, user.followers_count, user.statuses_count,
             tweet.created_at, tweet.text,))
        conn.commit()
    return()

user_list = list();
for row in c.execute('SELECT * FROM seedaccounts'):
    user = api.get_user(row[0])
    user_list.append(user);

for user in user_list:
    user_info()
    pull_user_tweets()

c.close()