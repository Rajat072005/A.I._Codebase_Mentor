"""
Keyword Retriever (TF-IDF)
---------------------------
Retrieves relevant chunks or files using TF-IDF cosine similarity.
Works alongside the semantic retriever — together they form the hybrid retrieval system.
"""

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def retrieve(question, documents, source_objects, top_k=3):
    """
    Retrieve the top-K most relevant objects using TF-IDF keyword matching.

    Args:
        question       : user's question string
        documents      : list of text strings (one per source object)
        source_objects : list of chunk or file dicts (parallel to documents)
        top_k          : number of unique results to return

    Returns:
        List of source_object dicts ranked by keyword relevance.
    """
    if not documents:
        return []

    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(documents)
    question_vector = vectorizer.transform([question])

    similarities = cosine_similarity(question_vector, doc_vectors)[0]
    top_indices = similarities.argsort()[::-1]

    seen_paths = set()
    unique_results = []

    for index in top_indices:
        result = source_objects[index]
        path = result["path"]
        if path not in seen_paths:
            unique_results.append(result)
            seen_paths.add(path)
        if len(unique_results) == top_k:
            break

    return unique_results
