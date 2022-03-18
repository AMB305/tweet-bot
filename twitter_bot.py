import gspread
import gspread_dataframe as gd
import tweepy
import random
import os

gc = gspread.service_account(filename='General-b4fefbff5499.json')
ws = gc.open("Just Vent Bot Data").worksheet("Sheet1")
user_reply = gd.get_as_dataframe(ws)
user_reply = user_reply.dropna(axis=1, how='all')
user_reply = user_reply.dropna(axis=0, how='all')

user_reply_dict = user_reply.to_dict("list")

all_usernames = list(user_reply.columns)

client = tweepy.Client(bearer_token=os.environ['BEARER_TOKEN'], consumer_key=os.environ['CONSUMER_KEY'], consumer_secret=os.environ['CONSUMER_SECRET'], access_token=os.environ['ACCESS_TOKEN'], access_token_secret=os.environ['ACCESS_TOKEN_SECRET'], wait_on_rate_limit=True)

all_users_to_follow = []
for i in all_usernames:
    user = client.get_user(username=i)
    if user.data is not None:
        all_users_to_follow.append(user.data.id)

all_users_to_follow = [str(i) for i in all_users_to_follow]

class IDPrinter(tweepy.Stream):

    def on_status(self, status):
      if str(status.user._json['id']) in all_users_to_follow:
        if status._json.get("in_reply_to_status_id") is None:
          if not status._json.get("retweeted"):
            reply_text = random.choice([i for i in user_reply_dict.get(status.user._json['screen_name']) if i==i])                
            client.create_tweet(text = reply_text, in_reply_to_tweet_id=status.id)

printer = IDPrinter(
  os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'],
  os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET']
)

printer.filter(follow=all_users_to_follow)
