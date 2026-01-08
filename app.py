"""
RAG JAM - Interface Streamlit
Chatbot de recherche bibliographique avec citations.
"""

import streamlit as st
from src.engine import query, create_query_engine


# --- Page Configuration ---
st.set_page_config(
    page_title="ML Assistant",
    page_icon="",
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
    st.header("Sources")
    st.caption("Documents used for the last response")
    
    if st.session_state.sources:
        for i, source in enumerate(st.session_state.sources, 1):
            with st.expander(f"Source {i} (score: {source['score']:.3f})"):
                # Display metadata
                metadata = source.get("metadata", {})
                if metadata:
                    if "cite_key" in metadata:
                        st.markdown(f"**Key:** `{metadata['cite_key']}`")
                    if "title" in metadata:
                        st.markdown(f"**Title:** {metadata['title']}")
                    if "author" in metadata:
                        st.markdown(f"**Author:** {metadata['author']}")
                    if "year" in metadata:
                        st.markdown(f"**Year:** {metadata['year']}")
                    if "file_name" in metadata:
                        st.markdown(f"**File:** {metadata['file_name']}")
                
                st.divider()
                st.markdown("**Excerpt:**")
                st.text(source["text"])
    else:
        st.info("Ask a question to see the sources used.")
    
    st.divider()
    
    # Settings
    st.header("Parameters")
    top_k = st.slider(
        "Number of sources to retrieve",
        min_value=1,
        max_value=10,
        value=3,
        help="More sources = more comprehensive answers but slower"
    )
    
    # Clear conversation button
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.sources = []
        st.rerun()


# --- Main Content ---
st.title("Machine Learning assistant")
st.caption("Ask your questions about the indexed documents")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask your question about the bibliography..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
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
st.caption("RAG JAM v0.1 | Prototype 48H | Data 100% local")
