@echo off
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Creating venv...
    python -m venv venv
)

call venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip uninstall pytest-selenium -y 2>nul

echo.
echo Running tests...
python -m pytest -v
pause
