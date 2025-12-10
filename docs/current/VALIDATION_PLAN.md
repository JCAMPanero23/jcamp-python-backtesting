# Regime & CSM Validation Plan - Python vs MT5 EA

**Created:** December 10, 2025
**Priority:** 🔥 CRITICAL - Must validate before Phase 7 strategy enhancements
**Estimated Effort:** 6-8 hours
**Goal:** Ensure Python regime detection and CSM calculations match MT5 EA exactly

---

## EXECUTIVE SUMMARY

Before implementing Phase 7 strategy enhancements, we need to validate that Python's regime detection and CSM calculations produce **identical results** to the MT5 EA (v1.96). Any discrepancies could cause strategies to behave differently in live trading.

**Key Validations:**
1. **Regime Detection:** Python vs MT5 regime classification (TRENDING/RANGING/TRANSITIONAL)
2. **CSM Calculation:** Python vs MT5 currency strength meter values
3. **Component Scores:** Compare individual indicator scores (ADX, EMA, ATR, Price Action)
4. **Edge Cases:** Handle missing data, market gaps, low liquidity

---

## CURRENT IMPLEMENTATION COMPARISON

### Python Regime Detection (`src/regime_detector.py`)

**Scoring Method:** Competitive scoring with 4 components
- **ADX Score (0-25):** Trend strength measurement
- **EMA Alignment (0-25):** Trend direction consistency (20/50/100 EMAs)
- **ATR Volatility (0-25):** Expanding/contracting volatility (48-bar lookback)
- **Price Action (0-25):** Recent bar patterns (10-bar lookback)

**Classification Logic:**
```python
# Total trending score (0-100) vs ranging score
if trending_score >= 55% and abs(trending - ranging) > 5%:
    return TRENDING
elif ranging_score >= 55% and abs(trending - ranging) > 5%:
    return RANGING
else:
    return TRANSITIONAL
```

**Key Parameters:**
- `TRENDING_THRESHOLD_PERCENT = 55` (%)
- `RANGING_THRESHOLD_PERCENT = 55` (%)
- `CLOSE_SCORES_THRESHOLD = 5.0` (%)
- `MIN_ADX_FOR_TRENDING = 30.0`
- `MIN_EMA_SEPARATION = 0.40` (%)

### MT5 EA Regime Detection (`Jcamp_BacktestEA.mq5` v1.96)

**Input Parameters (Tunable):**
```mq5
input int TrendingThresholdPercent = 55;         // Trending classification threshold (%)
input int RangingThresholdPercent = 40;          // Ranging classification threshold (%)
input double MinADXForTrending = 30.0;           // Min ADX for strong trend
input double MinEMASeparation = 0.40;            // Min EMA separation (%)
```

**Analysis Timeframe:** `PERIOD_H1` (1-hour candles)
**Execution Timeframe:** `PERIOD_M15` (15-minute entries)

**Known Differences to Address:**
1. ⚠️ **Ranging Threshold Mismatch:** Python uses 55%, MT5 uses 40%
   - This affects TRANSITIONAL zone classification
   - **Action:** Verify which is correct, align both

2. ⚠️ **Component Weights:** Need to verify MT5 uses same weights (0-25 each)

3. ⚠️ **Timeframe:** Python likely calculates on H1, verify alignment

---

### Python CSM Calculator (`src/csm_calculator.py`)

**Currencies Tracked (8 majors):**
- USD, EUR, GBP, JPY, CHF, AUD, CAD, NZD

**Pairs Tracked (15 major crosses):**
- EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD, NZDUSD, USDCAD
- EURGBP, EURJPY, EURCHF, GBPJPY, AUDJPY, NZDJPY, CADNZD

**Calculation Method:**
- 24-hour price change for each currency
- Strength index: (48-hour EMA of price - 48-hour EMA) normalized
- Lookback: 48 hours of H1 bars

**Key Parameters:**
- `CSM_LOOKBACK_HOURS = 48`
- `CSM_CALCULATION_PERIOD = 24` (hours for price change)

---

### MT5 CSM Implementation

**Status:** ❓ NEEDS INVESTIGATION
- MT5 EA v1.96 mentions CSM usage in input parameters
- Exact calculation method not visible in snippet provided
- **Action:** Extract CSM calculation logic from MT5 EA

---

## VALIDATION APPROACH

### Phase 1: Data Extraction & Export (2 hours)

#### Step 1.1: Create MT5 Validation Indicator
**File:** `Jcamp_BacktestEA_Validation.mq5` (NEW - MT5 indicator)

**Goal:** Export Python-compatible regime and CSM data for comparison

**Output File Format:** CSV with columns:
```
DateTime,Regime,ADXScore,EMAScore,ATRScore,PriceActionScore,TrendingPercent,RangingPercent,
CSM_EUR,CSM_GBP,CSM_USD,CSM_JPY,CSM_CHF,CSM_AUD,CSM_CAD,CSM_NZD
```

**Example:**
```
2024.12.01 01:00,TRENDING,24.5,18.3,20.1,16.2,69.5,30.5,62.3,48.7,55.1,52.0,...
2024.12.01 02:00,RANGING,18.2,15.6,12.4,14.8,40.2,59.8,61.5,49.2,54.3,51.1,...
```

**MT5 Indicator Features:**
- Runs on 1-hour chart
- Calculates all 4 regime components every bar
- Stores to CSV every hour (auto-append)
- Include confidence scores for comparison

---

#### Step 1.2: Extract Python Validation Data
**File:** `scripts/validate_regime_csm.py` (NEW - 300-400 LOC)

**Goal:** Run backtesting pipeline, export regime and CSM values at each bar

**Output File:** `validation_output_python.csv`

**Logic:**
```python
# Run backtest engine without trade execution
engine = BacktestEngine(strategy='VALIDATION_ONLY')
for each bar in historical data:
    regime = engine.regime_detector.detect(df, current_idx)
    csm = engine.csm_calculator.get_currencies_strength()

    # Export with component scores
    export_row(timestamp, regime, component_scores, csm_values)
```

---

### Phase 2: Validation Framework Setup (1-2 hours)

#### Step 2.1: Create Comparison Test Suite
**File:** `tests/test_regime_csm_validation.py` (NEW - 500-600 LOC)

**Test Cases:**

```python
class TestRegimeValidation:
    """Compare Python regime detection vs MT5 EA"""

    def test_regime_classification_match():
        """Verify TRENDING/RANGING/TRANSITIONAL matches exactly"""
        # Load both CSVs, compare regime column
        # Tolerance: 100% match expected (no fuzziness allowed)

    def test_component_scores_accuracy():
        """Verify ADX, EMA, ATR, Price Action scores within tolerance"""
        # Tolerance: ±0.1 for component scores
        # Any deviation indicates calculation mismatch

    def test_trending_percentage_accuracy():
        """Verify trending/ranging percentages within tolerance"""
        # Tolerance: ±1% for percentage scores

    def test_csm_currency_strength():
        """Verify CSM values for 8 currencies match"""
        # Tolerance: ±0.5 strength points per currency

    def test_csm_pair_differential():
        """Verify pair strength differentials match"""
        # E.g., EURUSD = EUR_strength - USD_strength
        # Tolerance: ±0.1 differential

    def test_edge_cases():
        """Handle missing data, gaps, low liquidity"""
        # Weekend gaps should be skipped consistently
        # Holiday closures should be handled identically
        # Low liquidity periods should not affect results
```

---

### Phase 3: Comparison & Analysis (2-3 hours)

#### Step 3.1: Run Validation Scripts
**Timeline:**
1. Start MT5 validation indicator on live chart (1 week data collection)
2. Run Python validation script on same date range
3. Compare outputs side-by-side

**Date Range for Validation:**
- **Preferred:** 1-2 weeks of recent data (Dec 1-15, 2024)
- **Rationale:** Shows current market behavior, varied regimes
- **Multiple Scenarios:** Include trending, ranging, and transitional days

---

#### Step 3.2: Statistical Comparison
**Metrics to Track:**

```python
# For Regime Classification
precision = exact_matches / total_bars
false_positives = wrongly_classified_trending
false_negatives = wrongly_classified_ranging

# For Component Scores (each component)
mean_error = avg(python_score - mt5_score)
max_error = max(abs(python_score - mt5_score))
std_error = stddev(python_score - mt5_score)

# For CSM Values
currency_correlation = corr(python_csm, mt5_csm)
differential_error = avg(abs(python_pair_diff - mt5_pair_diff))
```

---

#### Step 3.3: Root Cause Analysis
**If Discrepancies Found:**

1. **Classification Mismatch:**
   - Check threshold values (55%, 40%, etc.)
   - Verify component calculation methods
   - Review timeframe handling (H1 vs M15)

2. **Component Score Differences:**
   - Compare ADX calculation (EMA alignment, DI movement)
   - Verify ATR lookback period (48 bars = 2 days H1)
   - Check price action pattern detection (10-bar lookback)
   - Validate EMA calculation (20, 50, 100 periods)

3. **CSM Value Discrepancies:**
   - Verify 24-hour price change calculation
   - Check currency pair calculation order
   - Confirm normalization method
   - Review any smoothing/weighting applied

---

## VALIDATION CHECKLIST

### Pre-Validation
- [ ] Read this plan thoroughly
- [ ] Understand Python regime/CSM implementation
- [ ] Review MT5 EA v1.96 parameters
- [ ] Prepare test data (1-2 weeks H1 data)
- [ ] Set up both Python and MT5 environments

### Data Collection Phase
- [ ] Create MT5 validation indicator
- [ ] Deploy on live chart
- [ ] Collect 100+ bars of data (minimum 5-7 days H1)
- [ ] Create Python validation script
- [ ] Run on same date range as MT5
- [ ] Export both to CSV format

### Testing Phase
- [ ] Create comparison test suite
- [ ] Run all test cases
- [ ] Document any failures
- [ ] Analyze discrepancies
- [ ] Identify root causes
- [ ] Create fix list if needed

### Documentation Phase
- [ ] Write validation report
- [ ] Document all findings
- [ ] List any required fixes
- [ ] Update CLAUDE.md
- [ ] Archive validation data for reference

### Resolution Phase
- [ ] Fix any discrepancies found
- [ ] Re-run validation tests
- [ ] Confirm 100% match or acceptable tolerance
- [ ] Update code comments with learnings
- [ ] Commit validation work to git

---

## SUCCESS CRITERIA

### Regime Detection
- **Exact Match:** Python regime classification = MT5 regime classification
- **Tolerance:** 0% error rate acceptable (must match exactly)
- **Backup:** If discrepancies found, clear documentation of differences

### Component Scores
- **ADX Score:** ±0.1 tolerance (0-25 range)
- **EMA Alignment:** ±0.1 tolerance (0-25 range)
- **ATR Volatility:** ±0.1 tolerance (0-25 range)
- **Price Action:** ±0.1 tolerance (0-25 range)

### CSM Values
- **Currency Strength:** ±0.5 point tolerance (0-100 range)
- **Pair Differential:** ±0.1 tolerance
- **Trend:** CSM should show clear EUR/USD strength bias in trending

### Overall Validation
- [ ] 95%+ exact regime match
- [ ] 99%+ component score accuracy
- [ ] 99%+ CSM accuracy
- [ ] Clear documentation of any differences
- [ ] Root causes identified for any discrepancies

---

## DELIVERABLES

### Code Files
1. **`scripts/validate_regime_csm.py`** - Python validation exporter (300-400 LOC)
2. **`tests/test_regime_csm_validation.py`** - Test suite (500-600 LOC)
3. **`Jcamp_BacktestEA_Validation.mq5`** - MT5 validation indicator (NEW)

### Documentation
4. **Validation Report** - Findings, discrepancies, root causes (3-5 pages)
5. **Comparison Data** - MT5 vs Python CSV comparison (stored in `docs/validation/`)
6. **Fix List** - Any required code changes (if discrepancies found)

### Git Artifacts
7. **Validation Commits** - Separate commits for validation infrastructure
8. **Phase 7 Ready Confirmation** - Sign-off that strategies can proceed

---

## IMPLEMENTATION TIMELINE

| Phase | Task | Duration | Owner |
|-------|------|----------|-------|
| 1 | MT5 indicator development | 1-1.5 hrs | Claude |
| 1 | Python validation script | 1 hr | Claude |
| 2 | Test framework creation | 1-1.5 hrs | Claude |
| 3 | Data collection (passive) | 3-7 days | Automated |
| 3 | Comparison & analysis | 1.5-2 hrs | Claude |
| 4 | Documentation & fixes | 1 hr | Claude |

**Total Active Work:** 6-8 hours
**Total Elapsed Time:** 3-7 days (data collection passive)

---

## RISK MITIGATION

### Risk 1: Timeframe Mismatch
**Issue:** Python uses H1 but MT5 uses different lookback periods
**Mitigation:** Explicitly verify timeframes match exactly

### Risk 2: Missing Edge Cases
**Issue:** Validation data doesn't cover unusual markets (gaps, halts)
**Mitigation:** Include diverse market conditions in test data

### Risk 3: Precision Differences
**Issue:** Python float precision differs from MT5
**Mitigation:** Accept ±0.1 tolerance for component scores, ±0.5 for CSM

### Risk 4: Calculation Order
**Issue:** Different calculation order might cause cumulative errors
**Mitigation:** Match calculation sequence exactly (import from MT5 comments)

---

## NEXT STEPS AFTER VALIDATION

**If Validation PASSES (95%+ match):**
1. ✅ Confirm regime detection is correct
2. ✅ Confirm CSM calculation is correct
3. ✅ Proceed to Phase 7 strategy enhancements
4. ✅ Use regime and CSM with full confidence

**If Validation FAILS (significant discrepancies):**
1. 🔧 Fix identified discrepancies
2. 🧪 Re-run validation tests
3. 📊 Document root cause and solution
4. 📝 Update CLAUDE.md with findings
5. ✅ Re-validate until passing

---

## RESOURCES

### MT5 EA Reference
- File: `D:\JcampFxTrading\Jcamp_BacktestEA.mq5` v1.96
- Key sections: Regime detection parameters, CSM calculations
- Status: Partially visible (binary encoding visible in preview)

### Python Source Code
- Regime Detector: `src/regime_detector.py`
- CSM Calculator: `src/csm_calculator.py`
- Indicators: `src/indicators.py` (ATR, EMA, ADX, RSI)

### Configuration
- Settings: `config/mt5_settings.py`
- Defaults match MT5 input parameters

---

## NOTES

- This validation is **PREREQUISITE** to Phase 7 (cannot start strategy enhancements without validation)
- Results will be **ARCHIVED** in `docs/validation/` for future reference
- Any code changes resulting from validation should be **COMMITTED** with validation tag
- Validation data should be **RETAINED** for regression testing post-Phase 7

---

*Plan Created: December 10, 2025*
*Status: Ready for Implementation*
*Expected Completion: December 13-17, 2025*

