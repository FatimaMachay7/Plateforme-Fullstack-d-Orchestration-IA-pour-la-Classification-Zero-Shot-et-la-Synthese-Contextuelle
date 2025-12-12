# API de Classification et Analyse de Texte
### *Auteur :* __MACHAY Fatima__
### *Date :* __2025-12-12__

# Table des matières :
1. [Présentation du projet](#Présentation-du-projet)
2. [Fonctionnalités principales](#Fonctionnalités-principales)
3. [Architecture du système](#Architecture-du-système)
4. [Technologies utilisées](#Technologies-utilisées)
5. [Installation et exécution](#Installation-et-exécution)
6. [Configuration des variables d’environnement](#Configuration-des-variables-d’environnement)
7. [Base de données](#Base-de-données)
8. [Endpoints de l’API](#Endpoints-de-l’API)
9. [Déploiement avec Docker](#Déploiement-avec-Docker)
10. [Contact](#contact)


#  1. Présentation du projet:

Ce projet fournit une API permettant de classer, analyser et résumer des textes.
Elle combine l’intelligence artificielle de HuggingFace et Gemini, tout en enregistrant les résultats dans une base PostgreSQL. Un frontend complet est déjà disponible pour interagir avec l’API.

# 2. Fonctionnalités principales:

| Fonction                               | Description                                                                  |
|:-------------------------------------:|:----------------------------------------------------------------------------:|
| **Classification HF**                  | Détecte une catégorie parmi une liste prédéfinie (Finance, Politique, etc.). |
| **Analyse avec Gemini**                | Résume ou interprète un texte selon un prompt.                               |
| **Classification + Analyse combinées** | Combine HuggingFace pour classifier et Gemini pour expliquer le résultat.    |
| **Stockage en BD**                     | Sauvegarde des textes analysés et catégories dans PostgreSQL.                |
| **Interface Web**                      | Frontend en HTML/CSS/JS déjà intégré.                                        |


#  3. Architecture du système:
| Composant                   | Rôle                                                            |
|:---------------------------:|:--------------------------------------------------------------:|
| **Backend (FastAPI)**        | API de classification, analyse et enregistrement.            |
| **Frontend (HTML/CSS/JS)**  | Interface utilisateur affichant les résultats.               |
| **PostgreSQL**               | Stockage des textes classifiés.                               |
| **Docker / Docker Compose**  | Conteneurisation backend + frontend + base de données.       |


#  4. Technologies utilisées :
| Catégorie | Outils                                               |
|:---------:|:---------------------------------------------------:|
| Backend   | FastAPI, Pydantic, SQLAlchemy                        |
| IA        | HuggingFace Inference API, Gemini 2.5 Flash          |
| Base de données | PostgreSQL                                     |
| Déploiement | Docker, Docker Compose                             |
| Frontend  | HTML5, CSS3, JavaScript                              |

#  5.  Installation et exécution
🔹 __1. Cloner le projet :__
git clone <[git_clone](https://github.com/FatimaMachay7/Plateforme-Fullstack-d-Orchestration-IA-pour-la-Classification-Zero-Shot-et-la-Synthese-Contextuelle.git)>
cd project

🔹 __2. Installer les dépendances (sans Docker)__
pip install -r requirements.txt

🔹 __3. Lancer le backend__
uvicorn main:app --reload

🔹 __4. Accéder au frontend__

Ouvrir dans le navigateur : http://localhost:8000

# 6.  Configuration des variables d’environnement : 

Créer un fichier .env à la racine du backend :

| Variable        | Description                       |
|:---------------:|:---------------------------------:|
| `HF_TOKEN`      | Jeton HuggingFace                  |
| `GEMINI_API_KEY`| Clé API Gemini                     |
| `DATABASE_URL`  | URL PostgreSQL                     |


__Exemple :__

HF_TOKEN=xxxxxxxx
GEMINI_API_KEY=xxxxxxx
DATABASE_URL=postgresql://user:password@db:5432/classify

# 7. Base de données :

__Base créée :__ classify

__SGBD :__ PostgreSQL

__Table principale :__ classification

__Enregistrement automatique des :__

- texte soumis;
- catégorie détectée;
- score de confiance.

# 8.  Endpoints de l’API :
| Méthode  | Route                 | Description                                     |
|:--------:|:-------------------:|:-----------------------------------------------:|
| `GET`    | `/`                  | Affiche la page frontend                        |
| `POST`   | `/classify`          | Classification via HuggingFace                  |
| `POST`   | `/gemini`            | Analyse / résumé via Gemini                     |
| `POST`   | `/gemini-classify`   | Classification + analyse explicative           |

Chaque endpoint retourne une réponse JSON simple et claire.

# 9.  Déploiement avec Docker :
🔹 ___1. Construire et lancer les conteneurs ___
docker-compose up --build -d

🔹 __2. Vérifier les services__

Backend → http://localhost:8000
Frontend → selon ton Dockerfile (souvent port 80 )
Base PostgreSQL → port 5432

# 10.  Auteurs :

Développé par :
- MACHAY Fatima – Maroc – Projet académique / personnel 2025
- Projet réalisé dans le cadre d’un système IA de classification textuelle.