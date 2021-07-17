from top_tweets import config, get_tweets, twitter_auth


class Bot:
    """Quote Tweet or Retweet the top Tweets by other Twitter users.

    Attributes:
        usernames (list of str or None): a list of Twitter user screen names/handles (without "@")
            whose top Tweets will be shared. Either `usernames` or `user_ids` must be None.
        user_ids (list of str or None): a list of Twitter user unique identifiers whose top Tweets
            will be shared. Either `usernames` or `user_ids` must be None.
        metric (str, optional): the default metric to sort Tweets by, largest to smallest. One of:
            - likes
            - retweets
            - likes_retweets_combined
            Uses `likes_retweets_combined` by default.

    """
    def __init__(self, usernames=None, user_ids=None, metric="likes_retweets_combined"):
        assert usernames is None or user_ids is None, "Either `usernames` or `user_ids` must be " \
                                                      "None."
        self.usernames = usernames
        self.user_ids = user_ids
        self.metric = metric


# bot = Bot(usernames=config.SOURCE_USERNAMES)
