"""
Utilitaires pour le preprocessing du dataset CICIDS2017
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os


# Mapping des labels vers catégories d'attaques
# Pour dataset pré-nettoyé (7 catégories)
ATTACK_CATEGORIES_PRECLEANED = {
    'Normal Traffic': 'Normal',
    'Port Scanning': 'Reconnaissance',
    'Web Attacks': 'Web_Attack',
    'Brute Force': 'Brute_Force',
    'DDoS': 'DoS_DDoS',
    'Bots': 'Botnet',
    'DoS': 'DoS_DDoS'
}

# Mapping pour dataset original (15 classes)
ATTACK_CATEGORIES_ORIGINAL = {
    'BENIGN': 'Normal',
    'FTP-Patator': 'Brute_Force',
    'SSH-Patator': 'Brute_Force',
    'Web Attack – Brute Force': 'Brute_Force',
    'DoS slowloris': 'DoS_DDoS',
    'DoS Slowhttptest': 'DoS_DDoS',
    'DoS Hulk': 'DoS_DDoS',
    'DoS GoldenEye': 'DoS_DDoS',
    'DDoS': 'DoS_DDoS',
    'Web Attack – XSS': 'Web_Attack',
    'Web Attack – SQL Injection': 'Web_Attack',
    'PortScan': 'Reconnaissance',
    'Bot': 'Botnet',
    'Infiltration': 'Advanced_Threat',
    'Heartbleed': 'Advanced_Threat'
}

# Par défaut, utiliser le mapping pré-nettoyé
ATTACK_CATEGORIES = ATTACK_CATEGORIES_PRECLEANED


def clean_cicids2017(df, verbose=True):
    """
    Nettoie le dataset CICIDS2017
    
    Args:
        df (pd.DataFrame): DataFrame à nettoyer
        verbose (bool): Afficher les messages de progression
    
    Returns:
        pd.DataFrame: DataFrame nettoyé
    """
    if verbose:
        print("🧹 Nettoyage en cours...")
        print(f"Shape initiale: {df.shape}")
        print(f"Colonnes: {len(df.columns)}")
    
    # 1. Nettoyer les noms de colonnes (enlever espaces au début/fin)
    df.columns = df.columns.str.strip()
    if verbose:
        print("✅ Noms de colonnes nettoyés")
    
    # 2. Supprimer les duplications
    initial_rows = len(df)
    df = df.drop_duplicates()
    duplicates_removed = initial_rows - len(df)
    if verbose:
        print(f"✅ Duplications supprimées: {duplicates_removed}")
    
    # 3. Gérer les valeurs infinies
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    if verbose:
        print("✅ Valeurs infinies remplacées par NaN")
    
    # 4. Gérer les NaN
    nan_before = df.isnull().sum().sum()
    
    # Remplir avec la médiane pour les colonnes numériques (sauf Attack Type)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col].fillna(df[col].median(), inplace=True)
    
    nan_after = df.isnull().sum().sum()
    if verbose:
        print(f"✅ NaN traités: {nan_before} → {nan_after}")
    
    # 5. Corriger les valeurs négatives incorrectes
    positive_cols = ['Flow Duration', 'Total Fwd Packets', 'Total Length of Fwd Packets']
    for col in positive_cols:
        if col in df.columns:
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                df.loc[df[col] < 0, col] = 0
                if verbose:
                    print(f"✅ {col}: {negative_count} valeurs négatives corrigées")
    
    if verbose:
        print(f"\n🎉 Nettoyage terminé!")
        print(f"Shape finale: {df.shape}")
    
    return df


def create_binary_labels(df, label_col='Attack Type', normal_label='Normal Traffic'):
    """
    Crée des labels binaires : 0 = Normal, 1 = Attaque
    
    Args:
        df (pd.DataFrame): DataFrame contenant les labels
        label_col (str): Nom de la colonne des labels
        normal_label (str): Label représentant le trafic normal
    
    Returns:
        pd.DataFrame: DataFrame avec colonne 'Binary_Label' ajoutée
    """
    df['Binary_Label'] = (df[label_col] != normal_label).astype(int)
    
    print(f"Distribution binaire:")
    print(f"  0 (Normal): {(df['Binary_Label'] == 0).sum():,}")
    print(f"  1 (Attaque): {(df['Binary_Label'] == 1).sum():,}")
    
    return df


def map_labels(df, label_col='Attack Type', mapping=ATTACK_CATEGORIES):
    """
    Mappe les labels originaux vers des catégories d'attaques
    
    Args:
        df (pd.DataFrame): DataFrame contenant les labels
        label_col (str): Nom de la colonne des labels
        mapping (dict): Dictionnaire de mapping
    
    Returns:
        pd.DataFrame: DataFrame avec colonne 'Attack_Category' ajoutée
    """
    df['Attack_Category'] = df[label_col].map(mapping)
    
    # Vérifier s'il y a des labels non mappés
    unmapped = df['Attack_Category'].isnull().sum()
    if unmapped > 0:
        print(f"⚠️ Attention: {unmapped} labels non mappés")
        print("Labels non mappés:")
        print(df[df['Attack_Category'].isnull()][label_col].unique())
    
    return df


def encode_labels(df, category_col='Attack_Category', save_path=None):
    """
    Encode les catégories d'attaques en valeurs numériques
    
    Args:
        df (pd.DataFrame): DataFrame avec les catégories
        category_col (str): Nom de la colonne des catégories
        save_path (str): Chemin pour sauvegarder l'encodeur (optionnel)
    
    Returns:
        tuple: (DataFrame avec 'Label_Encoded', LabelEncoder)
    """
    le = LabelEncoder()
    df['Label_Encoded'] = le.fit_transform(df[category_col])
    
    # Afficher le mapping
    print("Mapping numérique:")
    for i, label in enumerate(le.classes_):
        count = (df['Label_Encoded'] == i).sum()
        print(f"{i}: {label} ({count} instances)")
    
    # Sauvegarder l'encodeur si demandé
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        joblib.dump(le, save_path)
        print(f"\n✅ Encodeur sauvegardé: {save_path}")
    
    return df, le


def prepare_features(df, label_cols=['Attack Type', 'Attack_Category', 'Label_Encoded'], 
                     scale=True, scaler_path=None):
    """
    Prépare les features pour l'entraînement
    
    Args:
        df (pd.DataFrame): DataFrame nettoyé
        label_cols (list): Colonnes de labels à exclure des features
        scale (bool): Normaliser les features
        scaler_path (str): Chemin pour sauvegarder le scaler (optionnel)
    
    Returns:
        tuple: (X, y, scaler ou None)
    """
    # Séparer features et labels
    feature_cols = [col for col in df.columns if col not in label_cols]
    X = df[feature_cols]
    y = df['Label_Encoded']
    
    print(f"Features shape: {X.shape}")
    print(f"Labels shape: {y.shape}")
    
    # Normaliser si demandé
    scaler = None
    if scale:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        X = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
        print("✅ Features normalisées")
        
        # Sauvegarder le scaler si demandé
        if scaler_path:
            os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
            joblib.dump(scaler, scaler_path)
            print(f"✅ Scaler sauvegardé: {scaler_path}")
    
    return X, y, scaler


def load_and_preprocess(file_path, clean=True, map_labels_flag=True, 
                        encode=True, prepare=True, verbose=True):
    """
    Pipeline complet de preprocessing
    
    Args:
        file_path (str): Chemin vers le fichier CSV
        clean (bool): Nettoyer le dataset
        map_labels_flag (bool): Mapper les labels
        encode (bool): Encoder les labels
        prepare (bool): Préparer les features
        verbose (bool): Afficher les messages
    
    Returns:
        dict: Dictionnaire contenant df, X, y, le, scaler
    """
    # Charger
    if verbose:
        print(f"📂 Chargement de: {file_path}")
    df = pd.read_csv(file_path)
    
    if verbose:
        print(f"Shape initiale: {df.shape}")
    
    # Nettoyer
    if clean:
        df = clean_cicids2017(df, verbose=verbose)
    
    # Mapper les labels
    if map_labels_flag:
        df = map_labels(df)
    
    # Encoder
    le = None
    if encode:
        df, le = encode_labels(df)
    
    # Préparer les features
    X, y, scaler = None, None, None
    if prepare:
        X, y, scaler = prepare_features(df)
    
    return {
        'df': df,
        'X': X,
        'y': y,
        'label_encoder': le,
        'scaler': scaler
    }


def verify_dataset(df):
    """
    Vérifie la qualité du dataset nettoyé
    
    Args:
        df (pd.DataFrame): DataFrame à vérifier
    """
    print("=" * 60)
    print("VÉRIFICATION DU DATASET")
    print("=" * 60)
    
    print(f"\n1. Shape: {df.shape}")
    
    print(f"\n2. Valeurs manquantes:")
    nan_count = df.isnull().sum().sum()
    print(f"   Total NaN: {nan_count}")
    if nan_count > 0:
        print("   ⚠️ Des valeurs NaN sont présentes!")
    else:
        print("   ✅ Aucune valeur NaN")
    
    print(f"\n3. Valeurs infinies:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    inf_count = np.isinf(df[numeric_cols]).sum().sum()
    print(f"   Total infinis: {inf_count}")
    if inf_count > 0:
        print("   ⚠️ Des valeurs infinies sont présentes!")
    else:
        print("   ✅ Aucune valeur infinie")
    
    print(f"\n4. Duplications:")
    dup_count = df.duplicated().sum()
    print(f"   Total duplications: {dup_count}")
    if dup_count > 0:
        print("   ⚠️ Des duplications sont présentes!")
    else:
        print("   ✅ Aucune duplication")
    
    if 'Attack_Category' in df.columns:
        print(f"\n5. Distribution des catégories:")
        print(df['Attack_Category'].value_counts())
    
    print("\n" + "=" * 60)
    
    # Score de qualité
    issues = (nan_count > 0) + (inf_count > 0) + (dup_count > 0)
    if issues == 0:
        print("✅ Dataset de haute qualité - Prêt pour l'entraînement!")
    elif issues == 1:
        print("⚠️ Dataset acceptable - Quelques problèmes mineurs")
    else:
        print("❌ Dataset problématique - Nettoyage supplémentaire requis")
    
    print("=" * 60)


if __name__ == "__main__":
    # Exemple d'utilisation
    print("Module de preprocessing CICIDS2017")
    print("Importez ce module dans vos notebooks:")
    print("  from src.preprocessing import clean_cicids2017, map_labels, encode_labels")
