@echo off
REM Start JCAMP Backtesting API Server (Windows)

echo ====================================================================== 
echo   JCAMP BACKTESTING API SERVER
echo ======================================================================
echo.

REM Check if virtual environment exists
if exist "%~dp0..\venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%~dp0..\venv\Scripts\activate.bat"
) else (
    echo Warning: Virtual environment not found
    echo Using system Python...
)

echo.
echo Clearing Python cache...
cd "%~dp0.."
python -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__') if p.exists()]"
echo Cache cleared.
echo.
echo Starting API server...
echo.

python scripts\start_api_server.py

pause
