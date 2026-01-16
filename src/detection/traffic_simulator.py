"""
Simulateur de trafic réseau pour NetGuardian-AI
Génère des flux de trafic pour tester le système de détection
"""

import pandas as pd
import numpy as np
import time
from pathlib import Path
from typing import Generator, Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class TrafficSimulator:
    """
    Simulateur de trafic réseau pour tests et démonstrations
    
    Peut fonctionner en mode:
    - REPLAY: Rejoue des données du dataset CICIDS2017
    - SYNTHETIC: Génère du trafic artificiel
    """
    
    def __init__(self, 
                 dataset_path: Optional[str] = None,
                 mode: str = 'synthetic',
                 attack_ratio: float = 0.2):
        """
        Initialise le simulateur
        
        Args:
            dataset_path: Chemin vers le dataset CICIDS2017 (pour mode replay)
            mode: 'replay' ou 'synthetic'
            attack_ratio: Ratio d'attaques dans le trafic généré (0.0 à 1.0)
        """
        self.dataset_path = dataset_path
        self.mode = mode
        self.attack_ratio = attack_ratio
        self.dataset: Optional[pd.DataFrame] = None
        self.current_index = 0
        
        # Statistiques
        self.packets_generated = 0
        
        logger.info(f"TrafficSimulator initialisé (mode={mode}, attack_ratio={attack_ratio})")
    
    def load_dataset(self) -> bool:
        """
        Charge le dataset pour le mode replay
        
        Returns:
            True si chargement réussi
        """
        if self.mode != 'replay':
            logger.warning("⚠️ Mode replay non activé")
            return False
        
        if not self.dataset_path or not Path(self.dataset_path).exists():
            logger.error(f"❌ Dataset introuvable: {self.dataset_path}")
            return False
        
        try:
            logger.info(f"📂 Chargement du dataset: {self.dataset_path}")
            self.dataset = pd.read_csv(self.dataset_path)
            logger.info(f"✅ Dataset chargé: {len(self.dataset)} lignes")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur de chargement: {e}")
            return False
    
    def generate_packet(self) -> pd.DataFrame:
        """
        Génère un seul paquet de trafic
        
        Returns:
            DataFrame avec un paquet
        """
        if self.mode == 'replay':
            return self._replay_packet()
        else:
            return self._generate_synthetic_packet()
    
    def generate_stream(self, 
                       packets_per_second: int = 10,
                       duration_seconds: Optional[int] = None) -> Generator[pd.DataFrame, None, None]:
        """
        Génère un flux continu de paquets
        
        Args:
            packets_per_second: Nombre de paquets par seconde
            duration_seconds: Durée de la simulation (None = infini)
        
        Yields:
            DataFrame avec un paquet à chaque itération
        """
        delay = 1.0 / packets_per_second
        start_time = time.time()
        
        while True:
            # Vérifier la durée
            if duration_seconds and (time.time() - start_time) > duration_seconds:
                logger.info(f"⏱️ Simulation terminée ({duration_seconds}s)")
                break
            
            # Générer un paquet
            packet = self.generate_packet()
            yield packet
            
            self.packets_generated += 1
            
            # Attendre avant le prochain paquet
            time.sleep(delay)
    
    def generate_batch(self, batch_size: int = 100) -> pd.DataFrame:
        """
        Génère un batch de paquets
        
        Args:
            batch_size: Nombre de paquets à générer
        
        Returns:
            DataFrame avec plusieurs paquets
        """
        packets = []
        for _ in range(batch_size):
            packet = self.generate_packet()
            packets.append(packet.iloc[0])
        
        return pd.DataFrame(packets)
    
    def _replay_packet(self) -> pd.DataFrame:
        """
        Rejoue un paquet du dataset
        
        Returns:
            DataFrame avec un paquet du dataset
        """
        if self.dataset is None:
            logger.error("❌ Dataset non chargé!")
            return self._generate_synthetic_packet()
        
        # Sélectionner un paquet
        if self.current_index >= len(self.dataset):
            self.current_index = 0  # Boucler
        
        packet = self.dataset.iloc[self.current_index:self.current_index+1]
        self.current_index += 1
        
        return packet
    
    def _generate_synthetic_packet(self) -> pd.DataFrame:
        """
        Génère un paquet synthétique
        
        Returns:
            DataFrame avec un paquet généré
        """
        # Déterminer si c'est une attaque ou du trafic normal
        is_attack = np.random.random() < self.attack_ratio
        
        if is_attack:
            return self._generate_attack_packet()
        else:
            return self._generate_normal_packet()
    
    def _generate_normal_packet(self) -> pd.DataFrame:
        """
        Génère un paquet de trafic normal
        
        Returns:
            DataFrame avec caractéristiques de trafic normal
        """
        # Caractéristiques typiques du trafic normal
        features = {
            'Flow Duration': np.random.exponential(5000),  # Courte durée
            'Total Fwd Packets': np.random.poisson(10),
            'Total Backward Packets': np.random.poisson(8),
            'Total Length of Fwd Packets': np.random.normal(1500, 500),
            'Total Length of Bwd Packets': np.random.normal(1200, 400),
            'Fwd Packet Length Max': np.random.normal(1500, 200),
            'Fwd Packet Length Min': np.random.normal(60, 20),
            'Fwd Packet Length Mean': np.random.normal(800, 200),
            'Fwd Packet Length Std': np.random.normal(300, 100),
            'Bwd Packet Length Max': np.random.normal(1500, 200),
            'Bwd Packet Length Min': np.random.normal(60, 20),
            'Bwd Packet Length Mean': np.random.normal(700, 200),
            'Bwd Packet Length Std': np.random.normal(300, 100),
            'Flow Bytes/s': np.random.normal(50000, 10000),
            'Flow Packets/s': np.random.normal(20, 5),
            'Flow IAT Mean': np.random.exponential(100),
            'Flow IAT Std': np.random.exponential(50),
            'Flow IAT Max': np.random.exponential(500),
            'Flow IAT Min': np.random.exponential(10),
            'Fwd IAT Total': np.random.exponential(1000),
            'Fwd IAT Mean': np.random.exponential(100),
            'Fwd IAT Std': np.random.exponential(50),
            'Fwd IAT Max': np.random.exponential(500),
            'Fwd IAT Min': np.random.exponential(10),
            'Bwd IAT Total': np.random.exponential(1000),
            'Bwd IAT Mean': np.random.exponential(100),
            'Bwd IAT Std': np.random.exponential(50),
            'Bwd IAT Max': np.random.exponential(500),
            'Bwd IAT Min': np.random.exponential(10),
        }
        
        # Ajouter des features aléatoires pour atteindre 78 features
        for i in range(len(features), 78):
            features[f'Feature_{i}'] = np.random.randn()
        
        return pd.DataFrame([features])
    
    def _generate_attack_packet(self) -> pd.DataFrame:
        """
        Génère un paquet d'attaque
        
        Returns:
            DataFrame avec caractéristiques d'attaque
        """
        # Choisir un type d'attaque aléatoire
        attack_types = ['DoS', 'DDoS', 'PortScan', 'BruteForce', 'WebAttack']
        attack_type = np.random.choice(attack_types)
        
        if attack_type in ['DoS', 'DDoS']:
            # DoS/DDoS: Beaucoup de paquets, haute fréquence
            features = {
                'Flow Duration': np.random.exponential(100),  # Très court
                'Total Fwd Packets': np.random.poisson(1000),  # Beaucoup de paquets
                'Total Backward Packets': np.random.poisson(5),  # Peu de réponses
                'Flow Bytes/s': np.random.normal(500000, 100000),  # Très rapide
                'Flow Packets/s': np.random.normal(1000, 200),  # Haute fréquence
            }
        elif attack_type == 'PortScan':
            # Port Scan: Beaucoup de connexions courtes
            features = {
                'Flow Duration': np.random.exponential(10),  # Très court
                'Total Fwd Packets': np.random.poisson(3),  # Peu de paquets
                'Total Backward Packets': np.random.poisson(1),
                'Flow Bytes/s': np.random.normal(1000, 200),
                'Flow Packets/s': np.random.normal(100, 20),
            }
        elif attack_type == 'BruteForce':
            # Brute Force: Connexions répétitives
            features = {
                'Flow Duration': np.random.exponential(1000),
                'Total Fwd Packets': np.random.poisson(50),
                'Total Backward Packets': np.random.poisson(40),
                'Flow Bytes/s': np.random.normal(10000, 2000),
                'Flow Packets/s': np.random.normal(50, 10),
            }
        else:  # WebAttack
            # Web Attack: Paquets de taille anormale
            features = {
                'Flow Duration': np.random.exponential(2000),
                'Total Fwd Packets': np.random.poisson(20),
                'Total Backward Packets': np.random.poisson(15),
                'Fwd Packet Length Max': np.random.normal(5000, 1000),  # Très gros
                'Flow Bytes/s': np.random.normal(20000, 5000),
                'Flow Packets/s': np.random.normal(10, 3),
            }
        
        # Ajouter des features aléatoires pour atteindre 78 features
        for i in range(len(features), 78):
            features[f'Feature_{i}'] = np.random.randn()
        
        return pd.DataFrame([features])
    
    def get_statistics(self) -> Dict:
        """
        Retourne les statistiques du simulateur
        
        Returns:
            Dictionnaire avec les statistiques
        """
        return {
            'mode': self.mode,
            'packets_generated': self.packets_generated,
            'attack_ratio': self.attack_ratio,
            'dataset_loaded': self.dataset is not None,
            'dataset_size': len(self.dataset) if self.dataset is not None else 0
        }


# Exemple d'utilisation
if __name__ == "__main__":
    print("=" * 60)
    print("NetGuardian-AI - Traffic Simulator")
    print("=" * 60)
    
    # Créer un simulateur en mode synthétique
    simulator = TrafficSimulator(mode='synthetic', attack_ratio=0.3)
    
    print(f"\n🌐 Mode: {simulator.mode}")
    print(f"⚔️ Ratio d'attaques: {simulator.attack_ratio * 100}%")
    
    # Générer un batch de test
    print("\n🔄 Génération de 10 paquets...")
    batch = simulator.generate_batch(10)
    
    print(f"✅ Généré: {len(batch)} paquets")
    print(f"📊 Features: {batch.shape[1]} colonnes")
    
    # Afficher les stats
    stats = simulator.get_statistics()
    print(f"\n📈 Statistiques:")
    print(f"  Paquets générés: {stats['packets_generated']}")
