from typing import List, Dict

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from database.db import get_products


# --- ML Performance Upgrade: Caching ---
# We cache the matrix math so it only runs once per hour, making page loads instant.
@st.cache_data(ttl=3600)
def _compute_similarity_matrix():
    """Computes and caches the cosine similarity matrix for the product catalog."""
    products = get_products()

    # ML Upgrade: Feature Engineering
    # We combine Category and Description.
    # Pro-tip: Repeating the category gives it slightly more weight in the TF-IDF calculation!
    products['combined_features'] = products['category'] + " " + products['category'] + " " + products['description']

    # Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(products["combined_features"])

    # Similarity Mapping
    cosine_sim = cosine_similarity(tfidf_matrix)

    return cosine_sim, products


def get_recommendations(product_id: int, top_n: int = 4) -> List[Dict]:
    """
    Calculates product similarity based on enriched metadata and returns
    the top N most similar product objects.
    """
    try:
        # Load the cached math instead of recalculating
        cosine_sim, products = _compute_similarity_matrix()

        # 1. Validation
        if not (products["id"] == product_id).any():
            return []

        # 2. Find the matrix index of our target product
        idx = products.index[products["id"] == product_id][0]

        # 3. Sort and Filter
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get top N indices (excluding the product itself at index 0)
        top_indices = [i[0] for i in sim_scores[1:top_n + 1]]

        # 4. Return full product details formatted for the UI
        recommendations = products.iloc[top_indices].to_dict('records')
        return recommendations

    except Exception as e:
        # Professional fallback: If the ML fails, return empty list so the UI doesn't crash
        print(f"Recommender Error: {e}")
        return []
