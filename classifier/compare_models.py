import json
from pathlib import Path

import joblib
from sentence_transformers import SentenceTransformer

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

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def prepare_data(dataset):

    texts = [example["text"] for example in dataset]

    labels = [example["intent"] for example in dataset]

    return texts, labels

def compare_predictions(texts, actual_labels, logistic_predictions, knn_predictions):

    both_correct = []
    both_wrong = []
    logistic_only_correct = []
    knn_only_correct = []

    for text, actual, logistic, knn in zip(
        texts, actual_labels, logistic_predictions, knn_predictions
    ):
        logistic_correct = logistic == actual
        knn_correct = knn == actual

        if logistic_correct and knn_correct:
            both_correct.append(
                {"text": text, "actual": actual, "logistic": logistic, "knn": knn}
            )
        elif logistic_correct and not knn_correct:
            logistic_only_correct.append(
                {"text": text, "actual": actual, "logistic": logistic, "knn": knn}
            )
        elif not logistic_correct and knn_correct:
            knn_only_correct.append(
                {"text": text, "actual": actual, "logistic": logistic, "knn": knn}
            )
        else:
            both_wrong.append(
                {"text": text, "actual": actual, "logistic": logistic, "knn": knn}
            )
    return (both_correct, logistic_only_correct, knn_only_correct, both_wrong)

def show_examples(title, examples):

    print("\n" + "=" * 70)

    print(title)

    print("=" * 70)

    print(f"\nTotal: {len(examples)}")

    for example in examples:
        print(f"\nQuestion : {example['text']}")
        print(f"Actual   : {example['actual']}")
        print(f"Logistic : {example['logistic']}")
        print(f"KNN      : {example['knn']}")

def main():
    (logistic_classifier, knn_classifer, label_encoder, embedding_model) = load_models()

    test_data = load_dataset("test.json")

    texts, actual_labels = prepare_data(test_data)

    print("Creating test embeddings...")

    test_embeddings = embedding_model.encode(texts, show_progress_bar=True)

    logistic_encoded_predictions = logistic_classifier.predict(test_embeddings)
    knn_predictions = knn_classifer.predict(test_embeddings)
    logistic_predictions = label_encoder.inverse_transform(logistic_encoded_predictions)

    (both_correct, logistic_only_correct, knn_only_correct, both_wrong) = (
        compare_predictions(texts, actual_labels, logistic_predictions, knn_predictions)
    )

                                              
             
                                              

    print("\n" + "=" * 70)
    print("MODEL COMPARISON SUMMARY")
    print("=" * 70)

    print(f"\nBoth Correct          : {len(both_correct)}")

    print(f"Only Logistic Correct  : {len(logistic_only_correct)}")

    print(f"Only KNN Correct       : {len(knn_only_correct)}")

    print(f"Both Wrong             : {len(both_wrong)}")

                                              
                            
                                              

    show_examples("ONLY LOGISTIC REGRESSION CORRECT", logistic_only_correct)

    show_examples("ONLY KNN CORRECT", knn_only_correct)

    show_examples("BOTH MODELS WRONG", both_wrong)

if __name__ == "__main__":
    main()
