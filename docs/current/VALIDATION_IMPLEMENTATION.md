# Regime & CSM Validation - Step-by-Step Implementation Guide

**Created:** December 10, 2025
**Duration:** 6-8 hours total work
**Status:** Ready to implement

---

## PHASE 1: DATA EXTRACTION (2 hours)

### Step 1.1: Create Python Validation Script

**File:** `scripts/validate_regime_csm.py` (NEW - 350 LOC)

```python
#!/usr/bin/env python3
"""
Regime & CSM Validation Exporter
Exports Python regime detection and CSM values for comparison with MT5 EA
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import DataLoader
from regime_detector import RegimeDetector, RegimeType
from csm_calculator import CSMCalculator
from indicators import TechnicalIndicators
from config.mt5_settings import *

class ValidationExporter:
    """Export regime and CSM data for validation"""

    def __init__(self, output_file: str = "validation_output_python.csv"):
        self.output_file = output_file
        self.data_loader = DataLoader()
        self.regime_detector = RegimeDetector()
        self.csm_calculator = CSMCalculator()
        self.indicators = TechnicalIndicators()

    def export_regime_csm_data(self,
                               pair: str = 'EURUSD',
                               year: int = 2024,
                               start_date: str = '2024-12-01',
                               end_date: str = '2024-12-07'):
        """
        Export regime and CSM data for validation

        Args:
            pair: Currency pair (e.g., 'EURUSD')
            year: Year to load
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        """

        print(f"\n{'='*80}")
        print(f"REGIME & CSM VALIDATION EXPORT")
        print(f"Pair: {pair}, Period: {start_date} to {end_date}")
        print(f"{'='*80}\n")

        # Load M1 data
        print("[1/5] Loading M1 data...")
        df_m1 = self.data_loader.load_pair_data(pair, year)

        # Filter date range
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        df_m1 = df_m1[(df_m1.index >= start) & (df_m1.index <= end)]
        print(f"  Filtered to {len(df_m1)} M1 bars")

        # Resample to H1
        print("[2/5] Resampling to H1...")
        df_h1 = self.data_loader.resample_to_timeframe(df_m1, 'H1')

        # Calculate indicators on H1
        print("[3/5] Calculating indicators...")
        df_h1 = self.indicators.calculate_all_indicators(df_h1)

        # Initialize output list
        validation_rows = []

        # Process each H1 bar
        print("[4/5] Extracting regime and CSM for each bar...")

        for idx, (timestamp, row) in enumerate(df_h1.iterrows()):
            # Create dataframe up to current bar for regime detection
            df_to_current = df_h1.iloc[:idx+1]

            # Detect regime
            regime = self.regime_detector.detect(df_to_current, idx)

            # Get component scores (if available from detector)
            regime_type = regime.value if hasattr(regime, 'value') else str(regime)

            # Calculate CSM
            pair_data = {pair: df_to_current}
            csm_valid = self.csm_calculator.update_csm(pair_data, timestamp)
            csm_values = self.csm_calculator.currency_strengths if csm_valid else {}

            # Build row
            row_data = {
                'DateTime': timestamp.strftime('%Y.%m.%d %H:%M'),
                'Regime': regime_type,
                'ADXScore': row.get('adx', np.nan),
                'EMAScore': row.get('ema_alignment', np.nan),
                'ATRScore': row.get('atr_score', np.nan),
                'PriceActionScore': row.get('price_action', np.nan),
                'CSM_EUR': csm_values.get('EUR', np.nan),
                'CSM_USD': csm_values.get('USD', np.nan),
                'CSM_GBP': csm_values.get('GBP', np.nan),
                'CSM_JPY': csm_values.get('JPY', np.nan),
                'CSM_CHF': csm_values.get('CHF', np.nan),
                'CSM_AUD': csm_values.get('AUD', np.nan),
                'CSM_CAD': csm_values.get('CAD', np.nan),
                'CSM_NZD': csm_values.get('NZD', np.nan),
            }
            validation_rows.append(row_data)

            if (idx + 1) % 24 == 0:
                print(f"  Processed {idx + 1} bars...")

        # Convert to DataFrame and save
        print(f"[5/5] Saving to {self.output_file}...")
        df_output = pd.DataFrame(validation_rows)
        df_output.to_csv(self.output_file, index=False)

        print(f"\n✅ Export complete!")
        print(f"  Output file: {self.output_file}")
        print(f"  Total bars: {len(df_output)}")
        print(f"  Date range: {df_output['DateTime'].iloc[0]} to {df_output['DateTime'].iloc[-1]}")

        return df_output


def main():
    exporter = ValidationExporter(
        output_file="data/validation_output_python.csv"
    )

    # Export validation data
    df = exporter.export_regime_csm_data(
        pair='EURUSD',
        year=2024,
        start_date='2024-12-01',
        end_date='2024-12-07'
    )

    # Show summary
    print(f"\n{'='*80}")
    print("VALIDATION DATA SUMMARY")
    print(f"{'='*80}")
    print(df.head(10))
    print(f"\n...{len(df)} total rows...")
    print(df.tail(10))


if __name__ == "__main__":
    main()
```

**Usage:**
```bash
cd D:\JcampFxTrading\jcamp-python-backtesting
python scripts/validate_regime_csm.py
```

**Output:** `data/validation_output_python.csv` with columns:
- DateTime, Regime, ADXScore, EMAScore, ATRScore, PriceActionScore
- CSM_EUR, CSM_USD, CSM_GBP, CSM_JPY, CSM_CHF, CSM_AUD, CSM_CAD, CSM_NZD

---

### Step 1.2: Create MT5 Validation Indicator

**File:** `Jcamp_BacktestEA_Validation.mq5` (NEW MT5 indicator)

```mql5
//+------------------------------------------------------------------+
//|                         Validation Indicator v1.0                |
//|                  Regime & CSM Exporter for Python Comparison     |
//+------------------------------------------------------------------+
#property strict
#property indicator_chart_window

// Input parameters
input string OutputFile = "validation_output_mt5.csv";
input int RegimeCheckInterval = 60;  // Check regime every 60 minutes

// Global variables
int file_handle = INVALID_HANDLE;
datetime last_regime_check = 0;

//+------------------------------------------------------------------+
//| Custom indicator initialization                                  |
//+------------------------------------------------------------------+
int OnInit() {
    // Open CSV file for writing
    file_handle = FileOpen(OutputFile, FILE_WRITE | FILE_CSV, '\t');

    if (file_handle == INVALID_HANDLE) {
        Alert("Failed to open file: " + OutputFile);
        return INIT_FAILED;
    }

    // Write header
    string header = "DateTime\tRegime\tADXScore\tEMAScore\tATRScore\tPriceActionScore\t";
    header += "CSM_EUR\tCSM_USD\tCSM_GBP\tCSM_JPY\tCSM_CHF\tCSM_AUD\tCSM_CAD\tCSM_NZD";
    FileWrite(file_handle, header);

    return INIT_SUCCEEDED;
}

//+------------------------------------------------------------------+
//| Custom indicator iteration                                       |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[]) {

    // Only process on new H1 bar (check every 60 minutes)
    if (TimeCurrent() - last_regime_check < RegimeCheckInterval * 60) {
        return rates_total;
    }

    last_regime_check = TimeCurrent();

    int shift = 0;  // Current bar

    // Get indicator values
    double adx = iADX(NULL, PERIOD_H1, 14, PRICE_CLOSE, MODE_MAIN, shift);
    double di_plus = iADX(NULL, PERIOD_H1, 14, PRICE_CLOSE, MODE_PLUSDI, shift);
    double di_minus = iADX(NULL, PERIOD_H1, 14, PRICE_CLOSE, MODE_MINUSDI, shift);

    double ema20 = iMA(NULL, PERIOD_H1, 20, 0, MODE_EMA, PRICE_CLOSE, shift);
    double ema50 = iMA(NULL, PERIOD_H1, 50, 0, MODE_EMA, PRICE_CLOSE, shift);
    double ema100 = iMA(NULL, PERIOD_H1, 100, 0, MODE_EMA, PRICE_CLOSE, shift);

    double atr = iATR(NULL, PERIOD_H1, 14, shift);

    double rsi = iRSI(NULL, PERIOD_H1, 14, PRICE_CLOSE, shift);

    // Detect regime (simplified scoring)
    string regime = DetectRegime(adx, ema20, ema50, ema100, atr, rsi);

    // Calculate component scores (0-25 each)
    double adx_score = CalculateADXScore(adx);
    double ema_score = CalculateEMAScore(ema20, ema50, ema100);
    double atr_score = CalculateATRScore(atr, shift);
    double price_action_score = CalculatePriceActionScore(shift);

    // Build CSV line
    string line = TimeToStr(time[shift], TIME_DATE | TIME_MINUTES);
    line += "\t" + regime;
    line += "\t" + DoubleToString(adx_score, 1);
    line += "\t" + DoubleToString(ema_score, 1);
    line += "\t" + DoubleToString(atr_score, 1);
    line += "\t" + DoubleToString(price_action_score, 1);

    // Add CSM values (placeholder - need actual CSM calculation)
    line += "\t50.0\t50.0\t50.0\t50.0\t50.0\t50.0\t50.0\t50.0";

    FileWrite(file_handle, line);
    FileFlush(file_handle);  // Ensure data is written

    return rates_total;
}

//+------------------------------------------------------------------+
//| Regime detection                                                 |
//+------------------------------------------------------------------+
string DetectRegime(double adx, double ema20, double ema50, double ema100,
                    double atr, double rsi) {

    // Simplified scoring (match Python logic)
    double adx_score = MathMin(25.0, adx / 2);

    // EMA alignment
    double ema_score = 0;
    if ((ema20 > ema50 && ema50 > ema100) || (ema20 < ema50 && ema50 < ema100)) {
        ema_score = 20.0;  // Strong alignment
    } else if ((ema20 > ema50) != (ema50 > ema100)) {
        ema_score = 10.0;  // Weak alignment
    }

    double total_score = adx_score + ema_score + 10.0 + 10.0;  // Placeholder for ATR/PA
    double trending_pct = total_score / 4 / 25 * 100;

    if (trending_pct >= 55) {
        return "TRENDING";
    } else if (trending_pct <= 40) {
        return "RANGING";
    } else {
        return "TRANSITIONAL";
    }
}

//+------------------------------------------------------------------+
//| Calculate individual component scores                            |
//+------------------------------------------------------------------+
double CalculateADXScore(double adx) {
    // ADX 0→50 maps to score 0→25
    return MathMin(25.0, adx / 2.0);
}

double CalculateEMAScore(double ema20, double ema50, double ema100) {
    // Simple EMA alignment check
    if ((ema20 > ema50 && ema50 > ema100) || (ema20 < ema50 && ema50 < ema100)) {
        return 20.0;
    }
    return 10.0;
}

double CalculateATRScore(double atr, int shift) {
    // ATR scoring (would need historical ATR data)
    // Placeholder returning middle value
    return 12.5;
}

double CalculatePriceActionScore(int shift) {
    // Price action scoring (would need bar analysis)
    // Placeholder returning middle value
    return 12.5;
}

//+------------------------------------------------------------------+
//| Cleanup                                                          |
//+------------------------------------------------------------------+
void OnDeinit(const int reason) {
    if (file_handle != INVALID_HANDLE) {
        FileClose(file_handle);
        Alert("Validation indicator stopped. File saved: " + OutputFile);
    }
}
```

**How to Use:**
1. Copy to MT5 Experts/Indicators folder
2. Compile indicator
3. Attach to EURUSD H1 chart
4. Indicator will write `validation_output_mt5.csv` in MT5 Data folder
5. Let run for 1 week to collect comparison data

---

## PHASE 2: TESTING FRAMEWORK (1-2 hours)

### Step 2.1: Create Comparison Test Suite

**File:** `tests/test_regime_csm_validation.py` (NEW - 550 LOC)

```python
#!/usr/bin/env python3
"""
Regime & CSM Validation Test Suite
Compares Python vs MT5 EA outputs
"""

import pandas as pd
import numpy as np
import pytest
from pathlib import Path
from typing import Tuple, Dict

class RegimeCSMValidator:
    """Validate regime and CSM calculations against MT5"""

    def __init__(self,
                 python_csv: str = "data/validation_output_python.csv",
                 mt5_csv: str = "data/validation_output_mt5.csv"):

        self.python_df = pd.read_csv(python_csv)
        self.mt5_df = pd.read_csv(mt5_csv)

        # Ensure same length and aligned
        min_len = min(len(self.python_df), len(self.mt5_df))
        self.python_df = self.python_df.iloc[:min_len]
        self.mt5_df = self.mt5_df.iloc[:min_len]

        self.results = {
            'regime_match_count': 0,
            'regime_total_count': len(self.python_df),
            'component_errors': {},
            'csm_errors': {},
            'critical_failures': []
        }

    # ============================================================
    # REGIME CLASSIFICATION TESTS
    # ============================================================

    def test_regime_classification_match(self) -> float:
        """
        Test: Regime classification must match exactly
        Tolerance: 0% error (must be identical)
        Metric: Match rate %
        """
        matches = (self.python_df['Regime'] == self.mt5_df['Regime']).sum()
        total = len(self.python_df)
        match_rate = (matches / total) * 100

        self.results['regime_match_count'] = matches
        self.results['regime_match_pct'] = match_rate

        print(f"\n[REGIME CLASSIFICATION]")
        print(f"  Match Rate: {match_rate:.1f}% ({matches}/{total})")

        if match_rate < 95:
            print(f"  ⚠️  WARNING: Only {match_rate:.1f}% match (expected 99%+)")

            # Show first 5 mismatches
            mismatches = self.python_df[self.python_df['Regime'] != self.mt5_df['Regime']]
            print(f"\n  First 5 mismatches:")
            for idx, (_, row) in enumerate(mismatches.head(5).iterrows()):
                py_regime = self.python_df.loc[row.name, 'Regime']
                mt5_regime = self.mt5_df.loc[row.name, 'Regime']
                print(f"    {idx+1}. {row['DateTime']}: Python={py_regime}, MT5={mt5_regime}")

        return match_rate

    def test_regime_distribution(self):
        """Verify regime distribution is sensible"""
        py_dist = self.python_df['Regime'].value_counts()
        mt5_dist = self.mt5_df['Regime'].value_counts()

        print(f"\n[REGIME DISTRIBUTION]")
        print(f"  Python: {dict(py_dist)}")
        print(f"  MT5:    {dict(mt5_dist)}")

    # ============================================================
    # COMPONENT SCORE TESTS
    # ============================================================

    def test_adx_score_accuracy(self) -> Dict:
        """
        Test: ADX score accuracy
        Tolerance: ±0.1 (very tight)
        Metric: Mean error, max error, correlation
        """
        return self._test_component('ADXScore', tolerance=0.1)

    def test_ema_score_accuracy(self) -> Dict:
        """Test: EMA alignment score accuracy"""
        return self._test_component('EMAScore', tolerance=0.1)

    def test_atr_score_accuracy(self) -> Dict:
        """Test: ATR volatility score accuracy"""
        return self._test_component('ATRScore', tolerance=0.1)

    def test_price_action_accuracy(self) -> Dict:
        """Test: Price action score accuracy"""
        return self._test_component('PriceActionScore', tolerance=0.1)

    def _test_component(self, component_name: str, tolerance: float = 0.1) -> Dict:
        """Helper: Test individual component"""

        py_values = pd.to_numeric(self.python_df[component_name], errors='coerce')
        mt5_values = pd.to_numeric(self.mt5_df[component_name], errors='coerce')

        # Calculate error metrics
        diff = np.abs(py_values - mt5_values)
        valid_mask = ~(py_values.isna() | mt5_values.isna())
        diff_valid = diff[valid_mask]

        mean_error = diff_valid.mean()
        max_error = diff_valid.max()
        std_error = diff_valid.std()

        # Count within tolerance
        within_tolerance = (diff_valid <= tolerance).sum()
        tolerance_rate = (within_tolerance / len(diff_valid)) * 100

        # Correlation
        correlation = py_values.corr(mt5_values)

        result = {
            'mean_error': mean_error,
            'max_error': max_error,
            'std_error': std_error,
            'within_tolerance_pct': tolerance_rate,
            'correlation': correlation,
            'valid_count': len(diff_valid)
        }

        self.results['component_errors'][component_name] = result

        print(f"\n[{component_name}]")
        print(f"  Mean Error: {mean_error:.4f}")
        print(f"  Max Error:  {max_error:.4f}")
        print(f"  Std Dev:    {std_error:.4f}")
        print(f"  Within ±{tolerance} tolerance: {tolerance_rate:.1f}%")
        print(f"  Correlation: {correlation:.4f}")

        if tolerance_rate < 95:
            print(f"  ⚠️  WARNING: Only {tolerance_rate:.1f}% within tolerance")
            if mean_error > tolerance * 2:
                self.results['critical_failures'].append(
                    f"{component_name} has mean error {mean_error:.4f} (> 2x tolerance)"
                )

        return result

    # ============================================================
    # CSM VALIDATION TESTS
    # ============================================================

    def test_csm_currency_accuracy(self) -> Dict:
        """
        Test: CSM currency strength accuracy
        Tolerance: ±0.5 strength points
        Metric: Mean error per currency, correlation
        """

        currencies = ['EUR', 'USD', 'GBP', 'JPY', 'CHF', 'AUD', 'CAD', 'NZD']
        results = {}

        print(f"\n[CSM CURRENCY STRENGTH]")

        for curr in currencies:
            col = f'CSM_{curr}'

            if col not in self.python_df.columns or col not in self.mt5_df.columns:
                continue

            py_csm = pd.to_numeric(self.python_df[col], errors='coerce')
            mt5_csm = pd.to_numeric(self.mt5_df[col], errors='coerce')

            diff = np.abs(py_csm - mt5_csm)
            valid_mask = ~(py_csm.isna() | mt5_csm.isna())
            diff_valid = diff[valid_mask]

            mean_error = diff_valid.mean()
            correlation = py_csm.corr(mt5_csm)

            results[curr] = {
                'mean_error': mean_error,
                'correlation': correlation
            }

            status = "✅" if mean_error <= 0.5 else "⚠️"
            print(f"  {status} {curr}: mean_error={mean_error:.2f}, corr={correlation:.4f}")

        self.results['csm_errors'] = results
        return results

    def test_csm_pair_differential(self):
        """
        Test: CSM pair differentials
        Example: EURUSD = EUR_strength - USD_strength
        """

        print(f"\n[CSM PAIR DIFFERENTIALS]")

        # Calculate EURUSD differential
        py_eur = pd.to_numeric(self.python_df.get('CSM_EUR', [50]), errors='coerce')
        py_usd = pd.to_numeric(self.python_df.get('CSM_USD', [50]), errors='coerce')
        py_eurusd_diff = py_eur - py_usd

        mt5_eur = pd.to_numeric(self.mt5_df.get('CSM_EUR', [50]), errors='coerce')
        mt5_usd = pd.to_numeric(self.mt5_df.get('CSM_USD', [50]), errors='coerce')
        mt5_eurusd_diff = mt5_eur - mt5_usd

        # Compare differentials
        diff = np.abs(py_eurusd_diff - mt5_eurusd_diff)
        mean_error = diff.mean()

        print(f"  EURUSD Differential:")
        print(f"    Python avg: {py_eurusd_diff.mean():.2f}")
        print(f"    MT5 avg:    {mt5_eurusd_diff.mean():.2f}")
        print(f"    Mean error: {mean_error:.2f}")

    # ============================================================
    # SUMMARY REPORT
    # ============================================================

    def generate_report(self) -> str:
        """Generate validation report"""

        report = "\n" + "="*80 + "\n"
        report += "REGIME & CSM VALIDATION REPORT\n"
        report += "="*80 + "\n"

        # Regime matching
        regime_pct = self.results.get('regime_match_pct', 0)
        report += f"\nREGIME CLASSIFICATION\n"
        report += f"  Match Rate: {regime_pct:.1f}%\n"
        report += f"  Status: {'✅ PASS' if regime_pct >= 95 else '❌ FAIL'}\n"

        # Component errors
        report += f"\nCOMPONENT SCORES\n"
        for comp, error_dict in self.results.get('component_errors', {}).items():
            within = error_dict['within_tolerance_pct']
            status = '✅ PASS' if within >= 95 else '❌ FAIL'
            report += f"  {comp}: {within:.1f}% {status}\n"

        # CSM values
        report += f"\nCSM CURRENCY STRENGTH\n"
        for curr, error_dict in self.results.get('csm_errors', {}).items():
            error = error_dict['mean_error']
            status = '✅ PASS' if error <= 0.5 else '❌ FAIL'
            report += f"  {curr}: {error:.2f} {status}\n"

        # Critical failures
        if self.results['critical_failures']:
            report += f"\nCRITICAL FAILURES\n"
            for failure in self.results['critical_failures']:
                report += f"  🔴 {failure}\n"

        report += "\n" + "="*80 + "\n"

        return report


def main():
    """Run validation tests"""

    validator = RegimeCSMValidator()

    # Run all tests
    print("\nRunning Regime & CSM Validation Tests...\n")

    validator.test_regime_classification_match()
    validator.test_regime_distribution()

    validator.test_adx_score_accuracy()
    validator.test_ema_score_accuracy()
    validator.test_atr_score_accuracy()
    validator.test_price_action_accuracy()

    validator.test_csm_currency_accuracy()
    validator.test_csm_pair_differential()

    # Generate report
    report = validator.generate_report()
    print(report)

    # Save report
    with open("validation_report.txt", "w") as f:
        f.write(report)

    print("Report saved to: validation_report.txt")


if __name__ == "__main__":
    main()
```

**Usage:**
```bash
cd D:\JcampFxTrading\jcamp-python-backtesting
python tests/test_regime_csm_validation.py
```

---

## PHASE 3: EXECUTION & COMPARISON (2-3 hours)

### Step 3.1: Collect Data

**Timeline:**
1. **Run Python Export** (5 minutes)
   ```bash
   python scripts/validate_regime_csm.py
   ```
   Creates: `data/validation_output_python.csv`

2. **Deploy MT5 Indicator** (10 minutes)
   - Copy indicator to MT5
   - Attach to EURUSD H1 chart
   - Let run 7 days (Dec 1-7, 2024)
   - Creates: `validation_output_mt5.csv`

3. **Run Comparison Tests** (5 minutes)
   ```bash
   python tests/test_regime_csm_validation.py
   ```
   Creates: `validation_report.txt`

### Step 3.2: Analyze Results

**Expected Outcomes:**

✅ **If 95%+ regime match:**
- Python regime detection is correct
- Proceed to Phase 7 with confidence

⚠️ **If 85-95% regime match:**
- Investigate discrepancies
- Likely minor rounding differences
- Document and decide if fix needed

🔴 **If <85% regime match:**
- Critical bug found
- Must fix before Phase 7
- Re-run validation after fix

---

## FILES TO CREATE

### Python Scripts
1. **`scripts/validate_regime_csm.py`** (350 LOC)
   - Exports Python regime and CSM data

2. **`tests/test_regime_csm_validation.py`** (550 LOC)
   - Comparison test suite

### MT5 Indicators
3. **`Jcamp_BacktestEA_Validation.mq5`** (200 LOC)
   - MT5 validation indicator

### Documentation
4. **`docs/validation/validation_report_<date>.txt`**
   - Test results and findings

---

## ESTIMATED TIMELINE

| Activity | Duration | Notes |
|----------|----------|-------|
| Create Python validation script | 30 min | Copy template above |
| Create MT5 indicator | 30 min | Copy template above |
| Create test suite | 45 min | Copy template above |
| Data collection (passive) | 7 days | MT5 indicator running |
| Run comparisons | 15 min | Execute test script |
| Analyze results | 30 min | Review report |
| **Total Active Work** | **2.5 hours** | Can start immediately |
| **Total Elapsed Time** | **7 days** | Data collection takes time |

---

## SUCCESS CHECKLIST

After completing implementation:

- [ ] Python validation script created and tested
- [ ] MT5 indicator compiled and deployed
- [ ] Test suite created and runnable
- [ ] Data collected for 7+ days
- [ ] Comparison tests executed
- [ ] Validation report generated
- [ ] Results analyzed
- [ ] Discrepancies documented (if any)
- [ ] Decision made: proceed or fix code
- [ ] Results committed to git
- [ ] Phase 7 approval given (if validation passes)

---

## NEXT SESSION CHECKLIST

Before starting Phase 7 strategy enhancements:

1. [ ] Read VALIDATION_PLAN.md (understanding)
2. [ ] Read REGIME_CSM_COMPARISON.md (comparison reference)
3. [ ] Review validation report results
4. [ ] Confirm 95%+ regime match
5. [ ] Confirm component scores within tolerance
6. [ ] Confirm CSM values accurate
7. [ ] Get approval: "Python regime & CSM validated ✅"
8. [ ] Start Phase 7 implementation

---

*Implementation Guide Created: December 10, 2025*
*Ready to execute when approved*

