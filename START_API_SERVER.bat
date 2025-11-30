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

echo Clearing Python cache...
cd /d D:\JcampFxTrading\jcamp-python-backtesting
python -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__') if p.exists()]"
echo Cache cleared.
echo.
echo Starting API Server...
echo Server will be available at: http://localhost:8000
echo.
python scripts\start_api_server.py

echo.
echo API Server stopped.
pause
