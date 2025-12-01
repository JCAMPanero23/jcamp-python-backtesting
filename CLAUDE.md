# CLAUDE.md - JCAMP Forex Trading System Context

**Purpose:** Single authoritative reference for Claude to understand project state and start working effectively.
**Last Updated:** December 1, 2025
**Current Phase:** Phase 5.3 - Chart Viewer Enhancements (Part 1: Viewport Bugs COMPLETE ✅)

---

## QUICK STATUS

| Component | Status | Details |
|-----------|--------|---------|
| **Python Backend** | ✅ Operational | FastAPI on port 8000 |
| **C# Chart Viewer** | ✅ Operational | M1 viewport positioning FIXED, playback smooth |
| **Tests** | 30/31 Passing | 1 Phase 2 test failing |
| **Main Branch** | ✅ Updated | Phase 5.2 complete, Phase 5.3 Part 1 complete |
| **Phase 5.3 Branch** | ✅ Active | phase5.3-ux-enhancements, viewport bugs resolved |

---

## PHASE 5.2 COMPLETION SUMMARY (Nov 29, 2025)

### ✅ EMA Display Bug - RESOLVED
- **Status:** FIXED - EMAs now displaying correctly in C# viewer
- **Root Cause:** H1 EMA interpolation was using future/incomplete H1 bars
- **Solution:** Modified EMA interpolation to use only COMPLETED H1 bars
- **Key Commit:** 13e2366 - "fix: Use only COMPLETED H1 bars for EMA interpolation (sub-agent analysis)"
- **Testing:** Verified with screenshots showing both M15 and H1 EMAs rendering correctly
- **Resolution:** Phase 5.3 can now proceed

### ✅ M1 Playback Enhancement
- Successfully added M1 OHLC endpoint for smooth playback
- M1 data properly filtered to match M15 date ranges
- 31,680 bars (2,112 M15 × 15 M1) rendering without gaps

---

## PHASE 5.3 PART 1 COMPLETION SUMMARY (Dec 1, 2025)

### ✅ M1 Viewport Positioning Bug - RESOLVED
- **Status:** FIXED - Current bar now positioned at exactly 80% from left
- **Root Cause:** M1→M15 coordinate mismatch. Using M1 bar indices (0-1440) in M15 viewport calculations (0-96)
- **Solution:** Convert M1 index to M15 equivalent: `currentM15Index = currentIndex / 15.0`
- **Key Commits:**
  - `2309b9d`: Convert M1 bar index to M15 equivalent for correct viewport positioning
  - `ed49bc2`: Apply M1→M15 conversion to reset button (non-playing viewport)
  - `f951fc0`: Remove Left==0 condition that was causing viewport zoom-out
  - `ec96f47`: Execute M1 viewport positioning every frame to prevent ScottPlot auto-scaling
- **Testing:** Verified with detailed debug logs showing correct 80% positioning at all times
- **Architecture Insight:** Viewport always in M15 coordinates; M1 used only for smooth candle animation within M15 bars

### ✅ Viewport Consistency
- Playback and reset button now use identical positioning logic
- Zoom level preserved during pause/resume cycles
- No unexpected jumps or crushing of X-axis

---

## PHASE 5.3 PART 2 & 3: UX ENHANCEMENTS - READY FOR IMPLEMENTATION (Dec 1, 2025)

### 📋 Enhancement #1 Adjustments: Timeline-Based Recent Trades (30-45 min)

**Requirement:** Modify recent trades list to show ALL trades filtered by playback position (live experience)

**Changes:**
1. Remove `.Take(30)` hardcoded limit (line 1491, ChartViewerWindow.xaml.cs)
2. Add `GetCurrentPlaybackTime()` helper method
3. Add time-based filter: `.Where(t => t.GetExitTime().Value <= currentTime)`
4. Update UI label: "Closed Trades" (instead of "Last 30 Closed Trades")

**Expected Result:**
- Trades appear as they close during playback
- Scrubbing backward removes future trades
- No 30-trade limit (50+ trades visible if available)

**Files to Modify:**
- `D:\JcampFxTrading\CSMMonitor\JcampForexTrader\ChartViewerWindow.xaml.cs` (lines 1482-1507)
- `D:\JcampFxTrading\CSMMonitor\JcampForexTrader\ChartViewerWindow.xaml` (line 210)

**Estimated Effort:** 30-45 minutes

---

### 🎯 Enhancement #3: Multi-Pair Chart Display (13-19 hours) - MAJOR FEATURE

**Objective:** Enable simultaneous display and playback of up to 4 currency pairs with adjustable layout

**Architecture:**
- 2x2 Grid layout with 3 chart panels + 1 info panel
- GridSplitters for draggable resizing (user can make one chart bigger)
- All pairs synchronized on same timeline
- Single unified play/pause/speed control
- Combined trades list from all pairs mixed by exit time

**Implementation Breakdown:**

**Phase 1: Backend API (4-6 hours)**
- New endpoint: `POST /run-multi` - Execute multi-pair backtests in parallel
- New endpoint: `GET /ohlc-multi` - Retrieve OHLC data for all pairs
- New service methods for multi-backtest execution and aggregation

**Phase 2: Frontend Models (1-2 hours)**
- C# models: `MultiBacktestRequest`, `MultiOhlcData`, `CombinedMetrics`
- API client methods: `RunMultiBacktestAsync()`, `GetMultiOhlcDataAsync()`

**Phase 3: Multi-Chart Viewer (6-8 hours)**
- NEW: `MultiChartViewerWindow.xaml` - 2x2 grid with GridSplitters
- NEW: `MultiChartViewerWindow.xaml.cs` - Chart state management, synchronized playback
- Reuse existing rendering logic from single-pair viewer

**Phase 4: Integration (2-3 hours)**
- Update `BacktestWindow.xaml` - Add symbol checkboxes for multi-select
- Update `BacktestWindow.xaml.cs` - Multi-pair launch logic
- Handle edge cases and error scenarios

**Files to Modify/Create:**
- Backend: `src/api/routes/backtest.py`, `src/api/services/backtest_service.py`, `src/api/models/`
- Frontend: NEW `MultiChartViewerWindow.xaml`, NEW `MultiChartViewerWindow.xaml.cs`
- Integration: `BacktestWindow.xaml`, `BacktestWindow.xaml.cs`

**Estimated Effort:** 13-19 hours

**For detailed code:** See plan file at `C:\Users\jcamp\.claude\plans\typed-baking-prism.md`

---

## PROJECT OVERVIEW

**Project:** jcamp-python-backtesting
**Description:** High-performance forex backtesting engine with C# WPF chart viewer integration
**Technology:** Python (FastAPI, Pandas, NumPy, TA-Lib) + C# WPF (ScottPlot)
**Key Achievement:** 100-600x faster than MT5 with identical trading logic
**Business Goal:** $5k/month forex signal service (14-16 months to launch)

---

## ARCHITECTURE

### Data Flow
```
CSV Files → DataLoader → Timeframe Converter → CSM Calculator
    ↓
Technical Indicators (EMA 20/50/100, ADX, RSI, ATR)
    ↓
Regime Detector (Trending/Ranging/Transitional)
    ↓
Trading Strategies (Simple Test / Trend Rider / Range Rider)
    ↓
Position Manager (Entry/Exit/Trailing Stop)
    ↓
Performance Tracker (R-multiples, Win Rate, etc.)
    ↓
Results Export (JSON/CSV/HTML/Charts)
```

### API Structure
```
FastAPI Server (src/api/main.py)
    ↓
Routes (src/api/routes/backtest.py)
    ↓
Services (src/api/services/backtest_service.py)
    ↓
BacktestEngine (src/backtest_engine.py)
    ↓
JSON Response to C#
```

---

## PROJECT STRUCTURE

```
D:\JcampFxTrading/
├── CLAUDE.md                                    # This file (startup context)
├── Claude_old version.md                        # Previous version (reference)
├── STATUS.md                                    # Dynamic status tracking
├── SUBSCRIPTION_BUSINESS_PLAN.md                # Business plan (markdown)
├── Jcamp_BacktestEA.mq5                        # MT5 Expert Advisor (reference)
│
├── jcamp-python-backtesting/                    # Python backtesting repo
│   ├── src/
│   │   ├── backtest_engine.py                  # Core engine (handles warmup)
│   │   ├── data_loader.py                      # Data loading & CSM
│   │   ├── indicators.py                       # EMA/ADX/RSI/ATR
│   │   ├── api/
│   │   │   ├── main.py                         # FastAPI server
│   │   │   ├── routes/backtest.py              # API endpoints
│   │   │   └── services/backtest_service.py    # OHLC response building
│   │   ├── strategies/
│   │   │   ├── simple_test.py
│   │   │   ├── trend_rider.py
│   │   │   └── range_rider.py
│   │   └── position_manager.py
│   ├── tests/
│   │   ├── test_phase1.py                      # (8/8)
│   │   ├── test_phase2.py                      # (7/8) ⚠️ 1 failing
│   │   ├── test_phase3.py                      # (8/8)
│   │   └── test_phase4.py                      # (7/7)
│   ├── docs/
│   │   ├── current/PHASE_5_7_MASTER_PLAN.md    # 7-phase development roadmap
│   │   ├── SUBSCRIPTION_BUSINESS_PLAN.md
│   │   ├── JCAMP_Business_Plan_v2.docx         # (uncommitted)
│   │   └── JCAMP_Financial_Projections.xlsx    # (uncommitted)
│   └── CSMMonitor/                             # Symbolic link to C# app
│
└── CSMMonitor/                                  # C# WPF app (separate git repo)
    ├── JcampForexTrader/
    │   ├── ChartViewerWindow.xaml.cs            # Chart display + playback
    │   └── BacktestWindow.xaml.cs               # Config UI
    └── .git/
```

---

## RECENT COMMIT HISTORY

### Commit c5e27f9 (Nov 29, 2025)
**Title:** Merge pull request #1 from JCAMPanero23/phase5-session1-api-foundation
- **Merged:** All Phase 5.2 EMA fixes and enhancements to main branch
- **Includes:** 20+ commits covering EMA interpolation fixes, M1 playback, and bug resolutions
- **Status:** Main branch now fully up to date with Phase 5.2 completion

### Commit 13e2366 (Phase 5.2 Critical Fix)
**Title:** fix: Use only COMPLETED H1 bars for EMA interpolation (sub-agent analysis)
- **Problem:** H1 EMA was interpolating from incomplete/future H1 bars causing lookahead bias
- **Solution:** Modified interpolation logic to use only bars with full OHLC data
- **Result:** EMAs now display correctly with proper alignment to M15 chart
- **Impact:** Resolved critical regression blocking Phase 5.2 completion

### Previous Phase 5 Commits
- `97ce473`: Eliminate H1 EMA lookahead bias and add smooth interpolation
- `32a4d4a`: Calculate H1 EMAs in Python with full warmup for accurate values
- `9cb356c`: Filter out warmup bars from OHLC data sent to C# viewer
- `768aa6d`: Multi-year data loading for warmup + EMA fixes

---

## DEVELOPMENT ROADMAP (PHASE_5_7_MASTER_PLAN.md)

### Phase 5.3: Chart Viewer Enhancements (CURRENT)
- **Part 1:** Critical bug fixes ✅ COMPLETE (Dec 1, 2025)
  - [x] Fix viewport positioning in M1 playback mode
  - [x] Fix reset button viewport calculation
  - [x] Fix zoom scale preservation during playback
  - [x] Root cause: M1→M15 index coordinate mismatch
  - **Key Commits:** 2309b9d, ed49bc2, f951fc0, ec96f47
- **Part 2:** H1/H4 timeframe switching (2-3 hours)
  - [ ] Implement timeframe aggregation logic
  - [ ] Recalculate indicators for each timeframe
  - [ ] Update grid spacing
- **Part 3:** UX enhancements (1-2 hours)
  - [ ] Skip weekend gaps during playback
  - [ ] Redesign recent trades sidebar (3-section tabs)
- **Part 4:** Pending trade functionality (3-4 hours)
- **Part 5:** MT5 EA comparison (4-6 hours)

### Phase 6: Multi-Pair Backtesting (6-8 hours)
- Multi-pair API endpoint
- Parallel execution
- Results aggregation
- C# multi-select UI

### Phase 7: Strategy Fixes & Enhancements (8-10 hours)
- **NOTE:** Strategy Logic Mismatch investigation is Phase 7, NOT Phase 1
- Trend Rider: trailing stops, multi-timeframe confirmation, breakeven logic
- Range Rider: better range detection, dynamic TP/SL
- Risk Management: daily loss limits, correlation filter
- Performance: indicator caching
- New Strategies: breakout + mean reversion

---

## BUSINESS PLAN SUMMARY

**Goal:** $5,000/month from 100 subscribers (Telegram-based signal service)
**Timeline:** 14-16 months
**Capital Required:** $0 (bootstrap)
**Break-even:** 3 subscribers ($150/month costs)
**Profit Margin:** 97% at scale

**Critical Success Factor:** 5-6 months real money validation BEFORE launch
- 2 months demo account
- 3-4 months live account ($500, micro lots, 2% risk)
- Document every trade with proof
- Target: Positive R-multiple, <25% drawdown, >45% win rate

---

## RESOURCES & REFERENCES

### Documentation
- **PHASE_5_7_MASTER_PLAN.md** - Detailed 7-phase implementation plan
- **SUBSCRIPTION_BUSINESS_PLAN.md** - Business strategy & timeline
- **STATUS.md** - Dynamic progress tracking

### Uncommitted Files (Ready to Stage)
- `docs/JCAMP_Business_Plan_v2.docx` - Updated business plan
- `docs/JCAMP_Financial_Projections.xlsx` - Financial model
- `results/backtests/*.png` - Testing screenshots

---

## QUICK COMMANDS

### Check Status
```bash
cd D:\JcampFxTrading\jcamp-python-backtesting
git status
git log -3 --oneline
```

### Run Tests
```bash
cd D:\JcampFxTrading\jcamp-python-backtesting
python -m pytest tests/ -v
```

### Start API Server
```bash
cd D:\JcampFxTrading\jcamp-python-backtesting
python -m uvicorn src.api.main:app --reload
```

### Build C# Project
```bash
cd D:\JcampFxTrading\CSMMonitor
dotnet build
```

---

## KEY METRICS

| Metric | Value |
|--------|-------|
| Total Code | ~4,500 LOC (production) |
| Test Coverage | 97% (30/31 tests) |
| Performance vs MT5 | 100-600x faster |
| API Endpoints | 5 operational |
| Strategies | 3 (Simple Test, Trend Rider, Range Rider) |
| Phases Complete | 5/5 (100% code) |

---

## CRITICAL NOTES

- **Phase 5.2 COMPLETE:** ✅ EMA overlay bug fixed - EMAs displaying correctly with H1 alignment
- **Phase 5.3 PART 1 COMPLETE:** ✅ M1 viewport positioning fixed - Playback smooth, current bar at 80%
- **Phase 5.3 PART 2 NEXT:** H1/H4 timeframe switching (TBD next session)
- **Two Git Repos:** Python backtesting and CSMMonitor are separate - commit independently
- **Branch Strategy:** Main branch updated with Phase 5.2. Using phase5.3-ux-enhancements branch for Phase 5.3 work
- **Architecture Note:** Viewport always in M15 coordinates (0-96 bars). M1 (0-1440 bars) used only for smooth animation within M15 candles
- **Strategy Logic:** Phase 7 task, NOT Phase 1 (per PHASE_5_7_MASTER_PLAN.md)
- **Business Timeline:** 5-6 months real money validation required before launch
- **Next Priority:** Phase 5.3 Part 2 (Timeframe switching) → Phase 6 (Multi-pair) → Phase 7 (Strategy fixes)

---

## SESSION CHECKLIST

### Start
- [ ] Read this file
- [ ] Check `git status` and `git log -3`
- [ ] Check CSMMonitor status if modified
- [ ] Understand current blockers

### End
- [ ] Update STATUS.md
- [ ] Commit Python repo changes
- [ ] Commit CSMMonitor changes (if modified)
- [ ] Confirm all saved

---

*Read this file at the start of every session for context.*
