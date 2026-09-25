# syntax=docker/dockerfile:1

# ---------- Stage 1 : build des dépendances ----------
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Stage 2 : image d'exécution minimale ----------
FROM python:3.12-slim

# Utilisateur non-root : requis par les règles de sécurité K8s (US 4.1 du cahier des charges)
RUN addgroup --system app && adduser --system --ingroup app --home /home/app app

WORKDIR /app

# On ne copie que les dépendances installées, pas les outils de build
COPY --from=builder /install /usr/local
COPY app.py .

USER app

EXPOSE 8080

# Healthcheck local (utile en docker-compose ; en K8s, les probes du Deployment prennent le relais)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--access-logfile", "-", "app:app"]
