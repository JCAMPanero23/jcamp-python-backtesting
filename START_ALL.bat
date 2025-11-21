@echo off
echo ========================================
echo  JCAMP FOREX BACKTESTING SYSTEM
echo ========================================
echo.
echo Starting API Server...
start "JCAMP API Server" cmd /k "cd /d D:\JcampFxTrading\jcamp-python-backtesting && python scripts\start_api_server.py"

echo Waiting for API server to start...
timeout /t 3 /nobreak > nul

echo Starting Monitor App...
start "JCAMP Monitor App" cmd /k "cd /d D:\JcampFxTrading\CSMMonitor && dotnet run --project JcampForexTrader\JcampForexTrader.csproj"

echo.
echo Both services started!
echo - API Server: http://localhost:8000
echo - Monitor App: Running in separate window
echo.
pause
