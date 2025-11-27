"""
Test with proper warmup period (data exists before start_date)
"""
import sys
import os
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'config'))

import pandas as pd
from src.data_loader import DataLoader
from src.indicators import TechnicalIndicators

# Test with date where warmup is actually applied
loader = DataLoader()
indicators_calc = TechnicalIndicators()

df_m1 = loader.load_pair_data('EURUSD', '2024')
df_full = loader.resample_to_timeframe(df_m1, 'M15')

# Calculate EMAs
df_full['ema_fast'] = indicators_calc.calculate_ema(df_full, 20)
df_full['ema_mid'] = indicators_calc.calculate_ema(df_full, 50)
df_full['ema_slow'] = indicators_calc.calculate_ema(df_full, 100)

# Use a start_date well into the dataset (January 15)
start_date = '2024-01-15'
end_date = '2024-01-31'
WARMUP_BARS = 500

print(f"\nTesting with start_date={start_date}, WARMUP_BARS={WARMUP_BARS}")
print(f"Full dataset has {len(df_full)} bars from {df_full.index[0]} to {df_full.index[-1]}")

start_timestamp = pd.Timestamp(start_date)
start_idx = df_full.index.get_indexer([start_timestamp], method='bfill')[0]
warmup_start_idx = max(0, start_idx - WARMUP_BARS)

print(f"\nWarmup logic:")
print(f"  start_idx: {start_idx} (bar at {df_full.index[start_idx]})")
print(f"  warmup_start_idx: {warmup_start_idx} (bar at {df_full.index[warmup_start_idx]})")
print(f"  Actual warmup bars: {start_idx - warmup_start_idx}")

# Slice dataframe
df = df_full.iloc[warmup_start_idx:]

# Filter end date
end_timestamp = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
df = df[df.index <= end_timestamp]

print(f"\nDataframe after slicing:")
print(f"  Total bars in df: {len(df)}")
print(f"  Date range: {df.index[0]} to {df.index[-1]}")
print(f"  EMAs present: ema_fast={('ema_fast' in df.columns)}, ema_mid={('ema_mid' in df.columns)}, ema_slow={('ema_slow' in df.columns)}")

# Check first 5 bars (warmup period)
print(f"\nFirst 5 bars (warmup period):")
for i in range(min(5, len(df))):
    row = df.iloc[i]
    print(f"  {i}: {df.index[i]} | EMA20={row['ema_fast']:.5f} | EMA50={row['ema_mid']:.5f} | EMA100={row['ema_slow']:.5f}")

# Check bars around backtest start (index = start_idx - warmup_start_idx)
backtest_start_idx = start_idx - warmup_start_idx
print(f"\nBars around backtest start (idx={backtest_start_idx}, actual start_date):")
for i in range(max(0, backtest_start_idx-2), min(len(df), backtest_start_idx+3)):
    row = df.iloc[i]
    marker = " <-- BACKTEST START" if i == backtest_start_idx else ""
    print(f"  {i}: {df.index[i]} | EMA20={row['ema_fast']:.5f} | EMA50={row['ema_mid']:.5f} | EMA100={row['ema_slow']:.5f}{marker}")

# Build candles like API does
candles = []
for idx, row in df.iterrows():
    candle = {
        "timestamp": idx.isoformat(),
        "ema_fast": float(row.get('ema_fast', 0)) if not pd.isna(row.get('ema_fast', 0)) else None,
        "ema_mid": float(row.get('ema_mid', 0)) if not pd.isna(row.get('ema_mid', 0)) else None,
        "ema_slow": float(row.get('ema_slow', 0)) if not pd.isna(row.get('ema_slow', 0)) else None,
    }
    candles.append(candle)

# Count None values
none_counts = {
    'ema_fast': sum(1 for c in candles if c['ema_fast'] is None),
    'ema_mid': sum(1 for c in candles if c['ema_mid'] is None),
    'ema_slow': sum(1 for c in candles if c['ema_slow'] is None)
}

print(f"\nNone value counts in API response:")
print(f"  ema_fast: {none_counts['ema_fast']}/{len(candles)} ({none_counts['ema_fast']/len(candles)*100:.1f}%)")
print(f"  ema_mid: {none_counts['ema_mid']}/{len(candles)} ({none_counts['ema_mid']/len(candles)*100:.1f}%)")
print(f"  ema_slow: {none_counts['ema_slow']}/{len(candles)} ({none_counts['ema_slow']/len(candles)*100:.1f}%)")

if all(v == 0 for v in none_counts.values()):
    print("\n[OK] All EMAs have valid values!")
    print("\nCONCLUSION: Python backend is working correctly.")
    print("If EMAs are not showing in C#, the issue is in:")
    print("  1. C# not receiving the data (check API call)")
    print("  2. C# deserialization (check JSON parsing)")
    print("  3. C# rendering (check chart plot code)")
else:
    print("\n[ERROR] Some EMAs are None!")
