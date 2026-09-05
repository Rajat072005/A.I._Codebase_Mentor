

import joblib
from pathlib import Path
from sentence_transformers import SentenceTransformer

                             
_BASE_DIR = Path(__file__).resolve().parent.parent
_MODEL_DIR = _BASE_DIR / "classifier" / "models"

                             
_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
_classifier = joblib.load(_MODEL_DIR / "intent_classifier.pkl")
_label_encoder = joblib.load(_MODEL_DIR / "label_encoder.pkl")

    

def classify_question(question: str) -> str:

    embedding = _embedding_model.encode([question])
    prediction = _classifier.predict(embedding)
    intent = _label_encoder.inverse_transform(prediction)[0]
    return intent
