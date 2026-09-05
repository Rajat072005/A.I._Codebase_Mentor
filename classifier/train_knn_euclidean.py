import json
from pathlib import Path

import joblib
import numpy as np              
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.neighbors import KNeighborsClassifier

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "datasets" / "processed"
MODEL_DIR = BASE_DIR / "models"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

with open(DATASET_DIR / "train.json" , "r" , encoding="utf-8")as f:
    train_data = json.load(f)

with open(DATASET_DIR / "test.json" , "r" , encoding="utf-8")as f:
    test_data = json.load(f)

train_texts = [item["text"] for item in train_data]
train_labels = [item["intent"] for item in train_data]

test_texts = [item["text"] for item in test_data]
test_labels = [item["intent"] for item in test_data]

embedding_model = SentenceTransformer(EMBEDDING_MODEL)

train_embeddings = embedding_model.encode(
    train_texts,
    show_progress_bar=True
)

test_embeddings = embedding_model.encode(
    test_texts,
    show_progress_bar=True
)

knn_classifier = KNeighborsClassifier(n_neighbors=5 , metric="euclidean")

knn_classifier.fit(
    train_embeddings,
    train_labels
)

test_predictions = knn_classifier.predict(
    test_embeddings
)

accuracy = accuracy_score(test_labels , test_predictions)

print(f"\nKNN Test Accuracy: {accuracy:.4f}")

print(
    classification_report(
        test_labels , test_predictions
    )
)

joblib.dump(knn_classifier , MODEL_DIR / "knn_euclidean_classifier.pkl")

print("\nKNN model saved successfully!")

