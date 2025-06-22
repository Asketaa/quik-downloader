@echo off
title QUIK Downloader - Installation
:: Installation script for QUIK Downloader on Windows

echo.
echo ========================================
echo    QUIK Downloader Installer
echo ========================================
echo.

:: --- Check for Python ---
echo [1/3] Checking for Python...
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [X] ERROR: Python is not installed or not in PATH.
    echo     Please install Python from https://python.org
    echo.
    echo Press any key to exit...
    pause >nul
    goto :end
)

echo [OK] Python found.

:: --- Create Virtual Environment ---
echo.
echo [2/3] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo.
    echo [X] ERROR: Failed to create virtual environment.
    echo.
    echo Press any key to exit...
    pause >nul
    goto :end
)
echo [OK] Virtual environment created.

:: --- Activate and Install Requirements ---
echo.
echo [3/3] Installing requirements...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [X] ERROR: Failed to install required packages.
    echo.
    echo Press any key to exit...
    pause >nul
    goto :end
)

echo [OK] Requirements installed successfully.
call deactivate

echo.
echo ========================================
echo    INSTALLATION SUCCESSFUL!
echo ========================================
echo.
echo You can now run the application by
echo double-clicking the 'run.bat' file.
echo.
echo Press any key to close this window...
pause >nul

:end 