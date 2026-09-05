

def build_context(chunk_map, results):

    context = ""

    for result in results:
        chunk = chunk_map[result["id"]]

        context += f"""
------------------------------------------------------------
FILE:
{chunk['path']}

CHUNK: {chunk['chunk_id']}

KNOWLEDGE:
{chunk['knowledge_document']}

CODE:
{chunk['content']}
------------------------------------------------------------
"""
    return context
