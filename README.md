# 🛡️ NetGuardian-AI

**Système de Détection Intelligente d'Intrusions (IDS) Hybride et Éducatif**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active_Development-green.svg)]()

> ⚠️ **Documentation Complète** : Pour tout guide détaillé, consultez [PROJECT_DOCUMENTATION_MASTER.md](PROJECT_DOCUMENTATION_MASTER.md)

---

## 📋 À Propos

NetGuardian-AI est un projet pédagogique et technique visant à créer un IDS moderne capable de détecter des attaques réseaux (DoS, Brute Force, Web Attacks) en utilisant une **approche hybride** :
1.  **Machine Learning (XGBoost)** pour filtrer rapidement le trafic.
2.  **Architecture Cascade** pour une classification précise des menaces.

Ce projet est structuré pour vous guider de la compréhension théorique (MITRE ATT&CK) jusqu'au déploiement d'un dashboard temps réel.

## 🚀 Démarrage Rapide

### 1. Installation

```bash
# Cloner le dépôt
git clone https://github.com/votre-user/NetGuardian-AI.git
cd NetGuardian-AI

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Structure du Projet

```
NetGuardian-AI/
├── notebooks/          # 🎓 Cœur pédagogique (5 phases)
│   ├── kaggle/         # 01_Analysis, 02_Prep, 03_Training, 04_Eval, 05_Sim
├── src/                # 🛠️ Code source partagé (nettoyage, model)
├── data/               # 💾 Données (non versionnées)
├── models/             # 🧠 Modèles entraînés (.pkl)
├── app/                # 🌐 Dashboard (Streamlit/Web)
└── PROJECT_DOCUMENTATION_MASTER.md  # 📘 TOUTE LA DOC EST ICI
```

### 3. Utilisation

*   **Pour apprendre** : Ouvrez les notebooks dans `notebooks/kaggle/` dans l'ordre (01 à 05).
*   **Pour le Dashboard** :
    ```bash
    streamlit run app/dashboard.py
    ```

## 📚 Documentation

Toute la documentation a été fusionnée en un seul fichier de référence :
👉 **[PROJECT_DOCUMENTATION_MASTER.md](PROJECT_DOCUMENTATION_MASTER.md)**

Ce fichier contient :
1.  La Base de Connaissances (Concepts IDS, ML, Outils)
2.  Le Guide du Dataset CICIDS2017
3.  L'explication de la Stratégie Hybride
4.  Les Guides Techniques (Git, Kaggle, Docker)
5.  Le Q&A

## 👥 Auteur

Projet académique - Cybersécurité, ENICar (5ème Semestre).
