# Deployment Guide

This document explains how to **package, push, and run** a project generated
from *monorepo-template*.

---

## 1. Build Artifacts

| Artifact | Produced by | Purpose |
|----------|-------------|---------|
| **PEX files** (`*.pex`) | `./pants package` | Self-contained Python binaries |
| **Docker images** | `./pants package` + image targets | Runtime containers for services / ML models |
| **Static assets** | Front-end build (`apps/web:build`) | Files served by CDN or API gateway |

All artifacts are created with a single command:

```
./pants package ::
```

Only targets affected by the current change set are rebuilt, so the command
remains fast even in very large repos.

---

## 2. Environments

| Environment | Branch / Trigger | Deployment Target | Notes |
|-------------|------------------|-------------------|-------|
| **Preview** | Every PR         | *Docker-Compose*  | Runs on ephemeral CI runner |
| **Staging** | `develop`        | *Kubernetes* (`staging` namespace) | Mirrors production topology |
| **Production** | `main`        | *Kubernetes* (`prod` namespace)    | Blue-/-green deployments |

Environment mapping is hard-coded in `scripts/deploy.py` but can be overridden:

```
python scripts/deploy.py --target kubernetes --env staging
```

---

## 3. Docker Deployment (local & preview)

```
# Build and start locally
make build           # packages everything
make dev             # docker-compose up -d
```

Environment variables live in `.env` and are automatically loaded by
`docker-compose.yml`.

---

## 4. Kubernetes Deployment

1. Ensure the **context** points to the correct cluster / namespace.
2. Package all targets:

   ```
   ./pants package ::
   ```

3. Push images (script detects what changed):

   ```
   ./scripts/deploy.py --target kubernetes --env staging
   ```

4. Kubernetes manifests are in `infrastructure/kubernetes/<env>/`.
   They reference the `{{cookiecutter.project_slug}}` Docker images created by
   Pants.

---

## 5. Zero-Downtime Release Pattern

1. **Blue pod** (`v-current`) keeps serving traffic.
2. **Green pod** (`v-next`) is rolled out with the new image tag.
3. Health checks pass → traffic shifts to **green**.
4. Blue is scaled to zero.

The helper `kustomization.yaml` templates handle the label flips; no manual
patching required.

---

## 6. Rollbacks

```
kubectl rollout undo deployment/{{cookiecutter.project_slug}} --to-revision=N
```

or, for Docker:

```
docker compose down
git checkout <last-known-good>
make dev
```

---

## 7. Secrets & Config

| Store      | Use case                    |
|------------|----------------------------|
| **Kubernetes Secrets** | DB credentials, API keys           |
| **Vault / AWS Secrets Manager** | Long-lived production secrets |
| **.env file**          | Local development only             |

Never commit secrets: `.env`, `*.tfstate`, and `*.pem` are in `.gitignore`
by default.

---

## 8. CI/CD Integration

* GitHub Actions workflow (`.github/workflows/ci.yml`)  
  – Runs `lint`, `test`, `package`, then calls `scripts/deploy.py` on `main`.

* Self-hosted GPU runners (optional)  
  – Execute training jobs when files under `models/` change.

---

## 9. Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Pod `CrashLoopBackOff` | Missing env var | Check secret/ConfigMap mount |
| Image pull fails | Wrong tag | Ensure CI pushed latest digest |
| Service 502 | Health check path wrong | Update `readinessProbe` URL |

---

*Last updated: {{ cookiecutter._now.strftime('%Y-%m-%d') }}*
