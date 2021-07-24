import datetime

import pytest
import tweepy

from top_tweets.bot import Bot
from top_tweets.get_tweets import Tweet


class MockStatus:
    def __init__(self, id, quoted_tweet_id, publish_time):
        self.id = id
        self.quoted_tweet_id = quoted_tweet_id
        self.publish_time = publish_time


@pytest.fixture
def mock_tweepy_cursor_items(monkeypatch):
    """Monkeypatch tweepy.Cursor.items()."""
    def mock_items(self):
        print("Mocking tweepy.Cursor.items()")
        s1 = MockStatus(None, None, datetime.datetime(2021, 1, 1))
        s2 = MockStatus(None, "quoted_tweet_id", datetime.datetime(2021, 1, 1))
        s3 = MockStatus(None, None, datetime.datetime(2021, 1, 1))
        return [s1, s2, s3]

    monkeypatch.setattr(tweepy.Cursor, "items", mock_items)


@pytest.fixture
def mock_tweet_prev_quoted(monkeypatch):
    """Monkeypatch Tweepy object init to use attrs from `MockStatus`."""
    def mock_init(self, status, account):
        self.id = status.id
        self.quoted_tweet_id = status.quoted_tweet_id
        self.publish_time = status.publish_time

    monkeypatch.setattr(Tweet, "__init__", mock_init)


@pytest.fixture
def mock_tweet_share_attrs(monkeypatch):
    """Monkeypatch Tweepy object attrs with manual attr assignment in __init__."""
    def mock_init(self, retweeted, mock_quoted):
        self.retweeted = retweeted
        self.mock_quoted = mock_quoted

    monkeypatch.setattr(Tweet, "__init__", mock_init)


class TestBot:
    def test_bot_init_assert(self):
        with pytest.raises(AssertionError):
            Bot(usernames=["test"], user_ids=["test"])

    def test_previously_quoted_false(self, mock_tweet_prev_quoted, mock_tweepy_cursor_items):
        status = MockStatus("not_quoted_id", None, None)
        tweet = Tweet(status, None)
        assert Bot.previously_quoted(tweet, 9999) is False

    def test_previously_quoted_true(self, mock_tweet_prev_quoted, mock_tweepy_cursor_items):
        status = MockStatus("quoted_tweet_id", None, None)
        tweet = Tweet(status, None)
        assert Bot.previously_quoted(tweet, 9999) is True

    def test_previously_quoted_false_date(self, mock_tweet_prev_quoted, mock_tweepy_cursor_items):
        status = MockStatus("quoted_tweet_id", None, None)
        tweet = Tweet(status, None)
        assert Bot.previously_quoted(tweet, 30) is False

    @pytest.fixture
    def mock_previously_quoted(self, monkeypatch):
        def mock_prev_quoted(tweet, num_days):
            return tweet.mock_quoted

        monkeypatch.setattr(Bot, "previously_quoted", mock_prev_quoted)

    def test_select_tweet_not_shared(self, mock_previously_quoted, mock_tweet_share_attrs):
        t1 = Tweet(False, False)
        t2 = Tweet(False, False)
        assert Bot._select_tweet([t1, t2], 99) == t1

    def test_select_tweet_retweeted(self, mock_previously_quoted, mock_tweet_share_attrs):
        t1 = Tweet(True, False)
        t2 = Tweet(False, False)
        assert Bot._select_tweet([t1, t2], 99) == t2

    def test_select_tweet_quoted(self, mock_previously_quoted, mock_tweet_share_attrs):
        t1 = Tweet(False, True)
        t2 = Tweet(False, False)
        assert Bot._select_tweet([t1, t2], 99) == t2

    def test_select_tweet_retweeted_quoted(self, mock_previously_quoted, mock_tweet_share_attrs):
        t1 = Tweet(True, True)
        t2 = Tweet(False, False)
        assert Bot._select_tweet([t1, t2], 99) == t2

    def test_select_tweet_all_shared(self, mock_previously_quoted, mock_tweet_share_attrs):
        t1 = Tweet(False, True)
        t2 = Tweet(True, False)
        with pytest.raises(ValueError):
            Bot._select_tweet([t1, t2], 99)

    def test_get_random_user_assert(self):
        bot = Bot()
        with pytest.raises(AssertionError):
            bot._get_random_user([])

    def test_get_random_user(self):
        bot = Bot()
        test_list = ["user1", "user2", "user3"]
        assert bot._get_random_user(test_list) in test_list
