"""
RAG JAM - Interface Streamlit
Chatbot de recherche bibliographique avec citations.
"""

import streamlit as st
from src.engine import query, create_query_engine


# --- Page Configuration ---
st.set_page_config(
    page_title="RAG JAM - Assistant Bibliographique",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "sources" not in st.session_state:
    st.session_state.sources = []

if "engine_ready" not in st.session_state:
    st.session_state.engine_ready = False


# --- Sidebar: Sources Panel ---
with st.sidebar:
    st.header("📄 Sources")
    st.caption("Documents utilisés pour la dernière réponse")
    
    if st.session_state.sources:
        for i, source in enumerate(st.session_state.sources, 1):
            with st.expander(f"Source {i} (score: {source['score']:.3f})"):
                # Display metadata
                metadata = source.get("metadata", {})
                if metadata:
                    if "cite_key" in metadata:
                        st.markdown(f"**Clé:** `{metadata['cite_key']}`")
                    if "title" in metadata:
                        st.markdown(f"**Titre:** {metadata['title']}")
                    if "author" in metadata:
                        st.markdown(f"**Auteur:** {metadata['author']}")
                    if "year" in metadata:
                        st.markdown(f"**Année:** {metadata['year']}")
                    if "file_name" in metadata:
                        st.markdown(f"**Fichier:** {metadata['file_name']}")
                
                st.divider()
                st.markdown("**Extrait:**")
                st.text(source["text"])
    else:
        st.info("Posez une question pour voir les sources utilisées.")
    
    st.divider()
    
    # Settings
    st.header("⚙️ Paramètres")
    top_k = st.slider(
        "Nombre de sources à récupérer",
        min_value=1,
        max_value=10,
        value=3,
        help="Plus de sources = réponses plus complètes mais plus lentes"
    )
    
    # Clear conversation button
    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.sources = []
        st.rerun()


# --- Main Content ---
st.title("📚 RAG JAM")
st.caption("Assistant de recherche bibliographique - Posez vos questions sur les documents indexés")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Posez votre question sur la bibliographie..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Recherche dans les documents..."):
            try:
                # Query the RAG engine
                result = query(prompt, similarity_top_k=top_k)
                
                response_text = result["response"]
                st.session_state.sources = result["sources"]
                
                st.markdown(response_text, unsafe_allow_html=True)
                
                # Add assistant response to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text
                })
                
            except Exception as e:
                error_msg = f"❌ Erreur lors de la requête: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
    
    # Rerun to update sidebar with new sources
    st.rerun()


# --- Footer ---
st.divider()
st.caption("RAG JAM v0.1 | Prototype 48H | Données 100% locales")
