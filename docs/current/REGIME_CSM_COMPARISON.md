# Regime Detection & CSM - Python vs MT5 EA Quick Reference

**Updated:** December 10, 2025
**Purpose:** Side-by-side comparison of Python and MT5 implementations

---

## REGIME DETECTION COMPARISON

### Python Implementation (Current)

```
COMPONENT SCORING (0-25 points each):
├── ADX Score (0-25)
│   └── Trend strength: 0→25 as ADX increases 0→50
│   └── Key: ADX >= 30 for strong trending
├── EMA Alignment (0-25)
│   └── 20 > 50 > 100 (uptrend) or 20 < 50 < 100 (downtrend)
│   └── Separation: >= 0.40% of close price
├── ATR Volatility (0-25)
│   └── Expanding: ATR ratio > 1.2 (trending signal)
│   └── Contracting: ATR ratio < 0.8 (ranging signal)
│   └── Lookback: 48 bars (2 days H1)
└── Price Action (0-25)
    └── Higher highs/lows (trending)
    └── Strong candle bodies > 60% of range (trending)
    └── Weak candle bodies < 30% of range (ranging)
    └── Lookback: 10 bars (1 bar per hour H1)

CLASSIFICATION LOGIC:
├── Calculate Trending Score: Sum of 4 components (0-100)
├── Calculate Ranging Score: 100 - Trending Score
├── Decision Tree:
│   ├── If |Trending% - Ranging%| <= 5%: TRANSITIONAL
│   ├── Else if Trending% >= 55%: TRENDING
│   ├── Else if Ranging% >= 55%: RANGING
│   └── Else: TRANSITIONAL
└── Parameters:
    ├── TRENDING_THRESHOLD_PERCENT = 55
    ├── RANGING_THRESHOLD_PERCENT = 55  ⚠️ NOTE: Different from MT5
    ├── MIN_ADX_FOR_TRENDING = 30.0
    ├── CLOSE_SCORES_THRESHOLD = 5.0%
    └── MIN_EMA_SEPARATION = 0.40%
```

### MT5 EA Implementation (v1.96)

```
INPUT PARAMETERS:
├── Analysis Timeframe: PERIOD_H1 (1-hour candles)
├── Execution Timeframe: PERIOD_M15 (15-minute entries)
├── TrendingThresholdPercent = 55
├── RangingThresholdPercent = 40  ⚠️ NOTE: Different from Python
├── MinADXForTrending = 30.0
├── MinEMASeparation = 0.40%
└── DynamicRegimeMinInterval = 60 minutes (re-check interval)

CLASSIFICATION LOGIC (Inferred from parameters):
├── Similar 4-component scoring approach
├── Decision Tree (likely):
│   ├── Check if ADX >= 30 (strong trend prerequisite)
│   ├── Check if EMA alignment >= 0.40% separation
│   ├── Evaluate overall trending% vs ranging%
│   ├── If Trending >= 55%: TRENDING
│   ├── If Ranging >= 40%: RANGING
│   └── Else: TRANSITIONAL
└── Dynamic Re-evaluation: Every 60 minutes (real-time updating)
```

### Key Differences Found

| Aspect | Python | MT5 | Impact |
|--------|--------|-----|--------|
| **Ranging Threshold** | 55% | 40% | 🔴 CRITICAL: Affects RANGING classification |
| **Dynamic Re-eval** | Static once | Every 60 min | 🟡 Python doesn't update during day |
| **Time Zone** | UTC implicit | Market time | ⚠️ May affect hour boundaries |
| **Component Method** | Clear scoring | Inferred | Need to verify exact formula |

---

## CSM CALCULATION COMPARISON

### Python Implementation

```
CURRENCY TRACKING (8 majors):
├── EUR (Euro)
├── USD (US Dollar)
├── GBP (British Pound)
├── JPY (Japanese Yen)
├── CHF (Swiss Franc)
├── AUD (Australian Dollar)
├── CAD (Canadian Dollar)
└── NZD (New Zealand Dollar)

PAIR TRACKING (15 crosses):
├── EURUSD, GBPUSD, USDJPY, USDCHF, AUDUSD
├── NZDUSD, USDCAD, EURGBP, EURJPY, EURCHF
├── GBPJPY, AUDJPY, NZDJPY, CADNZD
└── (Extends to 15+ pairs as configured)

CALCULATION METHOD:
├── Step 1: Calculate 24-hour price change for each pair
│   └── Formula: (Close_now - Close_24h_ago) / Close_24h_ago * 100
├── Step 2: Convert pair changes to 8 currency strengths
│   └── Build matrix: 8 currencies × 15 pairs
│   └── Solve for individual currency strength (LSQ or similar)
├── Step 3: Normalize to 0-100 scale
│   ├── Base strength = 50.0 (neutral)
│   ├── Strong currency = 60-100
│   └── Weak currency = 0-40
└── Parameters:
    ├── CSM_LOOKBACK_HOURS = 48 (2 days)
    ├── CSM_CALCULATION_PERIOD = 24 (hours)
    └── CSM_CURRENCIES = 8 majors
```

### MT5 EA Implementation

```
STATUS: ❓ NOT FULLY VISIBLE IN CODE SNIPPET
Mentioned in input parameters but calculation hidden in binary.

INFERRED PARAMETERS:
├── Likely uses similar 48-hour lookback
├── Likely calculates 24-hour price changes per pair
├── Likely normalizes currency strength 0-100
└── Likely includes volatility weighting

TO VALIDATE:
├── Exact currency pair list used
├── Normalization method (standard deviation, percentile, etc.)
├── Any smoothing/EMA applied to CSM values
├── Weight given to different pairs
└── Base value for neutral currency (50? 0?)
```

---

## COMPONENT SCORE EXAMPLES

### Example: EURUSD During Trending Day

```
Hour: 2024.12.01 10:00
Market Condition: Clear uptrend (strong buyers)

ADX Score: 24.5/25 ✅
├── ADX = 42.3 (very strong)
├── Calculation: min(25, ADX/2) = min(25, 21.15) = 21.15
└── Interpretation: Strong trend detected

EMA Alignment: 18.3/25 ✅
├── EMA20 = 1.1050
├── EMA50 = 1.1020  (1050 > 1020 > 1000 = uptrend)
├── EMA100 = 1.1000
├── Separation: (1050 - 1020) / 1020 = 0.29% >= 0.40%? ❌ Not enough
└── Score: 18.3 (partial credit for alignment)

ATR Volatility: 20.1/25 ✅
├── Current ATR = 0.00215
├── 48-hour avg ATR = 0.00179
├── Ratio = 0.00215 / 0.00179 = 1.20 = threshold
├── Score: 25 * (1.20 / 1.2) = 25.0 ✅ (expanding volatility)
└── Interpretation: Expanding volatility = trending market

Price Action: 16.2/25 ⚠️
├── Last 10 bars: 6 higher highs, 4 lower highs
├── Candle bodies: avg 65% of range (strong)
├── Score: 16.2 (good but not perfect)
└── Interpretation: Mixed signals (momentum slight weaker)

TOTAL TRENDING SCORE: 24.5 + 18.3 + 20.1 + 16.2 = 79.1 / 100 ✅
│
├── Trending Score: 79.1%
├── Ranging Score: 20.9%
├── Difference: 58.2% (well above 5% threshold)
└── CLASSIFICATION: ✅ TRENDING (strong confidence)
```

### Example: EURUSD During Ranging Day

```
Hour: 2024.12.03 14:00
Market Condition: Consolidation range, choppy

ADX Score: 12.2/25 ⚠️
├── ADX = 18.5 (weak)
├── Calculation: min(25, 18.5/2) = 9.25... (much lower)
└── Interpretation: Low trend strength

EMA Alignment: 14.6/25 ⚠️
├── EMA20 = 1.1050
├── EMA50 = 1.1055  (20 < 50 > 100 = mixed)
├── EMA100 = 1.1045
├── Separation: Much weaker alignment
└── Score: 14.6 (struggling to align)

ATR Volatility: 8.4/25 🔴
├── Current ATR = 0.00089
├── 48-hour avg ATR = 0.00187
├── Ratio = 0.00089 / 0.00187 = 0.48 << 0.8 (contracting)
├── Score: 0 (strong ranging signal)
└── Interpretation: ATR compression = consolidation

Price Action: 11.2/25 ⚠️
├── Last 10 bars: 3 higher highs, 3 lower lows (choppy)
├── Candle bodies: avg 28% of range (weak)
├── Score: 11.2 (weak bodies = ranging)
└── Interpretation: Consolidation pattern

TOTAL RANGING SCORE: 100 - (12.2 + 14.6 + 8.4 + 11.2) = 53.6 / 100 ✅
│
├── Trending Score: 46.4%
├── Ranging Score: 53.6%
├── Difference: 7.2% (above 5% threshold just barely)
└── CLASSIFICATION: ✅ RANGING (moderate confidence)
```

---

## VALIDATION PRIORITY

### Must Match Exactly:
1. **Regime Classification** - TRENDING/RANGING/TRANSITIONAL
   - No tolerance (either right or wrong)
   - If mismatch, strategies behave differently

2. **ADX Score Accuracy** - ±0.1 tolerance
   - Foundation for trend detection
   - Critical for trade quality

3. **EMA Alignment** - ±0.1 tolerance
   - Ensures entry condition matching
   - Prevents false signals

### Should Match Within Tolerance:
4. **ATR Volatility Score** - ±0.1 tolerance
   - Supports trend detection
   - Stop loss sizing depends on this

5. **Price Action Score** - ±0.1 tolerance
   - Recent market behavior indicator
   - Less critical than ADX/EMA

### CSM Validation:
6. **Currency Strength** - ±0.5 point tolerance
   - Used for pair selection and weighting
   - Pair differentials more important than absolute values

---

## RED FLAGS TO INVESTIGATE

🚩 **If Ranging Threshold remains 40% in MT5:**
- Python needs to match (55% is wrong)
- This affects 15% of trading hours (RANGING misclassifications)

🚩 **If dynamic re-evaluation is critical:**
- Python needs to add hourly regime checks
- Current static approach may miss transitions

🚩 **If component calculation differs:**
- ADX formula (SMA vs EMA smoothing?)
- ATR lookback (48 bars confirmed?)
- Price action pattern detection method

🚩 **If CSM normalization differs:**
- Currency strength calculation method
- Pair weight distribution
- Base neutral value (50 vs 0?)

---

## EXPECTED OUTCOMES

### Scenario 1: Perfect Match (95%+ agreement)
✅ **Action:** Proceed to Phase 7 strategy enhancements with confidence
✅ **Notes:** Python implementation is correct
✅ **Risk:** Minimal (strategies will behave as expected)

### Scenario 2: Minor Discrepancies (85-95% agreement)
⚠️ **Action:** Investigate discrepancies, determine if fix needed
⚠️ **Notes:** Likely rounding or precision differences
⚠️ **Risk:** Low (if tolerance-based, acceptable)

### Scenario 3: Major Discrepancies (<85% agreement)
🔴 **Action:** HALT Phase 7, fix Python implementation
🔴 **Notes:** Critical bug in regime or CSM calculation
🔴 **Risk:** HIGH (strategies will behave differently than MT5 EA)

---

## NEXT STEPS

1. **Implement validation framework** (2-3 hours)
   - Create MT5 validation indicator
   - Create Python validation exporter
   - Set up test suite

2. **Collect comparison data** (3-7 days passive)
   - Run MT5 indicator on live chart
   - Run Python exporter on same period
   - Export both to CSV

3. **Run validation tests** (1-2 hours)
   - Load both CSVs
   - Compare regime classifications
   - Compare component scores and CSM values

4. **Analyze results** (1 hour)
   - Calculate match percentages
   - Identify any systematic differences
   - Document findings

5. **Take action** (0-4 hours depending on outcome)
   - If match: Approve for Phase 7
   - If mismatch: Fix code and re-validate

---

*Reference Document Created: December 10, 2025*
*For detailed validation plan, see VALIDATION_PLAN.md*

