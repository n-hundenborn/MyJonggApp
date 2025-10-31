@echo off
echo Building MyJongg Calculator for Windows...
echo.

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build the executable
pyinstaller --log-level=INFO app.spec

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Build successful!
    echo Executable location: dist\MyJongg Calculator.exe
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Build failed! Check errors above.
    echo ========================================
)

pause


