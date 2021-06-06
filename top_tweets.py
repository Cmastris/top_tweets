import config
import twitter_auth


class Account:
    """Retrieve, sort, and return the Tweets of a Twitter user account."""

    # Attributes: account name, account handle, Tweets (list of Tweet)
    def __init__(self, handle):
        # TODO
        pass

    def __str__(self):
        # TODO
        pass

    def fetch_tweets(self):
        """Fetch the account's public Tweets via Tweepy and assign to self.tweets."""
        # TODO
        pass

    def sort_tweets(self, criteria):
        """Sort all Tweets by Likes or Retweets and assign to self.tweets."""
        # TODO
        pass

    def top_tweets_num(self, num):
        """Return the top `num` Tweets based on the most recent sort."""
        # TODO
        pass

    def top_tweets_percent(self, percent):
        """Return the top `percent` Tweets based on the most recent sort."""
        # TODO
        pass


class Tweet:
    """A single Tweet and its associated data/metrics."""
    # Attributes: Account, ID, text, hashtags, publish date, Likes, Retweets, number of replies
    def __init__(self, account, tid):
        # TODO
        pass
