# 🛡️ NetGuardian-AI

**Système de Détection Intelligente d'Intrusions (IDS) basé sur Machine Learning & Deep Learning**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-orange.svg)](https://www.tensorflow.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Description

NetGuardian-AI est un système intelligent de détection d'intrusions qui utilise des algorithmes de Machine Learning et Deep Learning pour identifier les comportements anormaux dans le trafic réseau d'une entreprise.

### 🎯 Objectifs

- Détecter les cyberattaques sophistiquées (DoS/DDoS, scans, brute-force, injections, botnets, exfiltration)
- Analyser le trafic réseau en temps réel
- Fournir un dashboard interactif pour la visualisation des alertes
- Intégrable dans un SOC/SIEM existant

---

## 🏗️ Architecture

```
NetGuardian-AI/
├── data/                       # Datasets
│   ├── raw/                    # Dataset brut (CICIDS2017)
│   ├── processed/              # Dataset nettoyé
│   └── samples/                # Échantillons pour tests
├── notebooks/                  # Jupyter Notebooks
│   ├── local/                  # Notebooks locaux
│   └── cloud/                  # Notebooks Colab/Kaggle
├── models/                     # Modèles entraînés
│   ├── ml/                     # Random Forest, XGBoost, SVM
│   └── dl/                     # LSTM, Autoencoder, MLP
├── src/                        # Code source
│   ├── data/                   # Chargement et préparation
│   ├── models/                 # Modèles ML/DL
│   ├── evaluation/             # Métriques et évaluation
│   ├── detection/              # Détection temps réel
│   └── utils/                  # Utilitaires
├── app/                        # Dashboard Streamlit
│   └── components/             # Composants UI
├── reports/                    # Rapports et analyses
├── logs/                       # Logs d'entraînement
└── tests/                      # Tests unitaires
```

---

## 🚀 Installation

### Prérequis

- Python 3.10+
- pip
- (Optionnel) GPU pour Deep Learning

### Setup Local

```bash
# Cloner le projet
cd "y:\ENICar\cours\5th Sem\CybSec\project\NetGuardian-AI"

# Créer environnement virtuel
python -m venv venv

# Activer l'environnement
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt
```

---

## 📊 Dataset

Ce projet utilise le dataset **CICIDS2017** (Canadian Institute for Cybersecurity Intrusion Detection System).

### Téléchargement

**Option 1 : Kaggle** (Recommandé)
- Dataset disponible sur Kaggle : [CICIDS2017](https://www.kaggle.com/datasets/cicdataset/cicids2017)
- Utiliser les notebooks Kaggle pour l'exploration

**Option 2 : Source Officielle**
- [Site officiel CIC](https://www.unb.ca/cic/datasets/ids-2017.html)

### Types d'Attaques Incluses

- ✅ DoS/DDoS
- ✅ Port Scan
- ✅ Brute Force (FTP, SSH)
- ✅ Web Attacks (SQL Injection, XSS)
- ✅ Botnet
- ✅ Infiltration

---

## 🤖 Modèles Implémentés

### Machine Learning Classique
- **Random Forest** : Ensemble learning pour classification robuste
- **XGBoost** : Gradient boosting optimisé
- **SVM** : Support Vector Machine avec kernel RBF
- **Isolation Forest** : Détection d'anomalies non supervisée
- **K-Means** : Clustering pour identifier comportements normaux

### Deep Learning
- **MLP** (Multi-Layer Perceptron) : Réseau de neurones dense
- **LSTM** (Long Short-Term Memory) : Pour séquences temporelles
- **Autoencoder** : Détection d'anomalies par reconstruction

---

## 🔧 Utilisation

### 1. Exploration des Données

```bash
# Lancer Jupyter Notebook
jupyter notebook notebooks/local/01_data_exploration.ipynb
```

### 2. Entraînement des Modèles

**ML Classique (Local)** :
```bash
python src/models/supervised.py --model random_forest
python src/models/supervised.py --model xgboost
```

**Deep Learning (Colab)** :
- Ouvrir `notebooks/cloud/NetGuardian_DL_Training.ipynb` dans Google Colab
- Monter Google Drive
- Exécuter les cellules

### 3. Évaluation

```bash
python src/evaluation/metrics.py --model all
```

### 4. Dashboard

```bash
streamlit run app/dashboard.py
```

Ouvrir le navigateur sur `http://localhost:8501`

---

## 📈 Métriques de Performance

Les modèles sont évalués selon :
- **Accuracy** : Taux de prédictions correctes
- **Precision** : Taux de vrais positifs parmi les positifs prédits
- **Recall** : Taux de vrais positifs détectés
- **F1-Score** : Moyenne harmonique de Precision et Recall
- **ROC/AUC** : Courbe de performance du classificateur

---

## 🌐 Solution Hybride

Ce projet utilise une approche hybride pour optimiser les ressources :

| Phase | Environnement | Raison |
|-------|---------------|--------|
| Exploration & Préparation | **Kaggle** | Dataset disponible, 30h GPU/semaine |
| Training ML | **Local** | Pas de limite de temps |
| Training DL | **Google Colab** | GPU T4 gratuit |
| Dashboard | **Local** | Interface Streamlit |

Voir [solution_hybride.md](../../../.gemini/antigravity/brain/194de74d-5294-4822-9c82-d639588be459/solution_hybride.md) pour plus de détails.

---

## 🐳 Docker

```bash
# Build l'image
docker-compose build

# Lancer le conteneur
docker-compose up

# Accéder au dashboard
# http://localhost:8501
```

---

## 📚 Documentation

- [Analyse du Projet](../../../.gemini/antigravity/brain/194de74d-5294-4822-9c82-d639588be459/analyse_projet_ids.md)
- [Plan d'Implémentation](../../../.gemini/antigravity/brain/194de74d-5294-4822-9c82-d639588be459/implementation_plan.md)
- [Solution Hybride](../../../.gemini/antigravity/brain/194de74d-5294-4822-9c82-d639588be459/solution_hybride.md)
- [Rapport Technique](reports/rapport_technique.md) *(à venir)*
- [Manuel d'Utilisation](reports/manuel_utilisation.md) *(à venir)*

---

## 🛠️ Technologies

### Core
- Python 3.10+
- Jupyter Notebook

### Data Processing
- Pandas
- NumPy
- Scikit-learn

### Machine Learning
- Scikit-learn (Random Forest, SVM, Isolation Forest)
- XGBoost

### Deep Learning
- TensorFlow/Keras
- PyTorch

### Visualization
- Matplotlib
- Seaborn
- Plotly

### Dashboard
- Streamlit

### DevOps
- Docker
- Git

---

## 📝 Roadmap

### Phase 1 : Analyse & Compréhension ✅
- [x] Analyse du projet
- [x] Plan d'implémentation
- [x] Solution hybride
- [ ] Étude des standards IDS

### Phase 2 : Dataset
- [ ] Téléchargement CICIDS2017
- [ ] Exploration des données
- [ ] Nettoyage et préparation
- [ ] Feature engineering

### Phase 3 : Modélisation
- [ ] Entraînement ML classique
- [ ] Entraînement Deep Learning
- [ ] Optimisation hyperparamètres

### Phase 4 : Évaluation
- [ ] Calcul des métriques
- [ ] Comparaison des modèles
- [ ] Sélection du meilleur modèle

### Phase 5 : Développement IDS
- [ ] Module de détection temps réel
- [ ] Dashboard Streamlit
- [ ] Système d'alertes

### Phase 6 : Documentation
- [ ] Rapport technique
- [ ] Manuel d'utilisation
- [ ] Suggestions d'évolution

---

## 👥 Auteur

**Projet Cybersécurité - ENICar**

---

## 📄 License

MIT License - voir [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- **CICIDS2017** : Canadian Institute for Cybersecurity
- **Kaggle** : Pour l'hébergement du dataset
- **Google Colab** : Pour le GPU gratuit
- **Communauté Open Source** : Pour les librairies ML/DL

---

> **Note** : Ce projet est développé dans le cadre d'un cours de Cybersécurité à l'ENICar. Il combine Machine Learning, Deep Learning et Cybersécurité pour créer une solution moderne de détection d'intrusions.
