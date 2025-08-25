# Developer Handbook

Follow these steps to get coding in minutes.

---

## 1. Prerequisites

* **Python {{cookiecutter.python_version}}**
* **Docker Desktop** (or Podman)
* **Node 18+** *(only if `include_frontend = y`)*
* **scie-pants** (installed automatically by `scripts/setup.py`)

---

## 2. First-Time Setup

```
git clone <repo>
cd {{cookiecutter.project_slug}}
python scripts/setup.py        # installs Pants & exports virtualenvs
make dev                       # starts local stack (DB, Redis, etc.)
```

Your IDE can point to the exported virtual-envs located in
`dist/export/python/virtualenv/`.

---

## 3. Everyday Commands

| Task | Command |
|------|---------|
| Run **tests** | `make test` |
| **Lint / type-check** | `make lint` |
| **Format** code | `make format` |
| **Start** services | `make dev` |
| **Hot-reload** API | Gunicorn auto-reloader provided via `uvicorn` |
| **Run a script** | `./pants run path/to:target` |

All commands are wrappers around Pants targets; anything Pants can do you can
also run directly.

---

## 4. Adding Code

### New shared utility
```
mkdir -p packages/shared-utils/src/{{cookiecutter.project_slug}}/utils/foo
touch packages/shared-utils/src/{{cookiecutter.project_slug}}/utils/foo/__init__.py
echo "python_sources()" >> packages/shared-utils/BUILD
```

### New API endpoint
1. Add FastAPI route under `services/main/src/.../api.py`.
2. Write tests in `services/main/tests/`.
3. Run `make test`.

### New ML model *(if enabled)*
```
pants tailor models/awesome-model::
# Generates BUILD stubs automatically
```

---

## 5. Dependency Management

* **`requirements/*.txt`** are single-source-of-truth.  
  Separate lockfiles for default, web, and ML resolves.
* Add PyPI packages to the appropriate file, then
  ```
  ./pants generate-lockfiles --resolve=<name>
  ```
* Node dependencies live under each app’s `package.json`.

---

## 6. Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Production releases |
| `develop` | Integration / staging |
| `feature/*` | Short-lived feature branches |
| `experiment/*` | ML research branches |

All PRs must pass **lint + tests** and include a CODEOWNERS-approved review.

---

## 7. Editor Integrations

* **VS Code**  
  – Enable *Pylance* for type checking, *Black* / *Ruff* extensions for linting.

* **PyCharm**  
  – Set the interpreter to `<repo>/dist/export/python/virtualenv/python-default`.

* **WebStorm** *(if frontend present)*  
  – Use workspace Node interpreter in `.pants.d/node`.

---

## 8. Common Issues

| Error | Fix |
|-------|-----|
| `ImportError: cannot import name ...` | `make install` to regenerate exports |
| Pants “missing lockfile” | `./pants generate-lockfiles --resolve=<name>` |
| Front-end **500** talking to API | Check CORS settings in `settings.py` |

---

Happy hacking!  
*Last updated: {{ cookiecutter._now.strftime('%Y-%m-%d') }}*
