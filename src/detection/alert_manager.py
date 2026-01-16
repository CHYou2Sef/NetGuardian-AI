"""
Gestionnaire d'alertes pour NetGuardian-AI
Enregistre et gère les alertes de sécurité
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class AlertManager:
    """
    Gestionnaire d'alertes pour le système de détection
    
    Fonctionnalités:
    - Enregistrement structuré des alertes
    - Export en CSV/JSON
    - Filtrage par sévérité
    - Cooldown pour éviter le spam
    """
    
    def __init__(self, log_dir: str = "logs", cooldown_seconds: int = 5):
        """
        Initialise le gestionnaire d'alertes
        
        Args:
            log_dir: Répertoire pour les logs
            cooldown_seconds: Délai minimum entre alertes du même type
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.cooldown_seconds = cooldown_seconds
        self.last_alert_time: Dict[str, datetime] = {}
        
        # Historique des alertes
        self.alerts: List[Dict] = []
        
        logger.info(f"AlertManager initialisé (log_dir={log_dir})")
    
    def record_alert(self, detection: Dict) -> bool:
        """
        Enregistre une alerte
        
        Args:
            detection: Dictionnaire de détection du RealtimeDetector
        
        Returns:
            True si alerte enregistrée, False si en cooldown
        """
        if not detection.get('is_attack', False):
            return False  # Pas d'alerte pour trafic normal
        
        attack_type = detection['type']
        
        # Vérifier le cooldown
        if self._is_in_cooldown(attack_type):
            return False
        
        # Créer l'alerte
        alert = {
            'timestamp': detection.get('timestamp', datetime.now().isoformat()),
            'type': attack_type,
            'severity': detection.get('severity', 'medium'),
            'confidence': detection.get('confidence', 0.0),
            'message': self._generate_message(detection)
        }
        
        # Enregistrer
        self.alerts.append(alert)
        self.last_alert_time[attack_type] = datetime.now()
        
        # Logger
        self._log_alert(alert)
        
        return True
    
    def _is_in_cooldown(self, attack_type: str) -> bool:
        """
        Vérifie si un type d'attaque est en cooldown
        
        Args:
            attack_type: Type d'attaque
        
        Returns:
            True si en cooldown
        """
        if attack_type not in self.last_alert_time:
            return False
        
        elapsed = (datetime.now() - self.last_alert_time[attack_type]).total_seconds()
        return elapsed < self.cooldown_seconds
    
    def _generate_message(self, detection: Dict) -> str:
        """
        Génère un message d'alerte
        
        Args:
            detection: Dictionnaire de détection
        
        Returns:
            Message formaté
        """
        severity_emoji = {
            'critical': '🚨',
            'high': '⚠️',
            'medium': '⚡',
            'low': 'ℹ️'
        }
        
        emoji = severity_emoji.get(detection.get('severity', 'medium'), '⚠️')
        attack_type = detection['type']
        confidence = detection.get('confidence', 0.0)
        
        return f"{emoji} ALERTE {detection.get('severity', 'MEDIUM').upper()}: {attack_type} détecté (Confiance: {confidence:.2%})"
    
    def _log_alert(self, alert: Dict):
        """
        Écrit l'alerte dans les logs
        
        Args:
            alert: Dictionnaire d'alerte
        """
        severity_level = {
            'critical': logging.CRITICAL,
            'high': logging.ERROR,
            'medium': logging.WARNING,
            'low': logging.INFO
        }
        
        level = severity_level.get(alert['severity'], logging.WARNING)
        logger.log(level, alert['message'])
    
    def get_alerts(self, 
                   limit: Optional[int] = None,
                   severity: Optional[str] = None,
                   attack_type: Optional[str] = None) -> List[Dict]:
        """
        Récupère les alertes avec filtres
        
        Args:
            limit: Nombre maximum d'alertes
            severity: Filtrer par sévérité
            attack_type: Filtrer par type d'attaque
        
        Returns:
            Liste d'alertes filtrées
        """
        alerts = self.alerts
        
        # Filtrer par sévérité
        if severity:
            alerts = [a for a in alerts if a['severity'] == severity]
        
        # Filtrer par type
        if attack_type:
            alerts = [a for a in alerts if a['type'] == attack_type]
        
        # Limiter
        if limit:
            alerts = alerts[-limit:]
        
        return alerts
    
    def get_statistics(self) -> Dict:
        """
        Retourne les statistiques des alertes
        
        Returns:
            Dictionnaire avec les statistiques
        """
        if not self.alerts:
            return {
                'total_alerts': 0,
                'by_severity': {},
                'by_type': {}
            }
        
        # Compter par sévérité
        by_severity = {}
        for alert in self.alerts:
            sev = alert['severity']
            by_severity[sev] = by_severity.get(sev, 0) + 1
        
        # Compter par type
        by_type = {}
        for alert in self.alerts:
            atype = alert['type']
            by_type[atype] = by_type.get(atype, 0) + 1
        
        return {
            'total_alerts': len(self.alerts),
            'by_severity': by_severity,
            'by_type': by_type
        }
    
    def export_csv(self, filepath: Optional[str] = None) -> str:
        """
        Exporte les alertes en CSV
        
        Args:
            filepath: Chemin du fichier (auto si None)
        
        Returns:
            Chemin du fichier créé
        """
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.log_dir / f"alerts_{timestamp}.csv"
        
        filepath = Path(filepath)
        
        if not self.alerts:
            logger.warning("⚠️ Aucune alerte à exporter")
            return str(filepath)
        
        # Écrire le CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.alerts[0].keys())
            writer.writeheader()
            writer.writerows(self.alerts)
        
        logger.info(f"✅ Alertes exportées: {filepath}")
        return str(filepath)
    
    def export_json(self, filepath: Optional[str] = None) -> str:
        """
        Exporte les alertes en JSON
        
        Args:
            filepath: Chemin du fichier (auto si None)
        
        Returns:
            Chemin du fichier créé
        """
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.log_dir / f"alerts_{timestamp}.json"
        
        filepath = Path(filepath)
        
        # Écrire le JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.alerts, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Alertes exportées: {filepath}")
        return str(filepath)
    
    def clear_alerts(self):
        """
        Efface toutes les alertes
        """
        self.alerts.clear()
        self.last_alert_time.clear()
        logger.info("🗑️ Alertes effacées")


# Exemple d'utilisation
if __name__ == "__main__":
    print("=" * 60)
    print("NetGuardian-AI - Alert Manager")
    print("=" * 60)
    
    # Créer le gestionnaire
    manager = AlertManager(log_dir="logs/test")
    
    # Simuler des alertes
    print("\n🚨 Simulation d'alertes...")
    
    detections = [
        {'type': 'DDoS', 'severity': 'critical', 'confidence': 0.98, 'is_attack': True},
        {'type': 'Port_Scanning', 'severity': 'medium', 'confidence': 0.85, 'is_attack': True},
        {'type': 'Web_Attack', 'severity': 'high', 'confidence': 0.92, 'is_attack': True},
    ]
    
    for det in detections:
        if manager.record_alert(det):
            print(f"✅ Alerte enregistrée: {det['type']}")
    
    # Afficher les stats
    print("\n📊 Statistiques:")
    stats = manager.get_statistics()
    print(f"  Total: {stats['total_alerts']}")
    print(f"  Par sévérité: {stats['by_severity']}")
    print(f"  Par type: {stats['by_type']}")
    
    # Exporter
    print("\n💾 Export...")
    csv_file = manager.export_csv()
    json_file = manager.export_json()
    print(f"  CSV: {csv_file}")
    print(f"  JSON: {json_file}")
