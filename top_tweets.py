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
        """Return the top `top_num` Tweets from the previous `num_days`, based on `metric`.

        For example, get_top_tweets_num(30, likes, 10) would return the top 10 Tweets based
        on their number of Likes (in order from highest to lowest Likes) from the previous
        30 days (including the current day).

        Args:
            num_days (int): the historic Tweet collection period in days, including the current day.
            metric (str): the metric to sort Tweets by, largest to smallest. One of:
                - likes
                - retweets
                - likes_retweets_combined
                - num_replies
            top_num (int): the top number of Tweets to return following sorting.

        Returns:
            list of Tweet: sorted and filtered based on `num_days`, `metric`, and `top_num`.
            """
        # TODO
        pass

    def get_top_tweets_percent(self, num_days, metric, top_percent):
        """Return the top `top_percent` Tweets from the previous `num_days`, based on `metric`.

        For example, get_top_tweets_percent(30, likes, 10) would return the top 10% of Tweets
        based on their number of Likes (in order from highest to lowest Likes) from the previous
        30 days (including the current day).

        Args:
            num_days (int): the historic Tweet collection period in days, including the current day.
            metric (str): the metric to sort Tweets by, largest to smallest. One of:
                - likes
                - retweets
                - likes_retweets_combined
                - num_replies
            top_percent (int): the top percentage (1-100) of Tweets to return following sorting.

        Returns:
            list of Tweet: sorted and filtered based on `num_days`, `metric`, and `top_percent`.
            """
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
    # number of combined Likes and Retweets, rank
    def __init__(self, account, tid):
        # TODO
        pass
