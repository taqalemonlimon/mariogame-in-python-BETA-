@echo off
REM ===============================================
REM   Super Mario Game - Build EXE
REM ===============================================
REM This script converts the Python game to a Windows .EXE file
REM
REM REQUIREMENTS:
REM   - Python 3.7 or higher
REM   - PyInstaller: pip install pyinstaller
REM   - PyGame: pip install pygame
REM
REM INSTRUCTIONS:
REM   1. Open Command Prompt (CMD)
REM   2. Navigate to the game folder
REM   3. Double-click this BUILD_EXE.bat file OR run: BUILD_EXE.bat
REM   4. Wait for the build to complete
REM   5. Your .EXE will be in the "dist" folder
REM
REM ===============================================

echo.
echo ========================================
echo Super Mario Game - Building EXE
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
python --version
echo.

REM Check if PyInstaller is installed
echo [2/4] Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo WARNING: PyInstaller not found!
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)
echo PyInstaller found!
echo.

REM Check if pygame is installed
echo [3/4] Checking pygame...
pip show pygame >nul 2>&1
if errorlevel 1 (
    echo WARNING: pygame not found!
    echo Installing pygame...
    pip install pygame
    if errorlevel 1 (
        echo ERROR: Failed to install pygame
        pause
        exit /b 1
    )
)
echo pygame found!
echo.

REM Build the EXE
echo [4/4] Building EXE file...
echo This may take 1-2 minutes...
echo.

pyinstaller --onefile ^
    --windowed ^
    --name "SuperMario" ^
    --icon "logo.ico" ^
    --add-data "MARIO.png:." ^
    --add-data "block.png:." ^
    --add-data "coin.png:." ^
    --add-data "monster.png:." ^
    --add-data "cloude.png:." ^
    --add-data "AHHH.png:." ^
    --add-data "nintendo.png:." ^
    --add-data "logo.ico:." ^
    --distpath "dist" ^
    --buildpath "build" ^
    --specpath "." ^
    super_mario_game.py

echo.
echo.

if exist "dist\SuperMario.exe" (
    echo.
    echo ========================================
    echo SUCCESS! EXE Created!
    echo ========================================
    echo.
    echo Your game is ready: dist\SuperMario.exe
    echo.
    echo You can now:
    echo   1. Run the game: dist\SuperMario.exe
    echo   2. Share it with friends
    echo   3. Create a shortcut for easy access
    echo.
    pause
) else (
    echo.
    echo ========================================
    echo ERROR: Build failed!
    echo ========================================
    echo Check the error messages above
    echo.
    pause
    exit /b 1
)
