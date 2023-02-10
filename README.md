# Top Tweets

Retrieve Tweets sorted by engagement and (optionally) republish them via a Twitter bot.

## Retrieve top Tweets

Use `get_tweets.py` to retrieve, sort, filter, and return the top Tweets of Twitter user accounts.

- Create an instance of `Account` using either a username or user ID
- Use `get_top_tweets_num()` to retrieve the top `top_num` Tweets (list of `Tweet`) from the previous `num_days`, based on `metric`
- Use `get_top_tweets_percent()` to retrieve the top `top_percent` Tweets (list of `Tweet`) from the previous `num_days`, based on `metric`
- `Tweet` instances have attributes including the Tweepy `Status` object, type of Tweet, ID, content, engagement metrics, and publish time 
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
- If the #1 Tweet has already been shared then the #2 Tweet will be shared instead, and so on
- Quote content includes the account, Tweet rank (e.g. number 1), `metric`, `num_days`, and (optionally) additional hashtags (see also: [changing the Quote Tweet content](#can-i-change-the-quote-tweet-content))
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

[@TechTopTweets1](https://twitter.com/TechTopTweets1) demonstrates the bot in action, implemented via `main()` in `bot.py`.

![Top Tweets Bot Example Tweet](/images/tech-top-tweets-bot-example.png)

## Setup
1. Requirements can be found in [requirements.txt](/requirements.txt). The project has been developed and tested using Python 3.9, but is likely to be compatible with other recent versions of Python 3.
2. Create a `config.py` file using [config_sample.py](/top_tweets/config_sample.py) as a template. Instructions for acquiring the required Twitter API credentials can be found in [Twitter's documentation](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api).

## FAQs

### Is the Twitter API used directly?

This project was built using [Tweepy](https://www.tweepy.org/), specifically [version 3.10.0](https://docs.tweepy.org/en/v3.10.0/), which is used to access version 1.1 of the Twitter API.

Thanks to the Tweepy team!

### Are there any limits?

Yes, the Twitter API's standard rate and request limits apply. Exceptions/errors relating to limits aren't explicitly handled, but [`tweepy.API`](https://docs.tweepy.org/en/v3.10.0/api.html#tweepy-api-twitter-api-wrapper) (editable in `twitter_auth.py`) can be configured to wait for rate limits to replenish.

More details can be found in Twitter's [API v1.1 rate limits documentation](https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits).

### Can I change the Quote Tweet content?

For simplicity, Quote Tweet content isn't editable via public `Bot` methods. However, you can edit how this content is constructed in the `Bot._get_quote_content()` method.

### How can I ask questions, report bugs, or provide feedback?
Feel free to create an issue or open a new discussion.

### Is this project in active development?
There are no further updates/features planned, and I'm not looking for contributions, but I'll be happy to fix any (significant) bugs.