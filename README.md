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
- Auto-generate JetBrains IDE run configurations based on project scripts

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
cookiecutter gh:JeffreyUrban/monorepo-template

# 2. Initialize development environment
cd my-monorepo
uv sync
```

**Input Requirements**: The template validates all inputs before generation. Here's what's expected:

- **project_name**: Your project's display name (max 100 characters)
- **project_slug**: Lowercase letters, numbers, and hyphens only (e.g., `my-monorepo`, `caption-ai`)
  - Must start with a letter and end with a letter or number
  - The template auto-generates a valid slug from your project name
  - Max 50 characters
- **project_description**: Brief description of your monorepo (max 500 characters)
- **author_name**: Your name (not the default placeholder)
- **author_email**: Valid email format (or leave as "(optional)")
- **github_username**: Your GitHub username (1-39 chars, alphanumeric and single hyphens only)
- **python_version**: Version in format "X.Y" (e.g., "3.11", "3.12"), must be 3.9 or higher

If validation fails, you'll see helpful error messages with suggestions for fixing the issues.

### Adding Projects (Post-Generation)

The generated monorepo includes tooling to add projects using external templates. **Supports both Cookiecutter templates and GitHub template repositories**:

```bash
# Add Python project from cookiecutter template
./scripts/add-project.py cli my-awesome-cli
# → Runs cookiecutter with your CLI template
# → Places in apps/my-awesome-cli/
# → Integrates with monorepo conventions

# Add React app from GitHub template repository
./scripts/add-project.py web-react my-web-app
# → Clones GitHub template directly
# → Places in apps/my-web-app/
# → Integrates automatically
```

**Template Types**:
- **Cookiecutter**: Interactive templates with variable prompts (Python projects)
- **GitHub Templates**: Direct repository clones (TypeScript/React projects)

**Automatic IDE Setup**:

For TypeScript/JavaScript projects, run configurations are automatically generated for JetBrains IDEs (WebStorm, IntelliJ IDEA, PyCharm):

```
# After adding a project:
./scripts/add-project.py web-react frontend-app

# Automatically creates:
.run/frontend-app__Dev_Server.run.xml
.run/frontend-app__Build.run.xml
.run/frontend-app__Tests.run.xml
.run/frontend-app__Lint.run.xml
# ... and more based on package.json scripts

# In IDE dropdown you'll see:
# - frontend-app: Dev Server
# - frontend-app: Build
# - frontend-app: Tests
# - frontend-app: Lint
```

The script detects available npm scripts (`dev`, `build`, `test`, `lint`, `typecheck`, etc.) and creates corresponding run configurations automatically.

**Template manifest** (`.monorepo/project-templates.yaml`):
```yaml
templates:
  # Cookiecutter templates (Python)
  cli:
    template_type: "cookiecutter"
    repo: "https://github.com/{{cookiecutter.github_username}}/cli-template"
    version: "main"
    target_dir: "apps"

  api:
    template_type: "cookiecutter"
    repo: "https://github.com/{{cookiecutter.github_username}}/api-template"
    version: "main"
    target_dir: "services"

  # GitHub template repositories (TypeScript/React)
  web-react:
    template_type: "github-template"
    repo: "https://github.com/{{cookiecutter.github_username}}/web-react-router-template"
    version: "main"
    target_dir: "apps"
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
