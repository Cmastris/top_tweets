import pytest

from top_tweets.bot import Bot
from top_tweets.get_tweets import Tweet


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
