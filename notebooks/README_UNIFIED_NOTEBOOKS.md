# 🛡️ NetGuardian-AI: Complete IDS Pipeline - Unified Notebooks

## 📚 Overview

This directory contains **comprehensive, all-in-one Google Colab notebooks** that consolidate the entire NetGuardian-AI Intrusion Detection System workflow. The original 8 separate notebooks have been merged into 3 well-documented parts with detailed step-by-step explanations.

## 📂 Notebook Structure

### Part 1: Foundation & Data Preparation
**File**: `NetGuardian_AI_Complete_Colab.ipynb`

**Covers**:
- ✅ **Phase 0**: Environment Setup
  - Library installation (XGBoost, imbalanced-learn, TensorFlow)
  - Import configuration
  - Visualization setup

- ✅ **Phase 1**: Dataset Construction & Cleaning
  - Loading CICIDS2017 dataset
  - Data quality checks (NaN, infinites, duplicates)
  - Comprehensive cleaning function
  - Attack distribution analysis

- ✅ **Phase 2**: MITRE ATT&CK Analysis
  - Mapping attacks to MITRE framework
  - Port and protocol analysis
  - Cybersecurity context

- ✅ **Phase 3**: Data Preparation
  - Binary label creation (Normal vs Attack)
  - Multi-class label creation (Attack types)
  - Feature normalization with StandardScaler
  - Train/test splitting with stratification

### Part 2: Model Training & Evaluation
**File**: `NetGuardian_AI_Complete_Part2.ipynb`

**Covers**:
- ✅ **Phase 4**: Hybrid Model Training
  - Binary detection model (XGBoost)
  - Multi-class classifier with SMOTE
  - Two-stage hybrid architecture
  - Model evaluation and confusion matrices
  - HybridIDS class implementation

- ✅ **Phase 5**: Model Evaluation & Robustness
  - Performance metrics (Precision, Recall, F1, AUC-ROC)
  - Robustness testing with Gaussian noise
  - Error analysis and confusion patterns
  - Insights for model improvement

### Part 3: Deployment & Benchmarking
**File**: `NetGuardian_AI_Complete_Part3.ipynb`

**Covers**:
- ✅ **Phase 6**: Real-Time Simulation
  - Packet-by-packet processing simulation
  - Real-time alert generation
  - Detection statistics
  - Operational behavior demonstration

- ✅ **Phase 7**: Model Comparison Benchmark
  - Random Forest comparison
  - SVM (Support Vector Machine)
  - KNN (K-Nearest Neighbors)
  - Autoencoder (unsupervised anomaly detection)
  - Performance vs speed trade-offs
  - Use case recommendations

## 🎯 Key Features

### Detailed Explanations
Each code cell includes:
- **Purpose**: What the code does
- **Why**: Rationale behind the approach
- **How**: Technical explanation of the implementation
- **Insights**: Interpretation of results

### Educational Content
- MITRE ATT&CK framework mapping
- Machine learning concept explanations
- Cybersecurity best practices
- Trade-off analysis (accuracy vs speed)

### Production-Ready Code
- Modular HybridIDS class
- Model persistence (joblib, pickle)
- Scalable architecture
- Error handling

## 🚀 Quick Start

### Option 1: Google Colab (Recommended)
1. Upload all 3 notebooks to Google Colab
2. Upload CICIDS2017 dataset to Colab or link from Kaggle
3. Run cells sequentially from Part 1 → Part 2 → Part 3

### Option 2: Local Jupyter
1. Install dependencies:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn xgboost imbalanced-learn tensorflow joblib
   ```
2. Download CICIDS2017 dataset
3. Update file paths in notebooks
4. Run cells sequentially

## 📊 Expected Outputs

### Models Generated
- `model1_binary.pkl` - Binary detection (Normal vs Attack)
- `model2_multiclass.pkl` - Multi-class classifier (Attack types)
- `hybrid_ids_system.pkl` - Complete hybrid system
- `scaler.pkl` - Feature normalizer
- `label_encoder.pkl` - Label encoder
- Benchmark models: `random_forest.pkl`, `svm.pkl`, `knn.pkl`, `autoencoder.h5`

### Visualizations
- Attack distribution charts
- Confusion matrices (binary and multi-class)
- Robustness vs noise plots
- Model comparison bar charts

### Performance Metrics
- Accuracy, Precision, Recall, F1-Score
- AUC-ROC curves
- Training time comparisons
- Confidence scores

## 📖 Detailed Phase Breakdown

### Phase 0: Environment Setup
**Time**: ~2 minutes  
**Purpose**: Install libraries and configure environment  
**Key Outputs**: Verified TensorFlow version, configured matplotlib

### Phase 1: Dataset Construction
**Time**: ~5-10 minutes (depends on dataset size)  
**Purpose**: Load and clean CICIDS2017  
**Key Outputs**: 
- Cleaned dataset with no NaN/infinites
- Attack distribution statistics
- Visualizations

### Phase 2: MITRE Analysis
**Time**: ~2 minutes  
**Purpose**: Map attacks to cybersecurity framework  
**Key Outputs**: 
- MITRE ATT&CK mapping table
- Port analysis by attack type

### Phase 3: Data Preparation
**Time**: ~5 minutes  
**Purpose**: Prepare features for ML  
**Key Outputs**:
- Binary labels (0/1)
- Multi-class labels (0-5)
- Normalized features (mean=0, std=1)
- Train/test splits (80/20)

### Phase 4: Hybrid Training
**Time**: ~10-20 minutes  
**Purpose**: Train two-stage IDS  
**Key Outputs**:
- Model 1: Binary classifier (AUC-ROC >0.99 expected)
- Model 2: Multi-class classifier (F1 >0.95 expected)
- HybridIDS system

### Phase 5: Evaluation
**Time**: ~5 minutes  
**Purpose**: Test robustness  
**Key Outputs**:
- Performance metrics
- Robustness curves
- Error analysis

### Phase 6: Simulation
**Time**: ~1 minute  
**Purpose**: Demonstrate real-time detection  
**Key Outputs**:
- Live attack alerts
- Detection statistics

### Phase 7: Comparison
**Time**: ~15-30 minutes  
**Purpose**: Benchmark different algorithms  
**Key Outputs**:
- Performance comparison table
- Speed vs accuracy trade-offs
- Recommendations

## 🔍 What Each Script Explains

### Data Cleaning
- **Why remove duplicates?** Prevents model from memorizing repeated patterns
- **Why use median for NaN?** Robust to outliers (unlike mean)
- **Why replace infinites?** Prevents numerical instability

### Feature Engineering
- **Why normalize?** Ensures all features contribute equally
- **Why stratified split?** Maintains class distribution in train/test

### Model Selection
- **Why XGBoost?** Fast, accurate, handles imbalance well
- **Why SMOTE?** Balances minority attack classes
- **Why hybrid?** Faster than single multi-class model

### Evaluation
- **Why F1-Score?** Balances precision and recall
- **Why AUC-ROC?** Threshold-independent performance measure
- **Why robustness testing?** Simulates real-world noise

## 🎓 Learning Outcomes

After completing these notebooks, you will understand:

1. **Data Science Pipeline**
   - Data cleaning and preprocessing
   - Feature engineering
   - Train/test splitting
   - Model evaluation

2. **Machine Learning**
   - Supervised learning (XGBoost, Random Forest, SVM, KNN)
   - Unsupervised learning (Autoencoder)
   - Class imbalance handling (SMOTE)
   - Hyperparameter tuning

3. **Cybersecurity**
   - MITRE ATT&CK framework
   - Network intrusion detection
   - Attack classification
   - False positive/negative trade-offs

4. **Production ML**
   - Model persistence
   - Real-time inference
   - Performance monitoring
   - System architecture

## 🛠️ Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'xgboost'`  
**Solution**: Run `!pip install xgboost` in a cell

**Issue**: `MemoryError` during training  
**Solution**: Reduce sample size in Phase 7 benchmark (change 50000 to 10000)

**Issue**: Low accuracy (<80%)  
**Solution**: Check if dataset paths are correct and data loaded properly

**Issue**: Slow training  
**Solution**: Reduce `n_estimators` or use smaller dataset sample

## 📚 Additional Resources

- **CICIDS2017 Paper**: [PDF Link](https://www.unb.ca/cic/datasets/ids-2017.html)
- **MITRE ATT&CK**: https://attack.mitre.org/
- **XGBoost Documentation**: https://xgboost.readthedocs.io/
- **SMOTE Paper**: https://arxiv.org/abs/1106.1813
- **Scikit-learn User Guide**: https://scikit-learn.org/stable/user_guide.html

## 🤝 Contributing

To improve these notebooks:
1. Add more detailed explanations
2. Include additional visualizations
3. Add hyperparameter tuning examples
4. Expand MITRE ATT&CK analysis

## 📝 License

This educational material is provided for learning purposes. The CICIDS2017 dataset has its own license terms.

---

**Created by**: NetGuardian-AI Team  
**Last Updated**: January 2026  
**Version**: 1.0

🎉 **Happy Learning!** 🎉
