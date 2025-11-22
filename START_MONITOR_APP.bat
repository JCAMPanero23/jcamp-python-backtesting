@echo off
echo ========================================
echo  JCAMP FOREX MONITOR APP
echo ========================================
echo.

REM Check if executable exists
set EXE_DIR=D:\JcampFxTrading\CSMMonitor\JcampForexTrader\bin\Debug\net8.0-windows
set EXE_PATH=%EXE_DIR%\JcampForexTrader.exe

if exist "%EXE_PATH%" (
    echo Starting Monitor App (pre-built executable)...
    echo.
    cd /d "%EXE_DIR%"
    "%EXE_PATH%"
) else (
    echo Executable not found at:
    echo %EXE_PATH%
    echo.
    echo Building and running with dotnet...
    echo This may take a moment...
    echo.
    cd /d "D:\JcampFxTrading\CSMMonitor"
    dotnet run --project JcampForexTrader\JcampForexTrader.csproj
)

echo.
echo Monitor App closed.
pause
