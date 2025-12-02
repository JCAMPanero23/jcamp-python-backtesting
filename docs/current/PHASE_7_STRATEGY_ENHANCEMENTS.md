# Phase 7: Strategy Enhancements - Master Plan

**Created:** December 2, 2025
**Priority:** 🔥 TOP PRIORITY (Next Session)
**Total Effort:** 14-18 hours
**Goal:** Improve strategy profitability and risk management to reach $5k/month signal service target

---

## EXECUTIVE SUMMARY

With Phase 1 performance optimization complete (13 min → 46 sec), we can now iterate quickly on strategy improvements. This phase focuses on enhancing Trend Rider and Range Rider strategies to maximize profitability while minimizing risk.

**Target Improvements:**
- **Trend Rider:** +9.18R → +15-20R (60% improvement)
- **Range Rider:** +6.86R → +10-12R (50% improvement)
- **Win Rate:** Maintain >50% while improving R-multiple
- **Risk Management:** Daily loss limits, position correlation

---

## CURRENT STRATEGY ANALYSIS

### SimpleTest Strategy ✅ (Working Well)
**Status:** Complete, no changes needed
**Purpose:** Chart viewer testing and validation
**Performance:** Fixed 2:1 R:R, reliable signals
**Entry:** M15 EMA 20/50 crossover + H1 confirmation
**Exit:** Fixed 5 pip SL, 10 pip TP

**Keep as-is** - This strategy is for testing only.

---

### Trend Rider Strategy ⚠️ (Needs Major Improvements)

**Current State:**
- 135-point confidence scoring (EMA, ADX, Momentum, CSM)
- Min confidence: 65%
- Stop loss: 1.2 x ATR (fixed)
- **NO trailing stop** ❌
- **NO take profit** ❌
- **NO breakeven logic** ❌
- **NO multi-timeframe confirmation beyond CSM** ❌

**Issues Identified:**
1. **Letting winners turn into losers** - No trailing stop means profitable trades often reverse
2. **No profit protection** - No breakeven move after reaching certain R-multiple
3. **Too aggressive** - Enters on 65% confidence without additional confirmation
4. **Weak exits** - Only stops out on SL, no dynamic profit-taking
5. **No risk management** - Can open multiple trending trades simultaneously without correlation check

**Target Performance:**
- Current: +9.18R (60W/61L)
- Target: +15-20R (improved win rate + bigger winners)

---

### Range Rider Strategy ⚠️ (Needs Moderate Improvements)

**Current State:**
- Support/resistance range trading
- RSI oversold/overbought confirmation
- Break-even exit at +0.5R ✅ (GOOD!)
- Max hold time: 48 hours ✅ (GOOD!)
- Stop loss: 1.0 x ATR

**Issues Identified:**
1. **Simple support/resistance detection** - Uses basic min/max over 48 bars
2. **No pivot point analysis** - Missing key S/R levels
3. **Fixed break-even** - Always exits at +0.5R, misses bigger moves
4. **No take profit targets** - Only exits at BE or max hold time
5. **Range detection too simplistic** - Needs better consolidation identification

**Target Performance:**
- Current: +6.86R (18W/10L)
- Target: +10-12R (better entries + bigger winners)

---

## PHASE 7 IMPLEMENTATION PLAN

### Part 1: Trend Rider Enhancements (6-8 hours) 🔥 HIGHEST PRIORITY

#### 1.1: Trailing Stop Logic (2 hours)

**Objective:** Let winners run, lock in profits as trade moves favorably

**Implementation:**
- File: `src/strategies/trend_rider.py`
- New method: `update_trailing_stop(position, current_price, df, current_idx)`
- New config: `trailing_stop_activation_r` (default: 1.5R)
- New config: `trailing_stop_distance_atr` (default: 1.0 x ATR)

**Logic:**
```python
# Activate trailing stop after reaching 1.5R profit
if current_r >= 1.5:
    # Trail by 1.0 x ATR from highest favorable price
    if signal == 'BUY':
        new_stop = max_favorable_price - (atr * 1.0)
        position.stop_loss = max(position.stop_loss, new_stop)
    else:  # SELL
        new_stop = min_favorable_price + (atr * 1.0)
        position.stop_loss = min(position.stop_loss, new_stop)
```

**Expected Impact:** +3-5R improvement (fewer winners reversing into losers)

---

#### 1.2: Breakeven Logic (1 hour)

**Objective:** Protect capital by moving stop to breakeven after small profit

**Implementation:**
- File: `src/strategies/trend_rider.py`
- New method: `check_breakeven_move(position, current_price, df, current_idx)`
- New config: `breakeven_activation_r` (default: 0.8R)
- New config: `breakeven_buffer_pips` (default: 2 pips)

**Logic:**
```python
# Move stop to breakeven + 2 pips after reaching 0.8R profit
if current_r >= 0.8 and not position.breakeven_moved:
    if signal == 'BUY':
        position.stop_loss = entry_price + (2 * pip_size)
    else:  # SELL
        position.stop_loss = entry_price - (2 * pip_size)
    position.breakeven_moved = True
```

**Expected Impact:** +2-3R improvement (reduce -1R losses to breakeven)

---

#### 1.3: Take Profit Targets (1.5 hours)

**Objective:** Scale out of positions at key profit levels

**Implementation:**
- File: `src/strategies/trend_rider.py`
- New method: `get_take_profit_levels(df, current_idx, signal)`
- New config: `use_partial_exits` (default: True)
- New config: `tp1_r_multiple` (default: 2.0R, close 50%)
- New config: `tp2_r_multiple` (default: 3.5R, close 30%)
- New config: `tp3_trail_remainder` (default: True, trail 20%)

**Logic:**
```python
# Partial exits at key R-multiples
TP1: Close 50% at 2.0R, move stop to breakeven
TP2: Close 30% at 3.5R, trail remainder by 1.0 ATR
TP3: Trail remaining 20% until stopped out
```

**Expected Impact:** +4-6R improvement (lock in profits while letting runners run)

---

#### 1.4: Multi-Timeframe Confirmation (1.5 hours)

**Objective:** Add H4 EMA confirmation to reduce false signals

**Implementation:**
- File: `src/backtest_engine.py` (calculate H4 EMAs)
- File: `src/strategies/trend_rider.py` (add H4 filter)
- New method: `check_h4_confirmation(df, current_idx, signal)`
- New config: `require_h4_confirmation` (default: True)

**Logic:**
```python
# Require H4 EMA 20/50/100 alignment for entry
# BUY: H4 EMA 20 > H4 EMA 50 > H4 EMA 100
# SELL: H4 EMA 20 < H4 EMA 50 < H4 EMA 100
# Skip trade if H4 alignment conflicts with M15 signal
```

**Expected Impact:** +1-2R improvement (fewer false breakouts, higher quality trades)

---

### Part 2: Range Rider Enhancements (3-4 hours) 🔥 HIGH PRIORITY

#### 2.1: Advanced Support/Resistance Detection (2 hours)

**Objective:** Identify higher-quality S/R levels using pivot points and volume

**Implementation:**
- File: `src/strategies/range_rider.py`
- New method: `find_pivot_levels(df, current_idx, lookback=100)`
- New method: `validate_support_resistance_quality(support, resistance, df, touches_required=3)`

**Logic:**
```python
# Pivot Point Detection:
# 1. Find local highs/lows (swing points)
# 2. Cluster nearby levels (within 10 pips)
# 3. Require minimum 3 touches for valid S/R
# 4. Score by touch count and recent price reactions

# Quality Scoring (0-100):
# - 3 touches: 60 points
# - 4 touches: 75 points
# - 5+ touches: 90 points
# - Recent bounce: +10 points
# - Wide range: +10 points
```

**Expected Impact:** +2-3R improvement (better entry locations, fewer false ranges)

---

#### 2.2: Dynamic Take Profit (1 hour)

**Objective:** Set TP targets based on range width, not just break-even

**Implementation:**
- File: `src/strategies/range_rider.py`
- New method: `calculate_dynamic_take_profit(support, resistance, signal)`
- New config: `tp_range_pct` (default: 50% of range width)

**Logic:**
```python
# Dynamic TP based on range width
range_width = resistance - support
target_distance = range_width * 0.5  # Target 50% range retracement

if signal == 'BUY':
    # Enter at support, target 50% to middle of range
    take_profit = entry_price + target_distance
else:  # SELL
    # Enter at resistance, target 50% to middle of range
    take_profit = entry_price - target_distance
```

**Expected Impact:** +2-3R improvement (capture mean reversion moves)

---

#### 2.3: Better Range Detection (1 hour)

**Objective:** Identify true consolidation ranges, filter out choppy markets

**Implementation:**
- File: `src/strategies/range_rider.py`
- New method: `is_consolidating(df, current_idx, lookback=48)`
- New config: `consolidation_atr_ratio` (default: 1.5)

**Logic:**
```python
# Consolidation Detection:
# 1. Compare recent ATR to longer-term ATR
# 2. ATR compression = consolidation
# 3. Require recent_atr < avg_atr * 0.7
# 4. Require range width > 1.5 x ATR

if recent_atr < (avg_atr_100 * 0.7):
    consolidating = True  # Low volatility = range forming
```

**Expected Impact:** +1-2R improvement (fewer whipsaw losses in choppy markets)

---

### Part 3: Risk Management System (3-4 hours) 🔥 CRITICAL

#### 3.1: Daily Loss Limit (1 hour)

**Objective:** Protect capital by stopping trading after max daily loss

**Implementation:**
- File: `src/performance_tracker.py` (already has placeholder!)
- Enable existing `is_daily_loss_limit_reached()` method
- New config: `max_daily_loss_pct` (default: 5% of balance)
- New config: `max_daily_loss_trades` (default: 3 consecutive losses)

**Logic:**
```python
# Stop trading for rest of day if:
# 1. Total loss for day > 5% of starting balance
# 2. Three consecutive losses (emotional protection)

if daily_loss_pct > 5.0 or consecutive_losses >= 3:
    return True  # Block new trades until next day
```

**Expected Impact:** -2 to -5R protection (prevent blown accounts)

---

#### 3.2: Position Correlation Filter (2 hours)

**Objective:** Avoid correlated positions that amplify risk

**Implementation:**
- File: `src/position_manager.py`
- New method: `check_correlation_limit(new_symbol, existing_positions)`
- New config: `max_correlated_positions` (default: 2)
- New config: `correlation_pairs` (dict of correlated pairs)

**Logic:**
```python
# Correlation Rules:
# 1. EURUSD + GBPUSD = correlated (EUR/GBP similar trends)
# 2. AUDUSD + NZDUSD = correlated (commodity currencies)
# 3. USDJPY + USDCHF = correlated (both USD-based)

# Block new trade if 2+ correlated positions already open
correlation_map = {
    'EURUSD': ['GBPUSD', 'EURGBP'],
    'GBPUSD': ['EURUSD', 'EURGBP'],
    'AUDUSD': ['NZDUSD', 'AUDNZD'],
    'NZDUSD': ['AUDUSD', 'AUDNZD'],
    'USDJPY': ['USDCHF'],
    'USDCHF': ['USDJPY']
}
```

**Expected Impact:** -1 to -3R protection (reduce correlated drawdowns)

---

#### 3.3: Maximum Concurrent Positions Enhancement (1 hour)

**Objective:** Smart position limits based on strategy type

**Implementation:**
- File: `src/position_manager.py`
- New config: `max_trend_positions` (default: 2)
- New config: `max_range_positions` (default: 1)
- New config: `max_total_positions` (default: 3)

**Logic:**
```python
# Strategy-Specific Limits:
# - Trend Rider: Max 2 positions (let winners run)
# - Range Rider: Max 1 position (mean reversion, quick exits)
# - Total: Max 3 positions across all strategies

def can_open_position(strategy_name):
    trend_count = count_positions_by_strategy('TREND_RIDER')
    range_count = count_positions_by_strategy('RANGE_RIDER')
    total_count = len(open_positions)

    if strategy_name == 'TREND_RIDER':
        return trend_count < 2 and total_count < 3
    elif strategy_name == 'RANGE_RIDER':
        return range_count < 1 and total_count < 3
```

**Expected Impact:** -1 to -2R protection (prevent overtrading)

---

### Part 4: New Strategy - Breakout Rider (3-4 hours) ⏸️ OPTIONAL

**Status:** OPTIONAL - Only if time permits after Parts 1-3

**Objective:** Capture explosive moves when price breaks key levels

**Entry Conditions:**
- Price breaks above/below consolidation range
- Volume spike confirmation (if available)
- ATR expansion (volatility increase)
- H1/H4 trend alignment

**Exit Conditions:**
- Trailing stop: 1.5 x ATR
- Take profit: 3.0R
- Max hold: 24 hours

**Expected Performance:** +8-12R (capture momentum moves)

**Files:**
- NEW: `src/strategies/breakout_rider.py` (300-400 LOC)
- Update: `src/backtest_engine.py` (add breakout strategy)

---

## TESTING STRATEGY

### Unit Tests (1 hour)
- Test trailing stop calculations
- Test breakeven logic
- Test take profit levels
- Test correlation filter
- Test daily loss limits

**Command:**
```bash
pytest tests/test_strategies.py -v
pytest tests/test_position_manager.py -v
pytest tests/test_performance_tracker.py -v
```

---

### Backtest Validation (1 hour)

**Test Scenarios:**
1. **EURUSD 2024 Full Year** - Baseline comparison
2. **GBPUSD 2024 Q1-Q2** - Trend Rider validation
3. **USDJPY 2024 Q3-Q4** - Range Rider validation
4. **Multi-pair 3 months** - Correlation filter testing

**Success Criteria:**
- Trend Rider R-multiple: +15 to +20 (vs +9.18 current)
- Range Rider R-multiple: +10 to +12 (vs +6.86 current)
- Win rate: >50% maintained
- Max drawdown: <25% (vs current unknown)
- Daily loss limit: 0 violations (stop trading when hit)

---

## IMPLEMENTATION PRIORITY

### 🔥 CRITICAL (Session 1 - 6-8 hours)
1. **Trend Rider Trailing Stop** (2 hrs) - Biggest impact
2. **Trend Rider Breakeven Logic** (1 hr) - Capital protection
3. **Trend Rider Take Profit Targets** (1.5 hrs) - Lock in profits
4. **Daily Loss Limit** (1 hr) - Risk management
5. **Position Correlation Filter** (2 hrs) - Risk management

**Rationale:** These 5 changes will have the biggest impact on profitability and risk reduction.

---

### ⚡ HIGH PRIORITY (Session 2 - 4-5 hours)
6. **Trend Rider Multi-Timeframe Confirmation** (1.5 hrs) - Quality filter
7. **Range Rider Advanced S/R Detection** (2 hrs) - Better entries
8. **Range Rider Dynamic Take Profit** (1 hr) - Bigger winners
9. **Range Rider Better Consolidation Detection** (1 hr) - Fewer false signals

**Rationale:** These improve entry/exit quality and reduce false signals.

---

### 🔄 OPTIONAL (Session 3 - 3-4 hours)
10. **Breakout Rider Strategy** (3-4 hrs) - New strategy for momentum

**Rationale:** Only if time permits. Current strategies should be profitable first.

---

## FILE CHANGES SUMMARY

### Files to Modify:
1. `src/strategies/trend_rider.py` (major updates)
   - Add trailing stop logic
   - Add breakeven logic
   - Add take profit logic
   - Add H4 confirmation check
   - ~200 LOC added

2. `src/strategies/range_rider.py` (moderate updates)
   - Improve S/R detection
   - Add dynamic TP
   - Better range detection
   - ~150 LOC added

3. `src/position_manager.py` (moderate updates)
   - Correlation filter
   - Strategy-specific position limits
   - ~100 LOC added

4. `src/performance_tracker.py` (minor updates)
   - Enable daily loss limit
   - ~50 LOC added

5. `src/backtest_engine.py` (minor updates)
   - Calculate H4 EMAs
   - Pass H4 data to strategies
   - ~30 LOC added

### Files to Create:
6. `src/strategies/breakout_rider.py` (optional)
   - NEW strategy implementation
   - ~300-400 LOC

7. `tests/test_strategy_enhancements.py` (NEW)
   - Unit tests for new features
   - ~200-300 LOC

### Files to Update:
8. `CLAUDE.md` - Update with Phase 7 status
9. `STATUS.md` - Update progress tracking
10. `docs/current/PHASE_5_7_MASTER_PLAN.md` - Mark Phase 7 complete

---

## EXPECTED OUTCOMES

### Performance Improvements:
| Strategy | Current R | Target R | Improvement |
|----------|-----------|----------|-------------|
| Trend Rider | +9.18R | +15-20R | +60-120% |
| Range Rider | +6.86R | +10-12R | +46-75% |
| Combined | +16.04R | +25-32R | +56-100% |

### Risk Improvements:
- Daily loss limit: Protect against -5%+ down days
- Correlation filter: Reduce correlated drawdowns by 30-50%
- Breakeven logic: Convert -1R losses to breakeven exits
- Max drawdown: Target <20% (from unknown current)

### Win Rate Target:
- Maintain >50% win rate (currently 52%)
- Improve average winner size (2.5R+ vs current ~1.5R)
- Reduce average loser size (0.5R vs current ~1.0R)

---

## BUSINESS IMPACT

**Current State:**
- Backtest performance: +16R (decent, but not validated)
- Win rate: 52% (good)
- No live trading validation yet

**After Phase 7:**
- Backtest performance: +25-32R (excellent)
- Improved risk management (daily loss limits, correlation)
- Ready for 2-month demo account validation
- Then 3-4 months live account validation ($500 micro lots)

**Path to $5k/month Signal Service:**
1. ✅ Phase 1-6: Build and optimize engine
2. 🔄 Phase 7: Enhance strategies (THIS PHASE)
3. ⏸️ 2 months demo validation (Feb-Mar 2026)
4. ⏸️ 4 months live validation (Apr-Jul 2026)
5. ⏸️ Launch signal service (Aug 2026)
6. 🎯 Scale to 100 subscribers @ $50/mo (Dec 2026)

**Phase 7 is CRITICAL** - Without profitable strategies, the business model fails.

---

## SESSION PLAN (Next Session)

### Pre-Session Checklist:
- [ ] Read this document
- [ ] Review current strategy performance
- [ ] Check git status (both repos)
- [ ] Ensure API server is ready

### Session Workflow:
1. **Start (10 min):** Review plan, prioritize changes
2. **Implementation (5-6 hrs):** Code the 5 critical changes
3. **Testing (1 hr):** Unit tests + backtest validation
4. **Commit (15 min):** Commit and push changes
5. **Documentation (30 min):** Update CLAUDE.md, STATUS.md

### Session Goals:
- Complete 5 critical enhancements (Trailing stop, BE, TP, Daily loss, Correlation)
- Pass all unit tests
- Run validation backtests
- Commit and push to phase6-multi-pair branch

---

## REFERENCES

### Current Strategy Files:
- `src/strategies/simple_test.py` (246 LOC) - Keep as-is
- `src/strategies/trend_rider.py` (429 LOC) - Major updates needed
- `src/strategies/range_rider.py` (495 LOC) - Moderate updates needed

### Supporting Files:
- `src/position_manager.py` - Add correlation filter
- `src/performance_tracker.py` - Enable daily loss limits
- `src/backtest_engine.py` - Add H4 EMAs

### Related Documents:
- `docs/current/PHASE_5_7_MASTER_PLAN.md` - Original plan
- `CLAUDE.md` - Project context
- `STATUS.md` - Progress tracking

---

**Next Session Priority:** 🔥 Start with Part 1.1 (Trailing Stop) - Biggest ROI

*Last Updated: December 2, 2025*
*Total Estimated Effort: 14-18 hours*
*Expected R-Multiple Improvement: +9 to +16R (+56-100%)*
