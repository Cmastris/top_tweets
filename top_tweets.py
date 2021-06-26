import datetime

import twitter_auth


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
            max_tweets (int or None): the maximum number of Tweets to retrieve from the previous
                `num_days`, before sorting and filtering (defaults to None). For example, can be
                used in combination with a very high `num_days` (e.g. 9999) to find top Tweets from
                the previous 100 Tweets regardless of their publish date.

        Returns:
            list of Tweet: sorted and filtered based on passed arguments.
            """
        # TODO
        pass

    def get_top_tweets_percent(self, num_days, metric, top_percent, max_tweets=None):
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
            max_tweets (int or None): the maximum number of Tweets to retrieve from the previous
                `num_days`, before sorting and filtering (defaults to None). For example, can be
                used in combination with a very high `num_days` (e.g. 9999) to find top Tweets from
                the previous 100 Tweets regardless of their publish date.

        Returns:
            list of Tweet: sorted and filtered based on passed arguments.
            """
        # TODO
        pass

    def _fetch_tweets(self, num_days, max_tweets):
        """Fetch and return a list of the account's public Tweets.

        Args:
            num_days (int): the historic Tweet collection period in days, including the current day.
            max_tweets (int or None): the maximum number of Tweets to retrieve from the previous
                `num_days` (defaults to None).

        """
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
    """A single Tweet and its associated data/metrics.

    https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet

    Attributes:
        account (Account): the Twitter user account which published the Tweet.
        status (Tweepy Status): the Tweepy Status (Tweet) object.
        id (str): the Tweet's unique identifier.
        publish_time (datetime): datetime.datetime representing when the Tweet was published.
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
    def __init__(self, account, status):
        self.account = account
        self.status = status
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
            time (datetime): a datetime.datetime object.

        """
        return self.publish_time < time


# test_tweets = twitter_auth.API.home_timeline()
# test_tweet = Tweet(Account("test"), test_tweets[0])

# test_tweets = twitter_auth.API.statuses_lookup([1405193581556637698])
# test_tweet = Tweet(Account("test"), test_tweets[0])

user_tweets = twitter_auth.API.user_timeline("TechTopTweets1", tweet_mode="extended")
test_tweet = Tweet(Account("test"), user_tweets[2])
test_retweet = Tweet(Account("test"), user_tweets[1])
test_quote_tweet = Tweet(Account("test"), user_tweets[0])

print(test_tweet.id)
print(test_tweet.publish_time)
print("Quote: " + str(test_tweet.is_quote_tweet))
print("Retweeted Tweet: " + str(test_tweet.retweeted_tweet))
print("Retweeted? " + str(test_tweet.retweeted))
print("Quoted ID: " + str(test_tweet.quoted_tweet_id))
print(test_tweet.text)
print(test_tweet.hashtags)
print(test_tweet.likes)
print(test_tweet.retweets)

print("")
print(test_retweet.id)
print(test_retweet.publish_time)
print("Quote: " + str(test_retweet.is_quote_tweet))
print("Retweeted Tweet: " + str(test_retweet.retweeted_tweet))
print("Retweeted? " + str(test_retweet.retweeted))
print("Quoted ID: " + str(test_retweet.quoted_tweet_id))
print(test_retweet.text)
print(test_retweet.hashtags)
print(test_retweet.likes)
print(test_retweet.retweets)

print("")
print(test_quote_tweet.id)
print(test_quote_tweet.publish_time)
print("Quote: " + str(test_quote_tweet.is_quote_tweet))
print("Retweeted Tweet: " + str(test_quote_tweet.retweeted_tweet))
print("Retweeted? " + str(test_quote_tweet.retweeted))
print("Quoted ID: " + test_quote_tweet.quoted_tweet_id)
print(test_quote_tweet.text)
print(test_quote_tweet.hashtags)
print(test_quote_tweet.likes)
print(test_quote_tweet.retweets)


test_acc = Account(username="TechTopTweets1")
