import json
import numpy as np
import faiss
import cohere
import os

with open("subreddit_data_db.json", "r") as f:
    subreddit_data = json.load(f)

with open('credentials.json') as f:
    credentials = json.load(f)

cohere_client = cohere.Client(api_key=credentials['cohere_api_key'])

for subreddit in subreddit_data:
    subreddit_name = subreddit['name']
    print(f'Creating embeddings for r/{subreddit_name}')

    post_titles = [subreddit['posts'][i]['title'] for i in range(len(subreddit['posts']))]

    posts_embed = cohere_client.embed(texts=post_titles, model='large').embeddings
    print('Cohere embeddings created successfully.')

    # Check the dimensions of the embeddings
    posts_embed = np.array(posts_embed)

    ## Indexing with FAISS

    # Step 5: Create a search index
    embedding_size = posts_embed.shape[1]
    index = faiss.IndexFlatL2(embedding_size)

    posts_embed_32 = posts_embed.astype('float32')

    # Step 6: Add embeddings to the search index
    faiss.normalize_L2(posts_embed_32)
    index.add(posts_embed_32)

    # Step 7: Save the search index
    file_name = f'indices/{subreddit_name}.idx'
    os.makedirs('indices', exist_ok=True) # make sure directory exists
    with open(file_name, 'w'): pass # make sure the file exists
    faiss.write_index(index, file_name)
    print('Wrote new embeddings successfully.')