from pathlib import Path # useless?
from typing import List, Optional
import chromadb
from chromadb.config import Settings

from llama_index.core import (
    VectorStoreIndex, 
    StorageContext,
    load_index_from_storage
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Document

from src.config import (
    STORAGE_DIR, 
    EMBED_MODEL, 
    CHUNK_SIZE, 
    CHUNK_OVERLAP
)
from src.loader import load_documents

# Collection name for ChromaDB
COLLECTION_NAME = "rag_bibliography"


def get_embedding_model():
    """
    Initialize the local embedding model.
    
    Returns:
        HuggingFaceEmbedding: Configured embedding model
    """
    # Extract model name from local: prefix
    model_name = EMBED_MODEL.replace("local:", "")
    
    return HuggingFaceEmbedding(
        model_name=model_name,
        cache_folder=str(STORAGE_DIR / "embeddings_cache")
    )


def get_vector_store() -> ChromaVectorStore:
    """
    Initialize ChromaDB with persistent storage.
    
    Returns:
        ChromaVectorStore: Configured vector store
    """
    # Initialize persistent ChromaDB client
    chroma_client = chromadb.PersistentClient(
        path=str(STORAGE_DIR / "chromadb"),
        settings=Settings(allow_reset=True, anonymized_telemetry=False)
    )
    
    # --- CORRECTION ---
    # Utilisation de get_or_create_collection au lieu du try/except
    chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
    print(f"Loaded or created collection: {COLLECTION_NAME}")
    # ------------------
    
    # Wrap in LlamaIndex ChromaVectorStore
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    return vector_store


def build_index(documents: Optional[List[Document]] = None) -> VectorStoreIndex:
    """
    Build a new vector index from documents.
    
    Args:
        documents: List of Document objects. If None, loads from data directory.
        
    Returns:
        VectorStoreIndex: The built index
    """
    if documents is None:
        print("Loading documents from data directory...")
        documents = load_documents()
    
    print(f"Processing {len(documents)} documents...")
    
    # Initialize components
    embed_model = get_embedding_model()
    vector_store = get_vector_store()
    
    # Configure storage context
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Create node parser for chunking
    node_parser = SentenceSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    
    # Build index
    print("Building vector index...")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
        node_parser=node_parser,
        show_progress=True
    )
    
    # Persist the index
    print(f"Saving index to {STORAGE_DIR}")
    index.storage_context.persist(persist_dir=str(STORAGE_DIR))
    
    return index


def load_index() -> Optional[VectorStoreIndex]:
    """
    Try to load an existing index from storage.
    
    Returns:
        VectorStoreIndex if found, None otherwise
    """
    try:
        # Check if storage directory has index data
        if not (STORAGE_DIR / "docstore.json").exists():
            print("No existing index found.")
            return None
        
        print("Loading existing index from storage...")
        
        # Initialize embedding model and vector store
        embed_model = get_embedding_model()
        vector_store = get_vector_store()
        
        # Configure storage context
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
            persist_dir=str(STORAGE_DIR)
        )
        
        # Load the index
        index = load_index_from_storage(
            storage_context=storage_context,
            embed_model=embed_model
        )
        
        print("Index loaded successfully!")
        return index
        
    except Exception as e:
        print(f"Error loading index: {e}")
        print("Will need to rebuild index...")
        return None


def get_or_create_index() -> VectorStoreIndex:
    """
    Load existing index or create a new one if none exists.
    
    Returns:
        VectorStoreIndex: Ready-to-use vector index
    """
    # Try to load existing index
    index = load_index()
    
    if index is None:
        # Build new index
        print("Building new index...")
        index = build_index()
    
    return index


# For testing and manual rebuilding
if __name__ == "__main__":
    print("Building RAG index...")
    index = build_index()
    print("Index built successfully!")
    
    # Test query
    query_engine = index.as_query_engine()
    response = query_engine.query("What is supervised learning?")
    print(f"\nTest query response: {response}")
