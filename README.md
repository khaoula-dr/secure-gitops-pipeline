# demo-api — Application de démo pour le projet GitOps/ArgoCD/Kustomize

Petite API Flask servant  de "repo application" pour le projet GitOps décrit dans le
cahier des charges. Elle expose volontairement des endpoints distincts pour la
liveness probe et la readiness probe, pour démontrer la différence en Kubernetes.

## Endpoints

| Route | Rôle |
|---|---|
| `GET /` | Message de bienvenue + nom/version de l'app |
| `GET /health` | **Liveness probe** — le process répond-il ? |
| `GET /ready` | **Readiness probe** — l'app est-elle prête à recevoir du trafic ? |
| `GET /info` | Métadonnées (version, hostname, timestamp) — utile pour vérifier visuellement quel tag d'image est déployé après un déploiement GitOps |

## Lancer en local (sans Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python app.py
# API disponible sur http://localhost:8080
```

## Lancer les tests

```bash
pytest -v
```

## Builder et lancer avec Docker

```bash
docker build -t demo-api:local .
docker run -p 8080:8080 -e APP_VERSION=local-test demo-api:local
```

Ou plus simple, avec Docker Compose :

```bash
docker compose up --build
```

Puis tester :
```bash
curl http://localhost:8080/health
curl http://localhost:8080/info
```

## Points de sécurité déjà en place dans l'image (pertinents pour le scan Trivy/Checkov)

- Build **multi-stage** : les outils de build ne se retrouvent pas dans l'image finale
- Base image **slim** (`python:3.12-slim`) pour réduire la surface d'attaque
- Exécution avec un **utilisateur non-root** (`USER app`)
- Pas de secret, pas de credential en dur dans le code ou l'image
- `HEALTHCHECK` défini explicitement dans le Dockerfile

## Prochaine étape

Ce repo doit être poussé sur GitHub et connecté au pipeline GitHub Actions
(Gitleaks → Semgrep → build → Trivy → push GHCR → mise à jour de l'overlay
Kustomize dans le repo infra), comme décrit dans le cahier des charges.
