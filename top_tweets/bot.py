from top_tweets import config, get_tweets, twitter_auth


class Bot:
    """Quote Tweet or Retweet the top Tweets by other Twitter users.

    Attributes:
        api (tweepy.API): Tweepy API object authenticated with the bot account credentials.
        usernames (list of str or None): a list of Twitter user screen names/handles (without "@")
            whose top Tweets will be shared. Either `usernames` or `user_ids` must be None.
        user_ids (list of str or None): a list of Twitter user unique identifiers whose top Tweets
            will be shared. Either `usernames` or `user_ids` must be None.
        metric (str): the default metric to sort Tweets by, largest to smallest. One of:
            - likes
            - retweets
            - likes_retweets_combined
            Uses `likes_retweets_combined` by default.

    """
    def __init__(self, api, usernames=None, user_ids=None, metric="likes_retweets_combined"):
        assert usernames is None or user_ids is None, "Either `usernames` or `user_ids` must be " \
                                                      "None."
        self.api = api
        self.usernames = usernames
        self.user_ids = user_ids
        self.metric = metric

    def share_from_user(self, num_days, username=None, user_id=None, metric="default", quote=True):
        """Quote Tweet or Retweet a top Tweet by a specific user.

        The top ranked Tweet (based on `metric`) from the previous `num_days` that hasn't already
        been shared will be Quote Tweeted (quote=True) or Retweeted (quote=False).

        Args:
            num_days (int): the historic Tweet collection period in days, including the current day.
            username (str or None): a Twitter user screen name/handle (without "@")
                whose top Tweet will be shared. Either `username` or `user_id` must be None.
            user_id (str or None): a Twitter user unique identifier whose top Tweet
                will be shared. Either `username` or `user_id` must be None.
            metric (str): the default metric to sort Tweets by, largest to smallest. One of:
                - likes
                - retweets
                - likes_retweets_combined
                Uses self.metric (`likes_retweets_combined` if not set during init) by default.
            quote (bool): whether the Tweet should be Quote Tweeted (True) or Retweeted (False)

        """
        # TODO
        pass

    def share_from_random_user(self, num_days, usernames=None, user_ids=None, metric="default",
                               quote=True):
        """Quote Tweet or Retweet a top Tweet by a user randomly selected from a list.

        The top ranked Tweet (based on `metric`) from the previous `num_days` that hasn't already
        been shared will be Quote Tweeted (quote=True) or Retweeted (quote=False). The list of users
        to randomly choose from defaults to self.usernames or self.user_ids (whichever isn't None),
        or another list of either `usernames` or `user_ids` can be provided.

        Args:
            num_days (int): the historic Tweet collection period in days, including the current day.
            usernames (list of str or None): a list of Twitter user screen names/handles (without
                "@") to randomly choose from. `usernames` or `user_ids` (or both) must be None.
            user_ids (list of str or None): a list of Twitter user unique identifiers to randomly
                choose fom. `usernames` or `user_ids` (or both) must be None.
            metric (str): the default metric to sort Tweets by, largest to smallest. One of:
                - likes
                - retweets
                - likes_retweets_combined
                Uses self.metric (`likes_retweets_combined` if not set during init) by default.
            quote (bool): whether the Tweet should be Quote Tweeted (True) or Retweeted (False)

        """
        # TODO
        pass

    def previously_shared(self, tweet):
        """Return whether (True/False) the tweet has been previously Quote Tweeted or Retweeted.

        Args:
            tweet(get_tweets.Tweet): the Tweet object representing the Tweet.

        """
        # TODO
        pass

    def _retweet(self, tweet):
        """Retweet the Tweet."""
        # TODO
        pass

    def _quote_tweet(self, tweet):
        """Quote Tweet the Tweet."""
        # TODO
        pass

    @staticmethod
    def _get_quote_content(tweet, metric):
        """Return the Quote Tweet content (str)."""
        # TODO
        pass

    @staticmethod
    def _get_random_user(usernames):
        """Return a randomly selected user from a list of usernames."""
        # TODO
        pass


# bot = Bot(twitter_auth.API, usernames=config.SOURCE_USERNAMES)
