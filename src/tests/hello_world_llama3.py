from llama_index.llms.ollama import Ollama

def test_connection():
    print("connection to the local llama3 model, hosted by Ollama.")
    
    llama3 = Ollama(model="llama3", request_timeout=60.0)

    # Simple completion test
    try:
        response = llama3.complete("Pourquoi utiliser un RAG (retrieval-augmented generation) pour la recherche bibliographique ? Réponds en une phrase.")
        print("\n  >>Llama3's answer:")
        print(f"--- \n{response}\n---")
    except Exception as e:
        print(f"\n Connection error : {e}")

if __name__ == "__main__":
    test_connection()