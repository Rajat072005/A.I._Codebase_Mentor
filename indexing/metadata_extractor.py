"""
Metadata Extractor
-------------------
Detects the module type and file type of a source file based on its path.
Used to tag each chunk with structural metadata for filtering purposes.
"""


# Map folder name → module type label
MODULE_KEYWORDS = {
    "pages": "page",
    "components": "component",
    "hooks": "hook",
    "features": "state",
    "store": "state",
    "context": "state",
    "api": "api",
    "services": "service",
    "utils": "utility",
    "styles": "style",
    "styling": "style",
    "middlewares": "backend",
}


def detect_module_type(path):
    """
    Detect the module type and file extension from a file path.

    Returns:
        (module_type, file_type) — e.g. ('component', 'jsx')
    """
    normalized = path.replace("\\", "/").lower()
    parts = normalized.split("/")
    file_name = parts[-1]
    file_type = file_name.split(".")[-1]

    for part in parts:
        if part in MODULE_KEYWORDS:
            return MODULE_KEYWORDS[part], file_type

    return "general", file_type
