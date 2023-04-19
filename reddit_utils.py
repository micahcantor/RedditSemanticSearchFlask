import praw
import pandas as pd

def authenticate_reddit(credentials):
  reddit = praw.Reddit(
      client_id=credentials['client_id'],
      client_secret=credentials['client_secret'],
      password=credentials['password'],
      user_agent=f"SemanticForum by u/{credentials['username']}",
      username=credentials['username']
  )
  return reddit

def reddit_search(reddit, subreddit_name, query):
    reddit_search_titles = []
    reddit_search_comments = []

    subreddit = reddit.subreddit(subreddit_name)

    search_obj = subreddit.search(query=query,
                                sort='hot',
                                syntax='lucene',
                                time_filter='all')

    for submission in search_obj:
        reddit_search_titles.append(submission.title)
        submission.comments.replace_more(limit=0)
        comments = [comment.body for comment in submission.comments]
        reddit_search_comments.append(comments)

    reddit_search = pd.DataFrame({"Posts":reddit_search_titles, "Comments":reddit_search_comments})
    
    return reddit_search