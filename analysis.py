from textblob import TextBlob


def get_tweet_sentiment(tweet):

    # Utility function to classify sentiment of passed tweet using textblob's sentiment method

    # create TextBlob object of passed tweet text
    analysis = TextBlob(tweet)
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'

    elif analysis.sentiment.polarity == 0:
        return 'neutral'
        
    else:
        return 'negative'


