"""
Test multi-year data loading for warmup
"""
import sys
import os
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'config'))

from src.data_loader import DataLoader
from src.indicators import TechnicalIndicators

print("="*70)
print("TESTING MULTI-YEAR DATA LOADING FOR WARMUP")
print("="*70)

# Test 1: Load 2023 + 2024
print("\n[TEST 1] Loading 2023 + 2024 data...")
loader = DataLoader()
df_m1 = loader.load_pair_data_multi_year('EURUSD', [2023, 2024])

print(f"\nResult:")
print(f"  Total M1 bars: {len(df_m1):,}")
print(f"  Date range: {df_m1.index[0]} to {df_m1.index[-1]}")
print(f"  Covers 2023: {df_m1.index[0].year == 2023}")
print(f"  Covers 2024: {df_m1.index[-1].year == 2024}")

# Test 2: Resample and calculate EMAs
print("\n[TEST 2] Resampling to M15 and calculating EMAs...")
df_m15 = loader.resample_to_timeframe(df_m1, 'M15')

indicators_calc = TechnicalIndicators()
df_m15['ema_fast'] = indicators_calc.calculate_ema(df_m15, 20)
df_m15['ema_mid'] = indicators_calc.calculate_ema(df_m15, 50)
df_m15['ema_slow'] = indicators_calc.calculate_ema(df_m15, 100)

print(f"\nResult:")
print(f"  Total M15 bars: {len(df_m15):,}")
print(f"  Date range: {df_m15.index[0]} to {df_m15.index[-1]}")

# Test 3: Check EMAs at Jan 1, 2024 (should be accurate due to 2023 data)
print("\n[TEST 3] Checking EMAs at Jan 1-2, 2024...")

import pandas as pd
jan1_idx = df_m15.index.get_indexer([pd.Timestamp('2024-01-01')], method='bfill')[0]

for i in range(jan1_idx, min(jan1_idx + 10, len(df_m15))):
    row = df_m15.iloc[i]
    timestamp = df_m15.index[i]
    print(f"  {timestamp}: EMA20={row['ema_fast']:.5f} | EMA50={row['ema_mid']:.5f} | EMA100={row['ema_slow']:.5f}")

# Check if EMAs are different (not all the same)
first_bar = df_m15.iloc[jan1_idx]
if abs(first_bar['ema_fast'] - first_bar['ema_mid']) > 0.0001:
    print("\n[OK] EMAs are DIFFERENT (calculated with history) - CORRECT!")
else:
    print("\n[ERROR] EMAs are IDENTICAL (calculated from first bar) - WRONG!")

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70)
