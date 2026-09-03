"""
File Reader
------------
Walks a cloned repository, reads all supported source files,
and generates LLM metadata for each file (with caching).

Skips:
  - Common non-source folders (.git, node_modules, __pycache__, etc.)
  - Lock files (package-lock.json, yarn.lock, etc.)
  - Files without a supported extension
"""

import os
import time
from indexing import llm_metadata_generator, metadata_cache, build_document

SKIP_FOLDERS = {".git", "node_modules", "__pycache__", "venv", "dist", "build"}

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".css", ".html", ".json", ".md", ".txt"
}

IGNORE_FILES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    ".config.js", "robot.json"
}


def read_repository(repo_path):
    """
    Walk a cloned repository and return a list of file dicts.

    Each file dict contains:
      path              : absolute file path
      knowledge_document : formatted metadata string
      content            : raw file content

    Args:
        repo_path : path to the cloned repository root

    Returns:
        List of file dicts ready for chunking.
    """
    all_files = []

    for root, dirs, files in os.walk(repo_path):
        # Skip non-source folders in-place
        dirs[:] = [d for d in dirs if d not in SKIP_FOLDERS]

        for file in files:
            extension = os.path.splitext(file)[1]

            if file in IGNORE_FILES:
                continue
            if extension not in ALLOWED_EXTENSIONS:
                continue

            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Get metadata from cache or generate fresh with Gemini
                meta = metadata_cache.get_metadata(file_path, content, repo_path)
                if meta is None:
                    meta = {
                        "purpose": "",
                        "responsibilities": [],
                        "concepts": [],
                        "keywords": []
                    }

                knowledge_document = build_document.build_knowledge_document(meta)
                all_files.append({
                    "path": file_path,
                    "knowledge_document": knowledge_document,
                    "content": content,
                })

            except Exception as error:
                print(f"  [skip] Could not read {file_path}: {error}")

    print(f"Total files read: {len(all_files)}")
    return all_files
