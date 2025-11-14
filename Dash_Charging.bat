@echo off
SETLOCAL ENABLEEXTENSIONS
cd /d "%~dp0"

REM === Activate virtual environment ===
if not exist ".venv\Scripts\activate.bat" (
    echo Virtual environment not found. Please run the setup script first.
    pause
    exit /b 1
)

call ".venv\Scripts\activate.bat"

REM === Run the app with venv's Python ===
REM Using full path to ensure we use the venv's interpreter
".venv\Scripts\python.exe" dash_charging.py >log.txt 2>&1

REM === Show log output if something went wrong ===
IF %ERRORLEVEL% NEQ 0 (
    echo Application exited with error %ERRORLEVEL%.
    echo --- LOG START ---
    type log.txt
    echo --- LOG END ---
)

pause