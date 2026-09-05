import json
from pathlib import Path

import joblib
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score

BASE_DIR = Path(__file__).resolve().parent

DATASET_DIR = BASE_DIR / "datasets" / "processed"

MODEL_DIR = BASE_DIR / "models"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def load_models():

    logistic_classifier = joblib.load(MODEL_DIR / "intent_classifier.pkl")

    knn_classifier = joblib.load(MODEL_DIR / "knn_tuned_classifier.pkl")

    label_encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")

    embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    return (logistic_classifier, knn_classifier, label_encoder, embedding_model)

def load_dataset(filename):

    filepath = DATASET_DIR / filename

    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def prepare_data(dataset):

    texts = [example["text"] for example in dataset]

    labels = [example["intent"] for example in dataset]

    return texts, labels

def analyze_logistic_confidence(texts, actual_labels, predicted_labels, probabilities):
    correct_confidences = []
    wrong_confidences = []
    wrong_examples = []

    for text, actual, predicted, probability_row in zip(
        texts , actual_labels, predicted_labels, probabilities
    ):
        confidence = probability_row.max()
        if actual == predicted:
            correct_confidences.append(confidence)

        else:
            wrong_confidences.append(confidence)

            wrong_examples.append(
                (
                    text,
                    actual,
                    predicted,
                    confidence
                )
            )

    print("\n" + "=" * 70)
    print("LOGISTIC REGRESSION CONFIDENCE ANALYSIS")
    print("=" * 70)

    print(
        f"\nAverage confidence when correct: "
        f"{sum(correct_confidences) / len(correct_confidences):.4f}"
    )

    print(
        f"Average confidence when wrong  : "
        f"{sum(wrong_confidences) / len(wrong_confidences):.4f}"
    )

    print(f"\nCorrect predictions: {len(correct_confidences)}")
    print(f"Wrong predictions  : {len(wrong_confidences)}")

    print("\n" + "=" * 70)
    print("LOGISTIC REGRESSION WRONG PREDICTIONS")
    print("=" * 70)

    for text, actual, predicted, confidence in wrong_examples:

        print(f"\nQuestion   : {text}")
        print(f"Actual     : {actual}")
        print(f"Predicted  : {predicted}")
        print(f"Confidence : {confidence:.4f}")

    print("\n" + "=" * 70)
    print("LOWEST CONFIDENCE CORRECT PREDICTIONS")
    print("=" * 70)

    sorted_correct = sorted(correct_confidences)

    for confidence in sorted_correct[:10]:
        print(f"{confidence:.4f}")

def main():
    (logistic_classifier, knn_classifier, label_encoder, embedding_model) = (
        load_models()
    )

    test_data = load_dataset("test.json")

    texts, actual_labels = prepare_data(test_data)

    embeddings = embedding_model.encode(texts, show_progress_bar=True)

    logistic_encoded_predictions = logistic_classifier.predict(embeddings)
    knn_predictions = knn_classifier.predict(embeddings)

    logistic_predictions = label_encoder.inverse_transform(logistic_encoded_predictions)

    logistic_probabilities = logistic_classifier.predict_proba(embeddings)
    analyze_logistic_confidence(
        texts , actual_labels, logistic_predictions, logistic_probabilities
    )

    logistic_accuracy = accuracy_score(actual_labels, logistic_predictions)
    knn_accuracy = accuracy_score(actual_labels, knn_predictions)

    print("\n" + "=" * 70)
    print("INDIVIDUAL MODEL ACCURACY")
    print("=" * 70)

    print(f"\nLogistic Regression Accuracy: {logistic_accuracy:.4f}")

    print(f"KNN Accuracy: {knn_accuracy:.4f}")

if __name__ == "__main__":
    main()
