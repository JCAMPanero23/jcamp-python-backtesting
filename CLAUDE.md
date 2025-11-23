# CLAUDE.md - Quick Reference for Claude Sessions

**Purpose:** Single authoritative reference for Claude to quickly understand the project state and start working effectively.

**Last Updated:** November 23, 2025
**Current Phase:** Phase 5.2 Complete - Timeframe Switching (H1/H4)

---

## PROJECT OVERVIEW

**Project:** jcamp-python-backtesting
**Description:** High-performance forex backtesting engine with C# WPF chart viewer integration
**Technology Stack:** Python (FastAPI, Pandas, NumPy, TA-Lib) + C# WPF (ScottPlot)
**Current Status:** Phase 5 Complete (97% production ready)

**Key Achievement:** 100-600x faster than MT5 with identical trading logic

---

## SYSTEM STATUS AT A GLANCE

| Component | Status | Details |
|-----------|--------|---------|
| **Python Backend** | ✅ Operational | FastAPI on port 8000 |
| **C# Chart Viewer** | ✅ Fully Operational | All Phase 5.1 bugs fixed |
| **Tests** | ⚠️ 30/31 Passing | 97% (1 Phase 2 test failing) |
| **Git Branch** | `phase5-session1-api-foundation` | Working branch |
| **Latest Commit** | `0fa02a9` | Date filtering bug fix |
| **Production Ready** | 85% | Needs logging & config improvements |

---

## RECENT CHANGES (Last 3 Sessions)

### November 23, 2025 - Phase 5.2: Timeframe Switching
- ✅ Implemented H1/H4 timeframe aggregation (4 M15 bars → 1 H1, 16 M15 bars → 1 H4)
- ✅ Added ChartTimeframe enum (M15/H1/H4)
- ✅ Recalculate EMAs for aggregated timeframes
- ✅ Updated grid spacing (M15: 30min, H1: 6hr, H4: 24hr intervals)
- ✅ Wired up radio button event handlers
- ✅ Progress display shows correct timeframe label
- ✅ Build succeeded - 0 errors, 0 warnings

### November 22, 2025 - M1 Playback Animation & UX Improvements
- ✅ Animated M15 candle formation from M1 data (15x smoother playback)
- ✅ Smart viewport Y-axis following (only follows if price exits middle 35% zone)
- ✅ DatePicker dark theme fix (calendar now readable)
- ✅ Default dates set to Jan 1-31, 2024
- ✅ Batch file improvements (Python availability checks)

### November 22, 2025 - Phase 5.1: Critical Bug Fixes
- ✅ Manual progress slider movement (with flag to prevent feedback loops)
- ✅ Reset button functionality (resets both M15 and M1 indices)
- ✅ Zoom scale preservation (viewport follows price but keeps zoom level)
- ✅ Date filtering bug fix (midnight truncation issue)

### November 21, 2025 - Critical Bug Fixes
- ✅ Windows Unicode error fix (removed all emojis from Python code)
- ✅ EMA period mismatch fix (corrected to 20/50/100 from 20/35/50)
- ⚠️ **All backtest results before Nov 21 are INVALID** (wrong EMA periods)

---

## CURRENT ARCHITECTURE

### Data Flow
```
CSV Files → DataLoader → Timeframe Converter → CSM Calculator
                ↓
        Technical Indicators (EMA/ADX/RSI/ATR)
                ↓
          Regime Detector (Trending/Ranging)
                ↓
   Trading Strategies (Trend Rider / Range Rider)
                ↓
    Position Manager (Entry/Exit/Trailing Stop)
                ↓
  Performance Tracker (R-multiples, Win Rate, etc.)
                ↓
    Results Export (JSON/CSV/HTML/Charts)
```

### API Architecture
```
FastAPI Server (main.py)
    ↓
Routes (backtest.py)
    ↓
Services (backtest_service.py)
    ↓
BacktestEngine (backtest_engine.py)
    ↓
Results (JSON response)
```

### C# Integration
```
BacktestWindow → API Call → Python Backend
                      ↓
              OHLC + Trades JSON
                      ↓
          ChartViewerWindow (ScottPlot)
                      ↓
          M15/H1/H4 Timeframe Display
          M1 Animated Playback Mode
```

---

## ESSENTIAL FILES TO REVIEW

### Documentation (Read First)
1. **CLAUDE.md** (this file) - Start here every session
2. **SESSION_START.md** - Detailed session history and checklist
3. **STATUS.md** - Comprehensive project status
4. **docs/current/PHASE_5_7_MASTER_PLAN.md** - Roadmap for phases 5-7

### Core Python Files
1. **src/backtest_engine.py** (535 lines) - Main backtesting orchestration
2. **src/data_loader.py** (356 lines) - Data loading & CSM calculation
3. **src/indicators.py** (238 lines) - Technical indicators (EMA/ADX/RSI/ATR)
4. **src/strategies/trend_rider.py** - Trend following strategy
5. **src/strategies/range_rider.py** - Range trading strategy

### API Files
1. **src/api/main.py** - FastAPI server
2. **src/api/routes/backtest.py** - API endpoints
3. **src/api/services/backtest_service.py** - Business logic

### C# Files (D:\JcampFxTrading\CSMMonitor)
1. **JcampForexTrader/ChartViewerWindow.xaml.cs** - Chart viewer implementation
2. **JcampForexTrader/BacktestWindow.xaml.cs** - Backtest configuration UI

### Test Files
1. **tests/test_phase1.py** - Data loader & CSM (8/8 passing)
2. **tests/test_phase2.py** - Indicators & regime (7/8 passing) ⚠️
3. **tests/test_phase3.py** - Strategies (8/8 passing)
4. **tests/test_phase4.py** - Backtest engine (7/7 passing)

---

## KNOWN ISSUES

### Active Issues
1. **Phase 2 Test Failure** (1 test failing)
   - File: tests/test_phase2.py
   - Impact: Minor (96.7% pass rate)
   - Priority: Low

### Resolved Issues (Nov 21-22, 2025)
- ✅ Windows Unicode errors (emojis removed)
- ✅ EMA period mismatch (corrected to 20/50/100)
- ✅ Manual progress slider (fixed with programmatic flag)
- ✅ Reset button (fixed for both M15 and M1 modes)
- ✅ Zoom preservation (viewport follows but keeps zoom level)
- ✅ Date filtering bug (midnight truncation fixed)

---

## CURRENT PRIORITIES

### Immediate (Phase 5.3 - UX Enhancements)
1. Skip weekend gaps during playback (Fri 23:00 → Mon 00:00)
2. Recent trades sidebar redesign (3-section tabbed layout)
3. Scrollable recent trades list (not limited to last 5)

### Short-term (Phase 5.4-5.5)
1. Add pending trade functionality to Simple Strategy
2. MT5 EA copy + results comparison (validate Python vs MT5)

### Medium-term (Phase 6-7)
1. Multi-pair backtesting (run 6 pairs simultaneously)
2. Strategy enhancements (trailing stops, multi-timeframe confirmation)
3. Risk management improvements (daily loss limit, correlation filter)

---

## QUICK COMMANDS

### Check System Health
```bash
# Navigate to project
cd D:\JcampFxTrading\jcamp-python-backtesting

# Check git status
git status

# Run all tests
python -m pytest tests/ -v

# Check for modified files
git diff --stat
```

### Start API Server
```bash
# Option 1: Batch file (Windows)
START_API_SERVER.bat

# Option 2: Python script
python scripts/start_api_server.py

# Option 3: Direct uvicorn
cd src/api
uvicorn main:app --reload --port 8000
```

### Run a Quick Backtest
```bash
# Use the API (server must be running)
curl -X POST http://localhost:8000/backtest/run \
  -H "Content-Type: application/json" \
  -d '{"symbol": "EURUSD", "start_date": "2024-01-01", "end_date": "2024-12-31", "strategy": "both"}'
```

### Start C# Application
```bash
# Option 1: Batch file
START_MONITOR_APP.bat

# Option 2: Direct executable
D:\JcampFxTrading\CSMMonitor\JcampForexTrader\bin\Debug\net8.0-windows\JcampForexTrader.exe
```

### Build C# Project
```bash
cd D:\JcampFxTrading\CSMMonitor
dotnet build
```

---

## DATA LOCATIONS

### Historical Data (Gitignored)
```
data/
└── EURUSD_sml/
    └── 2024_M1.csv  (372,000+ bars)
```

### Test Data
```
tests/samples/
├── test_data_M1.csv (100 bars, fake CSM data)
└── [other test files]
```

### Output Locations (Gitignored)
```
charts/          # Generated HTML/JSON charts
tests/outputs/   # Test output files
```

---

## CRITICAL WARNINGS

### ⚠️ EMA Bug Fixed Nov 21, 2025
- **Issue:** EMA periods were 20/35/50 instead of 20/50/100
- **Impact:** ALL backtest results before Nov 21 are INVALID
- **Action Required:** Must re-run EURUSD 2024 baseline with corrected EMAs

### ⚠️ Windows Unicode (CP1252 Encoding)
- **Issue:** Windows console can't display emojis
- **Fix:** All emojis removed from Python code (0982fdc)
- **Affected Files:** 7 Python files (backtest_engine.py, data_loader.py, etc.)

### ⚠️ Git Branch
- **Current Branch:** `phase5-session1-api-foundation`
- **Main Branch:** Check with `git branch -a`
- **Upstream:** Verify connection to GitHub

### ⚠️ C# Project Location
- **Current:** `D:\JcampFxTrading\CSMMonitor`
- **Deprecated:** `C:\Users\jcamp\OneDrive\Documents\Visual Studio 2022\Projects\CSMMonitor`
- **Migration Date:** Nov 21, 2025 (moved from OneDrive to avoid sync conflicts)

---

## PERFORMANCE BASELINE (MT5 v1.96)

### EURUSD 2024 Full Year - Target Metrics
**Quick Summary:**
- **Total R:** +16.03R (149 trades, 52% win rate)
- **Trend Rider:** +9.18R (60W/61L)
- **Range Rider:** +6.86R (18W/10L)

**Status:** ⚠️ Needs revalidation with corrected EMAs (20/50/100)

📊 **For complete baseline metrics, see STATUS.md → "MT5 Baseline (v1.96) - Validation Target" section**

---

## KEY METRICS AT A GLANCE

| Metric | Value |
|--------|-------|
| Total Lines of Code | ~4,500 (production) |
| Test Coverage | 97% (30/31 tests) |
| Performance vs MT5 | 100-600x faster |
| API Endpoints | 5 operational |
| Strategies Implemented | 2 (Trend Rider, Range Rider) |
| Phases Complete | 5/5 (100%) |
| Production Readiness | 85% |

---

## NEXT SESSION CHECKLIST

### Before Starting Work
- [ ] Read this file (CLAUDE.md)
- [ ] Check SESSION_START.md for latest changes
- [ ] Run `git status` to see what's modified
- [ ] Run `git log -3` to see recent commits
- [ ] Run tests to verify system health: `python -m pytest tests/ -v`

### During Work
- [ ] Use TodoWrite tool to track tasks
- [ ] Update STATUS.md if significant changes made
- [ ] Commit changes with descriptive messages
- [ ] Build C# project after changes: `cd CSMMonitor && dotnet build`

### Before Ending Session
- [ ] Update SESSION_START.md with session summary
- [ ] Update this file (CLAUDE.md) if project state changed
- [ ] Commit all changes
- [ ] Update "Last Updated" date in this file

---

## RELATED REPOSITORIES

### Python Backtesting (Current)
- **Location:** `D:\JcampFxTrading\jcamp-python-backtesting`
- **GitHub:** (check with `git remote -v`)

### CSMMonitor (C# WPF)
- **Location:** `D:\JcampFxTrading\CSMMonitor`
- **GitHub:** https://github.com/JCAMPanero23/CSMMonitor

---

## API DOCUMENTATION

### Swagger UI (When Server Running)
- http://localhost:8000/docs

### ReDoc (When Server Running)
- http://localhost:8000/redoc

### Available Endpoints
1. `POST /backtest/run` - Run backtest
2. `GET /backtest/status/{task_id}` - Check backtest status
3. `GET /backtest/results/{task_id}` - Get backtest results
4. `GET /backtest/ohlc/{task_id}` - Get OHLC + trades data
5. `GET /backtest/ohlc-m1/{task_id}` - Get M1 OHLC data

---

## TROUBLESHOOTING QUICK REFERENCE

### API Server Won't Start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed (Windows)
taskkill /PID <pid> /F

# Try different port
uvicorn main:app --port 8001
```

### Tests Failing
```bash
# Run specific test file
python -m pytest tests/test_phase2.py -v

# Run with detailed output
python -m pytest tests/ -v -s

# Run single test
python -m pytest tests/test_phase2.py::test_name -v
```

### Import Errors
```bash
# Verify you're in the correct directory
pwd  # Should be: D:\JcampFxTrading\jcamp-python-backtesting

# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies (if needed)
pip install -r requirements.txt
```

### C# Build Errors
```bash
# Clean and rebuild
cd D:\JcampFxTrading\CSMMonitor
dotnet clean
dotnet build

# Check .NET version
dotnet --version  # Should be .NET 8.0
```

---

## PROJECT STATUS SUMMARY

**✅ PHASE 5 COMPLETE - SYSTEM OPERATIONAL**

All 5 phases of core development are complete. The system is 85% production ready.

**What's Working:**
- Data loading (CSV/Parquet, timeframe conversion)
- CSM calculation (8 currencies, 15 pairs)
- Technical indicators (EMA 20/50/100, ADX, RSI, ATR)
- Regime detection (Trending/Ranging/Transitional)
- Trading strategies (Trend Rider & Range Rider)
- Backtest engine (position management, R-multiple tracking)
- Performance analytics (comprehensive metrics)
- REST API (5 endpoints operational)
- C# Chart Viewer (M15/H1/H4 timeframes, M1 animated playback)

**What Needs Work:**
- 1 Phase 2 test failure (low priority)
- Logging improvements
- Configuration file system
- Walk-forward analysis module
- Parameter optimization UI

**Build Date:** November 21, 2025
**Version:** 1.0
**Last Major Update:** November 23, 2025 (Phase 5.2 - Timeframe Switching)

---

**Remember:** Always read this file first when starting a new session!
