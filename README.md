# monorepo-template

**A Python + Typescript monorepo template that composes external project templates**

Unlike traditional monorepo templates that embed all project scaffolding, this template provides the monorepo *structure* and *tooling to add projects later* using your existing cookiecutter templates.

## Why This Exists

**The Problem**: You have separate cookiecutter templates for CLIs, APIs, web apps, etc. When creating a monorepo, you don't want to:
- Duplicate template code inside the monorepo template (sync nightmare)
- Abandon your standalone templates (you still create non-monorepo projects)
- Manually integrate new projects into monorepo conventions after generation

**This Solution**:
- Generate the monorepo skeleton (shared configs, tooling, directory structure)
- Reference your external templates in a manifest (`.monorepo/project-templates.yaml`)
- Add projects to the *living monorepo* using `scripts/add-project.py`
- Automatically integrate new projects with monorepo conventions via hooks

## Philosophy: Opinionated Where It Matters

**Strong Opinions** (reduces setup work):
- **Architecture**: Shared code lives in `packages/`, apps/services never import from each other
- **Tooling**: `uv` for package management, `ruff` for linting, `pyright` for type checking
- **Workspace structure**: `uv` workspaces with shared dependency constraints
- **Code style**: Single quotes, 120 char lines, type hints required

**Flexible** (doesn't assume too much):
- **Project types**: No assumptions about what apps/services/pipelines you need
- **Languages**: Python-first, but supports TypeScript/JavaScript projects
- **Database**: Write DB-agnostic SQLAlchemy code
- **Deployment**: Provide structure, but don't mandate Docker/K8s/etc.

## How It Works

### Initial Setup
```bash
# 1. Generate monorepo skeleton
cookiecutter gh:your-github-username/monorepo-template

# 2. Initialize development environment
cd my-monorepo
uv sync
```

### Adding Projects (Post-Generation)

The generated monorepo includes tooling to add projects using external templates:

```bash
# In your living, in-development monorepo:
./scripts/add-project.py cli my-awesome-cli
# → Pulls https://github.com/your-github-username/cli-template
# → Places in apps/my-awesome-cli/
# → Integrates with monorepo conventions (removes duplicate configs, creates workspace entry)

./scripts/add-project.py api user-service
# → Pulls https://github.com/your-github-username/api-template
# → Places in services/user-service/
# → Integrates automatically
```

**Template manifest** (`.monorepo/project-templates.yaml`):
```yaml
templates:
  cli:
    repo: "https://github.com/{{cookiecutter.github_username}}/cli-template"
    version: "main"
    target_dir: "apps"

  api:
    repo: "https://github.com/{{cookiecutter.github_username}}/api-template"
    version: "main"
    target_dir: "services"
```

**Integration hooks** (`.monorepo/integration-hooks/cli.py`):
```python
def integrate(project_path, monorepo_root):
    """Adapt external CLI template to monorepo conventions."""
    # Remove configs that should use monorepo shared versions
    remove_if_exists(project_path / "pyproject.toml")
    remove_if_exists(project_path / "ruff.toml")

    # Add to uv workspace
    add_workspace_member(monorepo_root, project_path)
```

## Monorepo Structure

```
my-monorepo/
├── .monorepo/
│   ├── project-templates.yaml       # Maps project types → external templates
│   └── integration-hooks/           # Post-processing per template type (optional)
│       ├── cli.py
│       └── api.py
├── scripts/
│   └── add-project.py               # Tool for adding projects
├── packages/                         # Shared code (ONLY place for cross-project imports)
│   └── shared-utils/
├── apps/                             # Applications (web, CLI, etc.)
├── services/                         # APIs, microservices
├── data-pipelines/                   # Data processing, ETL
├── pyproject.toml                    # Python workspace + shared configs
├── package.json                      # TypeScript workspace (for TS/JS projects)
├── ruff.toml                         # Shared Python linting config
└── pyrightconfig.json                # Shared Python type checking config
```

## Architecture Principles

### 1. No Cross-Dependencies Between Apps/Services/Pipelines

**Core Rule**: Apps, services, and pipelines NEVER import from each other. They ONLY import from `packages/`.

```python
# ❌ FORBIDDEN: App importing from another app
from apps.web.models import User

# ❌ FORBIDDEN: Service importing from pipeline
from data_pipelines.etl.utils import process

# ✅ CORRECT: Import from shared packages
from shared_db.models import User
```

**Why?** Prevents circular dependencies, enables independent deployment, maintains clear boundaries.

### 2. Shared Code Lives in packages/

Examples:
- `packages/shared-db/` - SQLAlchemy models, migrations
- `packages/shared-utils/` - Common utilities
- `packages/shared-types/` - Shared type definitions

Each app/service imports from packages but creates its own database engine, HTTP client, etc. with appropriate settings.

### 3. Hybrid Workspace Management (Python + TypeScript)

This template supports **polyglot monorepos** with both Python and TypeScript projects:

**Python workspace** (`pyproject.toml`):
- Managed by `uv`
- Auto-discovers projects with `pyproject.toml`
- Shared dev dependencies (ruff, pyright, pytest)
- Dependency version constraints across Python projects

**TypeScript workspace** (`package.json`):
- Managed by `npm`/`pnpm`/`yarn`
- Lists TypeScript projects in `workspaces` array
- Shared dependencies across TypeScript projects
- Each project has its own `package.json`

**Project detection is automatic**: `add-project.py` detects whether a project is Python or TypeScript and adds it to the appropriate workspace.

## Tooling

| Domain | Tool | Config Location |
|--------|------|-----------------|
| Package manager | `uv` | `pyproject.toml` |
| Linting | `ruff` | `ruff.toml` |
| Formatting | `ruff format` | `ruff.toml` |
| Type checking | `pyright` | `pyrightconfig.json` |
| Testing | `pytest` | Individual projects |
| CI/CD | GitHub Actions | `.github/workflows/` |

**Code Style**:
- Double quotes
- 120 character line limit
- Type hints required for function signatures
- Ruff rules: E, F, I (errors, pyflakes, isort)

## Quick Start

```bash
# Generate monorepo
cookiecutter gh:your-github-username/monorepo-template
cd my-monorepo

# Initialize
uv sync

# Add your first project
./scripts/add-project.py cli my-first-cli

# Run tests
pytest

# Lint
ruff check .

# Type check
pyright
```

## Comparison with Alternatives

| Approach | Initial Setup | Add Project Later | Template Sync | Use Case |
|----------|--------------|-------------------|---------------|----------|
| **This template** | Monorepo skeleton | External template + auto-integration | No sync needed (references external) | Living monorepos that grow over time |
| **Cookie Composer** | Compose multiple templates | Manual | Manual | One-time monorepo generation |
| **Embedded sub-templates** | Monorepo with embedded templates | Use embedded template | Sync both repos | Monorepo-only projects |
| **Manual integration** | Empty monorepo | Copy + manual integration | N/A | Full control, high effort |

**Key Differentiator**: This template optimizes for *post-generation workflow* - adding projects to an existing, evolving monorepo while maintaining external templates as single source of truth.

## Prerequisites

```bash
# macOS
brew install cookiecutter uv

# Linux
pip install cookiecutter
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Configuration

After generating the monorepo, update `.monorepo/project-templates.yaml` with your actual template repositories:

```yaml
templates:
  cli:
    repo: "https://github.com/{{cookiecutter.github_username}}/cli-template"
    version: "main"  # Git branch (typically "main" for latest)
    target_dir: "apps"
    description: "CLI application template"
```

Create integration hooks in `.monorepo/integration-hooks/` to adapt external templates to your monorepo conventions.

## Documentation

- **Architecture decisions**: Document in root `README.md` or `docs/architecture.md`
- **Development setup**: `docs/development.md`
- **Testing practices**: `docs/testing.md`
- **Database schema**: `docs/schema.md` (if using shared database models)

## License

MIT
