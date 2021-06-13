import twitter_auth


class Account:
    """Retrieve, sort, filter, and return the top Tweets of a Twitter user account."""

    # Attributes: username, display name
    def __init__(self, username):
        # TODO
        pass

    def __str__(self):
        # TODO
        pass

    def get_top_tweets_num(self, num_days, metric, top_num):
        """Return the top `top_num` Tweets from the previous `num_days`, based on `metric`."""
        # TODO
        pass

    def get_top_tweets_percent(self, num_days, metric, top_percent):
        """Return the top `top_percent` Tweets from the previous `num_days`, based on `metric`."""
        # TODO
        pass

    def _fetch_tweets(self, num_days):
        """Fetch and return the account's public Tweets from the previous `num_days`."""
        # TODO
        pass

    def _sort_tweets(self, tweets, metric):
        """Sort and return the Tweets based on `metric`."""
        # TODO
        pass

    def _filter_tweets(self, tweets, top_num):
        """Filter and return the `top_num` Tweets."""
        # TODO
        pass


class Tweet:
    """A single Tweet and its associated data/metrics."""
    # Attributes: Account, ID, text, hashtags, publish date, Likes, Retweets, number of replies,
    # total_engagement, rank
    def __init__(self, account, tid):
        # TODO
        pass
