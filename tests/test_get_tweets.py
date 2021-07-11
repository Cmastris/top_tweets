import datetime

import pytest

from top_tweets.get_tweets import Account, Tweet


@pytest.fixture
def mock_tweet(monkeypatch):
    """Monkeypatch Tweepy object attrs with manual attr assignment in __init__."""
    def mock_init(self, likes, retweets, likes_retweets_combined):
        self.likes = likes
        self.retweets = retweets
        self.likes_retweets_combined = likes_retweets_combined
        self.rank = None

    monkeypatch.setattr(Tweet, "__init__", mock_init)


class TestAccount:
    @pytest.fixture
    def mock_account(self, monkeypatch):
        """Monkeypatch __init__ to skip API calls."""

        def mock_init(self):
            self.name = "name"
            self.username = "username"

        monkeypatch.setattr(Account, "__init__", mock_init)

    def test_account_init_assert(self):
        with pytest.raises(ValueError):
            Account()

    def test_cut_off_time_curr_day(self):
        latest_date = datetime.date(2021, 7, 1)
        assert Account._cut_off_time(latest_date, 1) == datetime.datetime(2021, 7, 1, 0, 0, 0)

    def test_cut_off_time_multiple_days(self):
        latest_date = datetime.date(2021, 7, 1)
        assert Account._cut_off_time(latest_date, 3) == datetime.datetime(2021, 6, 29, 0, 0, 0)

    def test_sort_tweets_invalid_metric(self, mock_account, mock_tweet):
        with pytest.raises(AssertionError):
            acc = Account()
            acc._sort_tweets([Tweet(0, 5, 5), Tweet(5, 15, 20)], "invalid_metric")

    def test_sort_tweets_likes(self, mock_account, mock_tweet):
        acc = Account()
        l0 = Tweet(0, 5, 5)
        l5 = Tweet(5, 15, 20)
        l10 = Tweet(10, 0, 10)
        tweets = [l0, l5, l10]
        sorted_tweets = acc._sort_tweets(tweets, "likes")
        assert sorted_tweets == [l10, l5, l0]
        assert sorted_tweets[0].rank == 1

    def test_sort_tweets_retweets(self, mock_account, mock_tweet):
        acc = Account()
        r0 = Tweet(10, 0, 10)
        r5 = Tweet(0, 5, 5)
        r15 = Tweet(5, 15, 20)
        tweets = [r0, r5, r15]
        sorted_tweets = acc._sort_tweets(tweets, "retweets")
        assert sorted_tweets == [r15, r5, r0]
        assert sorted_tweets[1].rank == 2

    def test_sort_tweets_combined(self, mock_account, mock_tweet):
        acc = Account()
        c0 = Tweet(0, 0, 0)
        c5 = Tweet(0, 5, 5)
        c20 = Tweet(5, 15, 20)
        tweets = [c0, c5, c20]
        sorted_tweets = acc._sort_tweets(tweets, "likes_retweets_combined")
        assert sorted_tweets == [c20, c5, c0]
        assert sorted_tweets[2].rank == 3

    def test_filter_tweets_lower_num(self, mock_account, mock_tweet):
        acc = Account()
        l0 = Tweet(0, 5, 5)
        l5 = Tweet(5, 15, 20)
        l10 = Tweet(10, 0, 10)
        sorted_tweets = [l10, l5, l0]
        assert acc._filter_tweets(sorted_tweets, 2) == [l10, l5]

    def test_filter_tweets_higher_num(self, mock_account, mock_tweet):
        acc = Account()
        l0 = Tweet(0, 5, 5)
        l5 = Tweet(5, 15, 20)
        l10 = Tweet(10, 0, 10)
        sorted_tweets = [l10, l5, l0]
        assert acc._filter_tweets(sorted_tweets, 5) == [l10, l5, l0]


class TestTweet:
    @pytest.fixture
    def mock_dated_tweet(self, monkeypatch):
        """Monkeypatch Tweepy object attrs with manual attr assignment in __init__."""
        def mock_init(self, publish_time):
            self.publish_time = publish_time

        monkeypatch.setattr(Tweet, "__init__", mock_init)

    def test_published_before_true(self, mock_dated_tweet):
        tweet = Tweet(datetime.datetime(2021, 6, 1, 12, 0, 0))
        assert tweet.published_before(datetime.datetime(2021, 7, 1, 12, 0, 0))

    @pytest.mark.parametrize("time", [
        datetime.datetime(2021, 5, 1, 12, 0, 0),  # Before publish date
        datetime.datetime(2021, 6, 1, 12, 0, 0),  # Equal to publish date
    ])
    def test_published_before_false(self, mock_dated_tweet, time):
        tweet = Tweet(datetime.datetime(2021, 6, 1, 12, 0, 0))
        assert not tweet.published_before(time)
