import os
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)

APP_NAME = os.environ.get("APP_NAME", "demo-api")
APP_VERSION = os.environ.get("APP_VERSION", "dev")


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
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
