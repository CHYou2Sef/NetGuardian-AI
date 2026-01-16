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

#### 🎓 Pour apprendre
Ouvrez les notebooks dans `notebooks/kaggle/` dans l'ordre (01 à 05) ou utilisez les notebooks unifiés pour Colab.

#### 🌐 Dashboard en Temps Réel
```bash
# Lancer le dashboard Streamlit
streamlit run app/dashboard.py

# Ou avec Docker
docker-compose up
```

Accédez au dashboard sur **http://localhost:8501**

#### 🚀 Démonstration Rapide
```bash
# Simulation de 60 secondes
python scripts/run_realtime_demo.py --duration 60 --attack-rate 0.2

# Simulation personnalisée
python scripts/run_realtime_demo.py --duration 300 --attack-rate 0.3 --packets-per-second 20
```

## 🎯 Fonctionnalités du Dashboard

- **Détection en temps réel** avec visualisations interactives
- **Métriques live** : Total traité, attaques détectées, taux de détection
- **Graphiques** : Timeline, distribution des attaques, comparaisons
- **Contrôles** : Ajuster la vitesse de simulation et le ratio d'attaques
- **Export** : Sauvegarder les logs en CSV/JSON
- **Mode Mock** : Fonctionne sans modèles entraînés pour développement

> 💡 **Note** : Le système utilise des modèles mock par défaut. Pour utiliser les vrais modèles, entraînez-les d'abord avec les notebooks Colab, puis placez les fichiers `.pkl` dans `models/`.

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
