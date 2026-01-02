"""
NetGuardian-AI Configuration
Central configuration file for the IDS project
"""

import os
from pathlib import Path

# ============================================
# Project Paths
# ============================================
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLES_DATA_DIR = DATA_DIR / "samples"

MODELS_DIR = PROJECT_ROOT / "models"
ML_MODELS_DIR = MODELS_DIR / "ml"
DL_MODELS_DIR = MODELS_DIR / "dl"

LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, SAMPLES_DATA_DIR,
                  ML_MODELS_DIR, DL_MODELS_DIR, LOGS_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================
# Dataset Configuration
# ============================================
DATASET_NAME = "CICIDS2017"
DATASET_URL = "https://www.unb.ca/cic/datasets/ids-2017.html"

# Features to extract
FEATURE_COLUMNS = [
    'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets',
    'Total Length of Fwd Packets', 'Total Length of Bwd Packets',
    'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean',
    'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean',
    'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std',
    'Fwd IAT Total', 'Fwd IAT Mean', 'Bwd IAT Total', 'Bwd IAT Mean',
    'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags',
    'Fwd Header Length', 'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s',
    'Min Packet Length', 'Max Packet Length', 'Packet Length Mean',
    'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count',
    'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count',
    'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count', 'Down/Up Ratio',
    'Average Packet Size', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size',
    'Fwd Avg Bytes/Bulk', 'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate',
    'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate',
    'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets',
    'Subflow Bwd Bytes', 'Init_Win_bytes_forward', 'Init_Win_bytes_backward',
    'act_data_pkt_fwd', 'min_seg_size_forward', 'Active Mean', 'Active Std',
    'Active Max', 'Active Min', 'Idle Mean', 'Idle Std', 'Idle Max', 'Idle Min'
]

# Target column
TARGET_COLUMN = 'Label'

# Attack types mapping
ATTACK_TYPES = {
    'BENIGN': 0,
    'DoS Hulk': 1,
    'PortScan': 2,
    'DDoS': 3,
    'DoS GoldenEye': 4,
    'FTP-Patator': 5,
    'SSH-Patator': 6,
    'DoS slowloris': 7,
    'DoS Slowhttptest': 8,
    'Bot': 9,
    'Web Attack – Brute Force': 10,
    'Web Attack – XSS': 11,
    'Web Attack – Sql Injection': 12,
    'Infiltration': 13,
    'Heartbleed': 14
}

# ============================================
# Model Configuration
# ============================================

# Random Forest
RF_CONFIG = {
    'n_estimators': 100,
    'max_depth': 20,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': 42,
    'n_jobs': -1
}

# XGBoost
XGB_CONFIG = {
    'n_estimators': 100,
    'max_depth': 10,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'random_state': 42,
    'n_jobs': -1
}

# SVM
SVM_CONFIG = {
    'kernel': 'rbf',
    'C': 1.0,
    'gamma': 'scale',
    'random_state': 42
}

# Isolation Forest
IFOREST_CONFIG = {
    'n_estimators': 100,
    'contamination': 0.1,
    'random_state': 42,
    'n_jobs': -1
}

# K-Means
KMEANS_CONFIG = {
    'n_clusters': 2,
    'random_state': 42,
    'n_init': 10
}

# MLP (Multi-Layer Perceptron)
MLP_CONFIG = {
    'hidden_layers': [128, 64, 32],
    'activation': 'relu',
    'dropout_rate': 0.3,
    'learning_rate': 0.001,
    'batch_size': 256,
    'epochs': 50
}

# LSTM
LSTM_CONFIG = {
    'units': 64,
    'dropout_rate': 0.3,
    'learning_rate': 0.001,
    'batch_size': 256,
    'epochs': 50,
    'sequence_length': 10
}

# Autoencoder
AUTOENCODER_CONFIG = {
    'encoding_dim': 32,
    'hidden_layers': [64, 32, 16],
    'learning_rate': 0.001,
    'batch_size': 256,
    'epochs': 50
}

# ============================================
# Training Configuration
# ============================================
TRAIN_TEST_SPLIT = 0.2
VALIDATION_SPLIT = 0.1
RANDOM_STATE = 42

# ============================================
# Evaluation Configuration
# ============================================
METRICS = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']

# ============================================
# Dashboard Configuration
# ============================================
DASHBOARD_PORT = 8501
DASHBOARD_TITLE = "NetGuardian-AI - IDS Dashboard"
REFRESH_INTERVAL = 5  # seconds

# ============================================
# Logging Configuration
# ============================================
LOG_LEVEL = "INFO"
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
LOG_FILE = LOGS_DIR / "netguardian.log"

# ============================================
# Detection Configuration
# ============================================
DETECTION_THRESHOLD = 0.5  # Anomaly score threshold
ALERT_THRESHOLD = 0.8  # High priority alert threshold

# ============================================
# Google Drive Configuration (for Colab)
# ============================================
GDRIVE_DATA_PATH = "/content/drive/MyDrive/NetGuardian-AI/data/processed/"
GDRIVE_MODEL_PATH = "/content/drive/MyDrive/NetGuardian-AI/models/dl/"

# ============================================
# Kaggle Configuration
# ============================================
KAGGLE_DATASET = "cicdataset/cicids2017"

# ============================================
# Display Configuration
# ============================================
import warnings
warnings.filterwarnings('ignore')

# Pandas display options
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("✅ Configuration loaded successfully!")
print(f"📁 Project Root: {PROJECT_ROOT}")
print(f"📊 Dataset: {DATASET_NAME}")
print(f"🎯 Target Column: {TARGET_COLUMN}")
print(f"📈 Number of Attack Types: {len(ATTACK_TYPES)}")
