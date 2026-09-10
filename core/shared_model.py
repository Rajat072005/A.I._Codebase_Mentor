from sentence_transformers import SentenceTransformer
from fastembed import TextEmbedding
import warnings
warnings.filterwarnings("ignore")

# Load the model exactly once into memory to save massive amounts of RAM
print("Loading shared SentenceTransformer model...")
shared_embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("Loading shared FastEmbed model (all-MiniLM-L6-v2)...")
shared_embedding_model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

