@echo off
echo Starting IT Asset Management System...
echo.

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the application
python run.py

:: Deactivate virtual environment when the application closes
call venv\Scripts\deactivate.bat

echo.
echo Application closed.
pause
