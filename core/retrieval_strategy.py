"""
Retrieval Strategy Config
--------------------------
Defines HOW to retrieve context for each question intent.
Each strategy controls:
  - retrieve_files         : how many top files to fetch first
  - preview_chunks         : how many leading chunks to include (preview mode)
  - retrieve_chunks        : True = deep chunk retrieval, False = preview mode
  - neighbor_expansion     : include adjacent chunks around retrieved ones
  - chunks_per_file        : (unused in v1, reserved)
  - chunk_count            : how many final chunks to retrieve
  - confidence_threshold   : min Gemini reranker score (1-10) to answer
  - prompt_template        : which prompt template to use
"""

RETRIEVAL_STRATEGIES = {

    "overview": {
        "retrieve_files": 6,
        "preview_chunks": 2,
        "retrieve_chunks": False,
        "neighbor_expansion": False,
        "chunks_per_file": 2,
        "chunk_count": 0,
        "confidence_threshold": 4,
        "prompt_template": "overview"
    },

    "architecture": {
        "retrieve_files": 5,
        "preview_chunks": 0,
        "retrieve_chunks": True,
        "neighbor_expansion": False,
        "chunks_per_file": 0,
        "chunk_count": 5,
        "confidence_threshold": 5,
        "prompt_template": "architecture"
    },

    "debug": {
        "retrieve_files": 3,
        "preview_chunks": 0,
        "retrieve_chunks": True,
        "neighbor_expansion": True,
        "chunks_per_file": 0,
        "chunk_count": 6,
        "confidence_threshold": 6,
        "prompt_template": "debug"
    },

    "implementation": {
        "retrieve_files": 3,
        "preview_chunks": 0,
        "retrieve_chunks": True,
        "neighbor_expansion": False,
        "chunks_per_file": 0,
        "chunk_count": 6,
        "confidence_threshold": 5,
        "prompt_template": "implementation"
    },

    "comparison": {
        "retrieve_files": 4,
        "preview_chunks": 0,
        "retrieve_chunks": True,
        "neighbor_expansion": False,
        "chunks_per_file": 0,
        "chunk_count": 6,
        "confidence_threshold": 5,
        "prompt_template": "comparison"
    },

    "locate": {
        "retrieve_files": 2,
        "preview_chunks": 2,
        "retrieve_chunks": False,
        "neighbor_expansion": False,
        "chunks_per_file": 0,
        "chunk_count": 6,
        "confidence_threshold": 4,
        "prompt_template": "locate"
    },

    "casual": {
        "retrieve_files": 0,
        "preview_chunks": 0,
        "retrieve_chunks": False,
        "neighbor_expansion": False,
        "chunks_per_file": 0,
        "chunk_count": 0,
        "confidence_threshold": 5,
        "prompt_template": "casual"
    },
}


def get_strategy(intent: str) -> dict:
    """Return the retrieval strategy for a given intent."""
    return RETRIEVAL_STRATEGIES[intent]
