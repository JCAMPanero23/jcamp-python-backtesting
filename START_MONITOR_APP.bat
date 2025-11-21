@echo off
echo Starting JCAMP Forex Monitor App...
echo.
cd /d "D:\JcampFxTrading\CSMMonitor"
dotnet run --project JcampForexTrader\JcampForexTrader.csproj
pause
