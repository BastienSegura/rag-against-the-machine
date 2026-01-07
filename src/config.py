from pathlib import Path

# --- Project Paths ---
# Root directory of the project (assuming src/config.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Directory containing raw data (PDFs + .bib)
DATA_DIR = PROJECT_ROOT / "data"

# Directory for persistent vector storage (ChromaDB)
STORAGE_DIR = PROJECT_ROOT / "storage"

# Path to the BibTeX file
BIB_FILE = DATA_DIR / "supervised-learning.bib"

# Ensure storage directory exists
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# --- Model Configuration (Ollama) ---
# LLM Model Name (ensure you have run `ollama pull llama3`)
LLM_MODEL = "llama3"

# Embedding Model
# Using a local HuggingFace model via LlamaIndex/FastEmbed for speed and privacy
# Alternative: "nomic-embed-text" if using Ollama for embeddings
EMBED_MODEL = "local:BAAI/bge-small-en-v1.5"

# --- RAG Hyperparameters ---
# Chunk size for splitting documents (in tokens)
CHUNK_SIZE = 1024

# Overlap between chunks to preserve context
CHUNK_OVERLAP = 128