# Master Plan: Phase 5-7 Implementation

**Updated:** December 1, 2025
**Status:** Phase 5.3 Part 1 COMPLETE - Enhancements Ready for Implementation
**Current Work:** Phase 5.3 UX Enhancements (Enhancement #1 + #3)
**Estimated Total Effort for Remaining Work:** 14-20 hours

---

## QUICK STATUS

### ✅ Completed
- **Phase 5.3 Part 1:** M1 Viewport Positioning Bugs (COMPLETE)
  - M1→M15 coordinate mismatch resolved
  - Smooth M1 playback at 80% position
  - Zoom preservation working
  - Key commits: 2309b9d, ed49bc2, f951fc0, ec96f47

### 🔄 Ready Now
- **Enhancement #1 Adjustments:** Timeline-Based Recent Trades (30-45 min)
- **Enhancement #3:** Multi-Pair Chart Display (13-19 hours)

### 📋 Planned
- Part 2: H1/H4 Timeframe Switching (2-3 hours)
- Phase 6: Multi-Pair Backtesting API
- Phase 7: Strategy Enhancements

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

## Future Phases (Reference)

### Phase 5.3 Part 2: H1/H4 Timeframe Switching (PLANNED)
- Implement M15→H1/H4 aggregation
- Recalculate indicators per timeframe
- Update grid spacing based on timeframe

### Phase 6: Multi-Pair Backtesting (PLANNED)
- Enhanced multi-pair API support
- Results aggregation and display
- Portfolio-level metrics

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
| Dec 1 | Phase 5.3 Part 1 Verification | ✅ Complete |
| Dec 1+ | Phase 5.3 Enhancements (#1 & #3) | 🔄 Current |

---

**Last Updated:** December 1, 2025 by Claude Code
**Repository:** jcamp-python-backtesting + CSMMonitor (dual repos)
**Branch:** phase5.3-ux-enhancements (active development)
