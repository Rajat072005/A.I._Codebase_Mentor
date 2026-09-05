

from indexing import metadata_cache
from indexing import llm_metadata_batch_generator as batch_gen

_EMPTY_METADATA = {"purpose": "", "responsibilities": [], "concepts": [], "keywords": []}

def get_metadata_for_repo(files, repo_root , repo_name):

    results = {}
    misses = []

    for f in files:
        current_hash = metadata_cache._hash_content(f["content"])
        cache_path = metadata_cache._get_cache_path(f["path"], repo_root,repo_name)
        cached = metadata_cache._load_cache(cache_path)

        if cached is not None and cached["file_hash"] == current_hash:
            print(f"  [cache hit] {f['path']}")
            results[f["path"]] = cached["metadata"]
        else:
            misses.append(f)

    if not misses:
        return results

    print(f"  [batch indexing] {len(misses)} file(s) need fresh metadata")
    content_by_path = {f["path"]: f["content"] for f in misses}

    def _persist(path, metadata):

        if metadata is None:
            return                                                                                    
        current_hash = metadata_cache._hash_content(content_by_path[path])
        cache_path = metadata_cache._get_cache_path(path, repo_root , repo_name)
        metadata_cache._save_cache(cache_path, metadata, current_hash)

    fresh = batch_gen.generate_metadata_for_files(misses, on_result=_persist)

    for path, metadata in fresh.items():
        results[path] = metadata if metadata is not None else dict(_EMPTY_METADATA)

    return results
