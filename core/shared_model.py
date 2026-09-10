from fastembed import TextEmbedding
import warnings
warnings.filterwarnings("ignore")

print("Loading shared FastEmbed model (all-MiniLM-L6-v2)...")
shared_embedding_model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
