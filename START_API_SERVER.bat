@echo off
echo ========================================
echo  JCAMP PYTHON BACKTEST API SERVER
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python or add it to PATH.
    pause
    exit /b 1
)

echo Starting API Server...
echo Server will be available at: http://localhost:8000
echo.
cd /d D:\JcampFxTrading\jcamp-python-backtesting
python scripts\start_api_server.py

echo.
echo API Server stopped.
pause
