# file: utils/query_cache.py
import os
import pickle
import streamlit as st
from typing import Tuple, Dict, Any, Callable

def get_cached_answer(query, qa_chain):
    if "cached_answers" not in st.session_state:
        st.session_state["cached_answers"] = {}

    # Check if query is in cache
    if query in st.session_state["cached_answers"]:
        cached_data = st.session_state["cached_answers"][query]
        result = cached_data["result"]
        source_docs = cached_data.get("source_docs", None)
        return result, source_docs, True
    else:
        # Query not in cache, invoke model
        response = qa_chain(query)
        result = response["result"]
        source_docs = response.get("source_documents", None)
        
        # Store both result and source_docs in cache
        st.session_state["cached_answers"][query] = {
            "result": result,
            "source_docs": source_docs
        }
        
        return result, source_docs, False
def _normalize_query(query: str) -> str:
    """
    Normalize a query for better cache hit rate
    
    Args:
        query: The input query
        
    Returns:
        Normalized query string
    """
    # Convert to lowercase and remove extra whitespace
    return " ".join(query.lower().strip().split())

def _load_cache_from_disk(cache_file: str) -> Dict[str, Any]:
    """
    Load cached queries from disk if available
    
    Args:
        cache_file: Path to the cache file
    
    Returns:
        Dictionary with cached query results
    """
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading cache from disk: {e}")
    return {}

def _save_cache_to_disk(cache: Dict[str, Any], cache_file: str) -> None:
    """
    Save the current cache to disk
    
    Args:
        cache: The cache dictionary to save
        cache_file: Path where to save the cache
    """
    try:
        with open(cache_file, "wb") as f:
            pickle.dump(cache, f)
    except Exception as e:
        print(f"Error saving cache to disk: {e}")

def clear_cache(cache_file: str = "query_cache.pkl") -> None:
    """
    Clear both the in-memory and on-disk cache
    
    Args:
        cache_file: Path to the cache file
    """
    if 'query_cache' in st.session_state:
        st.session_state.query_cache = {}
    
    if os.path.exists(cache_file):
        try:
            os.remove(cache_file)
        except Exception as e:
            print(f"Error removing cache file: {e}")


def get_cached_answer_with_sources(query, qa_chain, cache_file="query_cache.pkl"):
    """
    Get answer from cache or invoke model if needed, including source documents
    
    Args:
        query: The question to answer
        qa_chain: The QA chain to use if cache miss occurs
        cache_file: Path to the file where cache will be stored
    
    Returns:
        Tuple of (result, source_docs, from_cache) where from_cache is a boolean
    """
    # Initialize cache in session state if it doesn't exist
    if 'query_cache' not in st.session_state:
        st.session_state.query_cache = _load_cache_from_disk(cache_file)
    
    # Normalize query to improve cache hit rate
    normalized_query = _normalize_query(query)
    
    # Check if query is in cache
    if normalized_query in st.session_state.query_cache:
        cached_entry = st.session_state.query_cache[normalized_query]
        result = cached_entry.get('result')
        source_docs = cached_entry.get('source_docs')
        return result, source_docs, True
    
    # Query not in cache, invoke model
    response = qa_chain(query)
    result = response["result"]
    source_docs = response.get("source_documents", None)
    
    # Store both result and source_docs in cache
    st.session_state.query_cache[normalized_query] = {
        'result': result,
        'source_docs': source_docs
    }
    _save_cache_to_disk(st.session_state.query_cache, cache_file)
    
    return result, source_docs, False