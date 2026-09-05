

from sentence_transformers import SentenceTransformer
from indexing import build_document

_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

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
