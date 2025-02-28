#!/usr/bin/env python3
"""
Setup script for Modern Warfare 2019 Advanced Statistics Tracker.
Creates a virtual environment and installs required dependencies.
"""

import os
import subprocess
import sys
import venv
from pathlib import Path


def check_dependencies():
    """Check if the dependencies directory exists."""
    deps_dir = Path('deps')
    if not deps_dir.exists():
        print("Error: 'deps' directory not found!")
        print("Please ensure the dependencies directory exists before running setup.")
        sys.exit(1)
    return deps_dir


def create_virtual_environment():
    """Create and configure a Python virtual environment."""
    print("Creating virtual environment...")
    venv_dir = Path('venv')
    
    # Create the virtual environment with pip
    venv.create(venv_dir, with_pip=True)
    
    # Create activation scripts for different platforms
    scripts = {
        "venv.ps1": "venv\\Scripts\\Activate.ps1",
        "venv.bat": "venv\\Scripts\\activate",
        "venv.sh": "source venv/bin/activate"  # Added for Unix/Linux users
    }
    
    for filename, content in scripts.items():
        with open(filename, "w") as f:
            f.write(content)
    
    return venv_dir


def get_pip_path(venv_dir):
    """Get the platform-specific path to pip in the virtual environment."""
    if sys.platform == 'win32':
        return venv_dir / 'Scripts' / 'pip'
    return venv_dir / 'bin' / 'pip'


def install_packages(pip_path, deps_dir):
    """Install required packages from the local dependencies directory."""
    print("Installing base packages...")
    base_packages = ['pip', 'wheel', 'build', 'pyinstaller']
    subprocess.check_call([
        str(pip_path), 'install', 
        '--no-index', 
        f'--find-links={deps_dir}',
        *base_packages
    ])
    
    print("Installing COD API package...")
    cod_api_wheel = 'cod_api-2.0.2-py3-none-any.whl'
    subprocess.check_call([
        str(pip_path), 'install',
        '--no-index',
        f'--find-links={deps_dir}',
        str(deps_dir / cod_api_wheel)
    ])


def clean_environment(pip_path):
    """Remove deprecated or conflicting packages."""
    print("Removing deprecated packages...")
    deprecated_packages = ['enum34']
    subprocess.check_call([
        str(pip_path), 'uninstall', *deprecated_packages, '-y'
    ])


def main():
    """Main setup function."""
    print("Starting setup for Modern Warfare 2019 Statistics Tracker...")
    
    # Check for dependencies directory
    deps_dir = check_dependencies()
    
    # Create and configure the virtual environment
    venv_dir = create_virtual_environment()
    
    # Get the appropriate pip path
    pip_path = get_pip_path(venv_dir)
    
    # Install required packages
    install_packages(pip_path, deps_dir)
    
    # Clean up environment
    clean_environment(pip_path)
    
    print("\nSetup completed successfully!")
    print(f"To activate the virtual environment, run:")
    if sys.platform == 'win32':
        print("  - PowerShell: .\\venv.ps1")
        print("  - Command Prompt: venv.bat")
    else:
        print("  - Bash/Zsh: source venv.sh")


if __name__ == "__main__":
    main()