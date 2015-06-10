#Import the necessary methods from tweepy library
import tweepy
import json

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def main():
  # Fill in your Twitter account information
  cfg = {
    "consumer_key"        : "your_consumer_key",
    "consumer_secret"     : "your_consumer_secret",
    "access_token"        : "your_access_token",
    "access_token_secret" : "your_access_token_secret"
    }

  api = get_api(cfg)

  max_tweets = 1000
  query = 'kingsman'
  searched_tweets = [status._json for status in tweepy.Cursor(api.search,  q=query).items(max_tweets)]

  with open('kingsman.txt', 'w') as outfile:
    json.dump(searched_tweets, outfile)

if __name__ == "__main__":
  main()

