"""
Build Document
--------------
Builds the text documents used for embeddings and the knowledge document
that gets attached to every chunk.

Three document types:
  1. knowledge_document  → human-readable summary of a file (from LLM metadata)
  2. code_embedding_doc  → knowledge + raw code, used for chunk-level embeddings
  3. repo_embedding_doc  → knowledge only, used for file-level embeddings
"""


def build_knowledge_document(metadata):
    """
    Format LLM-generated metadata into a readable knowledge document.
    This gets stored with every chunk and is used in prompts and embeddings.
    """
    concepts = ", ".join(metadata.get("concepts", []))
    keywords = ", ".join(metadata.get("keywords", []))
    responsibilities = metadata.get("responsibilities", [])
    bullets = "\n".join(f"* {r}" for r in responsibilities)

    doc = f"""
Purpose:
{metadata.get('purpose', '')}

Responsibilities:
{bullets if bullets else '* None specified'}

Concepts:
{concepts if concepts else 'None specified'}

Keywords:
{keywords if keywords else 'None specified'}
"""
    return doc.strip()


def build_code_embedding_document(chunk):
    """
    Build the text used to generate chunk-level (code) embeddings.
    Combines knowledge document + raw code for rich semantic matching.
    """
    return f"""
{chunk['knowledge_document']}

========================

Implementation:
{chunk['content']}
""".strip()


def build_repo_embedding_document(chunk):
    """
    Build the text used to generate file-level (repo) embeddings.
    Uses only the knowledge document — no raw code.
    This makes file-level search respond to 'what a file is about'
    rather than specific code tokens.
    """
    return chunk["knowledge_document"].strip()
