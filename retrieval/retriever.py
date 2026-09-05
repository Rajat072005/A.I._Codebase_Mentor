

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def retrieve(question, embeddings, chunk_map, top_k=3):

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

                                                                        
    seen_paths = set()
    unique_results = []
    for result in results:
        if result["path"] not in seen_paths:
            unique_results.append(result)
            seen_paths.add(result["path"])
        if len(unique_results) == top_k:
            break

    return unique_results
