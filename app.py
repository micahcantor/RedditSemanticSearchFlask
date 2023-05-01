from flask import Flask, render_template, request
import cohere
import json
import faiss
from cohere_utils import embed_query, semantic_search
from reddit_utils import authenticate_reddit, reddit_search

### Initialization ###

# Initialize Flask app
app = Flask(__name__)

# Load credentials
with open('credentials.json') as f:
  credentials = json.load(f)

# Load subreddit json db
with open("subreddit_data_db.json", "r") as f:
  subreddit_db = json.load(f)

# Initialize/authenticate Reddit
reddit = authenticate_reddit(credentials)

# Initialize Cohere API client
co = cohere.Client(credentials['cohere_api_key'])

### Routes ###

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/search')
def search():
  search_limit = 5 # limit for number of results to display

  # Get the query's embedding
  query = request.args['query']
  query_embed = embed_query(query, co)

  # Reddit keyword search
  subreddit_name = request.args['subreddit']
  reddit_results = reddit_search(reddit, subreddit_name, query, search_limit)

  # Cohere semantic search
  faiss_index = faiss.read_index(f'indices/{subreddit_name}.idx')
  subreddit_data = [data for data in subreddit_db if data['name'] == subreddit_name][0]
  semantic_results = semantic_search(query_embed, faiss_index, subreddit_data, search_limit)

  return render_template('search.html', reddit=reddit_results, semantic=semantic_results)



