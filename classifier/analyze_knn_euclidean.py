import json
from pathlib import Path

import joblib
from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

BASE_DIR = Path(__file__).resolve().parent

DATASET_DIR = BASE_DIR / "datasets" / "processed"

MODEL_DIR = BASE_DIR / "models"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def load_models():
    classifier = joblib.load(MODEL_DIR / "knn_euclidean_classifier.pkl")

    embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    return classifier , embedding_model

def load_dataset(filename):

    filepath = DATASET_DIR / filename

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def prepare_data(dataset):

    texts = [
        example["text"]
        for example in dataset
    ]

    labels = [
        example["intent"]
        for example in dataset
    ]

    return texts, labels

def predict(texts, embedding_model, classifier):

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True
    )

    predictions = classifier.predict(
        embeddings
    )

    probabilities = classifier.predict_proba(
        embeddings
    )

    return predictions , probabilities

def show_errors(
    texts,
    actual_labels,
    predicted_labels,
    probabilities,
    classifier
):

    print("\n" + "=" * 60)
    print("INCORRECT PREDICTIONS")
    print("=" * 60)

    error_count = 0

    for text, actual, predicted, probability_row in zip(
        texts,
        actual_labels,
        predicted_labels,
        probabilities
    ):

        if actual != predicted:

            error_count += 1

            print(f"\nQuestion : {text}")
            print(f"Actual   : {actual}")
            print(f"Predicted: {predicted}")

            print("\nTop 3 Predictions:")

            top_indices = probability_row.argsort()[-3:][::-1]

            for index in top_indices:

                intent = classifier.classes_[index]

                probability = probability_row[index]

                print(
                    f"{intent:15} → {probability:.4f}"
                )

    print(f"\nTotal Errors: {error_count}")

def show_confusion_matrix(actual_labels , predicted_labels , classifier):
    labels = classifier.classes_

    matrix = confusion_matrix(actual_labels , predicted_labels , labels=labels)

    print("\n" + "=" * 60)
    print("CONFUSION MATRIX")
    print("=" * 60)

    print("\nLabels:")
    print(labels)

    print("\nMatrix:")
    print(matrix)

def main():

    classifier, embedding_model = load_models()

    test_data = load_dataset("test.json")

    texts, actual_labels = prepare_data(
        test_data
    )

    predicted_labels, probabilities = predict(
        texts,
        embedding_model,
        classifier
    )

    accuracy = accuracy_score(
        actual_labels,
        predicted_labels
    )

    print(f"\nKNN Test Accuracy: {accuracy:.4f}")

    print("\nClassification Report:")

    print(
        classification_report(
            actual_labels,
            predicted_labels,
            labels=classifier.classes_
        )
    )

    show_errors(
        texts,
        actual_labels,
        predicted_labels,
        probabilities,
        classifier
    )

    show_confusion_matrix(
        actual_labels,
        predicted_labels,
        classifier
    )

if __name__ == "__main__":
    main()