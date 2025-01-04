@echo off

cd /d %~dp0  :: Change directory to the location of this batch file
call ../venv/Scripts/activate  :: Activate the virtual environment
pyinstaller --noconfirm --onefile --console --icon "../assets/icon.ico" get_cod_stats.py --distpath="../build/bin" -n "get_cod_stats"

rmdir /s /q build
del /q "get_cod_stats.spec"

pause