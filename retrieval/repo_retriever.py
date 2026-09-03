"""
Repository-Level Semantic Retriever
-------------------------------------
Finds the most relevant FILES (not individual chunks) for a question
by comparing the question embedding against repo-level embeddings.
Repo embeddings are built from knowledge documents only (no raw code),
making them better at representing what a file is "about".
"""

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_repo(question, embeddings, chunk_map, top_k):
    """
    Retrieve the top-K most relevant files for a question.

    Args:
        question   : user's question string
        embeddings : list of embedding dicts (each has 'id' and 'repo_embedding')
        chunk_map  : dict of {chunk_id -> chunk} for path lookup
        top_k      : number of unique files to return

    Returns:
        List of result dicts with 'id', 'path', 'semantic_score', 'content'.
    """
    question_embedding = _model.encode(question)
    results = []

    for item in embeddings:
        score = cosine_similarity(
            [question_embedding],
            [item["repo_embedding"]]
        )[0][0]

        chunk = chunk_map[item["id"]]
        results.append({
            "id": chunk["id"],
            "path": chunk["path"],
            "semantic_score": float(score),   # Fixed: was 'score', breaking the sort
            "content": chunk["content"]
        })

    # Sort by semantic score descending
    results.sort(key=lambda x: x["semantic_score"], reverse=True)

    # Return only one result per unique file path
    seen_paths = set()
    unique_results = []
    for result in results:
        if result["path"] not in seen_paths:
            seen_paths.add(result["path"])
            unique_results.append(result)
        if len(unique_results) == top_k:
            break

    return unique_results
