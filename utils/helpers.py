

import os
import stat
import git

                                                                                

def build_chunkmap(chunks):

    return {chunk["id"]: chunk for chunk in chunks}

def build_embeddingmap(embeddings):

    return {embedding["id"]: embedding for embedding in embeddings}

                                                                                

def make_repo_keyword_document(chunks):

    return [chunk["knowledge_document"] for chunk in chunks]

def make_code_keyword_document(chunks):

    return [chunk["knowledge_document"] + "\n" + chunk["content"] for chunk in chunks]

                                                                                

def extract_repo_name(repo_url):

    return repo_url.rstrip("/").split("/")[-1]

def create_repo_folder(repo_name):

    folder_path = f"data/{repo_name}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def get_saved_repos():

    repos = []
    for item in os.listdir("data"):
        path = f"data/{item}"
        if os.path.isdir(path):
            repos.append(item)
    return repos

def get_local_commit_hash(repo_folder):

    repo = git.Repo(repo_folder)
    return repo.head.commit.hexsha

def get_remote_commit_hash(repo_url):

    try:
        g = git.Git()
        output = g.ls_remote(repo_url, "HEAD")
        if output:
            return output.split()[0]
    except Exception as error:
        print("Error fetching remote commit hash:", error)
    return None

def remove_readonly(func, path, _):

    os.chmod(path, stat.S_IWRITE)
    func(path)
