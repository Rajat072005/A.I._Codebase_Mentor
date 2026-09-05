"""
Metadata Cache
---------------
Avoids redundant Gemini API calls by caching the generated metadata
for each file, keyed by its SHA-256 content hash.

If a file hasn't changed since the last index, the cached metadata
is returned immediately. If the file has changed, metadata is
regenerated and the cache is updated.
"""

import hashlib
import json
import os
import time
from pathlib import Path

from indexing import llm_metadata_generator

CACHE_ROOT = "metadata_cache"


def get_metadata(file_path, file_content, repo_root , repo_name):
    """
    Get metadata for a file — from cache if valid, or generate fresh.

    Args:
        file_path    : absolute path to the file
        file_content : raw text content of the file
        repo_root    : the root folder of the cloned repo (for relative path calculation)

    Returns:
        A metadata dict with keys: purpose, responsibilities, concepts, keywords.
    """
    current_hash = _hash_content(file_content)
    cache_path = _get_cache_path(file_path, repo_root,repo_name)
    cached = _load_cache(cache_path)

    if cached is None:
        # No cache exists — generate and save
        metadata = llm_metadata_generator.generate_llm_metadata(file_content)
        _save_cache(cache_path, metadata, current_hash)
        time.sleep(25)  # Respect Gemini rate limits
        return metadata

    if cached["file_hash"] == current_hash:
        print(f"  [cache hit] {file_path}")
        return cached["metadata"]

    # File has changed — regenerate
    metadata = llm_metadata_generator.generate_llm_metadata(file_content)
    _save_cache(cache_path, metadata, current_hash)
    time.sleep(25)
    return metadata


def _hash_content(content):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _get_cache_path(file_path, repo_root , repo_name):
    """
    Build the cache file path by mirroring the repo structure under metadata_cache/.
    Fix: repo_root is now dynamic instead of hardcoded.
    """
    relative = os.path.relpath(file_path, repo_root)
    base, _ = os.path.splitext(relative)
    cache_path = os.path.join(CACHE_ROOT, repo_name,  base + ".json")
    return cache_path


def _load_cache(cache_path):
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _save_cache(cache_path, metadata, file_hash):
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump({"file_hash": file_hash, "metadata": metadata}, f, indent=4)
