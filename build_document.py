def build_knowledge_document(metadata):
    concepts_str = ", ".join(metadata.get("concepts" ,[]))
    keywords_str = ", ".join(metadata.get("keywords" , []))
    responsibilities_list = metadata.get("responsibilities" , [])
    bullets = "\n".join(f"* {r}" for r in responsibilities_list)

    doc = f"""

Purpose:
{metadata.get('purpose', '')}

Responsibilities:
{bullets if bullets else '* None specified'}

Concepts:
{concepts_str if concepts_str else 'None specified'}

Keywords:
{keywords_str if keywords_str else 'None specified'}
"""
    return doc.strip()


def build_code_embedding_document(chunk):
    
    doc = f"""
{chunk["knowledge_document"]}

========================

Implementation: 
{chunk["content"]} 
"""
    
    return doc.strip()


def build_repo_embedding_document(chunk):
    
    doc = f"""
{chunk["knowledge_document"]}
"""
    
    return doc.strip()