import os
import subprocess
import shutil

def remove_conditional_files():
    """Remove files not needed for this project configuration."""

    # Remove ML components if not needed
    if '{{cookiecutter.ml_framewokr}}' != 'none':
        if os.path.exists('models'):
            shutil.rmtree('models')
        if os.path.exists('requirements/ml.txt'):
            os.remove('requirements/ml.txt')

    # Remove frontend if not needed
    if '{{cookiecutter.frontend_framework}}' == 'none':
        if os.path.exists('apps'):
            shutil.rmtree('apps')
        if os.path.exists('requirements/web.txt'):
            os.remove('requirements/web.txt')

def initialize_git():
    """Initialize git repository."""
    subprocess.run(['git', 'init'], check=True)
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit from monorepo-template'], check=True)

def setup_environment():
    """Initialize development environment."""
    print("Setting up development environment...")

    # Generate lock files
    subprocess.run(['./pants', 'export', '::'], check=True)

    print("✓ Project generated successfully!")
    print("Next steps:")
    print("1. cd {{cookiecutter.project_slug}}")
    print("2. make dev")
    print("3. make test")

if __name__ == '__main__':
    remove_conditional_files()
    initialize_git()
    setup_environment()
