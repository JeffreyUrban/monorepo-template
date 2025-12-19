#!/usr/bin/env python3
"""Pre-generation hook for monorepo-template"""

import re
import sys


def suggest_valid_slug(slug: str) -> str:
    """Generate a valid project slug suggestion from an invalid one."""
    # Remove invalid characters (keep only a-z, 0-9, -)
    suggested = re.sub(r"[^a-z0-9-]", "-", slug.lower())

    # Replace multiple consecutive hyphens with single hyphen
    suggested = re.sub(r"-+", "-", suggested)

    # Remove leading hyphens and non-letters
    suggested = re.sub(r"^[^a-z]+", "", suggested)

    # Remove trailing hyphens
    suggested = suggested.rstrip("-")

    # If empty or doesn't start with letter, prepend 'my'
    if not suggested or not suggested[0].isalpha():
        suggested = "my-" + suggested

    # If still invalid, provide a default
    if not suggested or not re.match(r"^[a-z][a-z0-9-]*[a-z0-9]$", suggested):
        suggested = "my-project"

    return suggested


def validate_email(email: str) -> bool:
    """Validate email format."""
    # Basic email validation
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_github_username(username: str) -> bool:
    """Validate GitHub username format."""
    # GitHub username rules:
    # - May only contain alphanumeric characters or single hyphens
    # - Cannot begin or end with a hyphen
    # - Maximum 39 characters
    if len(username) == 0 or len(username) > 39:
        return False
    if username.startswith("-") or username.endswith("-"):
        return False
    if "--" in username:
        return False
    return bool(re.match(r"^[a-zA-Z0-9-]+$", username))


def validate_python_version(version: str) -> bool:
    """Validate Python version format."""
    # Accept formats like "3.11", "3.12", "3.13", etc.
    if not re.match(r"^\d+\.\d+$", version):
        return False

    # Parse major.minor
    parts = version.split(".")
    major, minor = int(parts[0]), int(parts[1])

    # Must be Python 3.9 or higher
    if major != 3 or minor < 9:
        return False

    return True


# Get cookiecutter variables
project_name = "{{cookiecutter.project_name}}"
project_slug = "{{cookiecutter.project_slug}}"
project_description = "{{cookiecutter.project_description}}"
author_name = "{{cookiecutter.author_name}}"
author_email = "{{cookiecutter.author_email}}"
github_username = "{{cookiecutter.github_username}}"
python_version = "{{cookiecutter.python_version}}"

errors = []

# Validate project_name
if not project_name or project_name.strip() == "":
    errors.append("Project name cannot be empty.")
elif project_name == "My Monorepo":
    errors.append("Please provide a custom project name (not the default 'My Monorepo').")
elif len(project_name) > 100:
    errors.append(f"Project name is too long ({len(project_name)} characters, max 100).")

# Validate project_slug
if not re.match(r"^[a-z][a-z0-9-]*[a-z0-9]$", project_slug):
    errors.append(f"Project slug '{project_slug}' is invalid.")
    errors.append("  • Must be lowercase")
    errors.append("  • Must start with a letter")
    errors.append("  • Must contain only letters, numbers, and hyphens")
    errors.append("  • Must end with a letter or number (not a hyphen)")
    suggested = suggest_valid_slug(project_slug)
    errors.append(f"  Suggested: '{suggested}'")
elif len(project_slug) > 50:
    errors.append(f"Project slug '{project_slug}' is too long ({len(project_slug)} characters, max 50).")

# Validate project_description
if not project_description or project_description.strip() == "":
    errors.append("Project description cannot be empty.")
elif project_description == "A brief description of this monorepo":
    errors.append("Please provide a custom project description (not the default text).")
elif len(project_description) > 500:
    errors.append(f"Project description is too long ({len(project_description)} characters, max 500).")

# Validate author_name
if not author_name or author_name.strip() == "":
    errors.append("Author name cannot be empty.")
elif author_name == "Your Name":
    errors.append("Please provide your actual name (not the default 'Your Name').")

# Validate author_email
if author_email and author_email not in ("(optional)", ""):
    if not validate_email(author_email):
        errors.append(f"Author email '{author_email}' is not a valid email address.")

# Validate github_username
if not github_username or github_username.strip() == "":
    errors.append("GitHub username cannot be empty.")
elif github_username == "your-github-username":
    errors.append("Please provide your actual GitHub username (not the default 'your-github-username').")
elif not validate_github_username(github_username):
    errors.append(f"GitHub username '{github_username}' is invalid.")
    errors.append("  • Must be 1-39 characters")
    errors.append("  • May only contain alphanumeric characters or single hyphens")
    errors.append("  • Cannot begin or end with a hyphen")

# Validate python_version
if not validate_python_version(python_version):
    errors.append(f"Python version '{python_version}' is invalid.")
    errors.append("  • Must be in format 'X.Y' (e.g., '3.11', '3.12')")
    errors.append("  • Must be Python 3.9 or higher")

# Print errors and exit if any
if errors:
    print("\n" + "=" * 60)
    print("VALIDATION ERRORS")
    print("=" * 60)
    for error in errors:
        print(error)
    print("=" * 60)
    print("\nPlease run cookiecutter again with valid inputs.")
    sys.exit(1)

print(f"✓ Generating monorepo: {project_slug}")
