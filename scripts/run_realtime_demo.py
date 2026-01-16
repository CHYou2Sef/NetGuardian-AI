"""
Script de démonstration rapide pour NetGuardian-AI
Lance une simulation de détection en temps réel
"""

import argparse
import sys
from pathlib import Path

# Ajouter le chemin src
sys.path.append(str(Path(__file__).parent.parent))

from src.detection import RealtimeDetector, TrafficSimulator, AlertManager


def main():
    parser = argparse.ArgumentParser(
        description="Démonstration du système de détection NetGuardian-AI"
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='Durée de la simulation en secondes (défaut: 60)'
    )
    parser.add_argument(
        '--attack-rate',
        type=float,
        default=0.2,
        help='Ratio d\'attaques (0.0 à 1.0, défaut: 0.2)'
    )
    parser.add_argument(
        '--packets-per-second',
        type=int,
        default=10,
        help='Nombre de paquets par seconde (défaut: 10)'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🛡️  NetGuardian-AI - Démonstration en Temps Réel")
    print("=" * 70)
    print(f"\n⚙️  Configuration:")
    print(f"   Durée: {args.duration}s")
    print(f"   Ratio d'attaques: {args.attack_rate * 100}%")
    print(f"   Paquets/seconde: {args.packets_per_second}")
    print()
    
    # Initialiser le système
    print("🔄 Initialisation du système...")
    detector = RealtimeDetector(use_mock=True)
    
    if not detector.load_models():
        print("❌ Échec du chargement des modèles")
        return 1
    
    simulator = TrafficSimulator(mode='synthetic', attack_ratio=args.attack_rate)
    alert_manager = AlertManager()
    
    print("✅ Système prêt!\n")
    
    # Lancer la simulation
    print(f"🚀 Démarrage de la simulation ({args.duration}s)...\n")
    
    packet_count = 0
    
    try:
        for packet in simulator.generate_stream(
            packets_per_second=args.packets_per_second,
            duration_seconds=args.duration
        ):
            # Préprocesser
            processed = detector.process_traffic(packet)
            
            # Détecter
            detections = detector.detect(processed)
            
            # Enregistrer les alertes
            for detection in detections:
                if detection['is_attack']:
                    if alert_manager.record_alert(detection):
                        print(f"🚨 {detection['type']} détecté (confiance: {detection['confidence']:.2%})")
            
            packet_count += 1
            
            # Afficher les stats toutes les 50 paquets
            if packet_count % 50 == 0:
                stats = detector.get_statistics()
                print(f"\n📊 Stats: {stats['total_processed']} traités | "
                      f"{stats['attacks_detected']} attaques | "
                      f"{stats['normal_traffic']} normal")
    
    except KeyboardInterrupt:
        print("\n\n⏸️  Simulation interrompue par l'utilisateur")
    
    # Afficher le résumé final
    print("\n" + "=" * 70)
    print("📈 RÉSUMÉ FINAL")
    print("=" * 70)
    
    stats = detector.get_statistics()
    print(f"\n🔢 Détections:")
    print(f"   Total traité: {stats['total_processed']:,}")
    print(f"   Attaques: {stats['attacks_detected']:,}")
    print(f"   Trafic normal: {stats['normal_traffic']:,}")
    print(f"   Taux d'attaque: {stats['attack_percentage']:.2f}%")
    
    if stats['by_attack_type']:
        print(f"\n🎯 Par type d'attaque:")
        for attack_type, count in stats['by_attack_type'].items():
            print(f"   {attack_type}: {count}")
    
    alert_stats = alert_manager.get_statistics()
    print(f"\n🚨 Alertes:")
    print(f"   Total: {alert_stats['total_alerts']}")
    
    if alert_stats['by_severity']:
        print(f"   Par sévérité:")
        for severity, count in alert_stats['by_severity'].items():
            print(f"      {severity}: {count}")
    
    # Exporter les résultats
    print(f"\n💾 Export des résultats...")
    csv_file = alert_manager.export_csv()
    json_file = alert_manager.export_json()
    print(f"   CSV: {csv_file}")
    print(f"   JSON: {json_file}")
    
    print("\n✅ Démonstration terminée!")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
