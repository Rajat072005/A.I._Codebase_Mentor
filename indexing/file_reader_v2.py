"""
File Reader (batched)
-----------------------
Drop-in replacement for file_reader.py's read_repository(). Same
walking/skip logic as the original — imported directly from
file_reader.py so the skip rules live in exactly one place — but routes
metadata generation through batch_indexer.py instead of calling
metadata_cache.get_metadata() once per file.

file_reader.py itself is untouched. To switch over, change ONE import
line wherever read_repository() is currently called (see the message
this file was delivered with for the exact line).

Return shape is identical to file_reader.read_repository(): a list of
{path, knowledge_document, content} dicts — so chunker.py,
embedding_generator.py, and everything downstream needs zero changes.
"""

import os
from indexing import build_document, batch_indexer
from indexing.file_reader import SKIP_FOLDERS, ALLOWED_EXTENSIONS, IGNORE_FILES

_EMPTY_METADATA = {"purpose": "", "responsibilities": [], "concepts": [], "keywords": []}


# def read_repository(repo_path):
#     """
#     Same signature and return shape as file_reader.read_repository().
#     """
#     raw_files = []

#     for root, dirs, files in os.walk(repo_path):
#         dirs[:] = [d for d in dirs if d not in SKIP_FOLDERS]

#         for file in files:
#             extension = os.path.splitext(file)[1]

#             if file in IGNORE_FILES:
#                 continue
#             if extension not in ALLOWED_EXTENSIONS:
#                 continue

#             file_path = os.path.join(root, file)

#             try:
#                 with open(file_path, "r", encoding="utf-8") as f:
#                     content = f.read()
#                 raw_files.append({"path": file_path, "content": content})
#             except Exception as error:
#                 print(f"  [skip] Could not read {file_path}: {error}")

#     print(f"Total files read: {len(raw_files)}")

#     # This is the one call that replaces the old per-file
#     # metadata_cache.get_metadata() loop — everything else above/below
#     # is identical to file_reader.py.
#     metadata_by_path = batch_indexer.get_metadata_for_repo(raw_files, repo_path)

#     all_files = []
#     for f in raw_files:
#         meta = metadata_by_path.get(f["path"]) or dict(_EMPTY_METADATA)
#         knowledge_document = build_document.build_knowledge_document(meta)
#         all_files.append({
#             "path": f["path"],
#             "knowledge_document": knowledge_document,
#             "content": f["content"],
#         })

#     return all_files


def read_repository(repo_path):
    """
    Same signature and return shape as file_reader.read_repository().
    """
    raw_files = []

    for root, dirs, files in os.walk(repo_path):
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
                raw_files.append({"path": file_path, "content": content})
            except Exception as error:
                print(f"  [skip] Could not read {file_path}: {error}")

    print(f"Total files read: {len(raw_files)}")

    # repo_path looks like "data/{repo_name}/repository" — derive repo_name
    # for cache-subfolder separation without needing a new parameter here.
    repo_name = os.path.basename(os.path.dirname(repo_path.rstrip("/\\")))

    metadata_by_path = batch_indexer.get_metadata_for_repo(raw_files, repo_path, repo_name)

    all_files = []
    for f in raw_files:
        meta = metadata_by_path.get(f["path"]) 
        knowledge_document = build_document.build_knowledge_document(meta)
        all_files.append({
            "path": f["path"],
            "knowledge_document": knowledge_document,
            "content": f["content"],
        })

    return all_files
