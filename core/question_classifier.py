import joblib
from pathlib import Path
from core.shared_model import shared_embedding_model as _embedding_model

                             
_BASE_DIR = Path(__file__).resolve().parent.parent
_MODEL_DIR = _BASE_DIR / "classifier" / "models"

                             
_classifier = joblib.load(_MODEL_DIR / "intent_classifier.pkl")
_label_encoder = joblib.load(_MODEL_DIR / "label_encoder.pkl")

    

def classify_question(question: str) -> str:

    embedding = list(_embedding_model.embed([question]))
    prediction = _classifier.predict(embedding)
    intent = _label_encoder.inverse_transform(prediction)[0]
    return intent
