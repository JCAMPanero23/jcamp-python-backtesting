@echo off
echo ========================================
echo  JCAMP FOREX BACKTESTING SYSTEM
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python or add it to PATH.
    pause
    exit /b 1
)

REM Start API Server
echo [1/2] Starting Python API Server...
start "JCAMP API Server" cmd /k "cd /d D:\JcampFxTrading\jcamp-python-backtesting && python scripts\start_api_server.py"

REM Wait for API server to initialize
echo [2/2] Waiting for API server to start (3 seconds)...
timeout /t 3 /nobreak > nul

REM Check if executable exists
set EXE_DIR=D:\JcampFxTrading\CSMMonitor\JcampForexTrader\bin\Debug\net8.0-windows
set EXE_PATH=%EXE_DIR%\JcampForexTrader.exe

if exist "%EXE_PATH%" (
    echo Starting C# Monitor App (pre-built executable)...
    cd /d "%EXE_DIR%"
    start "" "%EXE_PATH%"
) else (
    echo Executable not found. Building and running with dotnet...
    echo This may take a moment...
    start "JCAMP Monitor App" cmd /k "cd /d D:\JcampFxTrading\CSMMonitor && dotnet run --project JcampForexTrader\JcampForexTrader.csproj"
)

echo.
echo ========================================
echo  BOTH SERVICES STARTED!
echo ========================================
echo - API Server: http://localhost:8000
echo - Monitor App: Running in separate window
echo.
echo Close this window to continue.
echo ========================================
pause
