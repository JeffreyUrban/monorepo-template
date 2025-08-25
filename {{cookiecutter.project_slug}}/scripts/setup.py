#!/usr/bin/env python3
"""
Bootstrap the development environment.

• Installs Pants via scie-pants
• Generates lock files
• Runs initial test + lint to verify setup
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def run(cmd: str) -> None:
    print(f"→ {cmd}")
    if subprocess.call(cmd, shell=True, cwd=ROOT):
        sys.exit(1)

def main() -> None:
    # 1. Install scie-pants if missing
    run("curl -fsSL https://static.pantsbuild.org/scie-pants | bash -s -- -d .pants")
    run("./pants --version")

    # 2. Export virtualenvs / node modules
    run("./pants export ::")

    # 3. First-time quality gate
    run("./pants lint ::")
    run("./pants test ::")
    print("\n✓ Environment ready. Use `make dev` to start containers.")

if __name__ == "__main__":
    main()
