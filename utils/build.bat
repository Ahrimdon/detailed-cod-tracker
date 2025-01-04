@echo off

cd /d %~dp0  :: Change directory to the location of this batch file
call ../venv/Scripts/activate  :: Activate the virtual environment
pyinstaller --noconfirm --onefile --console --icon "../assets/icon.ico" cod_api_tool.py --distpath="../build/bin" -n "cod_api_tool"

rmdir /s /q build
del /q "cod_api_tool.spec"

pause
