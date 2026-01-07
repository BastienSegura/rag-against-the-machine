# Journaling along the Development Process

## Vocabulary

* **open-weight models :** Machine learning models whose architecture and weights are publicly available, allowing for local deployment without reliance on external APIs.
* **DOI :** Digital Object Identifier. Used to uniquely identify academic documents.

## Free notes

* **effect of WSL on performance :** There is a slight performance hit when using WSL compared to a native Linux install. (up to 10%)
* **How to see if Ollama's server is running :** `curl http://localhost:11434` or `ollama list`
* **purpose of a .bib file :** It will act as the proof of what the llm answered from. It's a really important part of the RAG systems.
* **Easy way of building a .bib file :** Google Scholar -> "Cite" -> "BibTeX"
* **Difference between structured and unstructured data :** .pdf are unstructured, while .bib files are structured.

### Packages Install to interact with Ollama's server through Python

**-> see journal_00_setup_python_env.md for more details**


## Journal Entries

* **day1-08:30** - beginning of the project. Setting up the environment and gathering resources on open-weight models.
* **day1-09:37** - Ollama installed. Ollama is a local LLM server that supports various open-weight models.
* **day1-09:50** - Experimenting with Ollama using the Llama3:8B model.
* **day1-10:26** - Wrote a simple python script to interact with Ollama's server using the llama_index.llms.ollama module
* **day1-10:39** - Building the data corpus. Downloaded 10 research papers (PDF) and a BibTeX file on supervised learning in ML from arXiv.
* **day1-11:25** - The corpus is ready. Now I'm preparing the .bib file to extract metadata.