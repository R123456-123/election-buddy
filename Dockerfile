# =============================================================
# Dockerfile — Election Buddy (Cloud Run Optimized)
# =============================================================
# Multi-stage thinking but kept single-stage for Streamlit
# simplicity. Uses slim base to minimize image size.
# =============================================================

FROM python:3.12-slim

# Prevent Python from writing bytecode and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cloud Run injects PORT; Streamlit reads from .streamlit/config.toml
ENV PORT=8080

# Set working directory
WORKDIR /app

# Install dependencies first (cached layer if requirements.txt unchanged)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Expose the port Cloud Run will route to
EXPOSE 8080

# Health check for Cloud Run
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8080/_stcore/health || exit 1

# Run Streamlit — headless mode, no file watcher, port 8080
ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8080", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--server.fileWatcherType=none"]
