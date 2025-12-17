import pandas as pd
from thefuzz import fuzz, process

import json
import os

def load_synonyms():
    try:
        # Construct absolute path to synonyms.json
        base_path = os.path.dirname(__file__) # src/
        json_path = os.path.join(base_path, 'synonyms.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def smart_search(df, query, threshold=55): # Lowered threshold slightly
    """
    Performs a smart search on the dataframe.
    1. Check Synonyms
    2. Fuzzy match on Product Name, Model, Tags, Question.
    3. Returns relevant rows.
    """
    if not query:
        return pd.DataFrame() # Return empty if no query

    # 0. Synonym Normalization
    synonyms = load_synonyms()
    # Normalize: Check exact match first
    if query in synonyms:
        query = synonyms[query]
    
    results = []
    
    # Iterate through rows and score them
    # This is simple; for 100 items it's fast enough.
    for index, row in df.iterrows():
        # Create a combined string for searching High Priority fields
        target_text = f"{row['Product']} {row['Model']} {row['Tags']} {row['Question']}"
        
        # 1. Standard Token Set Ratio (Good for partial word matches)
        score_token = fuzz.token_set_ratio(query, target_text)
        
        # 2. Spaceless Partial Ratio (Good for typos hidden in long text without spaces)
        # We use partial_ratio to find if 'query' (with typo) exists as a substring in the long 'target'
        query_spaceless = query.replace(" ", "")
        target_spaceless = target_text.replace(" ", "")
        score_spaceless = fuzz.partial_ratio(query_spaceless, target_spaceless)
        
        # Use the maximum score
        score = max(score_token, score_spaceless)
        
        if score >= threshold:
            row_data = row.to_dict() # Convert row to dict
            row_data['score'] = score
            results.append(row_data)
            
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return pd.DataFrame(results)

def get_suggestion(df, query):
    """
    Finds a suggested correction for the query from existing data keywords.
    Returns the best match string and its score.
    """
    # Collect potential keywords
    keywords = set()
    if 'Product' in df.columns:
        keywords.update(df['Product'].dropna().unique())
    if 'Model' in df.columns:
        keywords.update(df['Model'].dropna().unique())
    if 'Tags' in df.columns:
        # Split tags by comma
        for tags in df['Tags'].dropna():
            if isinstance(tags, str):
                keywords.update([t.strip() for t in tags.split(',')])
                
    # Find best match
    best_match = process.extractOne(query, keywords, scorer=fuzz.ratio)
    
    # best_match is (string, score)
    if best_match and best_match[1] > 50: # Minimum confidence
        return best_match[0]
    return None
