import praw

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
            permalink = f'https://reddit.com{submission.permalink}'
            comment_limit = 5 # arbitrary, but allowing more comments is slower and need to deal with MoreComments objects
            comments = [comment.body for comment in submission.comments[:comment_limit]]
            search_result.append({'title': title, 'permalink': permalink, 'comments': comments})
        else: break
    
    return search_result