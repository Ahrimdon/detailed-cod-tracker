import os
import subprocess
import venv

def deps_exists():
    return os.path.exists('deps')

def create_venv():
    venv.create('venv', with_pip=True)
    # Create activation scripts
    with open("venv.ps1", "w") as f:
        f.write("venv\\Scripts\\Activate.ps1")

    with open("venv.bat", "w") as f:
        f.write("venv\\Scripts\\activate")

def upgrade_pip():
    subprocess.check_call([os.path.join('venv', 'Scripts', 'python'), '-m', 'pip', 'install', '--upgrade', 'pip'])

def install_wheel():
    subprocess.check_call([os.path.join('venv', 'Scripts', 'pip'), 'install', '--no-index', '--find-links=deps', 'wheel'])

def install_requirements_in_venv():
    # Use the full path to the wheel file
    wheel_path = os.path.join('src', 'cod_api-2.0.1-py3-none-any.whl')
    subprocess.check_call([os.path.join('venv', 'Scripts', 'pip'), 'install', '--no-index', '--find-links=deps', wheel_path]) 

if __name__ == "__main__":
    if not deps_exists():
        print("Error: 'deps' directory does not exist!")
        exit(1)    

    print("Creating virtual environment...")
    create_venv()
    print("Upgrading pip...")
    upgrade_pip()
    print("Installing wheel...")
    install_wheel()
    print("Installing packages in the virtual environment...")
    install_requirements_in_venv()  # Call the function to install the requirements
    print("Setup complete.")