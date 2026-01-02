# 🚀 Quick Start Guide - NetGuardian-AI

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir :
- ✅ Python 3.10 ou supérieur installé
- ✅ pip (gestionnaire de paquets Python)
- ✅ Git (optionnel, pour le versioning)
- ✅ Compte Kaggle (pour accéder au dataset CICIDS2017)
- ✅ Compte Google (pour utiliser Colab avec GPU)

---

## ⚡ Installation Rapide

### 1. Naviguer vers le projet
```bash
cd "y:\ENICar\cours\5th Sem\CybSec\project\NetGuardian-AI"
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
```

### 3. Activer l'environnement
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Installer les dépendances
```bash
pip install -r requirements.txt
```

---

## 📊 Obtenir le Dataset

### Option 1 : Kaggle (Recommandé)

1. **Créer un compte Kaggle** : https://www.kaggle.com/
2. **Accéder au dataset** : https://www.kaggle.com/datasets/cicdataset/cicids2017
3. **Télécharger** ou **utiliser directement dans un notebook Kaggle**

### Option 2 : Source Officielle

1. Visiter : https://www.unb.ca/cic/datasets/ids-2017.html
2. Télécharger les fichiers CSV
3. Placer dans `data/raw/`

---

## 🎯 Workflow Recommandé

### Phase 1 : Exploration (Kaggle)

1. **Créer un notebook Kaggle**
   - Aller sur https://www.kaggle.com/code
   - Nouveau notebook → Ajouter dataset CICIDS2017
   - Activer GPU : Settings → Accelerator → GPU

2. **Explorer les données**
   ```python
   import pandas as pd
   
   # Charger le dataset
   df = pd.read_csv('/kaggle/input/cicids2017/...')
   
   # Explorer
   print(df.head())
   print(df.info())
   print(df['Label'].value_counts())
   ```

3. **Sauvegarder les insights**
   - Créer des visualisations
   - Noter les observations

### Phase 2 : Préparation (Kaggle → Local)

1. **Nettoyer les données sur Kaggle**
   ```python
   # Supprimer les duplications
   df = df.drop_duplicates()
   
   # Gérer les valeurs manquantes
   df = df.dropna()
   
   # Sauvegarder
   df.to_csv('cicids2017_cleaned.csv', index=False)
   ```

2. **Télécharger le dataset nettoyé**
   - Cliquer sur "Output" dans Kaggle
   - Télécharger `cicids2017_cleaned.csv`
   - Placer dans `data/processed/`

3. **Uploader sur Google Drive** (pour Colab)
   - Créer dossier `NetGuardian-AI/data/processed/`
   - Uploader le CSV nettoyé

### Phase 3 : Training ML (Local)

1. **Lancer Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

2. **Créer un notebook** : `notebooks/local/03_ml_training.ipynb`

3. **Entraîner les modèles**
   ```python
   from sklearn.ensemble import RandomForestClassifier
   import joblib
   
   # Charger les données
   df = pd.read_csv('data/processed/cicids2017_cleaned.csv')
   
   # Préparer X et y
   X = df.drop('Label', axis=1)
   y = df['Label']
   
   # Entraîner Random Forest
   rf = RandomForestClassifier(n_estimators=100)
   rf.fit(X_train, y_train)
   
   # Sauvegarder
   joblib.dump(rf, 'models/ml/random_forest.pkl')
   ```

### Phase 4 : Training DL (Colab)

1. **Ouvrir Google Colab** : https://colab.research.google.com/

2. **Créer un nouveau notebook** : `NetGuardian_DL_Training.ipynb`

3. **Monter Google Drive**
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

4. **Vérifier GPU**
   ```python
   import tensorflow as tf
   print("GPU Available:", tf.config.list_physical_devices('GPU'))
   ```

5. **Entraîner LSTM/Autoencoder**
   ```python
   # Charger données depuis Drive
   df = pd.read_csv('/content/drive/MyDrive/NetGuardian-AI/data/processed/cicids2017_cleaned.csv')
   
   # Construire modèle LSTM
   from tensorflow.keras.models import Sequential
   from tensorflow.keras.layers import LSTM, Dense
   
   model = Sequential([
       LSTM(64, input_shape=(sequence_length, n_features)),
       Dense(32, activation='relu'),
       Dense(n_classes, activation='softmax')
   ])
   
   model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
   model.fit(X_train, y_train, epochs=50, batch_size=256)
   
   # Sauvegarder sur Drive
   model.save('/content/drive/MyDrive/NetGuardian-AI/models/dl/lstm_model.h5')
   ```

6. **Télécharger le modèle en local**
   - Depuis Google Drive
   - Placer dans `models/dl/`

### Phase 5 : Évaluation (Local)

1. **Créer notebook** : `notebooks/local/04_evaluation.ipynb`

2. **Charger tous les modèles**
   ```python
   import joblib
   from tensorflow.keras.models import load_model
   
   # ML models
   rf = joblib.load('models/ml/random_forest.pkl')
   xgb = joblib.load('models/ml/xgboost.pkl')
   
   # DL models
   lstm = load_model('models/dl/lstm_model.h5')
   ```

3. **Comparer les performances**
   ```python
   from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
   
   models = {'RF': rf, 'XGB': xgb, 'LSTM': lstm}
   results = {}
   
   for name, model in models.items():
       y_pred = model.predict(X_test)
       results[name] = {
           'accuracy': accuracy_score(y_test, y_pred),
           'precision': precision_score(y_test, y_pred, average='weighted'),
           'recall': recall_score(y_test, y_pred, average='weighted'),
           'f1': f1_score(y_test, y_pred, average='weighted')
       }
   
   print(pd.DataFrame(results).T)
   ```

### Phase 6 : Dashboard (Local)

1. **Lancer le dashboard**
   ```bash
   streamlit run app/dashboard.py
   ```

2. **Ouvrir le navigateur**
   - URL : http://localhost:8501

3. **Tester la détection**
   - Uploader un échantillon de données
   - Voir les prédictions en temps réel

---

## 🐳 Déploiement Docker (Optionnel)

### Build et Run
```bash
# Build l'image
docker-compose build

# Lancer le conteneur
docker-compose up

# Accéder au dashboard
# http://localhost:8501
```

### Arrêter
```bash
docker-compose down
```

---

## 📝 Checklist de Démarrage

### Setup Initial
- [ ] Python 3.10+ installé
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Compte Kaggle créé
- [ ] Compte Google créé

### Dataset
- [ ] Dataset CICIDS2017 téléchargé
- [ ] Dataset exploré sur Kaggle
- [ ] Dataset nettoyé
- [ ] Dataset uploadé sur Google Drive

### Training
- [ ] Modèles ML entraînés en local
- [ ] Modèles DL entraînés sur Colab
- [ ] Modèles sauvegardés

### Évaluation
- [ ] Métriques calculées
- [ ] Modèles comparés
- [ ] Meilleur modèle sélectionné

### Dashboard
- [ ] Dashboard lancé
- [ ] Détection testée
- [ ] Alertes vérifiées

---

## 🆘 Troubleshooting

### Problème : Erreur d'installation de dépendances
**Solution** :
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Problème : Dataset trop volumineux
**Solution** : Utiliser un échantillon
```python
df_sample = df.sample(frac=0.1, random_state=42)  # 10% du dataset
```

### Problème : Manque de mémoire
**Solution** : Charger par chunks
```python
chunks = pd.read_csv('data.csv', chunksize=10000)
for chunk in chunks:
    process(chunk)
```

### Problème : Colab se déconnecte
**Solution** : Utiliser le script keep-alive
```javascript
// Dans la console du navigateur (F12)
function ClickConnect(){
    console.log("Keeping alive...");
    document.querySelector("colab-toolbar-button#connect").click()
}
setInterval(ClickConnect, 60000)
```

---

## 📚 Ressources Utiles

- **Documentation Scikit-learn** : https://scikit-learn.org/
- **Documentation TensorFlow** : https://www.tensorflow.org/
- **Documentation Streamlit** : https://docs.streamlit.io/
- **CICIDS2017 Paper** : https://www.unb.ca/cic/datasets/ids-2017.html
- **MITRE ATT&CK** : https://attack.mitre.org/

---

## 🎯 Prochaines Étapes

1. ✅ Setup terminé
2. ⏳ Explorer le dataset sur Kaggle
3. ⏳ Nettoyer et préparer les données
4. ⏳ Entraîner les modèles
5. ⏳ Évaluer et comparer
6. ⏳ Déployer le dashboard

---

**Bon courage ! 🚀**
