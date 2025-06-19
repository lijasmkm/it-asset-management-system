@echo off
echo ===================================================
echo IT Asset Management System Installer
echo Version 1.0.0
echo ===================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment.
    echo Please make sure you have Python 3.8+ installed with venv module.
    echo.
    pause
    exit /b 1
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment.
    echo.
    pause
    exit /b 1
)

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies.
    echo.
    pause
    exit /b 1
)

:: Create directories
echo Creating necessary directories...
mkdir exports 2>nul
mkdir templates 2>nul
mkdir backups 2>nul
mkdir reports 2>nul

:: Create desktop shortcut
echo Creating desktop shortcut...
echo @echo off > "%USERPROFILE%\Desktop\IT Asset Management.bat"
echo cd /d "%~dp0" >> "%USERPROFILE%\Desktop\IT Asset Management.bat"
echo call venv\Scripts\activate.bat >> "%USERPROFILE%\Desktop\IT Asset Management.bat"
echo python run.py >> "%USERPROFILE%\Desktop\IT Asset Management.bat"
echo pause >> "%USERPROFILE%\Desktop\IT Asset Management.bat"

:: Create start menu shortcut
echo Creating start menu shortcut...
if not exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\IT Asset Management" (
    mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\IT Asset Management"
)
echo @echo off > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\IT Asset Management\IT Asset Management.bat"
echo cd /d "%~dp0" >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\IT Asset Management\IT Asset Management.bat"
echo call venv\Scripts\activate.bat >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\IT Asset Management\IT Asset Management.bat"
echo python run.py >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\IT Asset Management\IT Asset Management.bat"
echo pause >> "%APPDATA%\Microsoft\Windows\Start Menu\Programs\IT Asset Management\IT Asset Management.bat"

:: Initialize database
echo Initializing database...
python -c "from src.config.database import db_config; db_config.initialize_database()"
if %errorlevel% neq 0 (
    echo ERROR: Failed to initialize database.
    echo.
    pause
    exit /b 1
)

echo.
echo ===================================================
echo Installation completed successfully!
echo.
echo Default login credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo You can start the application using:
echo   1. Desktop shortcut "IT Asset Management"
echo   2. Start menu shortcut "IT Asset Management"
echo   3. Run "run.bat" in the installation directory
echo ===================================================
echo.
pause
