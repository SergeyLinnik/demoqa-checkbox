@echo off
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Creating venv...
    python -m venv venv
)

call venv\Scripts\activate.bat
python -m pip install -r requirements.txt

echo.
echo Running demo...
python main.py
pause
