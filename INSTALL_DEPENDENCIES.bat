@echo off
REM ===============================================
REM   Install Python Dependencies
REM ===============================================
REM This script installs all required Python packages
REM

echo.
echo ========================================
echo Installing Super Mario Game Dependencies
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/
    echo.
    echo IMPORTANT: During installation, check:
    echo   [x] Add Python to PATH
    echo.
    pause
    exit /b 1
)

echo [✓] Python found!
python --version
echo.

echo Installing packages...
echo.

REM Install pygame
echo [1/2] Installing pygame...
pip install pygame
if errorlevel 1 (
    echo ERROR: Failed to install pygame
    pause
    exit /b 1
)
echo [✓] pygame installed!
echo.

REM Install pyinstaller (optional, for EXE building)
echo [2/2] Installing pyinstaller (for building EXE)...
pip install pyinstaller
if errorlevel 1 (
    echo WARNING: Failed to install pyinstaller
    echo You can still run the game with Python, but won't be able to build EXE
    echo.
)
echo [✓] pyinstaller installed!
echo.

echo.
echo ========================================
echo All dependencies installed successfully!
echo ========================================
echo.
echo You can now:
echo   1. Run the game: python super_mario_game.py
echo   2. Build EXE: BUILD_EXE.bat
echo.
pause
