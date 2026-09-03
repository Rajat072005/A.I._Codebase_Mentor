"""
Context Builder
----------------
Assembles the final context string that gets injected into the LLM prompt.
Each retrieved chunk is formatted with its file path, chunk ID,
knowledge document (LLM-generated metadata), and raw code content.
"""


def build_context(chunk_map, results):
    """
    Build a readable context block from a list of retrieved chunks.

    Args:
        chunk_map : dict of {chunk_id -> chunk} for lookup
        results   : list of result dicts (each has an 'id' field)

    Returns:
        A formatted string ready to be inserted into the prompt.
    """
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
