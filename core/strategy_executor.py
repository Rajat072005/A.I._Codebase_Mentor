

from retrieval import repo_retriever, retriever, keyword_retriever, hybrid_retriever, reranker
from utils import helpers

def execute_strategy(question, strategy, chunks, chunk_map, embeddings):

    candidate_files, top_file_score = _retrieve_candidate_files(
        question, chunks, chunk_map, embeddings, strategy
    )
    expanded_chunks = _expand_candidate_files(candidate_files, chunk_map)
    context_chunks, top_chunk_score = _prepare_context_chunks(
        question, expanded_chunks, strategy, embeddings
    )

                                                                            
    final_score = top_chunk_score if top_chunk_score is not None else top_file_score
    return context_chunks, final_score

def _retrieve_candidate_files(question, chunks, chunk_map, embeddings, strategy):

    top_k = strategy["retrieve_files"]

                                              
    semantic_files = repo_retriever.retrieve_repo(question, embeddings, chunk_map, top_k)

                                                    
    keyword_documents = helpers.make_repo_keyword_document(chunks)
    keyword_files = keyword_retriever.retrieve(question, keyword_documents, chunks, top_k)

                                       
    merged_files = hybrid_retriever.merge_results_rrf(semantic_files, keyword_files)

                                                  
    candidate_files, top_file_score = reranker.rerank_results(question, merged_files)
    return candidate_files, top_file_score

def _expand_candidate_files(candidate_files, chunk_map):

    expanded_chunks = []
    candidate_paths = {f["path"] for f in candidate_files}

    for chunk in chunk_map.values():
        if chunk["path"] in candidate_paths:
            expanded_chunks.append(chunk)

    return expanded_chunks

def _prepare_context_chunks(question, expanded_chunks, strategy, embeddings):

    if not strategy["retrieve_chunks"]:
                                                                    
        preview_count = strategy["preview_chunks"]
        grouped = {}
        for chunk in expanded_chunks:
            grouped.setdefault(chunk["path"], []).append(chunk)

        final_chunks = []
        for file_chunks in grouped.values():
            final_chunks.extend(file_chunks[:preview_count])

        return final_chunks, None

                                                                     
    top_k = strategy["chunk_count"]

                                                                            
    expanded_chunk_map = {chunk["id"]: chunk for chunk in expanded_chunks}
    filtered_embeddings = [emb for emb in embeddings if emb["id"] in expanded_chunk_map]

                                    
    semantic_results = retriever.retrieve(question, filtered_embeddings, expanded_chunk_map, top_k)

                                   
    keyword_documents = helpers.make_code_keyword_document(expanded_chunks)
    keyword_results = keyword_retriever.retrieve(question, keyword_documents, expanded_chunks, top_k)

                    
    merged_results = hybrid_retriever.merge_results_rrf(semantic_results, keyword_results)
    reranked_results, top_chunk_score = reranker.rerank_results(question, merged_results)

                                                                                 
    if strategy["neighbor_expansion"]:
        final_chunks = _expand_neighbors(reranked_results, expanded_chunk_map)
        return final_chunks, top_chunk_score

    return reranked_results[:top_k], top_chunk_score

def _expand_neighbors(reranked_chunks, chunk_map):

    expanded = []

    for chunk in reranked_chunks:
        current_path = chunk["path"]
        current_id = chunk["chunk_id"]

        for candidate in chunk_map.values():
            if candidate["path"] == current_path:
                if candidate["chunk_id"] in range(current_id - 1, current_id + 2):
                    expanded.append(candidate)

                             
    seen = set()
    final_chunks = []
    for chunk in expanded:
        if chunk["id"] not in seen:
            seen.add(chunk["id"])
            final_chunks.append(chunk)

    return final_chunks
