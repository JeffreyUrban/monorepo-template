#!/usr/bin/env python3
"""
Simple deployment orchestrator.

Usage:
    python scripts/deploy.py --target docker
    python scripts/deploy.py --target kubernetes --env staging
"""
import argparse
import subprocess
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

def run(cmd: str, cwd: Path | None = None) -> None:
    """Run a shell command and stream output."""
    print(f"→ {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd or ROOT)
    if result.returncode:
        sys.exit(result.returncode)

def deploy_docker() -> None:
    run("./pants package ::")
    run("docker compose -f docker-compose.yml up -d")

def deploy_kubernetes(env: str) -> None:
    run("./pants package ::")
    k8s_dir = ROOT / "infrastructure" / "kubernetes" / env
    run(f"kubectl apply -f {k8s_dir}")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=["docker", "kubernetes"], required=True)
    parser.add_argument("--env", default="prod", help="k8s namespace / directory")
    args = parser.parse_args()

    match args.target:
        case "docker":
            deploy_docker()
        case "kubernetes":
            deploy_kubernetes(args.env)

if __name__ == "__main__":
    main()
