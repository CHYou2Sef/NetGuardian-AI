"""
Script pour analyser la structure du dataset CICIDS2017
Utilisez ce script pour vérifier les colonnes et la structure de votre dataset
"""

import pandas as pd
import numpy as np


def analyze_dataset_structure(file_path):
    """
    Analyse la structure du dataset CICIDS2017
    
    Args:
        file_path (str): Chemin vers le fichier CSV
    """
    print("=" * 70)
    print("ANALYSE DE LA STRUCTURE DU DATASET CICIDS2017")
    print("=" * 70)
    
    # Charger le dataset
    print(f"\n📂 Chargement de: {file_path}")
    df = pd.read_csv(file_path)
    
    # Informations générales
    print(f"\n📊 INFORMATIONS GÉNÉRALES")
    print(f"   Shape: {df.shape}")
    print(f"   Nombre de lignes: {df.shape[0]:,}")
    print(f"   Nombre de colonnes: {df.shape[1]}")
    print(f"   Taille en mémoire: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Liste des colonnes
    print(f"\n📋 LISTE DES COLONNES ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        dtype = df[col].dtype
        null_count = df[col].isnull().sum()
        print(f"   {i:2d}. '{col}' ({dtype}) - {null_count} NaN")
    
    # Identifier la colonne de labels
    print(f"\n🏷️  COLONNE DE LABELS:")
    label_candidates = [col for col in df.columns if 'label' in col.lower() or 'attack' in col.lower() or 'class' in col.lower()]
    if label_candidates:
        for col in label_candidates:
            print(f"   Trouvée: '{col}'")
            print(f"   Valeurs uniques: {df[col].nunique()}")
            print(f"   Distribution:")
            print(df[col].value_counts().to_string(max_rows=20))
    else:
        print("   ⚠️ Aucune colonne de label évidente trouvée")
    
    # Types de données
    print(f"\n📈 TYPES DE DONNÉES:")
    print(df.dtypes.value_counts())
    
    # Statistiques sur les valeurs manquantes
    print(f"\n❓ VALEURS MANQUANTES:")
    nan_counts = df.isnull().sum()
    if nan_counts.sum() > 0:
        print(f"   Total NaN: {nan_counts.sum():,}")
        print(f"   Colonnes avec NaN:")
        for col, count in nan_counts[nan_counts > 0].items():
            pct = (count / len(df)) * 100
            print(f"      - {col}: {count:,} ({pct:.2f}%)")
    else:
        print("   ✅ Aucune valeur NaN")
    
    # Statistiques sur les valeurs infinies
    print(f"\n♾️  VALEURS INFINIES:")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    inf_counts = {}
    for col in numeric_cols:
        inf_count = np.isinf(df[col]).sum()
        if inf_count > 0:
            inf_counts[col] = inf_count
    
    if inf_counts:
        print(f"   Total colonnes avec infinis: {len(inf_counts)}")
        for col, count in sorted(inf_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            pct = (count / len(df)) * 100
            print(f"      - {col}: {count:,} ({pct:.2f}%)")
    else:
        print("   ✅ Aucune valeur infinie")
    
    # Duplications
    print(f"\n🔄 DUPLICATIONS:")
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        pct = (dup_count / len(df)) * 100
        print(f"   Lignes dupliquées: {dup_count:,} ({pct:.2f}%)")
    else:
        print("   ✅ Aucune duplication")
    
    print("\n" + "=" * 70)
    
    return df


def get_feature_categories(df, label_col='Attack Type'):
    """
    Catégorise les features du dataset
    
    Args:
        df (pd.DataFrame): DataFrame
        label_col (str): Nom de la colonne de labels
    """
    print("\n" + "=" * 70)
    print("CATÉGORISATION DES FEATURES")
    print("=" * 70)
    
    # Exclure la colonne de labels
    feature_cols = [col for col in df.columns if col != label_col]
    
    categories = {
        'Port': [],
        'Duration/Time': [],
        'Packets': [],
        'Length/Size': [],
        'Bytes': [],
        'Rate (per second)': [],
        'IAT (Inter-Arrival Time)': [],
        'Header': [],
        'Flags': [],
        'Window': [],
        'Active/Idle': [],
        'Other': []
    }
    
    for col in feature_cols:
        col_lower = col.lower()
        
        if 'port' in col_lower:
            categories['Port'].append(col)
        elif 'duration' in col_lower or 'time' in col_lower:
            categories['Duration/Time'].append(col)
        elif 'packet' in col_lower and 'length' not in col_lower and 'size' not in col_lower:
            categories['Packets'].append(col)
        elif 'length' in col_lower or 'size' in col_lower:
            categories['Length/Size'].append(col)
        elif 'byte' in col_lower:
            categories['Bytes'].append(col)
        elif '/s' in col_lower or 'rate' in col_lower:
            categories['Rate (per second)'].append(col)
        elif 'iat' in col_lower:
            categories['IAT (Inter-Arrival Time)'].append(col)
        elif 'header' in col_lower:
            categories['Header'].append(col)
        elif 'flag' in col_lower:
            categories['Flags'].append(col)
        elif 'win' in col_lower:
            categories['Window'].append(col)
        elif 'active' in col_lower or 'idle' in col_lower:
            categories['Active/Idle'].append(col)
        else:
            categories['Other'].append(col)
    
    for category, cols in categories.items():
        if cols:
            print(f"\n📌 {category} ({len(cols)} features):")
            for col in cols:
                print(f"   - {col}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        print("Usage: python analyze_dataset.py <path_to_csv>")
        print("\nExemple:")
        print("  python scripts/analyze_dataset.py data/raw/Monday-WorkingHours.pcap_ISCX.csv")
        sys.exit(1)
    
    # Analyser la structure
    df = analyze_dataset_structure(file_path)
    
    # Catégoriser les features
    get_feature_categories(df)
    
    print("\n✅ Analyse terminée!")
