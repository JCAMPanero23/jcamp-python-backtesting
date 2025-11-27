"""
Test what happens when start_date is 2024-01-01 (before data exists)
"""
import sys
import os
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'config'))

import pandas as pd
from src.data_loader import DataLoader
from src.indicators import TechnicalIndicators

loader = DataLoader()
indicators_calc = TechnicalIndicators()

df_m1 = loader.load_pair_data('EURUSD', '2024')
df_full = loader.resample_to_timeframe(df_m1, 'M15')

print(f"\nFull dataset range: {df_full.index[0]} to {df_full.index[-1]}")
print(f"Total M15 bars: {len(df_full)}")

# Calculate EMAs
df_full['ema_fast'] = indicators_calc.calculate_ema(df_full, 20)
df_full['ema_mid'] = indicators_calc.calculate_ema(df_full, 50)
df_full['ema_slow'] = indicators_calc.calculate_ema(df_full, 100)

# Try to use Jan 1 as start_date (data doesn't exist!)
start_date = '2024-01-01'
WARMUP_BARS = 500

print(f"\n{'='*70}")
print(f"Testing with start_date={start_date} (DATA DOESN'T EXIST FOR THIS DATE)")
print(f"{'='*70}")

start_timestamp = pd.Timestamp(start_date)
print(f"Requested start_timestamp: {start_timestamp}")

# This will use 'bfill' (backfill) - finds NEXT available date
start_idx = df_full.index.get_indexer([start_timestamp], method='bfill')[0]
print(f"start_idx after bfill: {start_idx} (bar at {df_full.index[start_idx]})")

warmup_start_idx = max(0, start_idx - WARMUP_BARS)
print(f"warmup_start_idx: {warmup_start_idx} (bar at {df_full.index[warmup_start_idx]})")
print(f"Actual warmup bars: {start_idx - warmup_start_idx}")

print(f"\n[PROBLEM] Not enough warmup!")
print(f"  Requested: 500 bars")
print(f"  Actual: {start_idx - warmup_start_idx} bars")
print(f"  Missing: {500 - (start_idx - warmup_start_idx)} bars")

# Slice dataframe
df = df_full.iloc[warmup_start_idx:]

end_date = '2024-01-31'
end_timestamp = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
df = df[df.index <= end_timestamp]

print(f"\nDataframe after slicing:")
print(f"  Date range: {df.index[0]} to {df.index[-1]}")
print(f"  Total bars: {len(df)}")

# Check first few EMAs
print(f"\nFirst 10 EMAs (should have values even at start):")
for i in range(min(10, len(df))):
    row = df.iloc[i]
    print(f"  {i}: {df.index[i]} | EMA20={row['ema_fast']:.5f} | EMA50={row['ema_mid']:.5f} | EMA100={row['ema_slow']:.5f}")

print(f"\n{'='*70}")
print(f"CONCLUSION:")
print(f"{'='*70}")
print(f"The CSV data starts from 2024-01-02, NOT 2024-01-01")
print(f"When start_date=2024-01-01, warmup can only go back {start_idx - warmup_start_idx} bars")
print(f"This is NOT enough for proper EMA calculation!")
print(f"\nRECOMMENDATION: Start backtests from 2024-01-15 or later to allow full 500-bar warmup")
