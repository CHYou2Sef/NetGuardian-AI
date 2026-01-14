"""
Script d'exemple pour utiliser les fonctions de preprocessing
Utilisez ce script comme référence pour votre workflow Kaggle
"""

import pandas as pd
import sys
import os

# Ajouter le répertoire parent au path pour importer src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing import (
    clean_cicids2017,
    map_labels,
    encode_labels,
    prepare_features,
    verify_dataset,
    ATTACK_CATEGORIES
)


def example_workflow(input_file, output_dir='data/processed'):
    """
    Exemple de workflow complet de preprocessing
    
    Args:
        input_file (str): Chemin vers le fichier CSV brut
        output_dir (str): Répertoire de sortie
    """
    print("=" * 70)
    print("WORKFLOW DE PREPROCESSING CICIDS2017")
    print("=" * 70)
    
    # 1. Charger le dataset
    print(f"\n📂 Étape 1: Chargement du dataset")
    print(f"   Fichier: {input_file}")
    df = pd.read_csv(input_file)
    print(f"   ✅ Chargé: {df.shape}")
    
    # 2. Nettoyer
    print(f"\n🧹 Étape 2: Nettoyage du dataset")
    df_clean = clean_cicids2017(df, verbose=True)
    
    # 3. Mapper les labels
    print(f"\n🏷️  Étape 3: Mapping des labels")
    df_clean = map_labels(df_clean, label_col='Attack Type')
    print(f"   ✅ Labels mappés vers catégories")
    print(f"\n   Distribution des catégories:")
    print(df_clean['Attack_Category'].value_counts())
    
    # 4. Encoder les labels
    print(f"\n🔢 Étape 4: Encodage numérique")
    encoder_path = os.path.join(output_dir, 'label_encoder.pkl')
    df_clean, le = encode_labels(df_clean, save_path=encoder_path)
    
    # 5. Vérifier la qualité
    print(f"\n✅ Étape 5: Vérification de la qualité")
    verify_dataset(df_clean)
    
    # 6. Sauvegarder le dataset nettoyé
    print(f"\n💾 Étape 6: Sauvegarde")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'cicids2017_cleaned.csv')
    df_clean.to_csv(output_file, index=False)
    print(f"   ✅ Dataset sauvegardé: {output_file}")
    
    # 7. Préparer les features pour ML
    print(f"\n🎯 Étape 7: Préparation des features")
    scaler_path = os.path.join(output_dir, 'scaler.pkl')
    X, y, scaler = prepare_features(df_clean, scale=True, scaler_path=scaler_path)
    
    # Sauvegarder X et y
    import numpy as np
    np.save(os.path.join(output_dir, 'X_scaled.npy'), X.values)
    np.save(os.path.join(output_dir, 'y.npy'), y.values)
    print(f"   ✅ Features sauvegardées: X_scaled.npy, y.npy")
    
    print("\n" + "=" * 70)
    print("🎉 PREPROCESSING TERMINÉ AVEC SUCCÈS!")
    print("=" * 70)
    print(f"\nFichiers générés dans '{output_dir}':")
    print(f"   - cicids2017_cleaned.csv (dataset complet)")
    print(f"   - X_scaled.npy (features normalisées)")
    print(f"   - y.npy (labels encodés)")
    print(f"   - scaler.pkl (scaler pour normalisation)")
    print(f"   - label_encoder.pkl (encodeur de labels)")
    print("\n✅ Prêt pour l'entraînement des modèles!")
    print("=" * 70)
    
    return df_clean, X, y


def quick_example():
    """
    Exemple rapide pour tester les fonctions
    """
    print("=" * 70)
    print("EXEMPLE RAPIDE DE PREPROCESSING")
    print("=" * 70)
    
    # Créer un petit dataset d'exemple
    import numpy as np
    
    data = {
        'Destination Port': [80, 443, 22, 80, 443],
        'Flow Duration': [1000, 2000, np.inf, 1500, 2500],
        'Total Fwd Packets': [10, 20, 15, 12, 18],
        'Total Length of Fwd Packets': [500, 1000, 750, 600, 900],
        'Flow Bytes/s': [500.0, 500.0, np.nan, 400.0, 360.0],
        'Flow Packets/s': [10.0, 10.0, np.nan, 8.0, 7.2],
        'Attack Type': ['BENIGN', 'DoS Hulk', 'BENIGN', 'PortScan', 'DDoS']
    }
    
    df = pd.DataFrame(data)
    print("\n📊 Dataset d'exemple:")
    print(df)
    
    # Nettoyer
    print("\n🧹 Nettoyage...")
    df_clean = clean_cicids2017(df, verbose=True)
    
    # Mapper
    print("\n🏷️  Mapping des labels...")
    df_clean = map_labels(df_clean)
    
    # Encoder
    print("\n🔢 Encodage...")
    df_clean, le = encode_labels(df_clean)
    
    print("\n📊 Dataset final:")
    print(df_clean[['Attack Type', 'Attack_Category', 'Label_Encoded']])
    
    print("\n✅ Exemple terminé!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Preprocessing CICIDS2017')
    parser.add_argument('--input', type=str, help='Chemin vers le fichier CSV')
    parser.add_argument('--output', type=str, default='data/processed', 
                       help='Répertoire de sortie')
    parser.add_argument('--example', action='store_true', 
                       help='Exécuter l\'exemple rapide')
    
    args = parser.parse_args()
    
    if args.example:
        quick_example()
    elif args.input:
        example_workflow(args.input, args.output)
    else:
        print("Usage:")
        print("  python scripts/preprocessing_example.py --input data/raw/Monday.csv")
        print("  python scripts/preprocessing_example.py --example")
