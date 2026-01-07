# Packages Install to interact with Ollama's server through Python

```bash
# Télécharger et installer Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Vérifier l'installation
ollama --version

# Télécharger le modèle Llama 3
ollama pull llama3

# Lancer le serveur Ollama (il démarre automatiquement normalement)
ollama serve

# Intéraction avec le modèle via la ligne de commande
ollama run llama3

# Mettre à jour les paquets
sudo apt update

# Installer Python 3 et pip
sudo apt install python3 python3-pip python3-venv -y

# Vérifier
python3 --version
pip3 --version

# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate

# bibtexparser pour manipuler les fichiers .bib
pip install bibtexparser

# llama-index pour interagir avec Ollama
pip install llama-index-core llama-index-llms-ollama llama-index-embeddings-ollama

# Example to run the loader script
(.venv-rag) XXXXXX@XXXXXXX:~/myProjects/rag-poc$ python3 -m src.loader
```