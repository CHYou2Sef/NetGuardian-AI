# 🛡️ NetGuardian-AI Dashboard - Guide Utilisateur

## 📋 Table des Matières

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Démarrage Rapide](#démarrage-rapide)
4. [Interface du Dashboard](#interface-du-dashboard)
5. [Interprétation des Résultats](#interprétation-des-résultats)
6. [Troubleshooting](#troubleshooting)

---

## Introduction

Le dashboard NetGuardian-AI est une interface web interactive pour visualiser la détection d'intrusions réseau en temps réel. Il utilise le système hybride CNN-LSTM pour classifier le trafic réseau et identifier les attaques.

### Fonctionnalités Principales

- 📊 **Métriques en temps réel** : Statistiques de détection actualisées
- 🔍 **Flux de détections** : Tableau des dernières alertes
- 📈 **Visualisations** : Graphiques interactifs (timeline, distribution)
- ⚙️ **Contrôles de simulation** : Ajuster la vitesse et le ratio d'attaques
- 💾 **Export de données** : Sauvegarder les logs en CSV/JSON

---

## Installation

### Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- Docker (optionnel, pour déploiement containerisé)

### Option 1: Installation Locale

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-user/NetGuardian-AI.git
cd NetGuardian-AI

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer les répertoires nécessaires
mkdir -p logs models data
```

### Option 2: Installation avec Docker

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-user/NetGuardian-AI.git
cd NetGuardian-AI

# 2. Construire et lancer avec Docker Compose
docker-compose up --build
```

---

## Démarrage Rapide

### Lancer le Dashboard (Local)

```bash
# Depuis le répertoire racine du projet
streamlit run app/dashboard.py
```

Le dashboard sera accessible à: **http://localhost:8501**

### Lancer le Dashboard (Docker)

```bash
docker-compose up
```

Le dashboard sera accessible à: **http://localhost:8501**

### Démonstration en Ligne de Commande

Pour une démo rapide sans interface graphique:

```bash
# Simulation de 60 secondes avec 20% d'attaques
python scripts/run_realtime_demo.py --duration 60 --attack-rate 0.2

# Simulation de 5 minutes avec 30% d'attaques, 20 paquets/s
python scripts/run_realtime_demo.py --duration 300 --attack-rate 0.3 --packets-per-second 20
```

---

## Interface du Dashboard

### 1. En-tête et Métriques Principales

![Metrics](../docs/images/dashboard_metrics.png)

Quatre métriques clés sont affichées en haut:

- **📊 Total Traité** : Nombre total de paquets analysés
- **🚨 Attaques Détectées** : Nombre d'attaques identifiées
- **✅ Trafic Normal** : Nombre de paquets normaux
- **⏱️ Temps d'Exécution** : Durée de la session + vitesse de détection

### 2. Contrôles de Simulation (Sidebar)

**Bouton Démarrer/Arrêter**
- ▶️ **Démarrer** : Lance la simulation de trafic
- ⏸️ **Arrêter** : Met en pause la simulation

**Paramètres**
- **Paquets/seconde** (1-50) : Contrôle la vitesse de simulation
- **Ratio d'attaques** (0.0-1.0) : Proportion d'attaques dans le trafic généré

**Bouton Réinitialiser**
- 🔄 Efface toutes les statistiques et l'historique

### 3. Timeline des Détections

Graphique en ligne montrant l'évolution des détections au fil du temps:
- **Ligne verte** : Trafic normal
- **Ligne rouge** : Attaques détectées

### 4. Graphiques de Distribution

**Distribution des Attaques (Camembert)**
- Montre la répartition des différents types d'attaques détectées

**Trafic Normal vs Attaques (Barres)**
- Comparaison visuelle entre trafic légitime et malveillant

### 5. Flux de Détections Récentes

Tableau des 20 dernières détections avec:
- **Heure** : Timestamp de la détection
- **Icône** : Indicateur visuel de sévérité
  - 🚨 Critical
  - ⚠️ High
  - ⚡ Medium
  - ℹ️ Low
- **Type** : Type d'attaque ou "Normal Traffic"
- **Confiance** : Score de confiance du modèle (0-1)
- **Sévérité** : Niveau de gravité

---

## Interprétation des Résultats

### Types d'Attaques Détectées

| Type | Description | Sévérité Typique |
|------|-------------|------------------|
| **DoS/DDoS** | Déni de service, inondation de requêtes | 🚨 Critical |
| **Web_Attack** | Injections SQL, XSS, etc. | ⚠️ High |
| **Brute_Force** | Tentatives de connexion répétées | ⚠️ High |
| **Port_Scanning** | Reconnaissance, scan de ports | ⚡ Medium |
| **Botnet** | Activité de réseau de bots | ⚡ Medium |
| **Reconnaissance** | Collecte d'informations | ⚡ Medium |

### Scores de Confiance

- **> 0.9** : Très haute confiance, action immédiate recommandée
- **0.7 - 0.9** : Haute confiance, investigation recommandée
- **0.5 - 0.7** : Confiance moyenne, surveillance accrue
- **< 0.5** : Faible confiance, possible faux positif

### Niveaux de Sévérité

- **🚨 Critical** : Menace immédiate, action urgente requise
- **⚠️ High** : Menace sérieuse, investigation prioritaire
- **⚡ Medium** : Activité suspecte, surveillance recommandée
- **ℹ️ Low** : Anomalie mineure, à noter

---

## Troubleshooting

### Le dashboard ne démarre pas

**Problème** : Erreur lors du lancement de Streamlit

**Solutions** :
```bash
# Vérifier que Streamlit est installé
pip install streamlit

# Vérifier la version de Python
python --version  # Doit être >= 3.10

# Réinstaller les dépendances
pip install -r requirements.txt --force-reinstall
```

### Aucune détection n'apparaît

**Problème** : Le tableau de détections reste vide

**Solutions** :
1. Cliquez sur le bouton **▶️ Démarrer** dans la sidebar
2. Vérifiez que le simulateur est bien initialisé (message de succès au démarrage)
3. Augmentez la vitesse de simulation (paquets/seconde)

### Erreur "Modèles non chargés"

**Problème** : Message d'erreur concernant les modèles

**Solutions** :

**Mode Mock (Développement)** :
- Le système utilise automatiquement des modèles mock si les vrais modèles ne sont pas disponibles
- Vérifiez le message "Mode Mock" au démarrage

**Mode Production (Modèles réels)** :
1. Entraînez les modèles avec les notebooks Colab
2. Téléchargez les fichiers `.pkl` générés
3. Placez-les dans le dossier `models/`:
   ```
   models/
   ├── hybrid_ids_system.pkl
   ├── scaler.pkl
   └── label_encoder.pkl
   ```
4. Modifiez `config/config.yaml` : `use_mock_models: false`

### Le dashboard est lent

**Problème** : Interface qui lag ou se rafraîchit lentement

**Solutions** :
1. Réduire le nombre de paquets/seconde
2. Limiter l'historique dans `config/config.yaml`:
   ```yaml
   detection:
     max_history_size: 500  # Au lieu de 1000
   ```
3. Fermer les autres applications gourmandes en ressources

### Erreur Docker

**Problème** : `docker-compose up` échoue

**Solutions** :
```bash
# Nettoyer les conteneurs existants
docker-compose down

# Reconstruire l'image
docker-compose build --no-cache

# Relancer
docker-compose up
```

### Port 8501 déjà utilisé

**Problème** : "Address already in use"

**Solutions** :
```bash
# Option 1: Arrêter l'autre processus
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8501 | xargs kill -9

# Option 2: Changer le port
streamlit run app/dashboard.py --server.port=8502
```

---

## Support et Contribution

### Obtenir de l'Aide

- 📖 Documentation complète : [PROJECT_DOCUMENTATION_MASTER.md](../PROJECT_DOCUMENTATION_MASTER.md)
- 🐛 Signaler un bug : Créer une issue sur GitHub
- 💬 Questions : Ouvrir une discussion sur GitHub

### Logs et Débogage

Les logs sont enregistrés dans `logs/`:
- `logs/netguardian.log` : Logs système
- `logs/alerts_*.csv` : Exports d'alertes
- `logs/alerts_*.json` : Exports JSON

Pour activer le mode debug:
```yaml
# config/config.yaml
logging:
  level: "DEBUG"
```

---

## Prochaines Étapes

Une fois le dashboard maîtrisé:

1. **Entraîner les vrais modèles** : Utilisez les notebooks Colab pour entraîner sur CICIDS2017
2. **Intégrer du vrai trafic** : Modifier le simulateur pour capturer du trafic réel avec Scapy
3. **Déployer en production** : Utiliser Docker pour un déploiement robuste
4. **Personnaliser les alertes** : Configurer des notifications (email, Slack, etc.)

---

**Bon monitoring! 🛡️**
