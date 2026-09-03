"""
Question Classifier
-------------------
Uses the trained 7-intent Logistic Regression model (sentence-embedding based)
to classify a user question into one of:
  casual | overview | architecture | implementation | debug | locate | comparison
"""

import joblib
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Paths to the trained models
_BASE_DIR = Path(__file__).resolve().parent.parent
_MODEL_DIR = _BASE_DIR / "classifier" / "models"

# Load models once at startup
_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
_classifier = joblib.load(_MODEL_DIR / "intent_classifier.pkl")
_label_encoder = joblib.load(_MODEL_DIR / "label_encoder.pkl")


def classify_question(question: str) -> str:
    """
    Classify the user's question into one of 7 intents.
    Returns a string like 'debug', 'overview', 'casual', etc.
    """
    embedding = _embedding_model.encode([question])
    prediction = _classifier.predict(embedding)
    intent = _label_encoder.inverse_transform(prediction)[0]
    return intent
