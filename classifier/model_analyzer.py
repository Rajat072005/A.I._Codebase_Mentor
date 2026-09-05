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
    classifier = joblib.load(
        MODEL_DIR / "intent_classifier.pkl"
    )

    label_encoder = joblib.load(
        MODEL_DIR / "label_encoder.pkl"
    )

    embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    return classifier , label_encoder , embedding_model

def load_dataset(filename):
    filepath = DATASET_DIR / filename

    with open(filepath , "r" , encoding="utf-8")as f:
        return json.load(f)

def prepare_data(dataset):
    texts = [example["text"] for example in dataset]
    labels = [example["intent"] for example in dataset]

    return texts , labels

def encode_labels(labels , label_encoder):
    return label_encoder.transform(labels)

def predict(texts , embedding_model , classifer):
    embeddings = embedding_model.encode(
        texts,
        show_progress_bar = True
    )

    predictions = classifer.predict(embeddings)
    probabilities = classifer.predict_proba(embeddings)

    return predictions,probabilities

def decode_labels(predictions , label_encoder):
    return label_encoder.inverse_transform(predictions)

def show_errors(texts ,actual_labels , predicted_labels , probabilities , classifier,label_encoder):

    print("\n" + "=" * 60)
    print("INCORRECT PREDICTIONS")
    print("=" * 60)

    error_count = 0

    for text , actual , predicted , probability_row in zip(texts , actual_labels , predicted_labels , probabilities):
        if actual != predicted:
            error_count += 1
            print(f"\nQuestion : {text}")
            print(f"Actual   : {actual}")
            print(f"Predicted: {predicted}")

            print("\nTop 3 Predictions:")

            top_indices = probability_row.argsort()[-3:][::-1]

            for index in top_indices:
                encoded_class = classifier.classes_[index]
                intent = label_encoder.inverse_transform([encoded_class])[0]
                confidence = probability_row[index]
                print(f"{intent:15} → {confidence:.4f}")

    print(f"\nTotal Errors: {error_count}")

def show_confusion_matrix(
    actual_encoded,
    predicted_encoded,
    label_encoder
):

    matrix = confusion_matrix(
        actual_encoded,
        predicted_encoded
    )

    labels = label_encoder.classes_

    print("\n" + "=" * 60)
    print("CONFUSION MATRIX")
    print("=" * 60)

    print("\nLabels:")
    print(labels)

    print("\nMatrix:")
    print(matrix)

def main():

    classifier, label_encoder, embedding_model = load_models()

    test_data = load_dataset("test.json")

    texts, actual_labels = prepare_data(test_data)

    actual_encoded = encode_labels(
        actual_labels,
        label_encoder
    )

    predicted_encoded , probabilities = predict(
        texts,
        embedding_model,
        classifier
    )

    predicted_labels = decode_labels(
        predicted_encoded,
        label_encoder
    )

    accuracy = accuracy_score(
        actual_labels,
        predicted_labels
    )

    print(f"\nTest Accuracy: {accuracy:.4f}")

    print("\nClassification Report:")

    print(
        classification_report(
            actual_labels,
            predicted_labels,
            target_names=label_encoder.classes_
        )
    )

    show_errors(
        texts,
        actual_labels,
        predicted_labels,
        probabilities,
        classifier,
        label_encoder
    )

    show_confusion_matrix(
        actual_encoded,
        predicted_encoded,
        label_encoder
    )

if __name__ == "__main__":
    main()
        

