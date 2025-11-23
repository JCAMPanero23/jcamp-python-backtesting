# SESSION START - Quick Reference Guide

**Purpose:** This document provides immediate context when starting a new session. Read this FIRST before diving into work.

**Last Updated:** November 22, 2025
**Session:** M1 Playback Animation & UX Improvements

---

## QUICK PROJECT STATUS

| Aspect | Status | Details |
|--------|--------|---------|
| **Phase** | Phase 5 Complete | All 5 phases finished |
| **Branch** | `phase5-session1-api-foundation` | Working branch |
| **Tests** | 30/31 passing (97%) | 1 Phase 2 test failing |
| **API Server** | Operational | FastAPI on port 8000 |
| **Latest Commit** | 0982fdc | Windows Unicode fix |
| **Production Ready** | 85% | Needs logging & config improvements |

---

## WHAT HAPPENED THIS SESSION (Nov 22, 2025)

### M1 Playback Animation Feature
1. **Animated M15 Candle Formation**
   - **Goal:** Show M15 candles animating/forming as M1 data progresses
   - **Implementation:** Built M15 candles dynamically from M1 bars
   - **Behavior:** Like watching live MT5 candle form in real-time
   - **Files:** ChartViewerWindow.xaml.cs - added `BuildAnimatedM15Candles()` method
   - **Result:** 15x smoother playback visualization

2. **Smart Viewport Y-Axis Following**
   - **Goal:** Only follow price if it moves outside middle 35% zone
   - **Logic:** Price can move within central 35% without viewport adjustment
   - **Threshold:** Follow only if price < 32.5% or > 67.5% from bottom
   - **Files:** ChartViewerWindow.xaml.cs - added `ShouldFollowPrice()` helper
   - **Result:** Smoother viewing experience, less unnecessary viewport jumps

### UX Improvements
3. **DatePicker Dark Theme Fix**
   - **Issue:** Calendar had grayed-out text on dark background (poor contrast)
   - **Fix:** Added comprehensive CalendarDayButton and CalendarButton styles
   - **Files:** BacktestWindow.xaml - expanded Window.Resources
   - **Result:** Calendar now fully readable with white text

4. **Default Dates Updated**
   - **Changed:** From dynamic dates to fixed Jan 1-31, 2024
   - **Files:** BacktestWindow.xaml.cs - constructor default dates
   - **Result:** No more manual date entry needed

5. **Batch File Improvements**
   - **Fixed:** START_ALL.bat, START_MONITOR_APP.bat, START_API_SERVER.bat
   - **Improvements:** Python availability checks, better error messages, runs pre-built .exe
   - **Result:** Faster startup, better user experience

### Phase 5.1 Critical Bug Fixes (Nov 22, 2025 - Continuation)
6. **Manual Progress Slider Movement** ✅
   - **Issue:** Slider couldn't be moved manually, only responded to play/pause
   - **Root Cause:** Event handler triggered during programmatic updates and didn't handle M1 mode
   - **Fix:** Added `_isUpdatingSliderProgrammatically` flag to distinguish user vs programmatic changes
   - **Implementation:** Updated `ProgressSlider_ValueChanged` to handle both Standard and RealM1 playback modes
   - **Features:** Added `ReplayTradesUpToBar()` and `ReplayTradesUpToM1Bar()` to recalculate stats when scrubbing
   - **Files:** ChartViewerWindow.xaml.cs - lines 37-38, 228-230, 269-271, 939-975, 1016-1061
   - **Result:** Users can now manually scrub through the timeline in both playback modes

7. **Reset Button Functionality** ✅
   - **Issue:** Reset button didn't work in M1 playback mode
   - **Root Cause:** Only reset `_currentBarIndex`, not `_m1BarIndex`
   - **Fix:** Reset both indices and call appropriate advance method based on playback mode
   - **Files:** ChartViewerWindow.xaml.cs - ResetButton_Click (lines 990-1014)
   - **Result:** Reset button now works correctly in both Standard and M1 playback modes

8. **Zoom Scale Preservation** ✅
   - **Issue:** Y-axis zoom level reset to default when viewport followed price
   - **Root Cause:** Hard-coded 100 pips range when following price
   - **Fix:** Preserve current Y-axis range (zoom level) when following, only shift center
   - **Implementation:** Calculate `currentYRange` from existing limits, use it when centering on new price
   - **Files:** ChartViewerWindow.xaml.cs - RenderChartUpToBar (lines 499-509), RenderM1ChartUpToBar (lines 322-332)
   - **Result:** User's manual zoom level is now preserved when viewport auto-follows price

---

## WHAT HAPPENED PREVIOUS SESSION (Nov 21, 2025)

### Critical Bug Fixes
1. **Windows Unicode Error (0982fdc)**
   - **Issue:** Windows console can't display emojis (CP1252 encoding)
   - **Fix:** Replaced ALL emojis with ASCII in 7 Python files
   - **Impact:** System now runs on Windows without errors
   - **Files:** backtest_engine.py, data_loader.py, csm_calculator.py, indicators.py, performance_tracker.py, regime_detector.py, backtest_service.py

2. **EMA Period Mismatch (44c056b)**
   - **Issue:** EMA periods were 20/35/50 instead of 20/50/100
   - **Fix:** Corrected to match MT5 v1.96 spec
   - **Impact:** All historical results pre-Nov 21 are INVALID and need revalidation

3. **Documentation Cleanup (3bf76d8)**
   - Organized docs into `current/` and `archive/`
   - Created STATUS.md with comprehensive project tracking
   - Archived outdated Phase 4 bug reports

### Files Added
- `START_ALL.bat` - Launch both API server and C# app
- `START_API_SERVER.bat` - Launch API server only
- `START_MONITOR_APP.bat` - Launch C# app only
- `STATUS.md` - Project status tracking
- `SESSION_START.md` - This file

---

## CURRENT SYSTEM STATE

### What's Working ✅
- Data Loader: CSV/Parquet support, timeframe conversion
- CSM Calculator: 8 currencies, 15 pairs
- Technical Indicators: EMA (20/50/100), ADX, RSI, ATR
- Regime Detector: Trending/Ranging/Transitional
- Trading Strategies: Trend Rider & Range Rider
- Backtest Engine: Position management, R-multiple tracking
- Performance Tracker: Comprehensive analytics
- REST API: 5 endpoints operational
- Chart Visualization: Plotly HTML charts + OHLC JSON

### What's NOT Working ❌
- 1 Phase 2 test failing (96.7% pass rate)
- C# Chart Viewer has rendering issues (separate repo)

### What Needs Validation ⚠️
- Backtest results with corrected EMA periods (20/50/100)
- EURUSD 2024 baseline: Should match MT5 v1.96 results

---

## ESSENTIAL FILES TO REVIEW

### Documentation (Read First)
1. **`CLAUDE.md`** - **START HERE!** Quick reference for Claude sessions (consolidated overview)
2. `SESSION_START.md` - This file (detailed session history and checklist)
3. `STATUS.md` - Comprehensive project status
4. `README.md` - Project overview and setup

### Core Python Files
1. `src/backtest_engine.py` - Main backtesting orchestration (535 lines)
2. `src/data_loader.py` - Data loading & CSM calculation (356 lines)
3. `src/indicators.py` - Technical indicators (238 lines)
4. `src/strategies/trend_rider.py` - Trend following strategy
5. `src/strategies/range_rider.py` - Range trading strategy

### API Files
1. `src/api/main.py` - FastAPI server
2. `src/api/routes/backtest.py` - API endpoints
3. `src/api/services/backtest_service.py` - Business logic

### Test Files
1. `tests/test_phase1.py` - Data loader & CSM (8/8 passing)
2. `tests/test_phase2.py` - Indicators & regime (7/8 passing) ⚠️
3. `tests/test_phase3.py` - Strategies (8/8 passing)
4. `tests/test_phase4.py` - Backtest engine (7/7 passing)

---

## QUICK START COMMANDS

### Check System Health
```bash
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

### View API Documentation
```bash
# Start server, then visit:
http://localhost:8000/docs
```

---

## KNOWN ISSUES & WARNINGS

### Active Issues
1. **C# Chart Viewer Problems** (docs/current/CHART_VIEWER_ISSUES.md)
   - Candlesticks not rendering
   - Trade box positioning incorrect
   - Viewport auto-scroll not working
   - **Owner:** C# application (separate repository)
   - **Priority:** Medium (UX issue, not core functionality)

2. **Phase 2 Test Failure** (1 test failing)
   - **File:** tests/test_phase2.py
   - **Impact:** Minor (96.7% pass rate)
   - **Priority:** Low

### Critical Warnings
- **EMA Bug Fixed Nov 21:** All backtest results before Nov 21 used wrong EMA periods (35/50 instead of 50/100)
- **Validation Required:** Must re-run EURUSD 2024 baseline with corrected EMAs
- **Git Housekeeping:** Multiple __pycache__ files modified (see git status)

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

### Output Locations
```
charts/          # Generated HTML/JSON charts (gitignored)
tests/outputs/   # Test output files (gitignored)
```

---

## GIT WORKFLOW NOTES

### Current Branch
- **Working Branch:** `phase5-session1-api-foundation`
- **Main Branch:** Not set (check with `git branch -a`)
- **Upstream:** Check if connected to GitHub

### Typical Workflow
```bash
# Before starting work
git status
git log -1 --stat

# After completing work
git add <files>
git commit -m "Description"

# If pushing to remote
git push origin phase5-session1-api-foundation
```

### C# Project Location
- **Directory:** `D:\JcampFxTrading\CSMMonitor`
- **Previous:** `C:\Users\jcamp\OneDrive\Documents\Visual Studio 2022\Projects\CSMMonitor` (deprecated)
- **GitHub:** https://github.com/JCAMPanero23/CSMMonitor
- **Migration Date:** Nov 21, 2025 (moved from OneDrive to avoid sync conflicts)

---

## PERFORMANCE BASELINE (Target)

### EURUSD 2024 Full Year (MT5 v1.96)
- **Total R:** +16.03R
- **Trades:** 149
- **Win Rate:** 52%
- **Trend Rider:** +9.18R (60W/61L)
- **Range Rider:** +6.86R (18W/10L)

**Status:** ⚠️ Needs revalidation with corrected EMAs (20/50/100)

---

## ARCHITECTURE QUICK REFERENCE

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

---

## NEXT PRIORITIES (If Continuing Development)

### Immediate (Current Session)
1. ✅ Update STATUS.md with latest commit
2. ✅ Fix README.md broken documentation links
3. ✅ Create SESSION_START.md
4. Clean up __pycache__ files (optional)
5. Run backtest with corrected EMAs

### Short-term (This Week)
1. Investigate and fix Phase 2 test failure
2. Validate EURUSD 2024 baseline with corrected EMAs
3. Address C# chart viewer issues (if working on C# side)
4. Create configuration file system (move hardcoded values)
5. Expand logging (currently basic)

### Medium-term (Next 2 Weeks)
1. Walk-forward analysis module
2. Parameter optimization UI
3. Developer documentation
4. Clean up test file organization

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

### Encoding Errors
- **Fixed:** All emojis removed from Python code (0982fdc)
- If you see encoding errors, check if new code introduced emojis

---

## SESSION CHECKLIST

Before starting work:
- [ ] **Read CLAUDE.md first** (quick reference for current state)
- [ ] Read this file (SESSION_START.md) for detailed history
- [ ] Check STATUS.md for comprehensive project state
- [ ] Run `git status` to see what's modified
- [ ] Run `git log -3` to see recent commits
- [ ] Run tests to verify system health: `python -m pytest tests/ -v`

Before ending session:
- [ ] Update CLAUDE.md if project state changed (current status, priorities, metrics)
- [ ] Update STATUS.md if significant changes made
- [ ] Update this file (SESSION_START.md) if project state changed
- [ ] Commit changes with descriptive message
- [ ] Update "Last Updated" dates in modified files

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

## CONTACT & RESOURCES

### Documentation
- **STATUS.md** - Detailed project status
- **README.md** - Setup and usage guide
- **docs/current/** - Current documentation
- **docs/archive/** - Historical documentation

### API Documentation
- **Swagger UI:** http://localhost:8000/docs (when server running)
- **ReDoc:** http://localhost:8000/redoc (when server running)

### Related Repositories
- **CSMMonitor (C# WPF):** https://github.com/JCAMPanero23/CSMMonitor
  - Location: `D:\JcampFxTrading\CSMMonitor`
- **Python Backtesting:** (current repository)
  - Location: `D:\JcampFxTrading\jcamp-python-backtesting`

---

**Remember:** Always read CLAUDE.md first, then this file when starting a new session to get up to speed quickly!

**Project Status:** ✅ PHASE 5 COMPLETE - SYSTEM OPERATIONAL
**Build Date:** November 21, 2025
**Version:** 1.0
