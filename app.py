from flask import Flask, render_template
import cohere
import json

# Initialize Flask app
app = Flask(__name__)

# Load credentials
with open("credentials.json") as f:
  credentials = json.load(f)

# TODO: Load saved faiss index

# TODO: Initialize/authenticate Reddit

# Initialize Cohere API client
cohere_client = cohere.Client(api_key=credentials['cohere_api_key'])

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/search')
def search():
