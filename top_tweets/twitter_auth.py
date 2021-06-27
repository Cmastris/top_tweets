import tweepy

from top_tweets import config


def tweepy_auth():
    """Return an authenticated Tweepy API object."""
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
    # TODO: set retry values (10, 30) for production use
    return tweepy.API(auth, retry_count=0, retry_delay=0)


API = tweepy_auth()
