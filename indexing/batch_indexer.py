"""
Batch Indexer
--------------
Bridges llm_metadata_batch_generator.py with the existing on-disk cache
from metadata_cache.py — WITHOUT modifying metadata_cache.py. It reuses
that file's own hash/path/load/save helpers directly, so the cache
format stays byte-for-byte identical to what the rest of the project
already reads and writes.

This is the resumability layer: every file's metadata is written to
cache the instant it's generated, not batched up and written at the end.
If the process dies or a quota wall is hit mid-run, everything already
generated is safely on disk — a re-run just re-scans, sees the cache
hits, and only sends the still-missing files to Gemini.
"""

from indexing import metadata_cache
from indexing import llm_metadata_batch_generator as batch_gen

_EMPTY_METADATA = {"purpose": "", "responsibilities": [], "concepts": [], "keywords": []}


def get_metadata_for_repo(files, repo_root , repo_name):
    """
    files: list of {"path": ..., "content": ...} for every file read from
           the repo (unfiltered — cache hits/misses are resolved here).
    repo_root: root of the cloned repo, for cache path calculation
               (same as metadata_cache.get_metadata's repo_root arg).

    Returns: {path: metadata_dict} — cache hits plus freshly generated
    (batched) metadata for whatever was missing or stale.
    """
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
        """Write to cache the moment a result lands — the actual checkpoint."""
        if metadata is None:
            return  # generation failed even after retries/bisection — left uncached, retried next run
        current_hash = metadata_cache._hash_content(content_by_path[path])
        cache_path = metadata_cache._get_cache_path(path, repo_root , repo_name)
        metadata_cache._save_cache(cache_path, metadata, current_hash)

    fresh = batch_gen.generate_metadata_for_files(misses, on_result=_persist)

    for path, metadata in fresh.items():
        results[path] = metadata if metadata is not None else dict(_EMPTY_METADATA)

    return results
