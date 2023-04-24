import praw
import json
import os.path
import sys
from reddit_utils import authenticate_reddit

def fetch_subreddit_data(subreddit, limit):
  subreddit_data = {'name': subreddit.display_name, 'posts': []}
  for submission in subreddit.hot(limit=limit):
      submission.comments.replace_more(limit=0)
      post_comments = [{'id': comment.id, 'body': comment.body} for comment in submission.comments]
      post = {'id': submission.id, 'title': submission.title, 'comments': post_comments, 'comments_length': len(post_comments), 'permalink': submission.permalink}
      subreddit_data['posts'].append(post)
  return subreddit_data

with open('credentials.json') as f:
  credentials = json.load(f)

reddit = authenticate_reddit(credentials)

# get subreddit of interest
subreddit_name = sys.argv[1]
subreddit = reddit.subreddit(subreddit_name)

# get top 100 hottest posts and comments for subreddit of interest(s)
print(f'Fetching data for r/{subreddit_name}.')
subreddit_data = fetch_subreddit_data(subreddit, limit=100)
print('Data received successfully.')

existing_data = []
with open('subreddit_data_db.json', 'r') as f:
  try:
    existing_data = json.load(f)
    existing_data.append(subreddit_data)
  except json.JSONDecodeError:
    existing_data.append(subreddit_data)

with open('subreddit_data_db.json', 'w') as f:
  json.dump(existing_data, f)
  print('Wrote subreddit data successfully.')