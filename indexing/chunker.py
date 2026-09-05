

import re
from indexing import metadata_extractor

def _split_js(content):
    pattern = r"(?=export\s+default\s+function|function\s|class\s|export\s+default|const\s+\w+\s*=\s*\()"
    chunks = re.split(pattern, content)
    return [c.strip() for c in chunks if c.strip()]

def _split_python(content):
    pattern = r"(?=def\s|class\s)"
    chunks = re.split(pattern, content)
    return [c.strip() for c in chunks if c.strip()]

def _split_css(content):
    chunks = content.split("}")
    return [c.strip() + "}" for c in chunks if c.strip()]

def create_chunks(files):

    all_chunks = []

    for file in files:
        path = file["path"].lower()
        content = file["content"]
        knowledge_document = file["knowledge_document"]
        module_type, file_type = metadata_extractor.detect_module_type(path)

        if path.endswith((".js", ".jsx", ".ts", ".tsx")):
            file_chunks = _split_js(content)
        elif path.endswith(".py"):
            file_chunks = _split_python(content)
        elif path.endswith(".css"):
            file_chunks = _split_css(content)
        else:
            file_chunks = [content[i:i + 1000] for i in range(0, len(content), 1000)]

        for idx, chunk_content in enumerate(file_chunks, start=1):
            all_chunks.append({
                "id": f"{file['path']}_{idx}",
                "path": file["path"],
                "chunk_id": idx,
                "module_type": module_type,
                "file_type": file_type,
                "knowledge_document": knowledge_document,
                "content": chunk_content,
            })

    return all_chunks
