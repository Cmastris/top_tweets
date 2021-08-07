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
# Instantiate the account
account = Account(username="example_twitter_username")

# Retrieve the top 10 Tweets based on their number of Likes (in order from highest to lowest Likes) 
# from the previous 30 days (including the current day)
tweets = account.get_top_tweets_num(30, "likes", 10)
```
