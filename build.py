import os
import sys
import shutil
import subprocess
import PyInstaller.__main__

# Initialize constants
SCRIPT = "refactor.py"
ICON = "assets/icon.ico"
NAME = "cod_api_tool"
DIST_PATH = "bin/build"

# Get absolute paths to data files
script_dir = os.path.abspath(os.path.dirname(__file__))
charset_normalizer_data = os.path.join('deps', 'frequencies.json')
replacements_json = os.path.join(script_dir, 'data', 'replacements.json')

# Verify replacements.json exists before building
if not os.path.exists(replacements_json):
    print(f"ERROR: {replacements_json} not found. Make sure this file exists.")
    sys.exit(1)

# Activate the virtual environment
venv_activation_script = os.path.join(os.getcwd(), 'venv', 'Scripts', 'activate')
subprocess.call(venv_activation_script, shell=True)

# Run PyInstaller
PyInstaller.__main__.run([
    SCRIPT,
    '--name', NAME,
    '--noconfirm',
    '--onefile',
    '--console',
    '--icon', ICON,
    '--distpath', DIST_PATH,
    # This is the correct way to add the data file - preserve the directory structure
    '--add-data', f"{charset_normalizer_data};charset_normalizer/assets",
    '--add-data', f"{replacements_json};data"  # Note: using 'data' as the destination folder
])

# Clean up the build directory and spec file
shutil.rmtree('build')
os.remove(f'{NAME}.spec')

print(f"Build completed successfully. Executable is in {DIST_PATH}/{NAME}.exe")
input("Press Enter to continue...")