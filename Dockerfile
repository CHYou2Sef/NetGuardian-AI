# Dockerfile pour NetGuardian-AI Dashboard
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY src/ ./src/
COPY app/ ./app/
COPY config/ ./config/
COPY models/ ./models/

# Créer les répertoires nécessaires
RUN mkdir -p logs data

# Exposer le port Streamlit
EXPOSE 8501

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Commande de démarrage
CMD ["streamlit", "run", "app/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
