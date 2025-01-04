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

def setup_tools():
    subprocess.check_call([os.path.join('venv', 'Scripts', 'pip'), 'install', '--no-index', '--find-links=deps', 'pip', 'wheel', 'build', 'pyinstaller'])

def setup_api():
    wheel_path = os.path.join('deps', 'cod_api-2.0.2-py3-none-any.whl')
    subprocess.check_call([os.path.join('venv', 'Scripts', 'pip'), 'install', '--no-index', '--find-links=deps', wheel_path])

if __name__ == "__main__":
    if not deps_exists():
        print("Error: 'deps' directory does not exist!")
        exit(1)    

    print("Creating virtual environment...")
    create_venv()
    print("Setting up virtual environment...")
    setup_tools()
    setup_api()
    print("Setup complete.")