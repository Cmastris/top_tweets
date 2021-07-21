import pytest

from top_tweets.bot import Bot


class TestBot:
    def test_bot_init_assert(self):
        with pytest.raises(AssertionError):
            Bot(usernames=["test"], user_ids=["test"])

    def test_get_random_user_assert(self):
        bot = Bot()
        with pytest.raises(AssertionError):
            bot._get_random_user([])

    def test_get_random_user(self):
        bot = Bot()
        test_list = ["user1", "user2", "user3"]
        assert bot._get_random_user(test_list) in test_list
