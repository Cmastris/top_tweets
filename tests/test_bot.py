import pytest

from top_tweets.bot import Bot


class TestBot:
    def test_bot_init_assert(self):
        with pytest.raises(AssertionError):
            Bot(usernames=["test"], user_ids=["test"])