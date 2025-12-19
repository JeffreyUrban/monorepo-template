# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

This is a Python + TypeScript monorepo generated from [monorepo-template](https://github.com/{{cookiecutter.github_username}}/monorepo-template).

## Quick Start

```bash
# Install dependencies
uv sync

# Install Node dependencies (if you have TypeScript projects)
npm install

# Run tests
pytest
npm test  # For TypeScript projects
```

## Monorepo Structure

```
{{cookiecutter.project_slug}}/
├── apps/               # Applications (CLIs, web apps, etc.)
├── services/           # Backend services (APIs, workers, etc.)
├── packages/           # Shared libraries
├── data-pipelines/     # Data processing pipelines
├── .monorepo/          # Monorepo configuration
│   └── project-templates.yaml   # Template registry
├── scripts/            # Monorepo management scripts
├── pyproject.toml      # Python workspace configuration
└── package.json        # TypeScript workspace configuration
```

## Philosophy

**Strong Opinions** (reduces setup work):
- **Architecture**: Shared code lives in `packages/`, apps/services never import from each other
- **Tooling**: `uv` for Python, `npm` for TypeScript
- **Code style**: Single quotes, 120 char lines, type hints required
- **Git**: Single repository, all projects share git history

**Flexible** (doesn't assume too much):
- **Project types**: Add any combination of CLIs, APIs, web apps, pipelines
- **Languages**: Python-first, but supports TypeScript/JavaScript
- **Testing**: Each project can have its own test configuration

## Adding New Projects

Use the `add-project.py` script to add projects from templates:

```bash
# Add a Python CLI app
./scripts/add-project.py cli my-awesome-cli

# Add a Python API service
./scripts/add-project.py api user-service

# Add a React web app
./scripts/add-project.py web-react my-web-app

# Add a shared Python library
./scripts/add-project.py lib-python shared-utils
```

### Available Templates

Configure your templates in `.monorepo/project-templates.yaml`:

**Cookiecutter Templates** (Python):
- Python CLIs, APIs, web apps, libraries
- Interactive prompts for customization
- Automatically integrated into `uv` workspace

**GitHub Templates** (TypeScript/React):
- React apps, TypeScript libraries
- Direct repository clones
- Automatically integrated into `npm` workspace

See `.monorepo/project-templates.yaml` for configuration examples.

## Development Workflow

### Python Projects

```bash
# Activate virtual environment (optional, uv handles this automatically)
source .venv/bin/activate

# Run a specific project
cd apps/my-cli
python -m my_cli

# Run tests for a specific project
cd apps/my-cli
pytest

# Run tests for all Python projects
pytest

# Type checking
pyright

# Linting
ruff check .
ruff format .
```

### TypeScript Projects

```bash
# Run development server
cd apps/my-web-app
npm run dev

# Run tests
cd apps/my-web-app
npm test

# Type checking
npm run typecheck

# Linting
npm run lint

# Build for production
npm run build
```

## Working in Your IDE

### PyCharm / IntelliJ IDEA
- **Open**: Open the monorepo root directory
- **Python Interpreter**: PyCharm will auto-detect the `.venv` from uv
- **Run Configurations**: Create run configurations with working directory set to specific projects

### VS Code
- **Open**: Open the monorepo root directory
- **Python**: Select the `.venv/bin/python` interpreter
- **Multi-root**: Optionally use workspace feature to add individual projects

### WebStorm
- **Open**: Open the monorepo root directory
- **Node.js**: WebStorm will auto-detect workspace configuration
- **Run Configurations**: Use the provided `.run/*.run.xml` configurations (if present)

## Project Structure Guidelines

### Python Projects
```
apps/my-cli/
├── src/
│   └── my_cli/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_main.py
└── pyproject.toml
```

### TypeScript Projects
```
apps/my-web-app/
├── app/
│   ├── routes/
│   ├── components/
│   └── root.tsx
├── public/
├── package.json
└── tsconfig.json
```

## Shared Code (Packages)

Place shared code in `packages/`:

```bash
# Add a shared Python library
./scripts/add-project.py lib-python shared-utils

# Use it in other Python projects
# In pyproject.toml:
# dependencies = ["shared-utils"]

# Add a shared TypeScript library
./scripts/add-project.py lib-typescript ui-components

# Use it in other TypeScript projects
# In package.json:
# "dependencies": {"ui-components": "workspace:*"}
```

## Testing

### Python
```bash
# Run all tests
pytest

# Run tests for specific project
cd apps/my-cli
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_main.py
```

### TypeScript
```bash
# Run all tests in a project
cd apps/my-web-app
npm test

# Run tests in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage
```

## Continuous Integration

GitHub Actions workflows are configured at the monorepo level (`.github/workflows/`).

### Path Filtering

Workflows use path filters to run only when relevant files change:

```yaml
on:
  pull_request:
    paths:
      - 'apps/my-web-app/**'
      - 'packages/shared-utils/**'
```

### CI Workflow

The main CI workflow (`.github/workflows/ci.yml`) runs:
- Python: ruff, pyright, pytest
- TypeScript: eslint, typecheck, vitest

## Common Tasks

### Install Dependencies
```bash
# Python
uv sync

# TypeScript
npm install
```

### Update Dependencies
```bash
# Python - update all
uv lock --upgrade

# Python - update specific package
uv add package@latest

# TypeScript
npm update
```

### Clean Build Artifacts
```bash
# Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name "*.egg-info" -exec rm -rf {} +
find . -type d -name ".pytest_cache" -exec rm -rf {} +

# TypeScript
find . -type d -name "node_modules" -prune -o -type d -name "dist" -exec rm -rf {} +
find . -type d -name "build" -exec rm -rf {} +
```

### Add Git Hooks
```bash
# Install pre-commit hooks (if configured)
pre-commit install
```

## Troubleshooting

### Python Import Errors
```bash
# Ensure workspace is synced
uv sync

# Check if package is in workspace
uv pip list | grep package-name
```

### TypeScript Module Not Found
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install

# Rebuild
npm run build
```

### IDE Not Recognizing Imports
```bash
# Python: Restart PyCharm/VS Code and ensure .venv is selected
# TypeScript: Restart WebStorm/VS Code and reload window
```

## Contributing

### Adding a New Project

1. Add template configuration to `.monorepo/project-templates.yaml`
2. Run `./scripts/add-project.py <type> <name>`
3. Review generated code
4. Commit: `git add . && git commit -m "Add <name>"`

### Code Style

- **Python**: Follow PEP 8, enforced by ruff
- **TypeScript**: Follow ESLint rules
- **Formatting**: Use ruff (Python) and prettier (TypeScript)
- **Line length**: 120 characters
- **Quotes**: Single quotes preferred

### Commit Messages

Use conventional commits:
```
feat: add user authentication
fix: resolve login redirect issue
docs: update setup instructions
test: add tests for user service
refactor: extract common utilities
```

## License

{% if cookiecutter.license != "None" -%}
{{cookiecutter.license}}
{%- else -%}
See LICENSE file
{%- endif %}

## Maintainers

- {{cookiecutter.author_name}}{% if cookiecutter.author_email != "(optional)" %} <{{cookiecutter.author_email}}>{% endif %}
