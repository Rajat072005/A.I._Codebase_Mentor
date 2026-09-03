"""
Hybrid Retriever (Reciprocal Rank Fusion)
------------------------------------------
Merges semantic and keyword results into a single ranked list using RRF.

RRF formula: score = sum of 1 / (60 + rank) across all lists.
Results that appear in both lists get scores from both, naturally
rising to the top — no manual weight tuning needed.
"""


def merge_results_rrf(semantic_results, keyword_results):
    """
    Merge two ranked result lists using Reciprocal Rank Fusion.

    Args:
        semantic_results : ranked list from semantic retriever
        keyword_results  : ranked list from keyword retriever

    Returns:
        A single merged list sorted by RRF score (descending).
    """
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
