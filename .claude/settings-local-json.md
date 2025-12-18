# settings.local.json Philosophy

## Purpose

The `.claude/settings.local.json` file pre-approves common commands so Claude Code can work efficiently without constantly asking for permission. The goal is to **eliminate friction** while maintaining reasonable safety boundaries.

## Philosophy

### Be Liberal, Not Conservative

**Optimize for developer productivity, not theoretical purity.**

- If Claude uses a command frequently (even if it "should" use a different tool), approve it
- If a tool is common in monorepo development, approve it
- The cost of repeated permission prompts > risk of approved safe commands
- Don't enforce best practices through permissions - that's what guidance files are for

### Template vs Generated Monorepo

**Template repo** (`monorepo-template`):
- `.claude/settings.local.json` is committed and distributed
- Contains minimal permissions needed for template maintenance
- Includes: cookiecutter, basic git, uv workspace operations, basic testing
- Allows all Edit/Write/Read for template development

**Generated monorepos** (from template):
- Start with comprehensive `settings.local.json` from template
- Users customize for their specific monorepo needs
- Pre-populated with everything likely needed for monorepo development
- Can be gitignored or committed based on team preference

## What to Include

### 1. **File Operations**
Allow unrestricted file operations for development:
```json
"Edit",    // Allow all file edits
"Write",   // Allow all file writes
"Read"     // Allow all file reads
```

### 2. **Monorepo-Specific Tools**
Approve tools for managing monorepos:
```json
"Bash(uv sync:*)",           // Workspace synchronization
"Bash(uv add:*)",            // Add dependencies
"Bash(uv remove:*)",         // Remove dependencies
"Bash(uv run:*)",            // Run commands in workspace
"Bash(./scripts/add-project.py:*)",  // Add projects from external templates
```

### 3. **Quality Tools**
If the template includes it, approve related commands:
- Template uses ruff → approve `ruff check`, `ruff format`
- Template uses pyright → approve `pyright`
- Template uses pytest → approve all pytest variants
- Template uses uv → approve all uv commands

### 4. **Common Development Tools**
Approve tools commonly used in monorepo development:
- Shell: `sed`, `awk`, `echo`, `printf`, `grep`, `find`
- JSON/YAML: `jq`, `yamllint`
- Version control: All common git commands, all gh (GitHub CLI) commands
- Testing: All pytest variants, coverage
- Workspace: Directory navigation, file operations

### 5. **File Path Patterns**
Use wildcards for common patterns:
```json
"Bash(/tmp/*)",
"Bash(apps/**)",
"Bash(services/**)",
"Bash(packages/**)",
"Bash(data-pipelines/**)",
"Bash(tests/**)",
"Bash(*.log)"
```

### 6. **Environment Variables**
Approve common test/debug patterns:
```json
"Bash(CI=1 pytest:*)",
"Bash(NO_COLOR=1 *)",
"Bash(COLUMNS=* *)",
"Bash(SKIP=* pre-commit run:*)"
```

### 7. **Shell Constructs**
Claude uses these despite guidance to avoid - approve them:
```json
"Bash(echo:*)",
"Bash(printf:*)",
"Bash(for:*)",
"Bash(while read:*)",
"Bash(done)"
```

## What to Exclude/Deny

### Safety Boundaries

**Deny destructive operations:**
```json
"deny": [
  "Bash(brew install:*)",    // System modifications
  "Bash(brew uninstall:*)",
  "Bash(rm -rf:*)",          // Bulk deletion
  "Bash(sudo:*)"             // Privilege escalation
]
```

**Exclude localhost/development servers:**
```json
// Don't approve by default:
"WebFetch(domain:127.0.0.1)",
"WebFetch(domain:localhost)"
```

**Project-specific accumulated paths:**
Don't pre-approve hundreds of specific fixture files, output files, etc. These accumulate naturally as users work and approve them individually.

## Sources of Truth

When building settings.local.json for a monorepo, reference:
1. **This template's dependencies** - Check root `pyproject.toml` for workspace tools
2. **Existing monorepos** - Look at settings from mature monorepos (shoukan, etc.)
3. **Common patterns** - Workspace operations, cross-project testing, shared tooling
4. **Template structure** - Directory organization, script organization

## Maintenance

**For template repo (`monorepo-template`):**
- Keep minimal - only what's needed for template development
- Include monorepo-specific tools (uv workspace commands, add-project.py)
- Allow Edit/Write/Read for unrestricted template editing

**For generated monorepos:**
- Start comprehensive - include everything likely needed
- Users customize for their specific needs (polyglot vs Python-only, etc.)
- Accumulate project-specific permissions over time
- Team decides whether to commit or gitignore

## Example Workflow

When a new common tool/pattern emerges:
1. Notice repeated permission prompts across multiple monorepos
2. Identify if it's generally useful or monorepo-specific
3. If general: Add to template's settings.local.json
4. If monorepo-specific: User adds to their local settings
5. Template changes distribute to new monorepos only (existing monorepos don't auto-update)

## Monorepo-Specific Considerations

**Multi-project testing:**
- Approve pytest patterns that work across multiple projects
- Allow running tests in specific directories: `pytest apps/`, `pytest packages/`

**Workspace operations:**
- Approve all uv workspace commands (sync, add, remove)
- Allow cross-project dependency updates

**Integration scripts:**
- Pre-approve `scripts/add-project.py` and other monorepo management scripts
- Allow cookiecutter (used by add-project.py)

**Template development:**
- Template repos need unrestricted file operations (Edit/Write/Read)
- This allows rapid iteration on template structure and configuration
