

def build_knowledge_document(metadata):

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

    return f"""
{chunk['knowledge_document']}

========================

Implementation:
{chunk['content']}
""".strip()

def build_repo_embedding_document(chunk):

    return chunk["knowledge_document"].strip()
