@echo off
setlocal enabledelayedexpansion

echo ===================================================================
echo               NazarSetu - Autonomous Civic Action Platform         
echo ===================================================================
echo.

cd /d "%~dp0"

REM 1. Check Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in your PATH.
    echo Please install Python 3.10+ from https://python.org and add it to PATH.
    pause
    exit /b 1
)

REM 2. Setup Virtual Environment
if not exist "venv\Scripts\activate.bat" (
    echo [*] Creating virtual environment 'venv'...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM 3. Activate Virtual Environment
call "venv\Scripts\activate.bat"

REM 4. Install Dependencies
echo [*] Checking dependencies...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

REM 5. Initialize environment file if missing
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo [*] Initialized .env configuration file (Offline Fallback Mode).
    )
)

echo.
echo [*] Starting NazarSetu on http://localhost:8501 ...
echo [i] Press Ctrl+C in this terminal window to stop the server.
echo.

streamlit run app.py
pause
