from flask import Flask, render_template, request
import cohere
import json
from cohere_utils import *
from reddit_utils import *

### Initialization ###

# Initialize Flask app
app = Flask(__name__)

# Load credentials
with open('credentials.json') as f:
  credentials = json.load(f)

# Load r/economics json db
with open("econDB.json", "r") as f:
  econ_json = json.load(f)

# Load saved faiss index
faiss_index = faiss.read_index('faiss_index.idx')

# Initialize/authenticate Reddit
reddit = authenticate_reddit(credentials)

# Initialize Cohere API client
co = cohere.Client(credentials['cohere_api_key'])

### Routes ###

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/search',)
def search():
  search_limit = 5

  # Get the query's embedding
  query = request.args['query']
  query_embed = embed_query(query, co)
    
  # Reddit keyword search
  subreddit = request.args['subreddit']
  reddit_results = reddit_search(reddit, subreddit, query, search_limit)

  # Cohere semantic search
  semantic_pd = semantic_search(query_embed, faiss_index, econ_json, search_limit)
  semantic_results = []
  for i, title in enumerate(semantic_pd['PostTitle']):
    comments = [comment['CommentBody'] for comment in semantic_pd['PostComments'][i]]
    semantic_results.append({'title': title, 'comments': comments})

  return render_template('search.html', reddit=reddit_results, semantic=semantic_results)



