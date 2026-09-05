"""
Repository Manager
-------------------
Orchestrates the full indexing pipeline for a GitHub repository:
  1. Clone the repo
  2. Read all source files (with LLM metadata generation)
  3. Create chunks
  4. Generate embeddings
  5. Save everything to disk

This is the single function called when a user wants to index a repo.
"""

import os
import shutil

from git import Repo

from indexing import chunker, embedding_generator
from indexing import file_reader_v2 as file_reader
from utils import helpers, storage


def reindex_repository(repo_url):
    """
    Clone and fully index a GitHub repository.

    Args:
        repo_url : GitHub repository URL (e.g. https://github.com/user/repo)

    Saves to disk:
        data/{repo_name}/repo_info.json
        data/{repo_name}/chunks.json
        data/{repo_name}/embeddings.json
    """
    repo_name = helpers.extract_repo_name(repo_url)
    repo_folder = helpers.create_repo_folder(repo_name)
    repo_code_folder = f"{repo_folder}/repository"

    # Remove existing code if re-indexing
    if os.path.exists(repo_code_folder):
        shutil.rmtree(repo_code_folder, onexc=helpers.remove_readonly)

    # Clone the repo
    print(f"Cloning {repo_url} ...")
    Repo.clone_from(repo_url, repo_code_folder)
    print("Clone complete.")

    # Save commit hash for change detection later
    last_commit_hash = helpers.get_local_commit_hash(repo_code_folder)
    repo_info = {
        "repo_name": repo_name,
        "repo_url": repo_url,
        "last_commit_hash": last_commit_hash,
    }

    # Read files → chunk → embed → save
    print("Reading files and generating metadata...")
    files = file_reader.read_repository(repo_code_folder)

    print("Creating chunks...")
    chunks = chunker.create_chunks(files)
    print(f"Total chunks: {len(chunks)}")

    print("Generating embeddings...")
    embeddings = embedding_generator.generate_embeddings(chunks)

    print("Saving to disk...")
    storage.save_json(repo_info, f"{repo_folder}/repo_info.json")
    storage.save_json(chunks, f"{repo_folder}/chunks.json")
    storage.save_json(embeddings, f"{repo_folder}/embeddings.json")
    print(f"Repository '{repo_name}' indexed successfully.")

    return {
        "repo_name": repo_name,
        "file_count": len({c["path"] for c in chunks}),
        "chunk_count": len(chunks),
    }
