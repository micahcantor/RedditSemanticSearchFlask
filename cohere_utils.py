import json
import datetime as dt
import numpy as np
import faiss

def embed_query(query, cohere_client):
    query_embed = cohere_client.embed(texts=[query], model="large").embeddings
    
    # Convert the query_embed to a float32 NumPy array and normalize it
    query_embed_np = np.array(query_embed).astype('float32')
    faiss.normalize_L2(query_embed_np)

    return query_embed_np

def semantic_search(query_embed, index, db_json, limit):
    # Retrieve top 5 most similar indexed embeddings (D is distance and I is index)
    D, I = index.search(query_embed, limit)

    # Format the results
    results = [{'post': db_json['posts'][i], 'distance': D[0][j]} for j, i in enumerate(I[0])]
    comment_limit = 5
    for result in results:
        result['post']['permalink'] = 'https://reddit.com' + result['post']['permalink']
        result['post']['comments'] = result['post']['comments'][:comment_limit]
    
    return results

