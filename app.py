from flask import Flask, render_template, request
import cohere
import json
from cohere_utils import *
from reddit_utils import *

# Initialize Flask app
app = Flask(__name__)

# Load credentials
with open('credentials.json') as f:
  credentials = json.load(f)

# Load saved faiss index
faiss_index = faiss.read_index('faiss_index.idx')

# TODO: Load r/economics json db

# Initialize/authenticate Reddit
reddit = authenticate_reddit(credentials)

# Initialize Cohere API client
co = cohere.Client(credentials['cohere_api_key'])

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/search',)
def search():
  # Get the query's embedding
  query = request.args['query']
  query_embed = embed_query(query, co)
    
  # Cohere semantic search
  _, semantic_results = semantic_search(query_embed, faiss_index, db_json)

  # Reddit semantic search
  subreddit = request.args['subreddit']
  reddit_results = reddit_search(reddit, subreddit, query)

  # Slice the first five results
  top5_reddit = reddit_results.iloc[:5]
  top5_semantic = semantic_results[:5]

  return render_template('search.html', reddit=top5_reddit, semantic=top5_semantic)



