from typing import Optional

from llama_index.core import Settings, PromptTemplate
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.llms.ollama import Ollama

from src.config import LLM_MODEL
from src.indexer import get_or_create_index, get_embedding_model


# System prompt forcing citation and avoiding hallucinations
SYSTEM_PROMPT = """Tu es un assistant de recherche bibliographique expert. Tu dois:
1. Répondre UNIQUEMENT à partir des documents fournis dans le contexte
2. TOUJOURS citer tes sources avec le format [Auteur, Année] ou [cite_key]
3. Si l'information n'est pas dans les documents, réponds: "Je ne trouve pas d'information dans les documents fournis."
4. Être précis et concis dans tes réponses
5. Ne JAMAIS inventer d'informations"""

QA_PROMPT_TEMPLATE = """Contexte des documents de recherche:
---------------------
{context_str}
---------------------

En te basant UNIQUEMENT sur le contexte ci-dessus, réponds à la question suivante.
Cite toujours tes sources entre crochets [Auteur, Année].

Question: {query_str}

Réponse:"""


def get_llm(model_name: str = LLM_MODEL, temperature: float = 0.1) -> Ollama:
    """
    Initialize the Ollama LLM.
    
    Args:
        model_name: Name of the Ollama model to use
        temperature: Sampling temperature (lower = more deterministic)
        
    Returns:
        Ollama: Configured LLM instance
    """
    return Ollama(
        model=model_name,
        temperature=temperature,
        request_timeout=120.0,
        system_prompt=SYSTEM_PROMPT
    )


def configure_settings():
    """
    Configure global LlamaIndex settings with local models.
    """
    Settings.llm = get_llm()
    Settings.embed_model = get_embedding_model()


def create_query_engine(
    similarity_top_k: int = 3,
    streaming: bool = False
) -> RetrieverQueryEngine:
    """
    Create a RAG query engine with citation support.
    
    Args:
        similarity_top_k: Number of similar documents to retrieve
        streaming: Whether to enable streaming responses
        
    Returns:
        RetrieverQueryEngine: Configured query engine
    """
    # Configure global settings
    configure_settings()
    
    # Get or create the vector index
    index = get_or_create_index()
    
    # Create custom QA prompt
    qa_prompt = PromptTemplate(QA_PROMPT_TEMPLATE)
    
    # Create response synthesizer
    response_synthesizer = get_response_synthesizer(
        response_mode="compact",
        text_qa_template=qa_prompt,
        streaming=streaming
    )
    
    # Create retriever
    retriever = index.as_retriever(similarity_top_k=similarity_top_k)
    
    # Build query engine
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer
    )
    
    return query_engine


def query(
    question: str,
    similarity_top_k: int = 3
) -> dict:
    """
    Query the RAG system and return response with sources.
    
    Args:
        question: The user's question
        similarity_top_k: Number of documents to retrieve
        
    Returns:
        dict: Contains 'response' text and 'sources' list
    """
    query_engine = create_query_engine(similarity_top_k=similarity_top_k)
    
    # Execute query
    response = query_engine.query(question)
    
    # Extract sources from response
    sources = []
    if response.source_nodes:
        for node in response.source_nodes:
            source_info = {
                "text": node.node.text[:500] + "..." if len(node.node.text) > 500 else node.node.text,
                "score": node.score,
                "metadata": node.node.metadata
            }
            sources.append(source_info)
    
    return {
        "response": str(response),
        "sources": sources
    }


# For testing
if __name__ == "__main__":
    print("Testing RAG Engine...")
    
    test_question = "It is well established that the Lasso estimator corresponds to the Maximum A Posteriori (MAP) estimate using a double-exponential (Laplacian) prior, which explains its property of setting coefficients exactly to zero. However, if we perform full Bayesian inference and use the mean of the posterior distribution instead of the mode, does the resulting estimator retain this sparsity property? Please explain why or why not based on the geometry of the distribution."
    print(f"\nQuestion: {test_question}")
    
    result = query(test_question)
    
    print(f"\nResponse: {result['response']}")
    print(f"\n--- Sources ({len(result['sources'])}) ---")
    for i, source in enumerate(result['sources'], 1):
        print(f"\n[{i}] Score: {source['score']:.3f}")
        print(f"    Metadata: {source['metadata']}")
        print(f"    Preview: {source['text'][:200]}...")
