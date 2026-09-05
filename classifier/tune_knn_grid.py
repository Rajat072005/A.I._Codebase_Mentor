import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

BASE_DIR = Path(__file__).resolve().parent

DATASET_DIR = BASE_DIR / "datasets" / "processed"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

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

def main():

                                              
                                          
                                              

    train_data = load_dataset("train.json")
    validation_data = load_dataset("validation.json")

    train_texts, train_labels = prepare_data(
        train_data
    )

    validation_texts, validation_labels = prepare_data(
        validation_data
    )

                                              
                             
                                              

    embedding_model = SentenceTransformer(
        EMBEDDING_MODEL
    )

                                              
                               
                                              

    print("Creating training embeddings...")

    train_embeddings = embedding_model.encode(
        train_texts,
        show_progress_bar=True
    )

    print("\nCreating validation embeddings...")

    validation_embeddings = embedding_model.encode(
        validation_texts,
        show_progress_bar=True
    )

                                              
                               
                                              

    k_values = [1, 3, 5, 7, 9, 11, 15]

    weight_values = [
        "uniform",
        "distance"
    ]

    metric_values = [
        "cosine",
        "euclidean"
    ]

                                              
                      
                                              

    results = []

    print("\n" + "=" * 75)
    print("KNN GRID SEARCH")
    print("=" * 75)

                                              
                               
                                              

    for k in k_values:

        for weight in weight_values:

            for metric in metric_values:

                knn_classifier = KNeighborsClassifier(
                    n_neighbors=k,
                    weights=weight,
                    metric=metric
                )

                knn_classifier.fit(
                    train_embeddings,
                    train_labels
                )

                predictions = knn_classifier.predict(
                    validation_embeddings
                )

                accuracy = accuracy_score(
                    validation_labels,
                    predictions
                )

                result = {
                    "k": k,
                    "weights": weight,
                    "metric": metric,
                    "accuracy": accuracy
                }

                results.append(result)

                print(
                    f"k={k:<2} | "
                    f"weights={weight:<8} | "
                    f"metric={metric:<9} | "
                    f"accuracy={accuracy:.4f}"
                )

                                              
                     
                                              

    results.sort(
        key=lambda result: result["accuracy"],
        reverse=True
    )

                                              
                                
                                              

    print("\n" + "=" * 75)
    print("TOP KNN CONFIGURATIONS")
    print("=" * 75)

    for rank, result in enumerate(results[:10], start=1):

        print(
            f"\nRank {rank}"
        )

        print(
            f"k        : {result['k']}"
        )

        print(
            f"weights  : {result['weights']}"
        )

        print(
            f"metric   : {result['metric']}"
        )

        print(
            f"accuracy : {result['accuracy']:.4f}"
        )

if __name__ == "__main__":
    main()