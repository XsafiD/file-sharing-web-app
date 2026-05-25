@echo off
REM Webshare FastAPI Startup Script for Windows
REM Usage: start.bat [dev|prod]

setlocal enabledelayedexpansion

REM Configuration
set VENV_DIR=venv
set PYTHON_CMD=python
set APP_MODULE=app.main:app

REM Parse arguments
set MODE=%1
if "%MODE%"=="" set MODE=prod

echo ======================================
echo 🚀 Webshare FastAPI Server
echo ======================================
echo.

REM Check if venv exists
if not exist "%VENV_DIR%" (
    echo [WARNING] Virtual environment not found
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv %VENV_DIR%
    echo [OK] Virtual environment created
    echo.
)

REM Activate venv
echo Activating virtual environment...
call %VENV_DIR%\Scripts\activate.bat

REM Check if requirements are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [WARNING] Dependencies not installed
    echo Installing dependencies...
    pip install -q -r requirements.txt
    echo [OK] Dependencies installed
    echo.
)

REM Create data folder if not exists
if not exist "data" (
    echo Creating 'data' folder...
    mkdir data
    echo [OK] Data folder created
    echo.
)

REM Run server based on mode
if "%MODE%"=="dev" (
    echo [DEV] Starting in DEVELOPMENT mode...
    echo.
    uvicorn %APP_MODULE% --host 0.0.0.0 --port 8080 --reload
) else (
    echo [PROD] Starting in PRODUCTION mode...
    echo.
    uvicorn %APP_MODULE% --host 0.0.0.0 --port 8080 --workers 4 --log-level info
)

pause
