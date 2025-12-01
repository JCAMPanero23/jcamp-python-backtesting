# Master Plan: Phase 5-7 Implementation

**Updated:** December 1, 2025
**Status:** Phase 6 Part 1.1 IN PROGRESS - Simple Test Strategy EMA Crossover
**Current Work:** Phase 6 - Smart Portfolio Viewer
**Estimated Total Effort for Phase 6:** 16-22 hours

---

## QUICK STATUS

### ✅ Completed
- **Phase 5.3 Part 1:** M1 Viewport Positioning Bugs (COMPLETE)
  - M1→M15 coordinate mismatch resolved
  - Smooth M1 playback at 80% position
  - Zoom preservation working
  - Key commits: 2309b9d, ed49bc2, f951fc0, ec96f47

### 🔄 In Progress
- **Phase 6 Part 1.1:** Simple Test Strategy EMA Crossover (ACTIVE)
  - Replace time-based logic with EMA crossover + H1 confirmation
  - Expected: 1.5-2 hours implementation + 0.5-1 hour testing

### 📋 Planned
- **Phase 6 Parts 2-5:** Backend API, C# Services, Multi-Pair Viewer, Integration (14-19 hours)
- **Phase 5.3 Parts 2-5:** DEFERRED until after Phase 6 (Timeframe switching, UX enhancements)
- **Phase 7:** Strategy Enhancements (8-10 hours)

---

## Phase 5.3 UX Enhancements - Implementation Guide

### Enhancement #1: Timeline-Based Recent Trades (30-45 min)

**Current Issue:** Shows last 30 closed trades, ignoring playback position

**Changes Required:**
1. Remove `.Take(30)` from line 1491 in `ChartViewerWindow.xaml.cs`
2. Add `GetCurrentPlaybackTime()` helper method
3. Add time filter: `.Where(t => t.GetExitTime().Value <= currentTime)`
4. Update UI label in `ChartViewerWindow.xaml` line 210

**Expected Behavior:**
- Trades list empty at playback start
- Trades appear as they close during playback
- Scrubbing backward hides future trades
- No 30-trade limit (50+ trades visible)

**Files Affected:**
- `D:\JcampFxTrading\CSMMonitor\JcampForexTrader\ChartViewerWindow.xaml.cs`
- `D:\JcampFxTrading\CSMMonitor\JcampForexTrader\ChartViewerWindow.xaml`

---

### Enhancement #3: Multi-Pair Chart Display (13-19 hours)

**Architecture:** 2x2 Grid with GridSplitters + synchronized playback

**Objectives:**
- Display up to 4 currency pairs simultaneously
- All pairs on same timeline
- Single unified playback control
- GridSplitters allow resizing individual charts
- Combined trades list from all pairs

**Implementation Phases:**
1. **Backend API (4-6 hrs):** New endpoints `/run-multi` and `/ohlc-multi`
2. **Frontend Models (1-2 hrs):** C# models and API client
3. **Multi-Chart UI (6-8 hrs):** XAML layout, playback sync
4. **Integration (2-3 hrs):** BacktestWindow UI changes

**Key Files:**
- Backend: `src/api/routes/backtest.py`, `src/api/services/backtest_service.py`
- Frontend: NEW `MultiChartViewerWindow.xaml`, NEW `MultiChartViewerWindow.xaml.cs`
- Integration: `BacktestWindow.xaml`, `BacktestWindow.xaml.cs`

**For Detailed Implementation:** See `C:\Users\jcamp\.claude\plans\typed-baking-prism.md`

---

## Phase 6: Smart Portfolio Viewer (CURRENT)

**Status:** Part 1.1 IN PROGRESS
**Total Effort:** 16-22 hours
**Branch:** phase6-multi-pair (both repos)

### Objectives
- Multi-pair backtest execution (EURUSD, GBPUSD, USDJPY)
- Portfolio-level position limits (max 3 concurrent, configurable)
- CSM-based trade prioritization
- Smart auto-switching chart viewer
- Refactored Simple Test strategy (EMA crossover + H1 confirmation)

### Part 1: Simple Test Strategy Enhancement (2-3 hours) 🔄 IN PROGRESS

**Part 1.1: Modify Strategy** (1.5-2 hours) ⏳ ACTIVE
- File: `src/strategies/simple_test.py`
- Replace time-based logic with EMA crossover detection
- Entry: M15 EMA 20 crosses M15 EMA 50
- Confirmation: H1 EMAs must align in same direction
- Implementation: Detect crossover, validate H1 alignment, calculate confidence

**Part 1.2: Test Changes** (0.5-1 hour) ⏸️ PENDING
- Run pytest: `test_phase2.py::test_simple_test_strategy`
- Manual backtest: EURUSD 2024
- Verify crossover-only trades, H1 confirmation filtering

### Part 2: Backend Portfolio API (5-7 hours) ⏸️ PLANNED
- Portfolio Trade Allocator (position limits, CSM prioritization)
- Endpoints: `/run-multi`, `/ohlc-multi`
- Backend models: `MultiBacktestRequest`
- Service updates: portfolio-aware execution

### Part 3: Extract C# Services (3-4 hours) ⏸️ PLANNED
- ChartRenderingService (candlesticks, EMAs, trades)
- ChartViewportManager (M1→M15 conversion, positioning)
- **CRITICAL:** Preserve all Phase 5.3 Part 1 bug fixes

### Part 4: Frontend Multi-Pair Viewer (5-7 hours) ⏸️ PLANNED
- Functional pair tabs with auto-switching
- Multi-pair data management
- Portfolio metrics aggregation
- Smart chart display logic

### Part 5: Integration & Testing (2-3 hours) ⏸️ PLANNED
- BacktestWindow multi-pair launch UI
- End-to-end testing
- Regression testing (Phase 5.3 bugs preserved)

**Detailed Plan:** See `docs/current/PHASE_6_SMART_PORTFOLIO.md`

---

## Future Phases (Reference)

### Phase 5.3 Parts 2-5: DEFERRED Until After Phase 6
- Part 2: H1/H4 Timeframe Switching (2-3 hours)
- Part 3: UX enhancements (1-2 hours)
- Part 4: Pending trade functionality (3-4 hours)
- Part 5: MT5 EA comparison (4-6 hours)

### Phase 7: Strategy Enhancements (PLANNED)
- Trailing stops, breakeven logic
- Multi-timeframe confirmation
- Risk management (daily loss limits, correlation filter)
- New strategies (breakout, mean reversion)
- Performance optimization (indicator caching)

---

## Session Timeline

| Date | Work | Status |
|------|------|--------|
| Nov 22-30 | Phase 5.3 Part 1 | ✅ Complete |
| Dec 1 (AM) | Phase 5.3 Part 1 Verification | ✅ Complete |
| Dec 1 (PM) | Phase 6 Part 1.1 - Simple Test EMA Crossover | 🔄 Current |

---

**Last Updated:** December 1, 2025 by Claude Code
**Repository:** jcamp-python-backtesting + CSMMonitor (dual repos)
**Branch:** phase5.3-ux-enhancements (active development)
