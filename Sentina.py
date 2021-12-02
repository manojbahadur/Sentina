import tweepy
import time

# Sentiment analysis using Text blob
from analysis import get_tweet_sentiment

# NOTE: I put my keys in the keys.py to separate them
# from this main file.
from keys import *


print(name_tag)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('Retrieving and replying to tweets...')
    
    # NOTE: Last seen id to not reply to same message again and again
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    
    # using reversed to reply to older tweets first
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if get_tweet_sentiment(mention.full_text.lower()) == 'positive':
            print('found a positive tweet')
            print('responding back...')
            api.update_status('@' + mention.user.screen_name + " " +
                              "Hello, Iam Sentina. It's good to hear from you. " +
                              "Thanks for sharing your experience", mention.id)
        if get_tweet_sentiment(mention.full_text.lower()) == 'negative':
            print('found a negative tweet')
            print('responding back...')
            api.update_status('@' + mention.user.screen_name + " " + 'Sorry that you had a bad experience' +
                              " Please email us your issues at sentina@gmail.com", mention.id)

        if get_tweet_sentiment(mention.full_text.lower()) == 'neutral':
            print('found a neutral tweet')
            print('responding back...')
            api.update_status('@' + mention.user.screen_name + " " +
                              "Hello, Iam Sentina. Thanks for reaching us. If your have any issues in the future,"
                              + " Please email us your issues at sentina@gmail.com", mention.id)


while True:
    reply_to_tweets()
    time.sleep(15)
