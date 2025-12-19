#!/usr/bin/env python3
"""Post-generation hook for monorepo-template"""

import subprocess
import sys
from pathlib import Path


def handle_license():
    """Remove LICENSE file if 'None' license was selected."""
    license_choice = "{{cookiecutter.license}}"

    if license_choice == "None":
        license_file = Path("LICENSE")
        if license_file.exists():
            license_file.unlink()
            print("Removed LICENSE file (None selected)")


def initialize_git():
    """Initialize git repository with initial commit."""
    print("Initializing git repository...")
    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from monorepo-template"],
            check=True,
        )
        print("✓ Git repository initialized")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to initialize git: {e}")
        print("You can manually run: git init && git add . && git commit -m 'Initial commit'")


def setup_environment():
    """Set up development environment with uv."""
    print("\nSetting up development environment...")

    # Check if uv is installed
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: 'uv' is not installed")
        print("Install it with: brew install uv  (or see https://github.com/astral-sh/uv)")
        sys.exit(1)

    # Initialize uv workspace
    try:
        subprocess.run(["uv", "sync"], check=True)
        print("✓ Development environment set up")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to run 'uv sync': {e}")
        print("You can manually run: uv sync")


def print_next_steps():
    """Print helpful next steps for the user."""
    print("\n" + "=" * 60)
    print("✓ Monorepo '{{cookiecutter.project_slug}}' generated successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. cd {{cookiecutter.project_slug}}")
    print("  2. Configure .monorepo/project-templates.yaml with your template URLs")
    print("  3. Add your first project:")
    print("       ./scripts/add-project.py <template-type> <project-name>")
    print("\nUseful commands:")
    print("  uv sync              # Update workspace dependencies")
    print("  ruff check .         # Lint code")
    print("  pyright              # Type check")
    print("  pytest               # Run tests")
    print("\nDocumentation:")
    print("  README.md            # Overview and usage")
    print("  .monorepo/           # Template configuration")
    print("  scripts/             # Monorepo management scripts")
    print()


if __name__ == "__main__":
    handle_license()
    initialize_git()
    setup_environment()
    print_next_steps()
