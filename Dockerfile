# =============================================================================
# SmartStore — Dockerfile
# Builds a lightweight production image for the Streamlit app.
#
# Usage (local):
#   docker build -t smartstore .
#   docker run -p 8501:8501 smartstore
#   → open http://localhost:8501
#
# Usage (Azure Container Apps / Azure Container Instances):
#   az acr build --registry <your-acr-name> --image smartstore:latest .
# =============================================================================

# ─── Base Image ───────────────────────────────────────────────────────────────
FROM python:3.11-slim

# Metadata
LABEL maintainer="DebDev25"
LABEL description="SmartStore AI — Multi-role e-commerce app with ML features"
LABEL org.opencontainers.image.source="https://github.com/DebDev25/E-Comm-Site"
LABEL org.opencontainers.image.url="https://hub.docker.com/r/debdev25/smartstore"

# ─── System Dependencies ──────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# ─── App User (never run as root in production) ───────────────────────────────
RUN useradd -m -s /bin/bash appuser

# ─── Working Directory ────────────────────────────────────────────────────────
WORKDIR /app

# ─── Python Dependencies (install before copying code for layer caching) ──────
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ─── Copy Application Code ────────────────────────────────────────────────────
COPY . .

COPY .streamlit/config.toml /app/.streamlit/config.toml

# ─── Ownership ────────────────────────────────────────────────────────────────
RUN chown -R appuser:appuser /app
USER appuser

# ─── Port ─────────────────────────────────────────────────────────────────────
EXPOSE 8501

# ─── Health Check ─────────────────────────────────────────────────────────────
# Azure Load Balancer / Container Apps probe will use this
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8501/ || exit 1

# ─── Entrypoint ───────────────────────────────────────────────────────────────
ENTRYPOINT ["streamlit", "run", "app.py", \
            "--server.port=8501", \
            "--server.address=0.0.0.0", \
            "--server.headless=true"]
