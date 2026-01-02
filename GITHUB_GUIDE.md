# 🚀 Guide GitHub - NetGuardian-AI

## 📋 Étapes pour ajouter le projet à GitHub

### 1️⃣ Créer un dépôt sur GitHub

1. **Aller sur GitHub** : https://github.com/
2. **Se connecter** à votre compte
3. **Cliquer sur "New repository"** (bouton vert en haut à droite)
4. **Remplir les informations** :
   - **Repository name** : `NetGuardian-AI`
   - **Description** : `Système de Détection Intelligente d'Intrusions basé sur Machine Learning & Deep Learning`
   - **Visibilité** : 
     - ✅ **Public** (recommandé pour portfolio)
     - ⚠️ **Private** (si vous voulez garder le code privé)
   - **NE PAS** cocher "Add a README file" (on en a déjà un)
   - **NE PAS** cocher "Add .gitignore" (on en a déjà un)
   - **NE PAS** choisir de licence pour l'instant
5. **Cliquer sur "Create repository"**

### 2️⃣ Configuration Git Locale (Si pas déjà fait)

```bash
# Configurer votre nom (remplacer par votre nom)
git config --global user.name "Votre Nom"

# Configurer votre email (utiliser l'email de votre compte GitHub)
git config --global user.email "votre.email@example.com"
```

### 3️⃣ Initialiser et Pousser le Projet

Le dépôt Git a déjà été initialisé. Maintenant, exécutez ces commandes :

```bash
# Naviguer vers le projet
cd "y:\ENICar\cours\5th Sem\CybSec\project\NetGuardian-AI"

# Ajouter tous les fichiers
git add .

# Créer le premier commit
git commit -m "🎉 Initial commit: NetGuardian-AI - Intelligent IDS System"

# Ajouter le dépôt distant (remplacer USERNAME par votre nom d'utilisateur GitHub)
git remote add origin https://github.com/USERNAME/NetGuardian-AI.git

# Pousser vers GitHub
git push -u origin main
```

> **Note** : Si vous obtenez une erreur concernant la branche "master" au lieu de "main", utilisez :
> ```bash
> git branch -M main
> git push -u origin main
> ```

### 4️⃣ Authentification GitHub

Lors du premier push, GitHub vous demandera de vous authentifier. Vous avez deux options :

#### Option A : Personal Access Token (Recommandé)

1. **Aller sur GitHub** → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. **Generate new token** → Generate new token (classic)
3. **Donner un nom** : `NetGuardian-AI`
4. **Sélectionner les scopes** :
   - ✅ `repo` (tous les sous-scopes)
5. **Generate token**
6. **Copier le token** (vous ne pourrez plus le voir après !)
7. **Utiliser le token comme mot de passe** lors du push

#### Option B : GitHub CLI (Plus simple)

```bash
# Installer GitHub CLI
winget install --id GitHub.cli

# S'authentifier
gh auth login

# Suivre les instructions
```

### 5️⃣ Vérification

Après le push, allez sur votre dépôt GitHub :
```
https://github.com/USERNAME/NetGuardian-AI
```

Vous devriez voir tous vos fichiers !

---

## 📝 Commandes Git Utiles

### Ajouter des modifications
```bash
# Voir le statut
git status

# Ajouter tous les fichiers modifiés
git add .

# Ou ajouter un fichier spécifique
git add nom_du_fichier.py

# Commit avec message
git commit -m "Description des changements"

# Pousser vers GitHub
git push
```

### Créer une branche
```bash
# Créer et basculer vers une nouvelle branche
git checkout -b feature/nouvelle-fonctionnalite

# Pousser la branche vers GitHub
git push -u origin feature/nouvelle-fonctionnalite
```

### Mettre à jour depuis GitHub
```bash
# Récupérer les dernières modifications
git pull
```

---

## 🎨 Améliorer le README sur GitHub

Une fois le projet sur GitHub, vous pouvez améliorer le README avec des badges :

```markdown
# 🛡️ NetGuardian-AI

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-orange.svg)](https://www.tensorflow.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/USERNAME/NetGuardian-AI.svg)](https://github.com/USERNAME/NetGuardian-AI/stargazers)
```

---

## 🔒 Fichiers à NE PAS Pousser (déjà dans .gitignore)

- ❌ `data/raw/*` - Datasets (trop volumineux)
- ❌ `data/processed/*` - Données traitées
- ❌ `models/ml/*` - Modèles entraînés (.pkl)
- ❌ `models/dl/*` - Modèles Deep Learning (.h5)
- ❌ `venv/` - Environnement virtuel
- ❌ `logs/*` - Fichiers de logs
- ❌ `.env` - Variables d'environnement

Ces fichiers sont déjà exclus grâce au `.gitignore` !

---

## 📦 Utiliser Git LFS pour les Gros Fichiers (Optionnel)

Si vous voulez quand même pousser des modèles entraînés :

```bash
# Installer Git LFS
git lfs install

# Tracker les fichiers volumineux
git lfs track "*.pkl"
git lfs track "*.h5"
git lfs track "*.csv"

# Ajouter .gitattributes
git add .gitattributes

# Commit et push
git commit -m "Add Git LFS tracking"
git push
```

---

## 🌟 Créer une Belle Page GitHub

### Ajouter des Topics

Sur votre dépôt GitHub :
1. Cliquer sur ⚙️ (Settings) à côté de "About"
2. Ajouter des topics :
   - `machine-learning`
   - `deep-learning`
   - `cybersecurity`
   - `intrusion-detection`
   - `ids`
   - `python`
   - `tensorflow`
   - `streamlit`
   - `cicids2017`

### Ajouter une Description

Dans "About" :
```
Système de Détection Intelligente d'Intrusions basé sur ML/DL pour identifier les cyberattaques dans le trafic réseau
```

### Ajouter un Site Web

Si vous déployez le dashboard :
```
https://votre-dashboard-url.com
```

---

## 🔄 Workflow Recommandé

### Pour chaque nouvelle fonctionnalité :

```bash
# 1. Créer une branche
git checkout -b feature/nom-fonctionnalite

# 2. Faire vos modifications
# ... coder ...

# 3. Ajouter et commiter
git add .
git commit -m "✨ Add: description de la fonctionnalité"

# 4. Pousser la branche
git push -u origin feature/nom-fonctionnalite

# 5. Créer une Pull Request sur GitHub

# 6. Merger et supprimer la branche
git checkout main
git pull
git branch -d feature/nom-fonctionnalite
```

---

## 📊 Conventions de Commit

Utilisez des préfixes pour clarifier vos commits :

- `🎉 Initial commit:` - Premier commit
- `✨ Add:` - Nouvelle fonctionnalité
- `🐛 Fix:` - Correction de bug
- `📝 Docs:` - Documentation
- `🎨 Style:` - Formatage, style
- `♻️ Refactor:` - Refactoring de code
- `⚡ Perf:` - Amélioration de performance
- `✅ Test:` - Ajout de tests
- `🔧 Config:` - Fichiers de configuration
- `🚀 Deploy:` - Déploiement

Exemples :
```bash
git commit -m "✨ Add: Random Forest model implementation"
git commit -m "🐛 Fix: Data preprocessing bug with missing values"
git commit -m "📝 Docs: Update README with installation instructions"
```

---

## 🎯 Checklist GitHub

- [ ] Dépôt créé sur GitHub
- [ ] Git configuré localement (nom et email)
- [ ] Projet initialisé avec `git init`
- [ ] Fichiers ajoutés avec `git add .`
- [ ] Premier commit créé
- [ ] Remote ajouté (`git remote add origin ...`)
- [ ] Projet poussé sur GitHub (`git push -u origin main`)
- [ ] README visible sur GitHub
- [ ] Topics ajoutés
- [ ] Description ajoutée
- [ ] .gitignore fonctionne correctement

---

## 🆘 Problèmes Courants

### Erreur : "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/USERNAME/NetGuardian-AI.git
```

### Erreur : "failed to push some refs"
```bash
git pull origin main --rebase
git push -u origin main
```

### Erreur : "Permission denied"
- Vérifier votre Personal Access Token
- Ou utiliser GitHub CLI : `gh auth login`

---

**Prêt à pousser votre projet sur GitHub ! 🚀**
