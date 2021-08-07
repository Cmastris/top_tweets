# Top Tweets

Retrieve & sort Tweets by engagement and republish them via a Twitter bot.

## Retrieve top Tweets

Use `get_tweets.py` to retrieve, sort, filter, and return the top Tweets of Twitter user accounts.

- Create an instance of `Account` using either a username or user ID
- Use `get_top_tweets_num()` to retrieve the top `top_num` Tweets from the previous `num_days`, based on `metric`
- Use `get_top_tweets_percent()` to retrieve the top `top_percent` Tweets from the previous `num_days`, based on `metric`
- More detailed documentation is provided within the class and method docstrings

For example...

```
# Instantiate the account using a Twitter username
account = Account(username="example_twitter_username")

# Retrieve the top 10 Tweets based on their number of Likes (in order from highest to lowest Likes) 
# from the previous 30 days (including the current day)
tweets = account.get_top_tweets_num(30, "likes", 10)
```

## Republish top Tweets

Use `bot.py` to Retweet or Quote Tweet the top Tweets of Twitter user accounts.

- Create an instance of `Bot`, optionally providing a default list of usernames or user IDs to share from and a default metric to sort/rank Tweets by
- Use `share_from_user()` to Quote Tweet or Retweet a top Tweet (that hasn't already been shared) by a specific user, from the previous `num_days` based on `metric`
- Use `share_from_random_user()` to Quote Tweet or Retweet a top Tweet (that hasn't already been shared) by a randomly selected user from a list, from the previous `num_days` based on `metric`
- More detailed documentation is provided within the class and method docstrings

For example...

```
# Instantiate the bot using a default list of Twitter usernames
bot = Bot(usernames=["example_user_1", "example_user_2", "example_user_3"])

# Quote Tweet a top Tweet from a random user in the default list, 
# published in the previous 7 days (including the current day),
# where `likes_retweets_combined` is used by default to sort/rank Tweets
bot.share_from_random_user(7, quote=True)
```