import os
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)

APP_NAME = os.environ.get("APP_NAME", "demo-api")
APP_VERSION = os.environ.get("APP_VERSION", "dev")

# Secret monté en fichier par Kubernetes (Sealed Secrets), chemin standard
# pour un Secret monté en volume. Fallback sur une variable d'environnement
# pour permettre l'exécution locale hors cluster (docker-compose, tests).
API_KEY_FILE = os.environ.get("API_KEY_FILE", "/etc/secrets/API_KEY")


def load_api_key():
    """Lit le secret depuis le fichier monté par Kubernetes.
    Ne jamais logguer ni exposer la valeur elle-même."""
    try:
        with open(API_KEY_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return os.environ.get("API_KEY")


API_KEY = load_api_key()


@app.get("/")
def root():
    return jsonify(
        {
            "app": APP_NAME,
            "version": APP_VERSION,
            "message": "Bienvenue sur l'API de démo GitOps",
        }
    )


@app.get("/health")
def health():
    """Liveness probe : le process répond-il encore ?
    Kubernetes redémarre le pod si ce endpoint échoue."""
    return jsonify({"status": "ok"}), 200


@app.get("/ready")
def ready():
    """Readiness probe : l'app est-elle prête à recevoir du trafic ?
    Kubernetes retire le pod du Service (sans le redémarrer) si ce endpoint échoue.
    Ici on pourrait vérifier une connexion DB, un cache, etc."""
    return jsonify({"status": "ready"}), 200


@app.get("/info")
def info():
    return jsonify(
        {
            "app": APP_NAME,
            "version": APP_VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "hostname": os.uname().nodename,
            # Jamais la valeur du secret : juste une confirmation qu'il a
            # été chargé avec succès, utile pour vérifier le déploiement
            # sans jamais exposer de donnée sensible via l'API.
            "api_key_loaded": API_KEY is not None,
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("FLASK_DEV_HOST", "127.0.0.1")
    app.run(host=host, port=port)
# demo rollback US 6.1
# trigger 1791131234