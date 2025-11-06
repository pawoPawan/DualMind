@echo off
REM DualMind AI Chatbot Management Script for Windows
REM This is a wrapper that calls the PowerShell script

REM Check if PowerShell is available
where powershell >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: PowerShell is not available on this system.
    echo Please install PowerShell or use the dualmind.ps1 script directly.
    exit /b 1
)

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0

REM Call the PowerShell script with all arguments
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%dualmind.ps1" %*

