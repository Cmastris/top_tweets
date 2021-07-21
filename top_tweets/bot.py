import random

from top_tweets import config, get_tweets, twitter_auth


class Bot:
    """Quote Tweet or Retweet the top Tweets by other Twitter users.

    Attributes:
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
    def __init__(self, usernames=None, user_ids=None, metric="likes_retweets_combined"):
        assert usernames is None or user_ids is None, "Either `usernames` or `user_ids` must be " \
                                                      "None."
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
        if metric == "default":
            metric = self.metric

        account = get_tweets.Account(username=username, user_id=user_id)
        tweets = account.get_top_tweets_percent(num_days, metric, 100)
        tweet = self._select_tweet(tweets, num_days)

        if quote:
            content = self._get_quote_content(tweet, metric)
            self._quote_tweet(tweet, content)
        else:
            self._retweet(tweet)

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
        if metric == "default":
            metric = self.metric

        if usernames is not None:
            user = self._get_random_user(usernames)
            account = get_tweets.Account(username=user)
        elif user_ids is not None:
            user = self._get_random_user(user_ids)
            account = get_tweets.Account(user_id=user)
        else:
            # User list not provided, default list used instead
            if self.usernames is not None:
                user = self._get_random_user(self.usernames)
                account = get_tweets.Account(username=user)
            else:
                user = self._get_random_user(self.user_ids)
                account = get_tweets.Account(user_id=user)

        tweets = account.get_top_tweets_percent(num_days, metric, 100)
        tweet = self._select_tweet(tweets, num_days)

        if quote:
            content = self._get_quote_content(tweet, metric)
            self._quote_tweet(tweet, content)
        else:
            self._retweet(tweet)

    def previously_retweeted(self, tweet):
        """Return whether (True/False) the tweet has been previously Retweeted.

        Args:
            tweet(get_tweets.Tweet): the Tweet object representing the Tweet.

        """
        return tweet.retweeted

    def previously_quoted(self, tweet, num_days):
        """Return whether (True/False) the tweet has been Quote Tweeted in the previous `num_days`.

        Args:
            tweet(get_tweets.Tweet): the Tweet object representing the Tweet.
            num_days (int): the historic assessment period (i.e. whether the Tweet was Quote
                Tweeted) in days, including the current day.

        """
        # TODO
        # loop through user timeline
        # compare bot_tweet.quoted_tweet_id with tweet.id, return True if equal
        # return False if reached num_days

    def _select_tweet(self, tweets, num_days):
        """Return the top unshared (see notes) Tweet from a list of ranked Tweets.

        Specifically, a Tweet will be returned if it has never been Retweeted and if it hasn't been
        Quote Tweeted in the previous `num_days`.

        Args:
            tweets (list of get_tweets.Tweet): a list of Tweet objects.
            num_days (int): the historic assessment period (i.e. whether the Tweet was Quote
                Tweeted) in days, including the current day.
        """
        # TODO
        # Loop through Tweets
        # Return if not previously_retweeted() and not previously_quoted()
        # Raise exception if all Tweets already shared
        pass

    def _retweet(self, tweet):
        """Retweet the Tweet."""
        # TODO
        pass

    def _quote_tweet(self, tweet, content):
        """Quote Tweet the Tweet with the provided content."""
        # TODO
        pass

    @staticmethod
    def _get_quote_content(tweet, metric):
        """Return the Quote Tweet content (str)."""
        # TODO
        pass

    @staticmethod
    def _get_random_user(user_list):
        """Return a randomly selected item from a list of usernames or user IDs."""
        assert len(user_list) > 0, "No items in the user list; unable to select a random user."
        return random.choice(user_list)


# bot = Bot(usernames=config.SOURCE_USERNAMES)
