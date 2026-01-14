"""
Classe HybridIDS pour NetGuardian-AI
Système de détection d'intrusion hybride avec 2 modèles en cascade
"""

import numpy as np
import pandas as pd
import joblib


class HybridIDS:
    """
    Système de détection d'intrusion hybride
    
    Architecture:
        1. Modèle Binaire: Détecte si le trafic est normal ou une attaque
        2. Modèle Multi-Classes: Identifie le type d'attaque exact
    
    Attributes:
        binary_model: Modèle de détection binaire (Normal vs Attaque)
        multiclass_model: Modèle de classification multi-classes
        scaler: StandardScaler pour normalisation
        label_encoder: LabelEncoder pour les labels multi-classes
    """
    
    def __init__(self, binary_model, multiclass_model, scaler, label_encoder):
        """
        Initialise le système hybride
        
        Args:
            binary_model: Modèle entraîné pour détection binaire
            multiclass_model: Modèle entraîné pour classification
            scaler: Scaler pour normalisation des features
            label_encoder: Encodeur pour les labels
        """
        self.binary_model = binary_model
        self.multiclass_model = multiclass_model
        self.scaler = scaler
        self.le = label_encoder
    
    def predict(self, X):
        """
        Prédiction hybride en 2 étapes
        
        Args:
            X: Features (DataFrame ou array numpy)
        
        Returns:
            Liste de dictionnaires avec:
                - type: Type de trafic/attaque
                - confidence: Score de confiance
                - is_attack: Boolean indiquant si c'est une attaque
        """
        # Normaliser les features
        X_scaled = self.scaler.transform(X)
        
        # Étape 1 : Détection binaire
        is_attack = self.binary_model.predict(X_scaled)
        binary_proba = self.binary_model.predict_proba(X_scaled)
        
        results = []
        
        for i, (attack_flag, proba) in enumerate(zip(is_attack, binary_proba)):
            if attack_flag == 0:
                # Trafic normal
                results.append({
                    'type': 'Normal Traffic',
                    'confidence': float(proba[0]),
                    'is_attack': False,
                    'severity': 'low'
                })
            else:
                # Attaque détectée → Étape 2 : Classification
                attack_type_encoded = self.multiclass_model.predict(X_scaled[i:i+1])[0]
                attack_proba = self.multiclass_model.predict_proba(X_scaled[i:i+1])[0]
                attack_type = self.le.inverse_transform([attack_type_encoded])[0]
                
                # Déterminer la sévérité
                severity = self._get_severity(attack_type)
                
                results.append({
                    'type': attack_type,
                    'confidence': float(attack_proba.max()),
                    'is_attack': True,
                    'severity': severity
                })
        
        return results
    
    def predict_single(self, X):
        """
        Prédiction pour une seule instance
        
        Args:
            X: Features d'une seule instance (array 1D ou DataFrame 1 ligne)
        
        Returns:
            Dictionnaire avec type, confidence, is_attack, severity
        """
        if isinstance(X, pd.DataFrame):
            X = X.values
        
        if len(X.shape) == 1:
            X = X.reshape(1, -1)
        
        return self.predict(X)[0]
    
    def predict_df(self, X):
        """
        Prédiction avec résultat en DataFrame
        
        Args:
            X: Features (DataFrame ou array)
        
        Returns:
            DataFrame avec colonnes: type, confidence, is_attack, severity
        """
        results = self.predict(X)
        return pd.DataFrame(results)
    
    def _get_severity(self, attack_type):
        """
        Détermine la sévérité d'une attaque
        
        Args:
            attack_type: Type d'attaque
        
        Returns:
            Niveau de sévérité: 'critical', 'high', 'medium', 'low'
        """
        severity_map = {
            'DoS_DDoS': 'critical',
            'Web_Attack': 'high',
            'Brute_Force': 'high',
            'Bots': 'medium',
            'Port_Scanning': 'medium',
            'Reconnaissance': 'medium'
        }
        
        # Normaliser le nom
        normalized = attack_type.replace(' ', '_').replace('Attacks', 'Attack')
        
        return severity_map.get(normalized, 'medium')
    
    def get_alert_message(self, prediction):
        """
        Génère un message d'alerte basé sur la prédiction
        
        Args:
            prediction: Dictionnaire de prédiction
        
        Returns:
            Message d'alerte formaté
        """
        if not prediction['is_attack']:
            return "✅ Trafic normal détecté"
        
        severity_emoji = {
            'critical': '🚨',
            'high': '⚠️',
            'medium': '⚡',
            'low': 'ℹ️'
        }
        
        emoji = severity_emoji.get(prediction['severity'], '⚠️')
        
        return (f"{emoji} ALERTE {prediction['severity'].upper()}: "
                f"{prediction['type']} détecté "
                f"(Confiance: {prediction['confidence']:.2%})")
    
    @classmethod
    def load(cls, model_path='models/hybrid_ids_system.pkl'):
        """
        Charge un système hybride sauvegardé
        
        Args:
            model_path: Chemin vers le fichier .pkl
        
        Returns:
            Instance de HybridIDS
        """
        import pickle
        
        with open(model_path, 'rb') as f:
            system = pickle.load(f)
        
        return cls(
            binary_model=system['binary_model'],
            multiclass_model=system['multiclass_model'],
            scaler=system['scaler'],
            label_encoder=system['label_encoder']
        )
    
    def save(self, model_path='models/hybrid_ids_system.pkl'):
        """
        Sauvegarde le système hybride complet
        
        Args:
            model_path: Chemin de sauvegarde
        """
        import pickle
        import os
        
        system = {
            'binary_model': self.binary_model,
            'multiclass_model': self.multiclass_model,
            'scaler': self.scaler,
            'label_encoder': self.le
        }
        
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        with open(model_path, 'wb') as f:
            pickle.dump(system, f)
        
        print(f"✅ Système hybride sauvegardé: {model_path}")


# Exemple d'utilisation
if __name__ == "__main__":
    print("Module HybridIDS pour NetGuardian-AI")
    print("\nUtilisation:")
    print("  from src.hybrid_ids import HybridIDS")
    print("  ids = HybridIDS.load('models/hybrid_ids_system.pkl')")
    print("  predictions = ids.predict(X_new)")
