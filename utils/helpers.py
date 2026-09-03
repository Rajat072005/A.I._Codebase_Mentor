"""
General Helpers
----------------
Utility functions used across the Q&A pipeline.
"""

import os
import stat
import git


# ─── Data Structure Builders ──────────────────────────────────────────────────

def build_chunkmap(chunks):
    """Build a dict of {chunk_id -> chunk} for O(1) chunk lookup."""
    return {chunk["id"]: chunk for chunk in chunks}


def build_embeddingmap(embeddings):
    """Build a dict of {chunk_id -> embedding} for O(1) embedding lookup."""
    return {embedding["id"]: embedding for embedding in embeddings}


# ─── Keyword Document Builders ────────────────────────────────────────────────

def make_repo_keyword_document(chunks):
    """
    Build a list of text documents (one per chunk) for file-level TF-IDF search.
    Uses only the knowledge document (LLM metadata) — no raw code.
    """
    return [chunk["knowledge_document"] for chunk in chunks]


def make_code_keyword_document(chunks):
    """
    Build a list of text documents (one per chunk) for chunk-level TF-IDF search.
    Combines knowledge document + raw code content for richer matching.
    """
    return [chunk["knowledge_document"] + "\n" + chunk["content"] for chunk in chunks]


# ─── Repository Utilities ─────────────────────────────────────────────────────

def extract_repo_name(repo_url):
    """Extract the repo name from a GitHub URL. e.g. 'SyncSphere-Website'."""
    return repo_url.rstrip("/").split("/")[-1]


def create_repo_folder(repo_name):
    """Create and return the data folder path for a repo."""
    folder_path = f"data/{repo_name}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


def get_saved_repos():
    """Return a list of repo names that are indexed in the data/ folder."""
    repos = []
    for item in os.listdir("data"):
        path = f"data/{item}"
        if os.path.isdir(path):
            repos.append(item)
    return repos


def get_local_commit_hash(repo_folder):
    """Get the HEAD commit SHA of a locally cloned repo."""
    repo = git.Repo(repo_folder)
    return repo.head.commit.hexsha


def get_remote_commit_hash(repo_url):
    """Fetch the latest HEAD commit SHA from a remote GitHub repo."""
    try:
        g = git.Git()
        output = g.ls_remote(repo_url, "HEAD")
        if output:
            return output.split()[0]
    except Exception as error:
        print("Error fetching remote commit hash:", error)
    return None


def remove_readonly(func, path, _):
    """Helper for shutil.rmtree on Windows — removes read-only flag before deleting."""
    os.chmod(path, stat.S_IWRITE)
    func(path)
