

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_repo(question, embeddings, chunk_map, top_k):

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
            "semantic_score": float(score),                                          
            "content": chunk["content"]
        })

                                       
    results.sort(key=lambda x: x["semantic_score"], reverse=True)

                                                 
    seen_paths = set()
    unique_results = []
    for result in results:
        if result["path"] not in seen_paths:
            seen_paths.add(result["path"])
            unique_results.append(result)
        if len(unique_results) == top_k:
            break

    return unique_results
