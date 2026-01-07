### Project Structure

```text
rag-poc/
├── data/                   # Raw data (PDF + supervised-learning.bib)
├── storage/                # Local persistence of ChromaDB (generated)
├── src/
│   ├── __init__.py
│   ├── config.py           # Central configuration (models, paths, hyperparameters)
│   ├── loader.py           # Extraction logic (PDF + BibTeX Mapping)
│   ├── indexer.py          # Vectorization and storage logic (Embedding + ChromaDB)
│   ├── engine.py           # RAG logic (Query Engine, Prompts)
│   └── utils.py            # Helper functions (text cleaning, citation formatting)
├── app.py                  # Streamlit Interface (UI)
├── .env                    # Environment variables (if needed)
└── requirements.txt        # Dependencies (LlamaIndex, Ollama, Streamlit)
```

### Module Overview & Strategy

1. `config.py` — Central config: model names (Ollama), chunk size, data paths. Switch LLMs (Llama3/Mistral) here.
2. `loader.py` — Ingestion: read PDFs and parse .bib to build metadata dict. Extend here for JSON/Markdown.
3. `indexer.py` — Vectors: chunk text, embed, store in ChromaDB. Swap embedding backend (e.g., FastEmbed) here.
4. `engine.py` — RAG core: build query pipeline, prompts, context injection. Tune system prompt and citation style.
5. `app.py` — Streamlit UI only: presentation, no business logic. Calls `engine.query(message)`.
