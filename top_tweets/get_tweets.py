import datetime

import tweepy

from top_tweets import twitter_auth


class Account:
    """Retrieve, sort, filter, and return the top Tweets of a Twitter user account.

    https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/user

    Attributes:
        user (Tweepy User): the Tweepy User object.
        username (str): the User's screen name/handle (without "@").
        user_id (str): the User's unique identifier.
        name (str): the User's profile name.
        statuses_count (int): the number of Tweets (including Retweets) published by the User.

    """
    def __init__(self, username=None, user_id=None):
        if username is not None:
            self.user = twitter_auth.API.get_user(screen_name=username)
        elif user_id is not None:
            self.user = twitter_auth.API.get_user(user_id=user_id)
        else:
            raise ValueError("Error initialising Account. "
                             "You must provide a `username` or `user_id` as a keyword argument.")

        self.username = self.user.screen_name
        self.user_id = self.user.id_str
        self.name = self.user.name
        self.statuses_count = self.user.statuses_count

    def __str__(self):
        return "{} (@{})".format(self.name, self.username)

    def get_top_tweets_num(self, num_days, metric, top_num, max_tweets=None):
        """Return the top `top_num` Tweets from the previous `num_days`, based on `metric`.

        For example, get_top_tweets_num(30, "likes", 10) would return the top 10 Tweets based
        on their number of Likes (in order from highest to lowest Likes) from the previous
        30 days (including the current day).

        Excludes Retweets, Quote Tweets, and replies. API response and rate limits apply:
        https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline.

        Args:
            num_days (int): the historic Tweet collection period in days, including the current day.
            metric (str): the metric to sort Tweets by, largest to smallest. One of:
                - likes
                - retweets
                - likes_retweets_combined
            top_num (int): the top number of Tweets to return following sorting.
            max_tweets (int or None): the maximum number of Tweets to retrieve from the previous
                `num_days`, before sorting and filtering (defaults to None). For example, can be
                used in combination with a very high `num_days` (e.g. 9999) to find top Tweets from
                the previous 100 Tweets regardless of their publish date.

        Returns:
            list of Tweet: sorted and filtered based on passed arguments.

        """
        fetched_tweets = self._fetch_tweets(num_days, max_tweets)
        sorted_tweets = self._sort_tweets(fetched_tweets, metric)
        return self._filter_tweets(sorted_tweets, top_num)

    def get_top_tweets_percent(self, num_days, metric, top_percent, max_tweets=None):
        """Return the top `top_percent` Tweets from the previous `num_days`, based on `metric`.

        For example, get_top_tweets_percent(30, "likes", 10) would return the top 10% of Tweets
        based on their number of Likes (in order from highest to lowest Likes) from the previous
        30 days (including the current day).

        Excludes Retweets, Quote Tweets, and replies. API response and rate limits apply:
        https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline.

        Args:
            num_days (int): the historic Tweet collection period in days, including the current day.
            metric (str): the metric to sort Tweets by, largest to smallest. One of:
                - likes
                - retweets
                - likes_retweets_combined
            top_percent (int): the top percentage (1-100) of Tweets to return following sorting.
            max_tweets (int or None): the maximum number of Tweets to retrieve from the previous
                `num_days`, before sorting and filtering (defaults to None). For example, can be
                used in combination with a very high `num_days` (e.g. 9999) to find top Tweets from
                the previous 100 Tweets regardless of their publish date.

        Returns:
            list of Tweet: sorted and filtered based on passed arguments.

        """
        fetched_tweets = self._fetch_tweets(num_days, max_tweets)
        sorted_tweets = self._sort_tweets(fetched_tweets, metric)
        top_num = round((top_percent/100) * len(sorted_tweets))
        return self._filter_tweets(sorted_tweets, top_num)

    @staticmethod
    def cut_off_time(latest_date, num_days):
        """Return the Tweet collection cut-off (start) time (datetime.datetime).

        Specifically, this returns `latest_date` minus (`num_days` -1), i.e. the start time for
        `num_days` days of Tweets including the `latest_date`. For example,
        cut_off_time(datetime.date.today(), 1) would return a datetime.datetime object representing
        the start of the current day.

        Args:
            latest_date (datetime.date): a datetime.date object representing the latest
                (most recent) date to collect Tweets from, e.g. the current day.
            num_days (int): the historic Tweet collection period in days, inclusive of the
                `latest_date`.

        """
        date = latest_date - datetime.timedelta(days=(num_days - 1))
        return datetime.datetime(date.year, date.month, date.day)

    def _fetch_tweets(self, num_days, max_tweets):
        """Fetch and return a list of the account's public Tweets.

        Excludes Retweets, Quote Tweets, and replies. API response and rate limits apply:
        https://developer.twitter.com/en/docs/twitter-api/v1/tweets/timelines/api-reference/get-statuses-user_timeline.

        Args:
            num_days (int): the historic Tweet collection period in days, including the current day.
            max_tweets (int or None): the maximum number of Tweets to retrieve from the previous
                `num_days` (defaults to None).

        """
        cut_off = self.cut_off_time(datetime.date.today(), num_days)
        tweets = []
        print("Fetching Tweets by '{}'...".format(self))
        # Cursor object handles pagination and returns a list of Tweepy Status
        for t in tweepy.Cursor(twitter_auth.API.user_timeline,
                               id=self.user_id,
                               include_rts=False,
                               exclude_replies=True,
                               tweet_mode="extended").items():

            tweet = Tweet(t, self)
            if len(tweets) == max_tweets:
                break
            elif tweet.published_before(cut_off):
                break
            elif tweet.is_quote_tweet:
                continue
            else:
                tweets.append(tweet)

        assert len(tweets) > 0, "No Tweets (excluding Retweets/Quote Tweets/replies) returned " \
                                "for '{}' since {}.".format(self, cut_off)
        return tweets

    def _sort_tweets(self, tweets, metric):
        """Sort and return a list of Tweet based on `metric` (highest to lowest)."""
        metric = metric.lower()
        valid_metrics = ["likes", "retweets", "likes_retweets_combined"]
        assert metric in valid_metrics, "{} is not a valid metric to sort Tweets by.".format(metric)
        print("Sorting Tweets based on {}...".format(metric))
        sorted_tweets = sorted(tweets, key=lambda t: getattr(t, metric), reverse=True)

        rank = 1
        for tweet in sorted_tweets:
            tweet.rank = rank
            rank += 1

        return sorted_tweets

    def _filter_tweets(self, tweets, top_num):
        """Filter and return the `top_num` Tweets."""
        if top_num > len(tweets):
            print("Only {} Tweets fetched; returning all {}...".format(len(tweets), len(tweets)))
        else:
            print("Returning the top {} of {} Tweets...".format(top_num, len(tweets)))
        return tweets[:top_num]


class Tweet:
    """A single Tweet and its associated data/metrics.

    https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet

    Attributes:
        status (Tweepy Status): the Tweepy Status (Tweet) object.
        account (Account or None): the Twitter user account which published the Tweet, or None.
        id (str): the Tweet's unique identifier.
        publish_time (datetime.datetime): datetime object representing when the Tweet was published.
        is_quote_tweet (bool): whether the Tweet is a Quote Tweet.
        quoted_tweet_id (str or None): the quoted Tweet's unique identifier, or None if
            the Tweet is not a Quote Tweet.
        retweeted_tweet (tweepy.models.Status or None): the Retweeted Tweet Tweepy Status (Tweet)
            object, or None if the Tweet is not a Retweet.
        text (str): the UTF-8 text of the Tweet.
        hashtags (list of dict): list of Twitter API (v1) Hashtag object.
        likes (int): how many times the Tweet has been Liked.
        retweets (int): how many times the Tweet has been Retweeted.
        likes_retweets_combined (int): the sum of the Tweet's Likes and Retweets.
        rank (int or None): the Tweet's rank (1 is best/highest) relative to other Tweets that
            have been sorted by engagement, or None if Tweets haven't been sorted.
        retweeted (bool): whether the Tweet has been Retweeted by the authenticating user.

    """
    def __init__(self, status, account):
        self.status = status
        self.account = account
        self.id = status.id_str
        self.publish_time = status.created_at
        self.is_quote_tweet = status.is_quote_status
        if self.is_quote_tweet:
            self.quoted_tweet_id = status.quoted_status_id_str
        else:
            self.quoted_tweet_id = None

        try:
            self.retweeted_tweet = status.retweeted_status
        except AttributeError:
            self.retweeted_tweet = None

        try:
            # If `tweet_mode="extended"`
            self.text = status.full_text
        except AttributeError:
            self.text = status.text

        self.hashtags = status.entities.get("hashtags")
        self.likes = status.favorite_count
        self.retweets = status.retweet_count
        self.likes_retweets_combined = self.likes + self.retweets
        self.rank = None
        self.retweeted = status.retweeted

    def published_before(self, time):
        """Return whether (True/False) the Tweet was published before a given datetime.

        Args:
            time (datetime.datetime): a datetime.datetime object.

        """
        return self.publish_time < time
