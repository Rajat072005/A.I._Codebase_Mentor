

from core.shared_model import shared_embedding_model as _model
from indexing import build_document

def generate_embeddings(chunks):
    
    embeddings = []

    for chunk in chunks:
        code_text = build_document.build_code_embedding_document(chunk)
        repo_text = build_document.build_repo_embedding_document(chunk)

        code_vector = _model.encode(code_text)
        repo_vector = _model.encode(repo_text)

        embeddings.append({
            "id": f"{chunk['path']}_{chunk['chunk_id']}",
            "code_embedding": code_vector.tolist(),
            "repo_embedding": repo_vector.tolist(),
        })

    return embeddings
