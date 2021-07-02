import datetime

import pytest

from top_tweets.get_tweets import Account, Tweet


class TestTweet:
    def test_published_before(self, monkeypatch):
        def mock_init(self, publish_time):
            """Monkeypatch Tweepy object attrs with manual attr assignments in __init__."""
            self.publish_time = publish_time

        monkeypatch.setattr(Tweet, "__init__", mock_init)
        tweet = Tweet(datetime.datetime(2021, 6, 1, 12, 0, 0))
        assert tweet.published_before(datetime.datetime(2021, 7, 1, 12, 0, 0))
