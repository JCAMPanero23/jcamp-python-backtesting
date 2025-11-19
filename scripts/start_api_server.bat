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
echo Starting API server...
echo.

cd "%~dp0.."
python scripts\start_api_server.py

pause
