@echo off
title Streamlit App Launcher

:: Set the path to your project (modify this!)
set PROJECT_DIR=E:\Streamlit\local-math-assistant

:: Navigate to the project directory
cd /d "%PROJECT_DIR%"

echo.
echo Checking for virtual environment...
echo.

:: Activate the virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate
) else (
    echo Virtual environment not found. Using global Python environment.
    echo (Consider running 'python -m venv venv' and 'pip install streamlit')
)

echo.

echo.
echo Starting Streamlit app...
echo Press Ctrl+C to stop the server.
echo.

:: Run the Streamlit app
streamlit run plotter.py
echo.
echo Streamlit app closed.
pause