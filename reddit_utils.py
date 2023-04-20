import praw
from praw.models import MoreComments

def authenticate_reddit(credentials):
  reddit = praw.Reddit(
      client_id=credentials['client_id'],
      client_secret=credentials['client_secret'],
      password=credentials['password'],
      user_agent=f"SemanticForum by u/{credentials['username']}",
      username=credentials['username']
  )
  return reddit

def reddit_search(reddit, subreddit_name, query, limit):
    subreddit = reddit.subreddit(subreddit_name)

    search_obj = subreddit.search(query=query, sort='hot', time_filter='all')
    
    search_result = []
    for i, submission in enumerate(search_obj):
        if i < limit:
            title = submission.title
            comments = [comment.body for comment in submission.comments[:5]]
            search_result.append({'title': title, 'comments': comments})
        else: break
    
    return search_result