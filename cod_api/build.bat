@echo off

cd /d %~dp0  :: Change directory to the location of this batch file
call ../venv/Scripts/activate  :: Activate the virtual environment
python -m build

mv dist/cod_api-2.0.2-py3-none-any.whl ../deps/.

pause
