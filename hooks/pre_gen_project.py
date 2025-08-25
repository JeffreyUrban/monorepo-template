import re
import sys

project_slug = '{{cookiecutter.project_slug}}'

if not re.match(r'^[a-z][a-z0-9-]*[a-z0-9]$', project_slug):
    print(f'ERROR: {project_slug} is not a valid project slug.')
    print('Project slug must be lowercase, start with letter, and contain only letters, numbers, and hyphens.')
    sys.exit(1)

if len(project_slug) > 50:
    print(f'ERROR: Project slug {project_slug} is too long (max 50 characters).')
    sys.exit(1)

# Validate combinations
include_pytorch = '{{cookiecutter.ml_framework}}' == 'pytorch'

print(f'✓ Generating project: {project_slug}')
