#!/usr/bin/env python3
"""
Pre-commit hook to test cookiecutter template generation.

This script tests that the cookiecutter template can be generated successfully
without Jinja2 syntax errors or other issues.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def test_template_generation():
    """Test that the cookiecutter template generates successfully."""
    print("Testing cookiecutter template generation...")

    # Get the repository root
    repo_root = Path(__file__).parent.parent.resolve()

    # Create temporary directory for test generation
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Test parameters (same as used in CI)
        test_params = {
            "project_name": "Test Monorepo",
            "project_description": "A test monorepo for pre-commit validation",
            "author_name": "Test Author",
            "github_username": "testuser",
        }

        # Build cookiecutter command
        cmd = ["cookiecutter", str(repo_root), "--no-input", "--output-dir", str(tmp_path)]
        for key, value in test_params.items():
            cmd.extend([f"{key}={value}"])

        # Run cookiecutter
        print(f"  Running: {' '.join(cmd[:4])} ...")
        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                cwd=tmp_path,
            )
            print("  ✓ Template generated successfully")
        except subprocess.CalledProcessError as e:
            print(f"\n✗ Template generation failed!")
            print(f"\nStdout:\n{e.stdout}")
            print(f"\nStderr:\n{e.stderr}")
            return False

        # Find the generated project directory
        generated_dirs = list(tmp_path.iterdir())
        if not generated_dirs:
            print("✗ No project directory was generated")
            return False

        project_dir = generated_dirs[0]
        print(f"  Generated project at: {project_dir.name}")

        # Run ruff check on generated code
        print("  Running ruff check on generated code...")
        try:
            subprocess.run(
                ["ruff", "check", str(project_dir)],
                check=True,
                capture_output=True,
                text=True,
            )
            print("  ✓ Ruff check passed")
        except subprocess.CalledProcessError as e:
            print(f"\n✗ Ruff check failed!")
            print(f"\nStdout:\n{e.stdout}")
            print(f"\nStderr:\n{e.stderr}")
            print("\nHint: You can auto-fix most issues by running:")
            print(f"  cookiecutter . --no-input && cd test-monorepo && ruff check --fix .")
            return False
        except FileNotFoundError:
            print("  ⚠ Ruff not found, skipping lint check")
            print("    Install ruff with: pip install ruff")

        print("\n✓ All template generation tests passed!")
        return True


def main():
    """Main entry point."""
    success = test_template_generation()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
