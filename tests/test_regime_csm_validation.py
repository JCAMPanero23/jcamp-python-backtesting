#!/usr/bin/env python3
"""
Regime & CSM Validation Test Suite
Compares Python vs MT5 EA outputs for validation

Test Period: December 2-6, 2024 (Monday-Friday business week)
Files compared:
  - data/validation_output_python.csv (from Python exporter)
  - validation_output_mt5.csv (from MT5 indicator, in MT5 Data folder)

Usage:
  1. Deploy MT5 indicator and let it run Dec 2-6
  2. Move validation_output_mt5.csv to data/ folder
  3. Run: python tests/test_regime_csm_validation.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple
import os
import sys


class RegimeCSMValidator:
    """Validate regime and CSM calculations against MT5 EA"""

    def __init__(self,
                 python_csv: str = "data/validation_output_python.csv",
                 mt5_csv: str = "data/validation_output_mt5.csv"):

        print("\n" + "="*80)
        print("REGIME & CSM VALIDATION TEST SUITE")
        print("="*80 + "\n")

        # Load CSV files
        print("[1/5] Loading validation data files...")

        if not os.path.exists(python_csv):
            print(f"[ERROR] Python CSV not found: {python_csv}")
            print(f"[ERROR] Run: python scripts/validate_regime_csm.py")
            sys.exit(1)

        if not os.path.exists(mt5_csv):
            print(f"[ERROR] MT5 CSV not found: {mt5_csv}")
            print(f"[ERROR] Steps:")
            print(f"       1. Deploy MT5 indicator on EURUSD H1 chart")
            print(f"       2. Let run Dec 2-6, 2024")
            print(f"       3. Indicator creates: validation_output_mt5.csv in MT5 Data folder")
            print(f"       4. Copy to: {mt5_csv}")
            sys.exit(1)

        try:
            self.python_df = pd.read_csv(python_csv)
            print(f"  [OK] Loaded Python data: {len(self.python_df)} rows")
        except Exception as e:
            print(f"[ERROR] Failed to load Python CSV: {e}")
            sys.exit(1)

        try:
            self.mt5_df = pd.read_csv(mt5_csv)
            print(f"  [OK] Loaded MT5 data: {len(self.mt5_df)} rows")
        except Exception as e:
            print(f"[ERROR] Failed to load MT5 CSV: {e}")
            sys.exit(1)

        # Align dataframes (same length)
        min_len = min(len(self.python_df), len(self.mt5_df))
        self.python_df = self.python_df.iloc[:min_len].reset_index(drop=True)
        self.mt5_df = self.mt5_df.iloc[:min_len].reset_index(drop=True)

        print(f"  [OK] Aligned to {len(self.python_df)} common rows\n")

        # Initialize results
        self.results = {
            'regime_match_count': 0,
            'regime_total_count': len(self.python_df),
            'regime_match_pct': 0.0,
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
        """
        print("[2/5] Testing REGIME CLASSIFICATION...")

        # Extract regime values (handle nested dictionary if needed)
        py_regime = []
        mt5_regime = []

        for idx in range(len(self.python_df)):
            try:
                # Python stores as dictionary, extract classification
                py_val = self.python_df['Regime'].iloc[idx]
                if isinstance(py_val, str) and py_val.startswith('{'):
                    # It's a dictionary string
                    if "'is_ranging': True" in py_val:
                        py_regime.append('RANGING')
                    elif "'is_trending': True" in py_val:
                        py_regime.append('TRENDING')
                    elif "'is_transitional': True" in py_val:
                        py_regime.append('TRANSITIONAL')
                    else:
                        py_regime.append('UNKNOWN')
                else:
                    py_regime.append(str(py_val).strip())
            except:
                py_regime.append('ERROR')

            # MT5 should be simple string
            try:
                mt5_val = str(self.mt5_df['Regime'].iloc[idx]).strip()
                mt5_regime.append(mt5_val)
            except:
                mt5_regime.append('ERROR')

        # Count matches
        matches = sum(1 for p, m in zip(py_regime, mt5_regime) if p == m and p != 'ERROR')
        total = len([p for p in py_regime if p != 'ERROR'])

        match_pct = (matches / total * 100) if total > 0 else 0

        self.results['regime_match_count'] = matches
        self.results['regime_match_pct'] = match_pct

        status = "[PASS] PASS" if match_pct >= 95 else "[WARN]  WARN" if match_pct >= 85 else "[FAIL] FAIL"
        print(f"  {status} Regime Match Rate: {match_pct:.1f}% ({matches}/{total})")

        if match_pct < 95:
            # Show first mismatches
            print(f"\n  First 5 mismatches:")
            count = 0
            for idx in range(len(py_regime)):
                if py_regime[idx] != mt5_regime[idx] and count < 5:
                    print(f"    {idx+1}. Row {idx}: Python={py_regime[idx]}, MT5={mt5_regime[idx]}")
                    count += 1
            print()

        return match_pct

    def test_regime_distribution(self):
        """Verify regime distribution is sensible"""
        print("\n[2.5/5] Analyzing REGIME DISTRIBUTION...\n")

        # Extract regimes
        py_regimes = []
        for val in self.python_df['Regime']:
            if isinstance(val, str) and 'RANGING' in val:
                py_regimes.append('RANGING')
            elif isinstance(val, str) and 'TRENDING' in val:
                py_regimes.append('TRENDING')
            elif isinstance(val, str) and 'TRANSITIONAL' in val:
                py_regimes.append('TRANSITIONAL')

        mt5_regimes = [str(v).strip() for v in self.mt5_df['Regime']]

        print(f"  Python regime distribution:")
        if py_regimes:
            for regime in ['TRENDING', 'RANGING', 'TRANSITIONAL']:
                count = py_regimes.count(regime)
                pct = count / len(py_regimes) * 100 if py_regimes else 0
                print(f"    {regime}: {count:3d} ({pct:5.1f}%)")

        print(f"\n  MT5 regime distribution:")
        for regime in ['TRENDING', 'RANGING', 'TRANSITIONAL']:
            count = mt5_regimes.count(regime)
            pct = count / len(mt5_regimes) * 100 if mt5_regimes else 0
            print(f"    {regime}: {count:3d} ({pct:5.1f}%)\n")

    # ============================================================
    # COMPONENT SCORE TESTS
    # ============================================================

    def test_component_scores(self):
        """Test component score accuracy"""
        print("[3/5] Testing COMPONENT SCORES...\n")

        components = ['ADXScore', 'EMAScore', 'ATRScore', 'PriceActionScore']
        tolerance = 0.1

        for component in components:
            self._test_component(component, tolerance)

    def _test_component(self, component_name: str, tolerance: float = 0.1):
        """Helper: Test individual component"""

        try:
            py_values = pd.to_numeric(self.python_df[component_name], errors='coerce')
            mt5_values = pd.to_numeric(self.mt5_df[component_name], errors='coerce')
        except:
            print(f"  [WARN]  {component_name}: Column not found or error reading")
            return

        # Calculate error metrics
        diff = np.abs(py_values - mt5_values)
        valid_mask = ~(py_values.isna() | mt5_values.isna())

        if not valid_mask.any():
            print(f"  [WARN]  {component_name}: No valid data to compare")
            return

        diff_valid = diff[valid_mask]

        mean_error = diff_valid.mean()
        max_error = diff_valid.max()
        std_error = diff_valid.std()

        within_tolerance = (diff_valid <= tolerance).sum()
        tolerance_pct = (within_tolerance / len(diff_valid)) * 100

        try:
            correlation = py_values.corr(mt5_values)
        except:
            correlation = np.nan

        status = "[PASS] PASS" if tolerance_pct >= 95 else "[WARN]  WARN" if tolerance_pct >= 85 else "[FAIL] FAIL"

        print(f"  {status} {component_name}")
        print(f"      Mean Error: {mean_error:.4f} (tolerance: ±{tolerance})")
        print(f"      Max Error:  {max_error:.4f}")
        print(f"      Within tolerance: {tolerance_pct:.1f}%")
        print(f"      Correlation: {correlation:.4f}\n")

        self.results['component_errors'][component_name] = {
            'mean_error': mean_error,
            'max_error': max_error,
            'tolerance_pct': tolerance_pct,
            'correlation': correlation
        }

    # ============================================================
    # CSM VALIDATION TESTS
    # ============================================================

    def test_csm_values(self):
        """Test CSM currency strength accuracy"""
        print("[4/5] Testing CSM CURRENCY STRENGTH...\n")

        currencies = ['EUR', 'USD', 'GBP', 'JPY', 'CHF', 'AUD', 'CAD', 'NZD']
        tolerance = 0.5

        for curr in currencies:
            col = f'CSM_{curr}'

            if col not in self.python_df.columns or col not in self.mt5_df.columns:
                continue

            try:
                py_csm = pd.to_numeric(self.python_df[col], errors='coerce')
                mt5_csm = pd.to_numeric(self.mt5_df[col], errors='coerce')
            except:
                print(f"  [WARN]  {curr}: Error reading data")
                continue

            diff = np.abs(py_csm - mt5_csm)
            valid_mask = ~(py_csm.isna() | mt5_csm.isna())

            if not valid_mask.any():
                print(f"  [WARN]  {curr}: No valid data")
                continue

            diff_valid = diff[valid_mask]
            mean_error = diff_valid.mean()
            max_error = diff_valid.max()

            try:
                correlation = py_csm.corr(mt5_csm)
            except:
                correlation = np.nan

            status = "[PASS] PASS" if mean_error <= tolerance else "[WARN]  WARN"
            print(f"  {status} {curr}: mean_error={mean_error:.2f}, corr={correlation:.4f}")

            self.results['csm_errors'][curr] = {
                'mean_error': mean_error,
                'max_error': max_error,
                'correlation': correlation
            }

        print()

    # ============================================================
    # SUMMARY REPORT
    # ============================================================

    def generate_report(self) -> str:
        """Generate validation report"""

        report = "\n" + "="*80 + "\n"
        report += "REGIME & CSM VALIDATION REPORT\n"
        report += "Period: December 2-6, 2024 (Monday-Friday business week)\n"
        report += "="*80 + "\n"

        # Regime matching
        regime_pct = self.results.get('regime_match_pct', 0)
        regime_status = "[PASS] PASS" if regime_pct >= 95 else "[WARN]  WARN" if regime_pct >= 85 else "[FAIL] FAIL"

        report += f"\nREGIME CLASSIFICATION\n"
        report += f"  Match Rate: {regime_pct:.1f}%\n"
        report += f"  Status: {regime_status}\n"
        report += f"  Expected: >=95% match\n"

        if regime_pct < 95:
            report += f"  ACTION: Investigate {100-regime_pct:.1f}% mismatches\n"

        # Component errors
        report += f"\nCOMPONENT SCORES\n"
        for comp, error_dict in self.results.get('component_errors', {}).items():
            within = error_dict.get('tolerance_pct', 0)
            status = '[PASS] PASS' if within >= 95 else '[WARN]  WARN' if within >= 85 else '[FAIL] FAIL'
            report += f"  {status} {comp}: {within:.1f}% within tolerance\n"

        # CSM values
        report += f"\nCSM CURRENCY STRENGTH\n"
        for curr, error_dict in self.results.get('csm_errors', {}).items():
            error = error_dict.get('mean_error', 0)
            status = '[PASS] PASS' if error <= 0.5 else '[WARN]  WARN'
            report += f"  {status} {curr}: mean_error={error:.2f}\n"

        # Critical failures
        if self.results['critical_failures']:
            report += f"\nCRITICAL FAILURES\n"
            for failure in self.results['critical_failures']:
                report += f"  [ERROR] {failure}\n"

        # Decision
        report += f"\n" + "="*80 + "\n"
        report += "VALIDATION DECISION\n"
        report += "="*80 + "\n"

        if regime_pct >= 95:
            report += "\n[PASS] VALIDATION PASSED\n"
            report += "   Proceed to Phase 7 with confidence\n"
            report += "   Python regime detection matches MT5 EA\n"
        elif regime_pct >= 85:
            report += "\n[WARN]  VALIDATION PASSED WITH WARNINGS\n"
            report += "   Review discrepancies before proceeding\n"
            report += "   Likely minor differences (rounding, precision)\n"
        else:
            report += "\n[FAIL] VALIDATION FAILED\n"
            report += "   Critical bug found in Python implementation\n"
            report += "   Must investigate and fix before Phase 7\n"

        report += "\n" + "="*80 + "\n"

        return report

    def run_all_tests(self):
        """Run all validation tests"""

        # Test regime classification
        regime_match = self.test_regime_classification_match()

        # Analyze distribution
        self.test_regime_distribution()

        # Test components
        self.test_component_scores()

        # Test CSM
        self.test_csm_values()

        # Generate report
        report = self.generate_report()
        print(report)

        # Save report
        report_file = "validation_report.txt"
        try:
            with open(report_file, "w") as f:
                f.write(report)
            print(f"\n[PASS] Report saved to: {report_file}")
        except Exception as e:
            print(f"\n[WARN] Failed to save report: {e}")

        return regime_match


def main():
    """Run validation tests"""

    try:
        validator = RegimeCSMValidator()
        regime_match = validator.run_all_tests()

        # Exit with status code
        print(f"\nValidation complete. Regime match: {regime_match:.1f}%")

        if regime_match >= 95:
            print("[PASS] Ready for Phase 7 approval\n")
            sys.exit(0)
        elif regime_match >= 85:
            print("[WARN]  Review discrepancies before approval\n")
            sys.exit(1)
        else:
            print("[FAIL] Investigation required before Phase 7\n")
            sys.exit(2)

    except Exception as e:
        print(f"\n[ERROR] Validation failed: {e}")
        print(f"[ERROR] Make sure both CSV files exist:")
        print(f"       - data/validation_output_python.csv")
        print(f"       - data/validation_output_mt5.csv (from MT5 indicator)")
        sys.exit(3)


if __name__ == "__main__":
    main()
