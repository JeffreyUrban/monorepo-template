#!/usr/bin/env python3
"""
Add Project Tool - Integrate external cookiecutter templates into this monorepo

This script:
1. Reads .monorepo/project-templates.yaml to find template configuration
2. Runs cookiecutter with the external template
3. Places the generated project in the appropriate directory
4. Integrates it with monorepo conventions (removes duplicate configs, adds to workspace)

Usage:
    ./scripts/add-project.py <template-type> <project-name>

    Example:
        ./scripts/add-project.py cli my-awesome-cli
        ./scripts/add-project.py api user-service
        ./scripts/add-project.py lib shared-utils

Configuration:
    Add your template URLs to .monorepo/project-templates.yaml

Integration:
    This script includes inline integration logic. You can:
    - Customize the integrate() function below for your needs
    - Create separate integration hooks in .monorepo/integration-hooks/
    - Extend the script to support more complex workflows
"""

import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


def load_template_config(monorepo_root: Path) -> dict[str, Any]:
    """Load project template configuration from .monorepo/project-templates.yaml"""
    config_path = monorepo_root / ".monorepo" / "project-templates.yaml"

    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}")
        print("Please create .monorepo/project-templates.yaml with your template URLs")
        sys.exit(1)

    with open(config_path) as f:
        config = yaml.safe_load(f)

    if not config or "templates" not in config:
        print(f"Error: No templates defined in {config_path}")
        print("Add template configurations to the 'templates' section")
        sys.exit(1)

    return config["templates"]


def run_cookiecutter(template_config: dict[str, Any], project_name: str, target_dir: Path) -> Path:
    """Run cookiecutter with the external template"""
    repo = template_config["repo"]
    version = template_config.get("version", "main")

    print(f"Generating project from template: {repo} @ {version}")
    print(f"Target directory: {target_dir}")

    # Build cookiecutter command
    cmd = [
        "cookiecutter",
        repo,
        f"--checkout={version}",
        f"--output-dir={target_dir}",
    ]

    # Add defaults if provided
    if "defaults" in template_config:
        cmd.append("--no-input")
        # Pass defaults as extra context
        for key, value in template_config["defaults"].items():
            cmd.append(f"{key}={value}")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running cookiecutter: {e}")
        sys.exit(1)

    # Find the generated project directory
    # If integrate_path is specified, use it to locate the specific subdirectory
    if "integrate_path" in template_config:
        integrate_path_template = template_config["integrate_path"]
        # Replace {project_slug} placeholder with actual project slug
        # Cookiecutter converts project_name to slug (lowercase, hyphens)
        project_slug = project_name.lower().replace(" ", "-").replace("_", "-")
        integrate_path = integrate_path_template.replace("{project_slug}", project_slug)

        # The integrate_path is relative to target_dir, not the generated directory
        # For example: "test-cli-workspace/test-cli"
        full_path = target_dir / integrate_path
        if full_path.exists():
            print(f"  Using integrate_path: {integrate_path}")
            return full_path
        else:
            print(f"Warning: integrate_path '{integrate_path}' not found at {full_path}")
            # Fall back to finding the generated directory
            generated_dirs = [d for d in target_dir.iterdir() if d.is_dir() and project_slug in d.name.lower()]
            if generated_dirs:
                return generated_dirs[0]
            else:
                print(f"Warning: Could not find generated project in {target_dir}")
                return target_dir

    # Default behavior: find directory matching project name
    generated_dirs = [d for d in target_dir.iterdir() if d.is_dir() and project_name.lower() in d.name.lower()]

    if not generated_dirs:
        print(f"Warning: Could not automatically find generated project in {target_dir}")
        print("You may need to manually integrate the project")
        return target_dir

    return generated_dirs[0]


def move_nested_project(project_path: Path, target_dir: Path) -> Path:
    """
    Move a nested project to the target directory and clean up wrapper.

    For example:
    - Input: apps/test-cli-workspace/test-cli
    - Output: apps/test-cli
    - Cleanup: Remove apps/test-cli-workspace
    """
    import shutil

    # Only move if project_path has a parent directory that isn't the target_dir
    if project_path.parent != target_dir:
        final_path = target_dir / project_path.name

        # If final path already exists, remove it first
        if final_path.exists():
            shutil.rmtree(final_path)

        # Move the project directory
        shutil.move(str(project_path), str(final_path))
        print(f"  Moved {project_path.relative_to(target_dir)} → {final_path.name}")

        # Clean up the wrapper directory if it's now empty or only contains other projects
        wrapper_dir = project_path.parent
        if wrapper_dir.exists() and wrapper_dir != target_dir:
            try:
                # Try to remove - will fail if not empty, which is fine
                remaining = list(wrapper_dir.iterdir())
                if remaining:
                    print(f"  Cleaned up wrapper directory, skipping non-empty: {wrapper_dir.name}")
                else:
                    shutil.rmtree(wrapper_dir)
                    print(f"  Removed empty wrapper directory: {wrapper_dir.name}")
            except OSError:
                pass  # Directory not empty, that's ok

        return final_path

    return project_path


def integrate_project(project_path: Path, monorepo_root: Path) -> Path:
    """
    Integrate the generated project with monorepo conventions.

    This function demonstrates the integration pattern. Customize based on your needs.

    Common integration tasks:
    1. Detect project type (Python vs TypeScript)
    2. Remove duplicate configs (use monorepo's shared configs instead)
    3. Add to appropriate workspace (uv for Python, npm/pnpm for TypeScript)
    4. Update workspace configuration
    """
    print(f"\nIntegrating {project_path.name} into monorepo...")

    # 1. Detect project type
    has_pyproject = (project_path / "pyproject.toml").exists()
    has_package_json = (project_path / "package.json").exists()

    if has_pyproject and has_package_json:
        print("  Detected: Hybrid project (Python + TypeScript)")
        project_type = "hybrid"
    elif has_pyproject:
        print("  Detected: Python project")
        project_type = "python"
    elif has_package_json:
        print("  Detected: TypeScript project")
        project_type = "typescript"
    else:
        print("  Warning: Unknown project type (no pyproject.toml or package.json)")
        project_type = "unknown"

    # 2. Remove duplicate configuration files for Python projects
    if project_type in ["python", "hybrid"]:
        duplicate_configs = [
            "ruff.toml",
            ".ruff.toml",
            "pyrightconfig.json",
            ".pyrightconfig.json",
        ]

        for config_file in duplicate_configs:
            config_path = project_path / config_file
            if config_path.exists():
                print(f"  Removing duplicate config: {config_file}")
                config_path.unlink()

    # 3. Add to workspace
    if project_type in ["python", "hybrid"]:
        print("  Python project will be auto-discovered by uv workspace (glob patterns in pyproject.toml)")

    if project_type in ["typescript", "hybrid"]:
        # Add to npm/pnpm workspace
        import json

        package_json_path = monorepo_root / "package.json"
        if package_json_path.exists():
            with open(package_json_path) as f:
                package_data = json.load(f)

            # Get relative path from monorepo root
            relative_path = project_path.relative_to(monorepo_root)

            # Add to workspaces array if not already present
            if "workspaces" not in package_data:
                package_data["workspaces"] = []

            workspace_path = str(relative_path)
            if workspace_path not in package_data["workspaces"]:
                package_data["workspaces"].append(workspace_path)
                print(f"  Added to npm/pnpm workspace: {workspace_path}")

                # Write updated package.json
                with open(package_json_path, "w") as f:
                    json.dump(package_data, f, indent=2)
                    f.write("\n")  # Add trailing newline

    print("  ✓ Integration complete!")

    # 4. Update workspaces
    print("\nUpdating workspaces...")

    if project_type in ["python", "hybrid"]:
        try:
            subprocess.run(["uv", "sync"], cwd=monorepo_root, check=True, capture_output=True)
            print("  ✓ Python workspace synced (uv)")
        except subprocess.CalledProcessError:
            print("  Warning: Failed to run 'uv sync' - you may need to run it manually")

    if project_type in ["typescript", "hybrid"]:
        # Try npm install (will use pnpm/yarn if configured)
        try:
            subprocess.run(["npm", "install"], cwd=monorepo_root, check=True, capture_output=True)
            print("  ✓ TypeScript workspace synced (npm)")
        except subprocess.CalledProcessError:
            print("  Warning: Failed to run 'npm install' - you may need to run it manually")


def main() -> None:
    """Main entry point"""
    if len(sys.argv) != 3:
        print("Usage: ./scripts/add-project.py <template-type> <project-name>")
        print("\nExample:")
        print("  ./scripts/add-project.py cli my-awesome-cli")
        print("  ./scripts/add-project.py api user-service")
        print("\nAvailable templates are defined in .monorepo/project-templates.yaml")
        sys.exit(1)

    template_type = sys.argv[1]
    project_name = sys.argv[2]

    # Find monorepo root
    monorepo_root = Path(__file__).parent.parent.absolute()

    # Load template configuration
    templates = load_template_config(monorepo_root)

    if template_type not in templates:
        print(f"Error: Template type '{template_type}' not found in configuration")
        print(f"\nAvailable templates: {', '.join(templates.keys())}")
        sys.exit(1)

    template_config = templates[template_type]

    # Determine target directory
    target_dir_name = template_config.get("target_dir", "packages")
    target_dir = monorepo_root / target_dir_name

    if not target_dir.exists():
        print(f"Creating directory: {target_dir}")
        target_dir.mkdir(parents=True)

    # Run cookiecutter
    project_path = run_cookiecutter(template_config, project_name, target_dir)

    # Move nested project if needed (extract from workspace wrapper)
    if "integrate_path" in template_config:
        project_path = move_nested_project(project_path, target_dir)

    # Integrate with monorepo
    integrate_project(project_path, monorepo_root)

    print(f"\n✓ Project '{project_name}' added successfully!")
    print(f"  Location: {project_path.relative_to(monorepo_root)}")
    print("\nNext steps:")
    print(f"  1. cd {project_path.relative_to(monorepo_root)}")
    print("  2. Review the generated code")
    print("  3. Run tests: pytest")
    print(f"  4. Commit: git add . && git commit -m 'Add {project_name}'")


if __name__ == "__main__":
    main()
