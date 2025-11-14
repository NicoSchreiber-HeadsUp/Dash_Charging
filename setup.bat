REM -------------------------SETUP OF NEW PYTHON PROJECTS -------------------------------
@echo off

REM -------------------------------INITIALIZATION----------------------------------------
SETLOCAL ENABLEEXTENSIONS
SET PYTHON_VERSION=3.13.5
SET VENV_DIR=.venv
cd /d "%~dp0"

REM ---------------------VIRTUAL-ENVIRONMENT---------------------------------------------
echo Create virtual environment in: %VENV_DIR%
powershell.exe python -m venv "%VENV_DIR%"
IF %ERRORLEVEL% NEQ 0 (
    echo Virtual environment could not be installed
    pause
    exit /b 1
)
echo Virtual environment has been created

REM ----------------------PIP-AND-PACKAGES-----------------------------------------------
echo Activate virtual environment, upgrade PIP and install required python packages
call "%VENV_DIR%\Scripts\activate.bat"
echo Environment activated
python.exe -m pip install --upgrade pip
echo PIP has been upgraded
pip install -r requirements.txt
echo Requirements have been installed
echo Setup successful