@echo off
:: Run script for QUIK Downloader on Windows

:: --- Check for venv ---
if not exist "venv\\Scripts\\activate.bat" (
    echo X ERROR: Virtual environment not found.
    echo Please run the 'install.bat' script first.
    pause
    exit /b 1
)

:: --- Activate venv and run ---
call venv\Scripts\activate.bat
python main.py

:: --- Deactivate on exit ---
deactivate
echo.
echo Application closed.
pause 