import tweepy

import config


def tweepy_auth():
    """Return an authenticated Tweepy API object."""
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
    return tweepy.API(auth, retry_count=10, retry_delay=30)


API = tweepy_auth()
