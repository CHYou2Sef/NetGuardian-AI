"""
NetGuardian-AI - Dashboard de Détection en Temps Réel
Interface Streamlit pour visualiser les détections d'intrusions
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import sys
from pathlib import Path

# Ajouter le chemin src au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from src.detection import RealtimeDetector, TrafficSimulator, AlertManager


# Configuration de la page
st.set_page_config(
    page_title="NetGuardian-AI Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }
    .alert-critical {
        background-color: #fee;
        border-left: 4px solid #f00;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.3rem;
    }
    .alert-high {
        background-color: #ffeaa7;
        border-left: 4px solid #fdcb6e;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.3rem;
    }
    .alert-medium {
        background-color: #dfe6e9;
        border-left: 4px solid #74b9ff;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)


# Initialisation de la session state
if 'detector' not in st.session_state:
    st.session_state.detector = None
    st.session_state.simulator = None
    st.session_state.alert_manager = None
    st.session_state.is_running = False
    st.session_state.detection_history = []
    st.session_state.initialized = False


def initialize_system():
    """Initialise le système de détection"""
    if not st.session_state.initialized:
        with st.spinner("🔄 Initialisation du système..."):
            # Créer le détecteur (mode mock car modèles pas encore entraînés)
            st.session_state.detector = RealtimeDetector(use_mock=True)
            
            # Charger les modèles
            if st.session_state.detector.load_models():
                st.success("✅ Détecteur initialisé (Mode Mock)")
            else:
                st.error("❌ Échec de l'initialisation")
                return False
            
            # Créer le simulateur
            st.session_state.simulator = TrafficSimulator(
                mode='synthetic',
                attack_ratio=0.2
            )
            st.success("✅ Simulateur de trafic prêt")
            
            # Créer le gestionnaire d'alertes
            st.session_state.alert_manager = AlertManager()
            st.success("✅ Gestionnaire d'alertes prêt")
            
            st.session_state.initialized = True
            return True
    return True


def display_header():
    """Affiche l'en-tête du dashboard"""
    st.markdown('<h1 class="main-header">🛡️ NetGuardian-AI</h1>', unsafe_allow_html=True)
    st.markdown("### Système de Détection d'Intrusions en Temps Réel")
    st.markdown("---")


def display_metrics():
    """Affiche les métriques principales"""
    if not st.session_state.detector:
        return
    
    stats = st.session_state.detector.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Traité",
            value=f"{stats['total_processed']:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="🚨 Attaques Détectées",
            value=f"{stats['attacks_detected']:,}",
            delta=f"{stats['attack_percentage']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="✅ Trafic Normal",
            value=f"{stats['normal_traffic']:,}",
            delta=None
        )
    
    with col4:
        runtime = stats.get('runtime_seconds', 0)
        st.metric(
            label="⏱️ Temps d'Exécution",
            value=f"{runtime:.0f}s",
            delta=f"{stats.get('detection_rate', 0):.1f} pkt/s"
        )


def display_detection_feed():
    """Affiche le flux de détections récentes"""
    st.subheader("🔍 Détections Récentes")
    
    if not st.session_state.detector:
        st.info("Démarrez la simulation pour voir les détections")
        return
    
    # Récupérer les détections récentes
    recent = st.session_state.detector.get_alert_history(limit=20)
    
    if not recent:
        st.info("Aucune détection pour le moment...")
        return
    
    # Créer un DataFrame
    df = pd.DataFrame(recent)
    
    # Formater pour l'affichage
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%H:%M:%S')
    
    # Ajouter des emojis selon la sévérité
    severity_emoji = {
        'critical': '🚨',
        'high': '⚠️',
        'medium': '⚡',
        'low': 'ℹ️'
    }
    df['severity_icon'] = df['severity'].map(severity_emoji)
    
    # Afficher le tableau
    st.dataframe(
        df[['timestamp', 'severity_icon', 'type', 'confidence', 'severity']].rename(columns={
            'timestamp': 'Heure',
            'severity_icon': '',
            'type': 'Type',
            'confidence': 'Confiance',
            'severity': 'Sévérité'
        }),
        use_container_width=True,
        hide_index=True
    )


def display_charts():
    """Affiche les graphiques de visualisation"""
    if not st.session_state.detector:
        return
    
    stats = st.session_state.detector.get_statistics()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Distribution des Attaques")
        
        if stats['by_attack_type']:
            # Graphique en camembert
            attack_data = pd.DataFrame([
                {'Type': k, 'Count': v} 
                for k, v in stats['by_attack_type'].items()
            ])
            
            fig = px.pie(
                attack_data,
                values='Count',
                names='Type',
                title='Types d\'Attaques Détectées',
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune attaque détectée pour le moment")
    
    with col2:
        st.subheader("📊 Trafic Normal vs Attaques")
        
        # Graphique en barres
        traffic_data = pd.DataFrame([
            {'Type': 'Normal', 'Count': stats['normal_traffic']},
            {'Type': 'Attaques', 'Count': stats['attacks_detected']}
        ])
        
        fig = px.bar(
            traffic_data,
            x='Type',
            y='Count',
            title='Répartition du Trafic',
            color='Type',
            color_discrete_map={'Normal': '#00b894', 'Attaques': '#d63031'}
        )
        st.plotly_chart(fig, use_container_width=True)


def display_timeline():
    """Affiche la timeline des détections"""
    st.subheader("⏰ Timeline des Détections")
    
    if not st.session_state.detector:
        return
    
    history = st.session_state.detector.get_alert_history(limit=100)
    
    if not history:
        st.info("Aucune donnée de timeline disponible")
        return
    
    # Créer un DataFrame
    df = pd.DataFrame(history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Compter les détections par minute
    df['minute'] = df['timestamp'].dt.floor('10S')
    timeline_data = df.groupby(['minute', 'is_attack']).size().reset_index(name='count')
    timeline_data['type'] = timeline_data['is_attack'].map({True: 'Attaque', False: 'Normal'})
    
    # Graphique de ligne
    fig = px.line(
        timeline_data,
        x='minute',
        y='count',
        color='type',
        title='Évolution des Détections',
        labels={'minute': 'Temps', 'count': 'Nombre de Paquets', 'type': 'Type'},
        color_discrete_map={'Normal': '#00b894', 'Attaque': '#d63031'}
    )
    
    st.plotly_chart(fig, use_container_width=True)


def simulation_controls():
    """Contrôles de la simulation"""
    st.sidebar.header("⚙️ Contrôles")
    
    # Bouton Start/Stop
    if st.sidebar.button("▶️ Démarrer" if not st.session_state.is_running else "⏸️ Arrêter", 
                         use_container_width=True):
        st.session_state.is_running = not st.session_state.is_running
    
    # Paramètres de simulation
    st.sidebar.subheader("📊 Paramètres")
    
    packets_per_second = st.sidebar.slider(
        "Paquets/seconde",
        min_value=1,
        max_value=50,
        value=10,
        help="Vitesse de simulation"
    )
    
    attack_ratio = st.sidebar.slider(
        "Ratio d'attaques",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.05,
        help="Proportion d'attaques dans le trafic"
    )
    
    # Mettre à jour le simulateur
    if st.session_state.simulator:
        st.session_state.simulator.attack_ratio = attack_ratio
    
    return packets_per_second


def run_simulation_step(packets_per_second):
    """Exécute une étape de simulation"""
    if not st.session_state.is_running:
        return
    
    # Générer un batch de paquets
    batch_size = max(1, packets_per_second // 10)
    batch = st.session_state.simulator.generate_batch(batch_size)
    
    # Préprocesser
    processed = st.session_state.detector.process_traffic(batch)
    
    # Détecter
    detections = st.session_state.detector.detect(processed)
    
    # Enregistrer les alertes
    for detection in detections:
        if detection['is_attack']:
            st.session_state.alert_manager.record_alert(detection)


def display_sidebar_stats():
    """Affiche les statistiques dans la sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 Statistiques")
    
    if st.session_state.detector:
        stats = st.session_state.detector.get_statistics()
        
        st.sidebar.metric("Total Traité", f"{stats['total_processed']:,}")
        st.sidebar.metric("Attaques", f"{stats['attacks_detected']:,}")
        st.sidebar.metric("Taux d'Attaque", f"{stats['attack_percentage']:.1f}%")
    
    if st.session_state.alert_manager:
        alert_stats = st.session_state.alert_manager.get_statistics()
        st.sidebar.metric("Alertes Totales", f"{alert_stats['total_alerts']:,}")
    
    # Bouton de reset
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Réinitialiser", use_container_width=True):
        if st.session_state.detector:
            st.session_state.detector.reset_statistics()
        if st.session_state.alert_manager:
            st.session_state.alert_manager.clear_alerts()
        st.rerun()


def main():
    """Fonction principale du dashboard"""
    # Afficher l'en-tête
    display_header()
    
    # Initialiser le système
    if not initialize_system():
        st.error("❌ Impossible d'initialiser le système")
        return
    
    # Contrôles de simulation
    packets_per_second = simulation_controls()
    
    # Statistiques sidebar
    display_sidebar_stats()
    
    # Afficher les métriques
    display_metrics()
    
    st.markdown("---")
    
    # Colonnes principales
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Timeline
        display_timeline()
        
        # Graphiques
        display_charts()
    
    with col2:
        # Flux de détections
        display_detection_feed()
    
    # Exécuter la simulation si active
    if st.session_state.is_running:
        run_simulation_step(packets_per_second)
        time.sleep(0.1)  # Petit délai
        st.rerun()  # Rafraîchir l'interface


if __name__ == "__main__":
    main()
