import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent

TRAIN_PATH = BASE_DIR / "datasets" / "processed" / "train.json"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

embedding_model = SentenceTransformer(EMBEDDING_MODEL)

def load_data(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

train_data = load_data(TRAIN_PATH)

train_texts = [item["text"] for item in train_data]
train_intents = [item["intent"] for item in train_data]

train_embeddings = embedding_model.encode(train_texts, show_progress_bar=True)

                                               
                                                
                                                      
                                                   

def find_similar_examples(
    question, embedding_model, train_embeddings, train_texts, train_intents, top_k=5
):

    question_embedding = embedding_model.encode([question])

    similarities = cosine_similarity(question_embedding, train_embeddings)[0]

    top_indices = similarities.argsort()[-top_k:][::-1]

    results = []

    for index in top_indices:
        results.append(
            {
                "text": train_texts[index],
                "intent": train_intents[index],
                "similarity": similarities[index],
            }
        )

    return results

def analyze_neighbourhood(question , embedding_model , train_embeddings , train_intents , top_k):
    question_embedding = embedding_model.encode([question])

    similarities = cosine_similarity(question_embedding , train_embeddings)[0]

    top_indices = similarities.argsort()[-top_k:][::-1]

    intent_counts = {}

    for index in top_indices:
        intent = train_intents[index]
        intent_counts[intent] = intent_counts.get(intent , 0) + 1
    return intent_counts

neighborhood_sizes = [5, 10, 20, 50]

error_questions = [
    "What should contributors understand first?",
    "Great, thanks.",
    "This is really useful",
    "This is really useful.",
]

for question in error_questions:
                                               
                                                                                 
       

                                      
                                             

                                      
                                                                                         

                                             

    print("\n" + "=" * 60)
    print(f"Question: {question}")
    print("=" * 60)

    for top_k in neighborhood_sizes:
        intent_counts = analyze_neighbourhood(question,
                                              embedding_model , train_embeddings,
                                              train_intents,
                                              top_k=top_k)

        print(f"\nTop {top_k} Neighbours : ")

        sorted_counts = sorted(intent_counts.items(),
                               key=lambda item: item[1],
                               reverse = True)

        for intent , count in sorted_counts:
            print(f"{intent:15} → {count}")

