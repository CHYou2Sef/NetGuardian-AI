"""
Real-Time Network Intrusion Detection Engine
Utilise le système HybridIDS pour détecter les intrusions en temps réel
"""

import numpy as np
import pandas as pd
import joblib
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
from pathlib import Path

# Import du système hybride
import sys
sys.path.append(str(Path(__file__).parent.parent))
from hybrid_ids import HybridIDS


# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RealtimeDetector:
    """
    Moteur de détection en temps réel pour NetGuardian-AI
    
    Charge les modèles pré-entraînés et effectue la détection
    sur des flux de trafic réseau en temps réel.
    """
    
    def __init__(self, models_dir: str = "models", use_mock: bool = True):
        """
        Initialise le détecteur en temps réel
        
        Args:
            models_dir: Répertoire contenant les modèles entraînés
            use_mock: Si True, utilise des modèles mock pour développement
        """
        self.models_dir = Path(models_dir)
        self.use_mock = use_mock
        self.ids_system: Optional[HybridIDS] = None
        self.is_loaded = False
        
        # Statistiques de détection
        self.stats = {
            'total_processed': 0,
            'attacks_detected': 0,
            'normal_traffic': 0,
            'by_attack_type': {},
            'start_time': datetime.now()
        }
        
        # Historique des détections
        self.detection_history: List[Dict] = []
        self.max_history_size = 1000
        
        logger.info(f"RealtimeDetector initialisé (mock={use_mock})")
    
    def load_models(self) -> bool:
        """
        Charge les modèles pré-entraînés
        
        Returns:
            True si chargement réussi, False sinon
        """
        try:
            if self.use_mock:
                logger.warning("⚠️ Mode MOCK activé - Utilisation de modèles simulés")
                self._load_mock_models()
                self.is_loaded = True
                return True
            
            # Vérifier l'existence des fichiers de modèles
            required_files = [
                'hybrid_ids_system.pkl',
                'scaler.pkl',
                'label_encoder.pkl'
            ]
            
            missing_files = []
            for file in required_files:
                if not (self.models_dir / file).exists():
                    missing_files.append(file)
            
            if missing_files:
                logger.error(f"❌ Fichiers manquants: {missing_files}")
                logger.info("💡 Conseil: Entraînez d'abord les modèles avec les notebooks Colab")
                return False
            
            # Charger le système hybride
            logger.info("📦 Chargement des modèles...")
            self.ids_system = HybridIDS.load(
                str(self.models_dir / 'hybrid_ids_system.pkl')
            )
            
            self.is_loaded = True
            logger.info("✅ Modèles chargés avec succès!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement: {e}")
            return False
    
    def _load_mock_models(self):
        """
        Crée des modèles mock pour le développement
        """
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        
        # Créer des modèles factices
        binary_model = RandomForestClassifier(n_estimators=10, random_state=42)
        multiclass_model = RandomForestClassifier(n_estimators=10, random_state=42)
        
        # Créer des données factices pour l'entraînement
        X_mock = np.random.randn(100, 78)  # 78 features comme CICIDS2017
        y_binary = np.random.randint(0, 2, 100)
        y_multi = np.random.randint(0, 7, 100)
        
        binary_model.fit(X_mock, y_binary)
        multiclass_model.fit(X_mock, y_multi)
        
        # Scaler et encoder
        scaler = StandardScaler()
        scaler.fit(X_mock)
        
        le = LabelEncoder()
        le.fit(['Normal', 'DoS_DDoS', 'Port_Scanning', 'Web_Attack', 
                'Brute_Force', 'Botnet', 'Reconnaissance'])
        
        # Créer le système hybride
        self.ids_system = HybridIDS(
            binary_model=binary_model,
            multiclass_model=multiclass_model,
            scaler=scaler,
            label_encoder=le
        )
        
        logger.info("✅ Modèles MOCK créés pour développement")
    
    def process_traffic(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """
        Préprocesse les données de trafic brutes
        
        Args:
            raw_data: DataFrame avec les features brutes
        
        Returns:
            DataFrame préprocessé prêt pour la détection
        """
        # Copier pour ne pas modifier l'original
        data = raw_data.copy()
        
        # Nettoyer les noms de colonnes
        data.columns = data.columns.str.strip()
        
        # Gérer les valeurs infinies et NaN
        data.replace([np.inf, -np.inf], np.nan, inplace=True)
        
        # Remplir les NaN avec la médiane
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if data[col].isnull().any():
                data[col].fillna(data[col].median(), inplace=True)
        
        return data
    
    def detect(self, features: pd.DataFrame) -> List[Dict]:
        """
        Effectue la détection sur les features
        
        Args:
            features: DataFrame avec les features (déjà préprocessées)
        
        Returns:
            Liste de dictionnaires avec les résultats de détection
        """
        if not self.is_loaded:
            logger.error("❌ Modèles non chargés! Appelez load_models() d'abord")
            return []
        
        try:
            # Prédiction avec le système hybride
            predictions = self.ids_system.predict(features.values)
            
            # Ajouter timestamp et mettre à jour les stats
            for pred in predictions:
                pred['timestamp'] = datetime.now().isoformat()
                
                # Mettre à jour les statistiques
                self.stats['total_processed'] += 1
                
                if pred['is_attack']:
                    self.stats['attacks_detected'] += 1
                    attack_type = pred['type']
                    self.stats['by_attack_type'][attack_type] = \
                        self.stats['by_attack_type'].get(attack_type, 0) + 1
                else:
                    self.stats['normal_traffic'] += 1
                
                # Ajouter à l'historique
                self.detection_history.append(pred)
                
                # Limiter la taille de l'historique
                if len(self.detection_history) > self.max_history_size:
                    self.detection_history.pop(0)
            
            return predictions
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la détection: {e}")
            return []
    
    def detect_single(self, features: pd.Series) -> Dict:
        """
        Détecte une seule instance de trafic
        
        Args:
            features: Series avec les features d'une instance
        
        Returns:
            Dictionnaire avec le résultat de détection
        """
        df = pd.DataFrame([features])
        results = self.detect(df)
        return results[0] if results else {}
    
    def get_statistics(self) -> Dict:
        """
        Retourne les statistiques de détection
        
        Returns:
            Dictionnaire avec les statistiques
        """
        runtime = (datetime.now() - self.stats['start_time']).total_seconds()
        
        return {
            **self.stats,
            'runtime_seconds': runtime,
            'detection_rate': self.stats['total_processed'] / runtime if runtime > 0 else 0,
            'attack_percentage': (self.stats['attacks_detected'] / self.stats['total_processed'] * 100) 
                                if self.stats['total_processed'] > 0 else 0
        }
    
    def get_alert_history(self, limit: int = 100, 
                          severity: Optional[str] = None) -> List[Dict]:
        """
        Retourne l'historique des alertes
        
        Args:
            limit: Nombre maximum d'alertes à retourner
            severity: Filtrer par sévérité (critical, high, medium, low)
        
        Returns:
            Liste des alertes récentes
        """
        history = self.detection_history[-limit:]
        
        if severity:
            history = [h for h in history if h.get('severity') == severity]
        
        return history
    
    def get_recent_attacks(self, limit: int = 50) -> List[Dict]:
        """
        Retourne les attaques récentes détectées
        
        Args:
            limit: Nombre maximum d'attaques à retourner
        
        Returns:
            Liste des attaques récentes
        """
        attacks = [h for h in self.detection_history if h['is_attack']]
        return attacks[-limit:]
    
    def reset_statistics(self):
        """
        Réinitialise les statistiques de détection
        """
        self.stats = {
            'total_processed': 0,
            'attacks_detected': 0,
            'normal_traffic': 0,
            'by_attack_type': {},
            'start_time': datetime.now()
        }
        self.detection_history.clear()
        logger.info("📊 Statistiques réinitialisées")
    
    def export_history(self, filepath: str, format: str = 'csv'):
        """
        Exporte l'historique des détections
        
        Args:
            filepath: Chemin du fichier de sortie
            format: Format d'export ('csv' ou 'json')
        """
        if not self.detection_history:
            logger.warning("⚠️ Aucune détection à exporter")
            return
        
        df = pd.DataFrame(self.detection_history)
        
        if format == 'csv':
            df.to_csv(filepath, index=False)
        elif format == 'json':
            df.to_json(filepath, orient='records', indent=2)
        
        logger.info(f"✅ Historique exporté: {filepath}")


# Exemple d'utilisation
if __name__ == "__main__":
    print("=" * 60)
    print("NetGuardian-AI - Real-Time Detector")
    print("=" * 60)
    
    # Créer le détecteur en mode mock
    detector = RealtimeDetector(use_mock=True)
    
    # Charger les modèles
    if detector.load_models():
        print("\n✅ Détecteur prêt!")
        
        # Simuler une détection
        print("\n🔍 Test de détection...")
        mock_features = pd.DataFrame(np.random.randn(5, 78))
        
        results = detector.detect(mock_features)
        
        print(f"\n📊 Résultats: {len(results)} détections")
        for i, result in enumerate(results, 1):
            emoji = "🚨" if result['is_attack'] else "✅"
            print(f"{emoji} {i}. {result['type']} (confiance: {result['confidence']:.2%})")
        
        # Afficher les stats
        print("\n📈 Statistiques:")
        stats = detector.get_statistics()
        print(f"  Total traité: {stats['total_processed']}")
        print(f"  Attaques: {stats['attacks_detected']}")
        print(f"  Normal: {stats['normal_traffic']}")
    else:
        print("\n❌ Échec du chargement des modèles")
