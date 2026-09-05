

import os
import shutil

from git import Repo

from indexing import chunker, embedding_generator
from indexing import file_reader_v2 as file_reader
from utils import helpers, storage

def reindex_repository(repo_url):

    repo_name = helpers.extract_repo_name(repo_url)
    repo_folder = helpers.create_repo_folder(repo_name)
    repo_code_folder = f"{repo_folder}/repository"

                                         
    if os.path.exists(repo_code_folder):
        shutil.rmtree(repo_code_folder, onexc=helpers.remove_readonly)

                    
    print(f"Cloning {repo_url} ...")
    Repo.clone_from(repo_url, repo_code_folder)
    print("Clone complete.")

                                                 
    last_commit_hash = helpers.get_local_commit_hash(repo_code_folder)
    repo_info = {
        "repo_name": repo_name,
        "repo_url": repo_url,
        "last_commit_hash": last_commit_hash,
    }

                                       
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
