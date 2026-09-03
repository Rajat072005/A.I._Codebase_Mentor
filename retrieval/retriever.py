"""
Chunk-Level Semantic Retriever
--------------------------------
Finds the most relevant individual CODE CHUNKS for a question.
Uses code embeddings (knowledge document + raw code content)
for more precise, implementation-level matching.
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def retrieve(question, embeddings, chunk_map, top_k=3):
    """
    Retrieve the top-K most relevant chunks for a question.

    Args:
        question   : user's question string
        embeddings : list of embedding dicts (filtered to the expanded file set)
        chunk_map  : dict of {chunk_id -> chunk} for lookup
        top_k      : number of unique results to return

    Returns:
        List of result dicts with 'id', 'chunk_id', 'score', 'path', 'content'.
    """
    question_embedding = _model.encode(question)
    results = []

    for item in embeddings:
        score = cosine_similarity(
            [question_embedding],
            [item["code_embedding"]]
        )[0][0]

        chunk = chunk_map[item["id"]]
        results.append({
            "id": item["id"],
            "chunk_id": chunk["chunk_id"],
            "score": float(score),
            "path": chunk["path"],
            "content": chunk["content"]
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    # One result per unique file to avoid flooding context with one file
    seen_paths = set()
    unique_results = []
    for result in results:
        if result["path"] not in seen_paths:
            unique_results.append(result)
            seen_paths.add(result["path"])
        if len(unique_results) == top_k:
            break

    return unique_results
