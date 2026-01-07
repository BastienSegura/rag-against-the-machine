# Manifeste du projet RAG JAM

## 1. Vision, Contexte & Posture Stratégique

### 1.1. Le Défi : Sprint "Commando" 48H

Ce projet n'est pas un développement classique, mais un **défi technique chronométré**.

* **Contrainte :** 48 heures de la conception à la démo fonctionnelle.
* **Esprit :** "Product-First". On privilégie ce qui fonctionne immédiatement sur ce qui est élégant ou complexe. Chaque heure doit produire une valeur tangible.
* **Objectif final :** Prouver la viabilité d'un système RAG appliqué à la recherche bibliographique avec un prototype interactif.

### 1.2. Contexte du Projet : L'Intelligence Bibliographique

Le corpus documentaire scientifique et technique est devenu trop vaste pour une lecture humaine exhaustive.

* **Problématique :** Comment extraire rapidement des connaissances précises d'une base de données bibliographique sans subir les hallucinations des IA généralistes ?
* **Solution :** Développer un moteur de "Retrieval-Augmented Generation" (RAG) spécialisé qui agit comme un assistant de recherche capable de sourcer chaque mot qu'il prononce.

### 1.3. Philosophie du MVP (Minimum Viable Product)

Pour tenir les délais, nous adoptons une approche **"No-Frills" (Sans fioritures)** :

1. **Fiabilité sur Exhaustivité :** Il vaut mieux que le système réponde parfaitement sur 50 documents clés que de manière instable sur 10 000.
2. **Transparence Algorithmique :** L'utilisateur doit voir ce que l'IA "lit" (les sources) pour valider la réponse.
3. **Vitesse d'Itération :** On déploie une version "v0.1" (ingestion + chat basique) dès la 12ème heure.

### 1.4. Le "North Star" (L'objectif de succès)

À T+48h, nous devons être capables de poser une question complexe à notre base de données (ex: *"Quelles sont les limites identifiées dans les études sur le graphène entre 2020 et 2022 ?"*) et d'obtenir une réponse structurée avec des liens vers les PDF ou entrées BibTeX correspondants.

### 1.5. Le Corpus de Données (Target Data)

Pour ce POC, nous ne visons pas l'exhaustivité mais la **représentativité**.

* **Domaine thématique :** L'apprentissage supervisé en Machine Learning (ML). C'est un sujet riche en terminologie spécifique, idéal pour tester la capacité du système à gérer un vocabulaire pointu.
* **Volume cible :** Entre 10 et 50 documents (PDF). C'est suffisant pour tester la pertinence sans saturer les capacités de calcul locales durant les tests.
* **Nature des fichiers :** * Articles scientifiques (format double colonne, souvent complexe pour l'extraction).
* Rapports techniques (format texte riche).
* Un fichier `.bib` (pour les métadonnées structurées). data/supervised-learning.bib
* **Source des données :** Utilisation de bases ouvertes comme arXiv, HAL, ou des rapports techniques publics.
* **Objectif de test :** Vérifier si le RAG arrive à distinguer des concepts proches mais différents (ex: Ridge vs Lasso regression) en se basant sur les documents fournis.


## 2. Architecture & Stack Technique (Version On-Premise Ready)

Pour ce sprint, nous allons pivoter vers une stack **100% locale** mais extrêmement simple à mettre en œuvre.
Tout sera installé sur ma machine locale (Windows avec WSL2) pour simuler un environnement "On-Premise".

### 2.1. Le choix des outils "Commando Local"

| Composant | Outil Sélectionné | Pourquoi ce choix ? |
| --- | --- | --- |
| **Serveur d'Inférence** | **Ollama** | C'est le "Docker" des LLM. Il permet de faire tourner Llama 3 ou Mistral en local avec une simplicité déconcertante. Indispensable pour du On-Premise. |
| **LLM (Le cerveau)** | **Llama 3 (8B) ou Mistral** | Modèles légers, performants, capables de tourner sur un PC portable avec 16Go de RAM. |
| **Embedding** | **FastEmbed** ou **Ollama** | Permet de transformer vos textes en vecteurs localement sans envoyer de données à l'extérieur. |
| **Vector DB** | **ChromaDB** | Base de données "In-memory" ou stockée dans un simple dossier local. Pas de serveur à gérer. |
| **Orchestrateur** | **LlamaIndex** | Très efficace pour la gestion des PDF/BibTeX et parfaitement compatible avec Ollama. |
| **Interface** | **Streamlit** | Pour garder la rapidité de développement de l'UI. |

### 2.2. Pourquoi cette stack est stratégique pour vous ?

1. **Confidentialité totale :** Aucune donnée ne sort de votre machine. C'est l'argument n°1 pour votre futur environnement professionnel.
2. **Transposabilité :** Le code que nous allons écrire pour ce MVP sera **95% identique** à celui que vous déploierez sur les serveurs de votre entreprise.
3. **Apprentissage concret :** Vous allez toucher aux problématiques de performance machine (CPU/GPU), ce qui est crucial pour un ingénieur data supervisant du On-Premise.

### 2.3. Les "Risques" à surveiller en 48h

* **Performance matérielle :** Si votre machine n'a pas de carte graphique (GPU) dédiée, la réponse de l'IA sera un peu lente (quelques secondes par phrase). C'est acceptable pour un prototype.
* **Poids des modèles :** Il faudra télécharger environ 5Go de modèles au début du sprint.

## 3. Périmètre Strict (Strict Scope) - MVP 48H

Pour ne pas dériver, nous nous fixons ces limites :

* **Entrées :** Un dossier contenant des fichiers PDF et un fichier `.bib` (BibTeX).
* **Traitement :** Extraction du texte brut et des métadonnées (auteur, année, titre).
* **Fonctionnalité clé :** "Chat with your bibliography" - L'utilisateur pose une question, le système affiche la réponse et le nom du document source.
* **Exclusion :** Pas de gestion de base de données SQL complexe, pas de système de "re-ranking" avancé pour le moment (on garde ça pour la v2).

## 4. Journal de Bord : Chronologie du Sprint (48H)

### Phase 1 : Fondations & Ingestion (H0 - H12)

**Objectif :** Transformer les fichiers bruts en vecteurs exploitables.

* **H0 - H3 : Setup Environnement.** Installation d'Ollama, téléchargement de `llama3` (ou `mistral`) et du modèle d'embedding. Test d'un "Hello World" en Python pour vérifier que le LLM répond localement.
* **H3 - H8 : Pipeline d'Ingestion.** Écriture du script avec `LlamaIndex` pour lire les PDF et le `.bib`.
* *Point critique :* Nettoyage des métadonnées (extraire titre/auteur du BibTeX pour les lier au vecteur du PDF).


* **H8 - H12 : Création de l'Index.** Premier "Vector Store" avec `ChromaDB`. Sauvegarde de l'index sur le disque pour ne pas avoir à ré-ingérer à chaque redémarrage.

### Phase 2 : Le Moteur RAG & Logique de Retrieval (H12 - H24)

**Objectif :** Faire en sorte que le système trouve les bons documents.

* **H12 - H18 : Test de Similarité.** Développement d'un script de test : "Pour cette question, quels sont les 3 extraits les plus proches que le système trouve ?".
* **H18 - H24 : "Prompt Engineering" Local.** Configuration du `System Prompt` pour forcer le modèle à utiliser uniquement le contexte fourni et à citer ses sources (ex: *"D'après [Auteur, 2023]..."*).
* *Note :* Les modèles locaux sont parfois moins dociles que GPT-4, le prompt doit être très directif.

### Phase 3 : Interface & Intégration (H24 - H36)

**Objectif :** Rendre l'outil utilisable via une interface graphique.

* **H24 - H30 : Développement Streamlit.** Création d'une interface de chat simple : une barre de recherche, une fenêtre de discussion, et un panneau latéral affichant les sources trouvées.
* **H30 - H36 : Boucle de Feedback.** Test de l'application sur 5 questions complexes. Ajustement de la taille des "chunks" (morceaux de texte) si les réponses sont trop vagues.

### Phase 4 : Optimisation & Finalisation (H36 - H48)

**Objectif :** Fiabiliser et documenter pour le futur On-Premise.

* **H36 - H42 : Gestion de la Performance.** Optimisation de la consommation RAM. Vérification de la latence (temps de réponse moyen).
* **H42 - H48 : Documentation "On-Premise Ready".** Rédaction d'un `README.md` technique expliquant comment déployer cette stack sur un serveur interne (dépendances, gestion des volumes pour ChromaDB).

## 5. Matrice de Risques Spéciale "Local"

| Risque | Impact | Solution de secours |
| --- | --- | --- |
| **Lenteur LLM** | Élevé | Passer sur un modèle plus petit (ex: `Phi-3` de Microsoft) via Ollama. |
| **OOM (Out of Memory)** | Critique | Réduire la taille du contexte envoyé au modèle (moins de chunks). |
| **Parsing PDF corrompu** | Moyen | Utiliser `PyMuPDF` ou `Unstructured` pour une extraction plus robuste. |

## 5. Critères de Succès & KPIs (Version "Light")

Nous divisons le succès en trois axes : Technique (On-Premise), Métier (Bibliographique) et Fiabilité.

### 5.1. Performance Technique (Le test "On-Premise")

* **Temps de Réponse (Latency) :** Le système doit fournir le premier mot de la réponse en moins de **8 secondes** (sur votre machine locale).
* *Pourquoi ?* Au-delà, l'expérience utilisateur sur un serveur interne sera jugée trop lourde.


* **Consommation RAM :** Le pipeline complet (Ollama + VectorDB + Streamlit) doit rester sous la barre des **12-14 Go de RAM**.
* *Pourquoi ?* Pour garantir la portabilité sur une station de travail standard en entreprise.



### 5.2. Qualité de l'Information (Le test "Bibliographique")

* **Taux de Citation :** 100% des réponses générées doivent comporter au moins **une référence explicite** (ex: Nom du PDF ou clé BibTeX).
* **Précision du Retrieval (Top-3) :** Sur 5 questions de test, les documents sources pertinents doivent apparaître dans les **3 premiers résultats** renvoyés par la base vectorielle.

### 5.3. Robustesse & Confiance (Le test "Hallucination")

* **Gestion de l'Ignorance :** Si la réponse n'est pas dans la base de données, le système doit répondre *"Je ne trouve pas d'information dans les documents fournis"* plutôt que d'inventer une réponse.
* **Parsing Success :** Le système doit être capable d'ingérer sans erreur au moins **3 formats de PDF différents** (articles de journaux, rapports techniques, thèses).