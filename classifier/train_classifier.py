import json
from pathlib import Path

import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

BASE_DIR = Path(__file__).resolve().parent

DATASET_DIR = BASE_DIR / "datasets" / "processed"

MODEL_DIR = BASE_DIR / "models"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

RANDOM_SEED = 42        

def load_datasets():
    datasets = {}

    for filename in ["train.json" , "validation.json" , "test.json"]:
        filepath = DATASET_DIR / filename

        with open(filepath , "r" , encoding="utf-8") as f:
            datasets[filename] = json.load(f)

    return datasets

def prepare_data(dataset):
    texts = [example["text"] for example in dataset]
    labels = [example["intent"] for example in dataset]

    return texts,labels

def encode_labels(train_labels , validation_labels , test_labels):
    label_encoder = LabelEncoder()

    train_encoded = label_encoder.fit_transform(train_labels)
    validation_encoded = label_encoder.transform(validation_labels)
    test_encoded = label_encoder.transform(test_labels)

    return(
        train_encoded, validation_encoded, test_encoded , label_encoder
    )

def generate_embeddings(texts , model):
    return model.encode(
        texts,
        show_progress_bar = True
    )

def train_classifier(train_embeddings , train_labels):

    classifier = LogisticRegression(
        random_state=RANDOM_SEED,
        max_iter=1000
    )

    classifier.fit(train_embeddings,train_labels)

    return classifier

def evaluate_model(classifier , embeddings , labels , dataset_name):

    predictions = classifier.predict(embeddings)
    accuracy = accuracy_score(labels , predictions)

    print(f"\n{dataset_name} Accuracy: {accuracy:.4f}")

    print(
        classification_report(
            labels,
            predictions
        )
    )

def save_model(classifier, label_encoder):

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    classifier_path = MODEL_DIR / "intent_classifier.pkl"

    label_encoder_path = MODEL_DIR / "label_encoder.pkl"

    joblib.dump(classifier, classifier_path)

    joblib.dump(label_encoder, label_encoder_path)

    print("\nModels saved successfully!")

def main():

    datasets = load_datasets()

    train_texts, train_labels = prepare_data(
        datasets["train.json"]
    )

    validation_texts, validation_labels = prepare_data(
        datasets["validation.json"]
    )

    test_texts, test_labels = prepare_data(
        datasets["test.json"]
    )

    (
        train_labels,
        validation_labels,
        test_labels,
        label_encoder
    ) = encode_labels(
        train_labels,
        validation_labels,
        test_labels
    )

    embedding_model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    train_embeddings = generate_embeddings(
        train_texts,
        embedding_model
    )

    validation_embeddings = generate_embeddings(
        validation_texts,
        embedding_model
    )

    test_embeddings = generate_embeddings(
        test_texts,
        embedding_model
    )

    classifier = train_classifier(
        train_embeddings,
        train_labels
    )

    evaluate_model(
        classifier,
        validation_embeddings,
        validation_labels,
        "Validation"
    )

    evaluate_model(
        classifier,
        test_embeddings,
        test_labels,
        "Test"
    )

    save_model(
        classifier,
        label_encoder
    )

if __name__ == "__main__":
    main()

