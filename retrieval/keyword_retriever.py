

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def retrieve(question, documents, source_objects, top_k=3):

    if not documents:
        return []

    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(documents)
    question_vector = vectorizer.transform([question])

    similarities = cosine_similarity(question_vector, doc_vectors)[0]
    top_indices = similarities.argsort()[::-1]

    seen_paths = set()
    unique_results = []

    for index in top_indices:
        result = source_objects[index]
        path = result["path"]
        if path not in seen_paths:
            unique_results.append(result)
            seen_paths.add(path)
        if len(unique_results) == top_k:
            break

    return unique_results
