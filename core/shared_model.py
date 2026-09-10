from sentence_transformers import SentenceTransformer
import warnings
warnings.filterwarnings("ignore")

# Load the model exactly once into memory to save massive amounts of RAM
print("Loading shared SentenceTransformer model...")
shared_embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

