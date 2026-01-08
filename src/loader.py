from pathlib import Path
from typing import Dict, Any, List

import bibtexparser
from llama_index.core import SimpleDirectoryReader, Document
from llama_index.core.node_parser import SentenceSplitter

from src.config import DATA_DIR, BIB_FILE, CHUNK_SIZE, CHUNK_OVERLAP


def parse_bibtex(bib_path: Path = BIB_FILE) -> Dict[str, Dict[str, Any]]:
    """
    Parse a BibTeX file and extract metadata.
    
    Args:
        bib_path: Path to the .bib file
        
    Returns:
        Dictionary mapping cite keys to metadata (title, author, year)
    """
    with open(bib_path, "r", encoding="utf-8") as f:
        bib_database = bibtexparser.load(f)
    
    metadata_dict = {}
    for entry in bib_database.entries:
        cite_key = entry.get("ID", "")
        metadata_dict[cite_key] = {
            "title": entry.get("title", "Unknown Title"),
            "author": entry.get("author", "Unknown Author"),
            "year": entry.get("year", "Unknown Year"),
            "cite_key": cite_key,
        }
    
    return metadata_dict


def load_documents(data_path: Path = DATA_DIR) -> List[Document]:
    """
    Load PDF documents and enrich them with BibTeX metadata.
    
    Args:
        data_path: Directory containing PDF files
        
    Returns:
        List of LlamaIndex Document objects with enriched metadata
    """
    # Parse BibTeX for metadata lookup
    bib_metadata = parse_bibtex()
    
    # Load PDFs using SimpleDirectoryReader
    reader = SimpleDirectoryReader(
        input_dir=str(data_path),
        required_exts=[".pdf"],
        recursive=False,
    )
    documents = reader.load_data()
    
    # Enrich each document with BibTeX metadata
    for doc in documents:
        # Extract filename without extension (should match cite key)
        file_path = Path(doc.metadata.get("file_path", ""))
        cite_key = file_path.stem  # e.g., "lecun2015deep" from "lecun2015deep.pdf"
        
        # Look up metadata from BibTeX
        if cite_key in bib_metadata:
            bib_info = bib_metadata[cite_key]
            doc.metadata["title"] = bib_info["title"]
            doc.metadata["author"] = bib_info["author"]
            doc.metadata["year"] = bib_info["year"]
            doc.metadata["cite_key"] = bib_info["cite_key"]
        else:
            # Fallback: use filename as reference
            doc.metadata["title"] = cite_key
            doc.metadata["author"] = "Unknown"
            doc.metadata["year"] = "Unknown"
            doc.metadata["cite_key"] = cite_key
    
    return documents
