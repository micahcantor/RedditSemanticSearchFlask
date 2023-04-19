import pandas as pd
import json
import datetime as dt
import numpy as np
import faiss

def calculate_stats(df):
    minComs = df.NumComments.min()
    maxComs = df.NumComments.max()
    meanComs = df.NumComments.mean()
    totalComments = df.NumComments.sum()
    return minComs, maxComs, meanComs, totalComments

def embed_query(query, cohere_client):
    query_embed = cohere_client.embed(texts=[query], model="large").embeddings
    
    # Convert the query_embed to a float32 NumPy array and normalize it
    query_embed_np = np.array(query_embed).astype('float32')
    faiss.normalize_L2(query_embed_np)

    return query_embed_np

def semantic_search(query_embed, index, db_json):
    
    # Mapping between unique indices and original post information
    id_to_post = {i: post for i, post in enumerate(pd.DataFrame(db_json).to_dict('records'))}
    
    # Retrieve top 5 most similar indexed embeddings (D is distance and I is index)
    D, I = index.search(query_embed, 5)

    # Format the results
    results = pd.DataFrame(data={'PostID': [id_to_post[i]['Posts']['PostID'] for i in I[0]], 
                                'PostTitle': [id_to_post[i]['Posts']['PostTitle'] for i in I[0]], 
                                'distance': D[0]})

    resultsComments = [{"PostID":db_json['Posts'][i]['PostID'], 
                        "PostComments":db_json['Posts'][i]['PostComments']} for i in range(len(db_json['Posts'])) if db_json['Posts'][i]['PostID'] in list(results.PostID)]
    

    resultsCommentsdf = pd.DataFrame(resultsComments)
    semantic_comments = results.merge(resultsCommentsdf, left_on='PostID', right_on='PostID')

    # they all start with the same comment becauase it is the moderation comment from the particular subreddit
    semantic_search = [results['PostTitle'][i] for i in range(len(results['PostTitle']))]
    
    return (semantic_search, semantic_comments)

