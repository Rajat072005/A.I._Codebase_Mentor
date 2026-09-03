"""
Strategy Executor
------------------
Orchestrates the 3-step retrieval pipeline:
  Step 1 → Find candidate files (semantic + keyword, then RRF + rerank)
  Step 2 → Expand those files into all their chunks
  Step 3 → Either preview first N chunks OR do deep chunk-level retrieval
"""

from retrieval import repo_retriever, retriever, keyword_retriever, hybrid_retriever, reranker
from utils import helpers


def execute_strategy(question, strategy, chunks, chunk_map, embeddings):
    """
    Full retrieval pipeline for a question + strategy.

    Args:
        question   : user's question string
        strategy   : strategy config dict from retrieval_strategy.py
        chunks     : list of all chunk dicts for the repo
        chunk_map  : dict of {chunk_id -> chunk} for fast lookup
        embeddings : list of all embedding dicts for the repo

    Returns:
        (context_chunks, final_score)
    """
    candidate_files, top_file_score = _retrieve_candidate_files(
        question, chunks, chunk_map, embeddings, strategy
    )
    expanded_chunks = _expand_candidate_files(candidate_files, chunk_map)
    context_chunks, top_chunk_score = _prepare_context_chunks(
        question, expanded_chunks, strategy, embeddings
    )

    # Use chunk-level score if available, else fall back to file-level score
    final_score = top_chunk_score if top_chunk_score is not None else top_file_score
    return context_chunks, final_score


def _retrieve_candidate_files(question, chunks, chunk_map, embeddings, strategy):
    """
    Step 1: Find the most relevant files using hybrid retrieval + Gemini reranking.
    Returns (candidate_files, top_score).
    """
    top_k = strategy["retrieve_files"]

    # Semantic search on repo-level embeddings
    semantic_files = repo_retriever.retrieve_repo(question, embeddings, chunk_map, top_k)

    # Keyword (TF-IDF) search on knowledge documents
    keyword_documents = helpers.make_repo_keyword_document(chunks)
    keyword_files = keyword_retriever.retrieve(question, keyword_documents, chunks, top_k)

    # Merge with Reciprocal Rank Fusion
    merged_files = hybrid_retriever.merge_results_rrf(semantic_files, keyword_files)

    # Gemini reranks and scores the merged results
    candidate_files, top_file_score = reranker.rerank_results(question, merged_files)
    return candidate_files, top_file_score


def _expand_candidate_files(candidate_files, chunk_map):
    """
    Step 2: Collect ALL chunks belonging to the candidate files.
    This gives us the full content of each top file to work with.
    """
    expanded_chunks = []
    candidate_paths = {f["path"] for f in candidate_files}

    for chunk in chunk_map.values():
        if chunk["path"] in candidate_paths:
            expanded_chunks.append(chunk)

    return expanded_chunks


def _prepare_context_chunks(question, expanded_chunks, strategy, embeddings):
    """
    Step 3a (preview mode): Take the first N chunks from each file.
    Step 3b (retrieval mode): Run another round of hybrid retrieval + reranking
                              on the expanded chunks for precise chunk selection.
    Returns (context_chunks, top_chunk_score or None).
    """
    if not strategy["retrieve_chunks"]:
        # Preview mode — just take the leading chunks from each file
        preview_count = strategy["preview_chunks"]
        grouped = {}
        for chunk in expanded_chunks:
            grouped.setdefault(chunk["path"], []).append(chunk)

        final_chunks = []
        for file_chunks in grouped.values():
            final_chunks.extend(file_chunks[:preview_count])

        return final_chunks, None

    # Retrieval mode — deep chunk-level search within expanded chunks
    top_k = strategy["chunk_count"]

    # Build a fast lookup dict and filter embeddings to only expanded chunks
    expanded_chunk_map = {chunk["id"]: chunk for chunk in expanded_chunks}
    filtered_embeddings = [emb for emb in embeddings if emb["id"] in expanded_chunk_map]

    # Semantic search at chunk level
    semantic_results = retriever.retrieve(question, filtered_embeddings, expanded_chunk_map, top_k)

    # Keyword search at chunk level
    keyword_documents = helpers.make_code_keyword_document(expanded_chunks)
    keyword_results = keyword_retriever.retrieve(question, keyword_documents, expanded_chunks, top_k)

    # Merge + rerank
    merged_results = hybrid_retriever.merge_results_rrf(semantic_results, keyword_results)
    reranked_results, top_chunk_score = reranker.rerank_results(question, merged_results)

    # Optional: include neighboring chunks for better context (e.g. debug intent)
    if strategy["neighbor_expansion"]:
        final_chunks = _expand_neighbors(reranked_results, expanded_chunk_map)
        return final_chunks, top_chunk_score

    return reranked_results[:top_k], top_chunk_score


def _expand_neighbors(reranked_chunks, chunk_map):
    """
    For each retrieved chunk, also include the chunk before and after it
    in the same file. Useful for debug questions that need surrounding context.
    """
    expanded = []

    for chunk in reranked_chunks:
        current_path = chunk["path"]
        current_id = chunk["chunk_id"]

        for candidate in chunk_map.values():
            if candidate["path"] == current_path:
                if candidate["chunk_id"] in range(current_id - 1, current_id + 2):
                    expanded.append(candidate)

    # Deduplicate by chunk ID
    seen = set()
    final_chunks = []
    for chunk in expanded:
        if chunk["id"] not in seen:
            seen.add(chunk["id"])
            final_chunks.append(chunk)

    return final_chunks
