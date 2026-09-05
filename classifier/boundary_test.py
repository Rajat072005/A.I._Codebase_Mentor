from pathlib import Path

import joblib
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def load_models():
    classifier = joblib.load(MODEL_DIR / "intent_classifier.pkl")

    label_encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")

    embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    return classifier , label_encoder , embedding_model

def predict_questions(questions , classifier , label_encoder , embedding_model):

    embeddings = embedding_model.encode(questions , show_progress_bar = True)

    predictions = classifier.predict(embeddings)

    predicted_intents = label_encoder.inverse_transform(predictions)

    return predicted_intents

def main():

    classifier, label_encoder, embedding_model = load_models()

    questions = [

                                                    
                      
                                                    

        "How does authentication connect to the API?",
        "How does authentication fit into the overall system?",
        "How does authentication communicate with other components?",
        "What role does authentication play in the application?",
        "How does authentication data flow through the system?",

                                                    
                        
                                                    

        "How does authentication process credentials internally?",
        "What happens internally when authentication runs?",
        "How does authentication work under the hood?",
        "What steps does authentication perform internally?",
        "How is the authentication logic executed?",

                                                    
                
                                                    

        "Where is authentication implemented?",
        "Which file contains the authentication logic?",
        "Which module handles authentication?",
        "Where can I find the authentication code?",
        "Point me to the authentication implementation."
    ]

    predictions = predict_questions(
        questions,
        classifier,
        label_encoder,
        embedding_model
    )

    print("\n" + "=" * 70)
    print("BOUNDARY TEST")
    print("=" * 70)

    for question, prediction in zip(
        questions,
        predictions
    ):

        print(f"\nQuestion : {question}")
        print(f"Predicted: {prediction}")

if __name__ == "__main__":
    main()