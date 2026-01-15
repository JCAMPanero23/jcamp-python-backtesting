# BUG: Strategy Selection Not Implemented in Multi-Pair Backtest

**Date:** January 11, 2026
**Severity:** HIGH
**Phase:** Phase 8.1 - Multi-Pair Backtest Implementation
**Status:** IDENTIFIED - FIX IN PROGRESS

---

## Summary

The multi-pair backtest API accepts a `strategies` parameter in the request but does not use it. All backtests default to `simple_test` strategy regardless of what strategies are requested.

---

## Evidence

### Request (test_multi_pair_request.json)
```json
{
  "pairs": ["EURUSD", "GBPUSD"],
  "strategies": ["trend_rider", "range_rider"],  // ← Requested strategies
  ...
}
```

### Response (test_results.json)
```json
{
  "trades": [
    {
      "strategy": "SIMPLE_TEST",  // ← All trades use SIMPLE_TEST
      ...
    }
  ],
  "strategy_breakdown": {}  // ← Empty - no per-strategy statistics
}
```

**Expected:** Trades should use trend_rider and range_rider strategies.
**Actual:** All trades use SIMPLE_TEST strategy.

---

## Root Cause

### File: `src/backtest_engine.py`

**Line 330:** Always calls simple_test
```python
st_signal, st_confidence, st_details = self.simple_test.generate_signal(
```

**Lines 342, 354:** Trend Rider and Range Rider are commented out
```python
# tr_signal, tr_confidence, tr_details = self.trend_rider.generate_signal(
...
# rr_signal, rr_confidence, rr_details = self.range_rider.generate_signal(
```

**Line 197:** `run_backtest()` method signature
```python
def run_backtest(
    self,
    symbol: str,
    year: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict:
```
**Missing parameter:** `strategies: List[str]`

### File: `src/api/services/backtest_service.py`

**Line 827:** Doesn't pass strategies to engine
```python
results = engine.run_backtest(
    symbol=symbol,
    year=year,
    start_date=request['start_date'],
    end_date=request['end_date']
)
# Missing: strategies=request['strategies']
```

---

## Impact

1. **Functional Impact:**
   - Users cannot test with trend_rider or range_rider strategies
   - Multi-pair backtest is limited to simple_test only
   - Strategy comparison is impossible

2. **Data Impact:**
   - `strategy_breakdown` field is always empty
   - Cannot analyze performance by strategy
   - No way to compare strategy effectiveness

3. **Phase 8 Impact:**
   - Phase 8.1 Python API Enhancement is INCOMPLETE
   - Phase 8.2 C# multi-strategy UI will have nothing to display
   - Blocks progress on Phase 8 goals

---

## Fix Required

### 1. Update `BacktestEngine.run_backtest()` signature
Add `strategies` parameter:
```python
def run_backtest(
    self,
    symbol: str,
    year: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    strategies: List[str] = None  # NEW
) -> Dict:
```

### 2. Update evaluation logic
Uncomment and enable trend_rider and range_rider based on `strategies` parameter:
```python
if 'trend_rider' in strategies:
    tr_signal, tr_confidence, tr_details = self.trend_rider.generate_signal(...)

if 'range_rider' in strategies:
    rr_signal, rr_confidence, rr_details = self.range_rider.generate_signal(...)
```

### 3. Update `backtest_service.py`
Pass strategies to engine:
```python
results = engine.run_backtest(
    symbol=symbol,
    year=year,
    start_date=request['start_date'],
    end_date=request['end_date'],
    strategies=request['strategies']  # NEW
)
```

### 4. Update strategy breakdown calculation
Ensure `_merge_multi_pair_results()` properly groups trades by strategy field.

---

## Testing Plan

1. Run multi-pair backtest with `["trend_rider"]`
   - Verify all trades show `"strategy": "TREND_RIDER"`
   - Verify `strategy_breakdown` has trend_rider statistics

2. Run multi-pair backtest with `["range_rider"]`
   - Verify all trades show `"strategy": "RANGE_RIDER"`
   - Verify `strategy_breakdown` has range_rider statistics

3. Run multi-pair backtest with `["trend_rider", "range_rider"]`
   - Verify trades show mix of both strategies
   - Verify `strategy_breakdown` has both strategies

4. Re-run Phase 8.1 unit tests (10/10 should still pass)

5. Re-run Phase 8.1 integration test

---

## Timeline

- **Bug Identified:** January 11, 2026 02:05 AM
- **Fix Started:** January 11, 2026 02:10 AM
- **Fix Complete:** TBD
- **Testing Complete:** TBD

---

## Related Files

- `src/backtest_engine.py` (lines 197-400)
- `src/api/services/backtest_service.py` (line 827)
- `tests/test_phase8.py` (Phase 8.1 tests)
- `verification_summary.md` (verification results)
