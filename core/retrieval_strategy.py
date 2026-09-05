

RETRIEVAL_STRATEGIES = {

    "overview": {
        "retrieve_files": 6,
        "preview_chunks": 2,
        "retrieve_chunks": False,
        "neighbor_expansion": False,
        "chunks_per_file": 3,
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

    return RETRIEVAL_STRATEGIES[intent]
