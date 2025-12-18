#!/usr/bin/env python3
"""Pre-generation hook for monorepo-template"""

import re
import sys

project_slug = "{{cookiecutter.project_slug}}"

# Validate project slug format
if not re.match(r"^[a-z][a-z0-9-]*[a-z0-9]$", project_slug):
    print(f"ERROR: {project_slug} is not a valid project slug.")
    print("Project slug must be lowercase, start with letter, and contain only letters, numbers, and hyphens.")
    sys.exit(1)

if len(project_slug) > 50:
    print(f"ERROR: Project slug {project_slug} is too long (max 50 characters).")
    sys.exit(1)

print(f"✓ Generating monorepo: {project_slug}")
