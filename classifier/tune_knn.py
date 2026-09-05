import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

BASE_DIR = Path(__file__).resolve().parent

DATASET_DIR = BASE_DIR / "datasets" / "processed"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def load_dataset(filename):

    filepath = DATASET_DIR / filename

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def prepare_data(dataset):

    texts = [example["text"] for example in dataset]
    labels = [example["intent"] for example in dataset]

    return texts, labels

def main():

    train_data = load_dataset("train.json")
    validation_data = load_dataset("validation.json")

    train_texts, train_labels = prepare_data(train_data)
    validation_texts, validation_labels = prepare_data(validation_data)

    embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    print("Creating training embeddings...")

    train_embeddings = embedding_model.encode(train_texts, show_progress_bar=True)

    print("\nCreating validation embeddings...")

    validation_embeddings = embedding_model.encode(
        validation_texts, show_progress_bar=True
    )

                                        

    print("\n" + "=" * 60)
    print("KNN HYPERPARAMETER TUNING")
    print("=" * 60)

                        

                                                
                            
                             
           

                             
                               
                          
           

                                               
                                   
           

                                    
                                
                         
           

                
                                                                 
           

    print("\n" + "=" * 60)
    print("KNN WEIGHT TUNING")
    print("=" * 60)

                                            
                                                
                                                            
           

                                                            

                                                                     

                                                                   

                                                                               

    uniform_classifier = KNeighborsClassifier(
        n_neighbors=3, metric="cosine", weights="uniform"
    )

    distance_classifier = KNeighborsClassifier(
        n_neighbors=3, metric="cosine", weights="distance"
    )   

    uniform_classifier.fit(train_embeddings, train_labels)

    distance_classifier.fit(train_embeddings, train_labels)

    uniform_predictions = uniform_classifier.predict(validation_embeddings)

    distance_predictions = distance_classifier.predict(validation_embeddings)

    different_predictions = 0

    for text , actual ,uniform_prediction, distance_prediction in zip(
        validation_texts , validation_labels ,uniform_predictions, distance_predictions
    ):
        if uniform_prediction != distance_prediction:
                different_predictions += 1
                print(f"\nQuestion: {text}")
                print(f"Actual:   {actual}")
                print(f"Uniform:  {uniform_prediction}")
                print(f"Distance: {distance_prediction}")

                if uniform_prediction == actual:
                    print("Winner: Uniform")

                elif distance_prediction == actual:
                    print("Winner: Distance")

                else:
                    print("Winner: Neither")

    print("\n" + "=" * 60)
    print("UNIFORM VS DISTANCE PREDICTION COMPARISON")
    print("=" * 60)

    print(f"\nDifferent Predictions: {different_predictions}")

if __name__ == "__main__":
    main()
