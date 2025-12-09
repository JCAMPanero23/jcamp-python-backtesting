#!/usr/bin/env python
"""
Quick script to run MT5 indicator validation tests
Tests Python indicator calculations against MT5 EA reference values
"""

import sys
import os

# Add src to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

from indicators import TechnicalIndicators
from data_loader import DataLoader

print("\n" + "="*80)
print("MT5 INDICATOR VALIDATION TEST")
print("="*80)

# Load data
print("\nLoading EURUSD H1 data (2024)...")
loader = DataLoader(data_dir="data")
df_h1 = loader.load_pair_data('EURUSD', 2024)
df_h1 = loader.resample_to_timeframe(df_h1, 'H1')

# Calculate indicators
print("Calculating indicators...")
indicators = TechnicalIndicators()
df_h1['atr'] = indicators.calculate_atr(df_h1, period=14)
df_h1['ema_20'] = indicators.calculate_ema(df_h1, period=20)
df_h1['ema_50'] = indicators.calculate_ema(df_h1, period=50)
df_h1['ema_100'] = indicators.calculate_ema(df_h1, period=100)

adx, plus_di, minus_di = indicators.calculate_adx(df_h1, period=14)
df_h1['adx'] = adx
df_h1['plus_di'] = plus_di
df_h1['minus_di'] = minus_di

df_h1['rsi'] = indicators.calculate_rsi(df_h1, period=14)

# Filter to test date range
df_h1 = df_h1.loc['2024-12-01':'2024-12-07']
print(f"Loaded {len(df_h1)} H1 bars for 2024-12-01 to 2024-12-07")

# MT5 Reference values (from EURUSD 2025-12-09 export, dates converted to 2024-12 with times adjusted to match available data)
# Available data range: 2024-12-02 to 2024-12-06
test_cases = {
    'atr': {
        '2024-12-06 20:00:00': 0.00120,  # Converted from 2025-12-09 20:00
        '2024-12-06 10:00:00': 0.00082,  # Converted from 2025-12-08 10:00
        '2024-12-05 09:00:00': 0.00060,  # 2025-12-05 09:00 -> 2024-12-05 09:00 (available)
        '2024-12-04 04:00:00': 0.00086,  # 2025-12-04 04:00 -> 2024-12-04 04:00 (available)
        '2024-12-03 15:00:00': 0.00082,  # 2025-12-03 15:00 -> 2024-12-03 15:00 (available)
        '2024-12-02 20:00:00': 0.00112,  # 2025-12-02 20:00 -> 2024-12-02 20:00 (available)
    },
    'ema_20': {
        '2024-12-06 20:00:00': 1.16375,  # Converted from 2025-12-09 20:00
        '2024-12-06 10:00:00': 1.16522,  # Converted from 2025-12-08 10:00
        '2024-12-05 09:00:00': 1.16563,
        '2024-12-04 04:00:00': 1.16595,
        '2024-12-03 15:00:00': 1.16426,
    },
    'ema_50': {
        '2024-12-06 20:00:00': 1.16423,  # Converted from 2025-12-09 20:00
        '2024-12-06 10:00:00': 1.16513,  # Converted from 2025-12-08 10:00
        '2024-12-05 09:00:00': 1.16530,
        '2024-12-04 04:00:00': 1.16428,
        '2024-12-03 15:00:00': 1.16270,
    },
    'ema_100': {
        '2024-12-06 20:00:00': 1.16417,  # Converted from 2025-12-09 20:00
        '2024-12-06 10:00:00': 1.16435,  # Converted from 2025-12-08 10:00
        '2024-12-05 09:00:00': 1.16394,
        '2024-12-04 04:00:00': 1.16244,
        '2024-12-03 15:00:00': 1.16120,
    },
    'adx': {
        '2024-12-06 20:00:00': 34.47,  # Converted from 2025-12-09 20:00
        '2024-12-06 19:00:00': 30.94,  # Converted from 2025-12-09 19:00
        '2024-12-06 18:00:00': 28.75,  # Converted from 2025-12-09 18:00
        '2024-12-06 17:00:00': 27.71,  # Converted from 2025-12-09 17:00
        '2024-12-06 16:00:00': 24.04,  # Converted from 2025-12-09 16:00
    },
    'plus_di': {
        '2024-12-06 20:00:00': 8.05,
        '2024-12-06 19:00:00': 9.29,
        '2024-12-06 18:00:00': 10.72,
        '2024-12-06 17:00:00': 8.31,
        '2024-12-06 16:00:00': 9.58,
    },
    'minus_di': {
        '2024-12-06 20:00:00': 29.80,
        '2024-12-06 19:00:00': 24.58,
        '2024-12-06 18:00:00': 22.54,
        '2024-12-06 17:00:00': 26.00,
        '2024-12-06 16:00:00': 21.23,
    },
    'rsi': {
        '2024-12-06 20:00:00': 36.31,  # Converted from 2025-12-09 20:00
        '2024-12-06 19:00:00': 38.29,  # Converted from 2025-12-09 19:00
        '2024-12-06 18:00:00': 47.15,  # Converted from 2025-12-09 18:00
        '2024-12-06 17:00:00': 38.31,  # Converted from 2025-12-09 17:00
        '2024-12-06 16:00:00': 44.74,  # Converted from 2025-12-09 16:00
    },
}

# Run validation tests
print("\n" + "="*80)
print("VALIDATION RESULTS")
print("="*80)

total_tests = 0
passed_tests = 0
failed_tests = []

for indicator_name, test_values in test_cases.items():
    print(f"\n{indicator_name.upper()}:")
    print("-" * 40)

    if indicator_name == 'atr':
        tolerance = 0.00001
        fmt = ".5f"
    elif indicator_name.startswith('ema'):
        tolerance = 0.00001
        fmt = ".5f"
    else:  # ADX, DI, RSI
        tolerance = 0.1
        fmt = ".2f"

    for timestamp, expected_value in test_values.items():
        total_tests += 1

        try:
            actual_value = df_h1.loc[timestamp, indicator_name]
            difference = abs(actual_value - expected_value)

            if difference <= tolerance:
                status = "[PASS]"
                passed_tests += 1
            else:
                status = "[FAIL]"
                failed_tests.append({
                    'indicator': indicator_name,
                    'timestamp': timestamp,
                    'actual': actual_value,
                    'expected': expected_value,
                    'diff': difference,
                    'tolerance': tolerance
                })

            print(f"  {timestamp}: Python={actual_value:{fmt}} MT5={expected_value:{fmt}} Diff={difference:.6f} {status}")
        except KeyError:
            print(f"  {timestamp}: MISSING (not in test data)")
            failed_tests.append({
                'indicator': indicator_name,
                'timestamp': timestamp,
                'error': 'Timestamp not found in data'
            })

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Total Tests: {total_tests}")
print(f"Passed: {passed_tests}")
print(f"Failed: {len(failed_tests)}")

if failed_tests:
    print("\n" + "-"*80)
    print("FAILED TESTS:")
    print("-"*80)
    for failure in failed_tests:
        if 'error' in failure:
            print(f"{failure['indicator']} @ {failure['timestamp']}: {failure['error']}")
        else:
            print(f"{failure['indicator']} @ {failure['timestamp']}")
            print(f"  Python: {failure['actual']:.6f}")
            print(f"  MT5:    {failure['expected']:.6f}")
            print(f"  Diff:   {failure['diff']:.6f} (tolerance: {failure['tolerance']:.6f})")

print("\n" + "="*80)
if len(failed_tests) == 0:
    print("[PASS] ALL TESTS PASSED - Python indicators match MT5 EA!")
else:
    print("[FAIL] Some tests failed - Review differences above")
print("="*80 + "\n")

sys.exit(0 if len(failed_tests) == 0 else 1)
