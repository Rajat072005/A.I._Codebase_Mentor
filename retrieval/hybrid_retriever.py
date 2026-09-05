

def merge_results_rrf(semantic_results, keyword_results):

    rrf_scores = {}

    for rank, result in enumerate(semantic_results, start=1):
        doc_id = result["id"]
        entry = rrf_scores.setdefault(doc_id, result.copy())
        entry["rrf_score"] = entry.get("rrf_score", 0) + 1 / (60 + rank)

    for rank, result in enumerate(keyword_results, start=1):
        doc_id = result["id"]
        entry = rrf_scores.setdefault(doc_id, result.copy())
        entry["rrf_score"] = entry.get("rrf_score", 0) + 1 / (60 + rank)

    merged = list(rrf_scores.values())
    merged.sort(key=lambda x: x["rrf_score"], reverse=True)
    return merged
