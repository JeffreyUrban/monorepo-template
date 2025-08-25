# monorepo-template
A production-intent monorepo template for fullstack + machine learning projects built with python backends, typescript frontends, and ML workflows.

Supports: API services, full-stack apps, ML pipelines

## Prerequisites

On macOS:

    brew install cookiecutter

## Quick start

1. Generate a project


    cookiecutter gh:your-github/monorepo-template

2. Bootstrap dev environment


    cd {{ cookiecutter.project_slug }}
    python scripts/setup.py    # installs Pants + exports virtualenvs
    make dev                   # docker-compose up -d

3. Iterate


    make test                  # run all tests
    make lint                  # ruff + mypy
    make build                 # packages PEXes / Docker images

See **docs/development.md** for the full developer handbook.

---

## Repo layout

```
services/           ← application code (API, worker, CLI, etc.)
packages/           ← shared libraries (imported everywhere)
apps/               ← web front-ends 
models/             ← ML training + inference 
data/               ← ETL / feature pipelines 
infrastructure/     ← Docker, K8s, Terraform
docs/               ← project documentation
```

Each directory contains its own `BUILD` file so Pants can build and test targets
independently.

---

## Toolchain

| Domain       | Tool |
|--------------|------|
| Build        | **Pants** |
| Python deps  | Multiple lockfiles via Pants resolves |
| JS/TS build  | Node + Nx |
| Formatting   | Black, Ruff |
| Type checking| Mypy, TypeScript |
| Testing      | Pytest, Jest |
| Containers   | Pants Docker targets |
| CI/CD        | GitHub Actions |
| ML workflow  | MLflow, GPU Dockerfiles |

---

## Deployment workflow

1. `make build` → build PEX & Docker images  
2. `python scripts/deploy.py --target docker` or `--target kubernetes`  
3. GitHub Actions runs the same steps on `main` after tests pass.

Detailed instructions live in **docs/deployment.md**.
