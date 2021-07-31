import datetime
import random

import tweepy

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

    def share_from_user(self, num_days, username=None, user_id=None, metric="default", quote=True,
                        extra_hashtags=None, max_chars=140):
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
            quote (bool): whether the Tweet should be Quote Tweeted (True) or Retweeted (False).
            extra_hashtags (list of str, or None): a list of hashtags (without '#') to include in
                the Quote Tweet (if applicable) before any original Tweet hashtags.
            max_chars (int): the maximum number of Quote Tweet characters (potentially limits the
                number of hashtags that will be included).

        """
        if metric == "default":
            metric = self.metric

        account = get_tweets.Account(username=username, user_id=user_id)
        tweets = account.get_top_tweets_percent(num_days, metric, 100)
        tweet = self._select_tweet(tweets, num_days)

        if quote:
            content = self._get_quote_content(tweet, metric, num_days, extra_hashtags, max_chars)
            self._quote_tweet(tweet, content)
        else:
            self._retweet(tweet)

    def share_from_random_user(self, num_days, usernames=None, user_ids=None, metric="default",
                               quote=True, extra_hashtags=None, max_chars=140):
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
            quote (bool): whether the Tweet should be Quote Tweeted (True) or Retweeted (False).
            extra_hashtags (list of str, or None): a list of hashtags (without '#') to include in
                the Quote Tweet (if applicable) before any original Tweet hashtags.
            max_chars (int): the maximum number of Quote Tweet characters (potentially limits the
                number of hashtags that will be included).

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
            content = self._get_quote_content(tweet, metric, num_days, extra_hashtags, max_chars)
            self._quote_tweet(tweet, content)
        else:
            self._retweet(tweet)

    @staticmethod
    def previously_retweeted(tweet):
        """Return whether (True/False) the tweet has been previously Retweeted.

        Args:
            tweet(get_tweets.Tweet): the Tweet object representing the Tweet.

        """
        return tweet.retweeted

    @staticmethod
    def previously_quoted(tweet, num_days):
        """Return whether (True/False) the tweet has been Quote Tweeted in the previous `num_days`.

        Args:
            tweet(get_tweets.Tweet): the Tweet object representing the Tweet.
            num_days (int): the historic assessment period (i.e. whether the Tweet was Quote
                Tweeted) in days, including the current day.

        """
        cut_off = get_tweets.Account.cut_off_time(datetime.date.today(), num_days)
        # Cursor object handles pagination and returns a list of Tweepy Status
        for t in tweepy.Cursor(twitter_auth.API.user_timeline,
                               include_rts=False,
                               exclude_replies=True,
                               tweet_mode="extended").items():
            bot_tweet = get_tweets.Tweet(t, None)
            if bot_tweet.published_before(cut_off):
                break

            if bot_tweet.quoted_tweet_id == tweet.id:
                return True

        return False

    @staticmethod
    def _select_tweet(tweets, num_days):
        """Return the top unshared (see notes) Tweet from a list of ranked Tweets.

        Specifically, a Tweet will be returned if it has never been Retweeted and if it hasn't been
        Quote Tweeted in the previous `num_days`.

        Args:
            tweets (list of get_tweets.Tweet): a list of Tweet objects in order of rank.
            num_days (int): the historic assessment period (i.e. whether the Tweet was Quote
                Tweeted) in days, including the current day.
        """
        for t in tweets:
            if (not Bot.previously_retweeted(t)) and (not Bot.previously_quoted(t, num_days)):
                return t

        raise ValueError("No eligible Tweets to share; all Tweets have either been Retweeted "
                         "previously or Quote Tweeted in the previous `num_days`.")

    @staticmethod
    def _retweet(tweet):
        """Retweet the Tweet."""
        url = "https://twitter.com/{}/status/{}".format(tweet.account.username, tweet.id)
        print("Retweeting Tweet (rank {}): {}".format(tweet.rank, url))
        twitter_auth.API.retweet(tweet.id)

    @staticmethod
    def _quote_tweet(tweet, content):
        """Quote Tweet (embed) the Tweet with the provided content."""
        embed_url = "https://twitter.com/{}/status/{}".format(tweet.account.username, tweet.id)
        print("Publishing Quote Tweet...")
        print(content + " " + embed_url)
        twitter_auth.API.update_status(content, attachment_url=embed_url)

    @staticmethod
    def _get_quote_content(tweet, metric, num_days, extra_hashtags, max_chars):
        """Return the Quote Tweet content (str).

        Args:
            tweet(get_tweets.Tweet): the Tweet object representing the Tweet.
            metric (str): the default metric to sort Tweets by, largest to smallest. One of:
                - likes
                - retweets
                - likes_retweets_combined
                Uses self.metric (`likes_retweets_combined` if not set during init) by default.
            num_days (int): the historic Tweet collection period in days, including the current day.
            extra_hashtags (list of str, or None): a list of hashtags (without '#') to include in
                the Quote Tweet (if applicable) before any original Tweet hashtags.
            max_chars (int): the maximum number of Quote Tweet characters (potentially limits the
                number of hashtags that will be included).

        """
        if metric == "likes":
            metric_str = "liked"
        elif metric == "retweets":
            metric_str = "retweeted"
        else:
            metric_str = "liked & retweeted"

        content = "Number {} most {} Tweet by @{} in the previous {} days (incl. today)." \
                  "".format(tweet.rank, metric_str, tweet.account.username, num_days)

        hashtags = [h["text"] for h in tweet.hashtags]
        if extra_hashtags is not None:
            hashtags = extra_hashtags + hashtags

        for hashtag in hashtags:
            if len(content) + len(hashtag) > max_chars:
                break

            content += " #" + hashtag

        return content

    @staticmethod
    def _get_random_user(user_list):
        """Return a randomly selected item from a list of usernames or user IDs."""
        assert len(user_list) > 0, "No items in the user list; unable to select a random user."
        return random.choice(user_list)


def main():
    """Quote Tweet a top Tweet from a random user in `SOURCE_USERNAMES`."""
    bot = Bot(usernames=config.SOURCE_USERNAMES)
    bot.share_from_random_user(7)


if __name__ == "__main__":
    main()
