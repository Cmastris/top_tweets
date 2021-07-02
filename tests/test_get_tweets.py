import datetime

import pytest

from top_tweets.get_tweets import Account, Tweet


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
