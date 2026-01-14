# 📘 NetGuardian-AI : Le Manuel Complet
> **"La Cybersécurité expliquée simplement, du hacking à l'intelligence artificielle."**

---

# 📑 Table des Matières

1.  **[Introduction : La Mission](#1-introduction--la-mission-netguardian)**
    *   C'est quoi un IDS ?
    *   L'histoire du Gendarme et du Voleur
    *   Pourquoi l'IA change tout
2.  **[Le Terrain de Jeu : Comprendre les Attaques](#2-le-terrain-de-jeu--comprendre-les-attaques)**
    *   Le Framework MITRE ATT&CK
    *   Les 7 Méchants (Types d'attaques du projet)
3.  **[Les Indices : Le Dataset CICIDS2017](#3-les-indices--le-dataset-cicids2017)**
    *   À quoi ressemble du trafic réseau ?
    *   Les Features (Indices) importantes
4.  **[Le Cerveau : L'Approche Hybride](#4-le-cerveau--lapproche-hybride-notre-stratégie)**
    *   Pourquoi deux cerveaux valent mieux qu'un ?
    *   Technique : XGBoost & SMOTE expliqués
5.  **[L'Usine : De la Donnée Brute au Modèle](#5-lusine--de-la-donnée-brute-au-modèle)**
    *   Nettoyage, Encodage, Scaling (La recette de cuisine)
    *   Le Pipeline de code
6.  **[Le Test Final : Sommes-nous prêts ?](#6-le-test-final--sommes-nous-prêts-)**
    *   Les résultats (Accuracy, Matrice de Confusion)
    *   Le test de résistance (Bruit)
7.  **[Mise en Pratique : Installation & Codes](#7-mise-en-pratique--installation--codes)**

---

# 1. Introduction : La Mission NetGuardian

Imaginez que vous êtes le chef de la sécurité d'un immense centre commercial (le réseau d'une entreprise). Des milliers de personnes entrent et sortent chaque jour. La plupart sont des clients honnêtes (**Trafic Normal**), mais certains sont des voleurs ou des vandales (**Attaquants**).

Votre mission ? Repérer les méchants *avant* qu'ils ne cassent quelque chose.

### C'est quoi un IDS ?
Un **IDS** (*Intrusion Detection System*) est comme une caméra de surveillance intelligente.
*   **L'ancienne méthode (Signatures)** : Le gardien a une photo des criminels connus. Si quelqu'un ressemble à la photo 📸, on l'arrête. *Problème : Si le voleur met une moustache (nouvelle attaque), il passe.*
*   **Notre méthode (Anomalie / IA)** : Le gardien observe le comportement. "Tiens, ce client court très vite et essaie d'ouvrir toutes les portes du couloir". C'est suspect ! L'IA apprend ce qui est "normal" pour repérer ce qui est "anormal".

### 🎯 Objectifs Spécifiques du Projet
1.  **Construire un modèle hybride** : Combiner apprentissage supervisé et règles pour une détection optimale.
2.  **Explorer le Non-Supervisé** : Utiliser des techniques pour détecter les anomalies inconnues.
3.  **Comparer les Modèles** : Nous ne nous arrêtons pas à une seule solution. Le projet vise à benchmarker :
    *   **Classiques** : SVM, Random Forest, KNN.
    *   **Deep Learning** : Réseaux de neurones (MLP), Autoencoders.
    *   **Ensemble** : XGBoost (Notre champion actuel).

### Pourquoi l'IA ?
Les pirates inventent de nouvelles attaques tous les jours. Un humain ne peut pas surveiller 1 million de connexions par seconde. L'Intelligence Artificielle (**Machine Learning**), elle, le peut. Elle ne dort jamais et repère des détails invisibles à l'œil nu.

---

# 2. Le Terrain de Jeu : Comprendre les Attaques

Pour attraper un pirate, il faut penser comme un pirate. Nous utilisons le **MITRE ATT&CK**, qui est l'encyclopédie mondiale des techniques de hackers.

### Les 7 Familles de Méchants que nous détectons :

1.  **DoS / DDoS (Déni de Service)** 🚧
    *   *L'analogie* : Une foule de robots bloque l'entrée du magasin pour empêcher les vrais clients d'entrer.
    *   *Technique* : Inonder le serveur de fausses demandes.
2.  **Port Scanning (Reconnaissance)** 🔭
    *   *L'analogie* : Un voleur qui vérifie chaque fenêtre de la maison pour voir laquelle est ouverte.
    *   *Technique* : Tester tous les ports de connexion d'un serveur.
3.  **Web Attacks (Injections, XSS)** 🕸️
    *   *L'analogie* : Essayer de tromper le vendeur en lui donnant un faux billet ou une commande piégée.
    *   *Technique* : Entrer du code malveillant dans un formulaire web.
4.  **Brute Force** 🔑
    *   *L'analogie* : Essayer toutes les clés possibles sur une serrure jusqu'à ce qu'elle s'ouvre.
    *   *Technique* : Tester des milliers de mots de passe par seconde.
5.  **Botnet** 🤖
    *   *L'analogie* : Des ordinateurs zombies contrôlés à distance par le grand méchant.
6.  **Infiltration** 🕵️
    *   *L'analogie* : Le voleur est déjà à l'intérieur et essaie de se déplacer vers le coffre-fort.

---

# 3. Les Indices : Le Dataset CICIDS2017

Pour entraîner notre IA, nous avons besoin d'exemples. Nous utilisons le dataset **CICIDS2017**. C'est un immense fichier Excel (CSV) de **2.5 millions de lignes**.

Chaque ligne est une "connexion" réseau.
Chaque colonne est un "indice" (**Feature**).

### Les Indices Clés (Top Features)
Si vous étiez le détective, vous regarderiez quoi ?

1.  **`Flow Duration`** (Durée) : Une connexion normale pour charger une page web est courte. Une attaque DoS peut durer très longtemps ou être très brève et répétitive.
2.  **`Total Fwd Packets`** (Nombre de paquets envoyés) : Quelqu'un qui envoie 10 000 demandes sans jamais rien recevoir en retour ? Suspect (Probablement un Scan ou DoS).
3.  **`Flow Bytes/s`** (Vitesse) : Un téléchargement va vite. Une attaque "Low and Slow" va très lentement pour ne pas se faire voir.
4.  **`Initial Window Bytes`** : La taille de la "fenêtre" TCP. C'est comme la poignée de main au début de la conversation. Les outils de piratage ont souvent des poignées de main bizarres.

> **Le Défi** : Le dataset est "Déséquilibré". Il y a 80% de trafic normal et seulement 0.1% d'attaques Web. C'est comme chercher une aiguille dans une botte de foin.

---

# 4. Le Cerveau : L'Approche Hybride (Notre Stratégie)

C'est ici que réside le génie de NetGuardian-AI. Au lieu d'utiliser un seul cerveau, on en utilise deux en équipe.

### L'Architecture "Cascade"

Imaginez un aéroport avec deux contrôles de sécurité :

1.  **Le Gardien Rapide (Modèle 1 - Binaire)** 🛡️
    *   *Sa mission* : Trier "Normal" vs "Suspect".
    *   *Son outil* : **XGBoost** (Binary Classifier).
    *   *Pourquoi ?* Il doit être hyper rapide car il voit tout le trafic. S'il dit "Normal", ça passe. S'il dit "Suspect", il envoie au spécialiste.

2.  **L'Expert (Modèle 2 - Multi-classes)** 🕵️‍♂️
    *   *Sa mission* : Dire exactement "C'est une attaque DDoS Hulk !".
    *   *Son outil* : **XGBoost + SMOTE**.
    *   *Pourquoi ?* Il ne regarde que les alertes. Il a plus de temps pour analyser. On l'a entraîné avec **SMOTE** (une technique qui "clone" artificiellement les exemples rares comme les Web Attacks pour qu'il apprenne à les reconnaître).

---

# 5. L'Usine : De la Donnée Brute au Modèle

Comment on fabrique ça concrètement ? Voici la recette (toute codée en Python).

### Étape 1 : Le Nettoyage (`02_data_preparation.ipynb`)
Comme des légumes sales, les données brutes ne sont pas prêtes à cuire.
*   Enlever les **NaN** (trous dans les données).
*   Enlever les **Infinis** (erreurs de calcul).
*   Supprimer les doublons.

### Étape 2 : La Traduction (Encoding)
L'ordinateur ne comprend pas les mots "DoS Attack". Il ne comprend que les chiffres.
*   L'Encodage (**LabelEncoder**) transforme :
    *   `Benign` -> `0`
    *   `DDoS` -> `1`
    *   `PortScan` -> `2`

### Étape 3 : La Mise à l'Échelle (Scaling)
*   La `Durée` peut être de 10 000 000 (microsecondes).
*   Le `Nombre de paquets` peut être de 5.
L'IA va penser que la Durée est plus importante car le chiffre est plus gros. C'est faux !
*   **Solution** : Le **StandardScaler**. Il ramène tout le monde sur une même échelle (autour de 0).

---

# 6. Le Test Final : Sommes-nous prêts ?

Nous avons donné à notre IA un examen final (le **Test Set** : des données qu'elle n'a jamais vues).

### Les Résultats
*   **Précision Globale** : ~99.8% (Très haut, mais attention au déséquilibre !)
*   **Matrice de Confusion** : C'est le tableau des erreurs.
    *   *Vrai Positif* : Alerte sonnée, c'était une attaque. (Bravo !)
    *   *Faux Positif* : Alerte sonnée, c'était un client normal. (Ennuyeux, mais mieux que l'inverse).
    *   *Faux Négatif* : Pas d'alerte, c'était une attaque. (Catastrophe ! C'est ce qu'on veut éviter à tout prix).

### Le Test de Résistance (Robustness)
Dans la vraie vie, le réseau est bruité (wifi qui capte mal, latence...). Nous avons ajouté du "bruit" aléatoire aux données pour voir si l'IA panique.
*   *Résultat* : NetGuardian-AI reste stable même avec un peu de bruit, ce qui prouve qu'il a bien appris les "règles" et pas juste par cœur.

---

# 7. Mise en Pratique : Installation & Codes

Tout le code est organisé pour que vous puissiez le lancer vous-même.

### Structure des dossiers
*   `notebooks/kaggle/` :
    *   `01_analysis_and_mitre.ipynb` : Pour voir les graphiques et comprendre les données.
    *   `02_data_preparation.ipynb` : Pour préparer les données.
    *   `03_hybrid_model_training.ipynb` : Pour entraîner votre propre IA.
    *   `06_model_comparison.ipynb` : **Nouveau !** Pour comparer SVM, KNN, Autoencoder vs Random Forest.
    *   `05_realtime_simulation.ipynb` : Pour voir l'IA agir en direct !
*   `src/` : Le code "propre" caché (les engrenages).

### Comment lancer ?
1.  Installez Python et les outils : `pip install -r requirements.txt`
2.  Lancez Jupyter : `jupyter notebook`
3.  Ouvrez `05_realtime_simulation.ipynb` et faites "Run All".

---

> **Conclusion** : NetGuardian-AI n'est pas juste un programme. C'est la démonstration que l'on peut apprendre à une machine à distinguer le bien du mal dans le monde numérique complexe d'aujourd'hui. À vous de jouer ! 🛡️
