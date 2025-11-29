"""
Test API response to check if EMAs are included in JSON
"""
import sys
import os
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'config'))

import pandas as pd
from src.data_loader import DataLoader
from src.indicators import TechnicalIndicators

# Simulate what backtest_service.py does
print("Testing API response building...")

# Step 1: Prepare data with EMAs
loader = DataLoader()
indicators_calc = TechnicalIndicators()

df_m1 = loader.load_pair_data('EURUSD', '2024')
df_full = loader.resample_to_timeframe(df_m1, 'M15')

# Calculate EMAs
df_full['ema_fast'] = indicators_calc.calculate_ema(df_full, 20)
df_full['ema_mid'] = indicators_calc.calculate_ema(df_full, 50)
df_full['ema_slow'] = indicators_calc.calculate_ema(df_full, 100)

# Step 2: Apply warmup slicing
start_date = '2024-01-01'
end_date = '2024-01-02'
WARMUP_BARS = 500

start_timestamp = pd.Timestamp(start_date)
start_idx = df_full.index.get_indexer([start_timestamp], method='bfill')[0]
warmup_start_idx = max(0, start_idx - WARMUP_BARS)

df = df_full.iloc[warmup_start_idx:]

# Filter end date
end_timestamp = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
df = df[df.index <= end_timestamp]

print(f"\n[1] Dataframe after warmup + date filtering:")
print(f"    Bars: {len(df)}")
print(f"    Columns: {df.columns.tolist()}")
print(f"    Date range: {df.index[0]} to {df.index[-1]}")

# Step 3: Simulate OHLC response building (like backtest_service.py does)
print(f"\n[2] Building OHLC response (like backtest_service.py)...")

candles = []
for idx, row in df.iterrows():
    candle = {
        "timestamp": idx.isoformat(),
        "open": float(row['open']),
        "high": float(row['high']),
        "low": float(row['low']),
        "close": float(row['close']),
        "ema_fast": float(row.get('ema_fast', 0)) if not pd.isna(row.get('ema_fast', 0)) else None,
        "ema_mid": float(row.get('ema_mid', 0)) if not pd.isna(row.get('ema_mid', 0)) else None,
        "ema_slow": float(row.get('ema_slow', 0)) if not pd.isna(row.get('ema_slow', 0)) else None,
    }
    candles.append(candle)

print(f"    Total candles: {len(candles)}")

# Check first 10 and last 10 candles
print(f"\n[3] Checking EMA values in first 10 candles:")
for i in range(min(10, len(candles))):
    c = candles[i]
    print(f"    {i}: {c['timestamp']} | EMA20={c['ema_fast']} | EMA50={c['ema_mid']} | EMA100={c['ema_slow']}")

print(f"\n[4] Checking EMA values in last 10 candles:")
for i in range(max(0, len(candles)-10), len(candles)):
    c = candles[i]
    print(f"    {i}: {c['timestamp']} | EMA20={c['ema_fast']} | EMA50={c['ema_mid']} | EMA100={c['ema_slow']}")

# Count None values
none_counts = {
    'ema_fast': sum(1 for c in candles if c['ema_fast'] is None),
    'ema_mid': sum(1 for c in candles if c['ema_mid'] is None),
    'ema_slow': sum(1 for c in candles if c['ema_slow'] is None)
}

print(f"\n[5] None value counts:")
print(f"    ema_fast: {none_counts['ema_fast']}/{len(candles)} ({none_counts['ema_fast']/len(candles)*100:.1f}%)")
print(f"    ema_mid: {none_counts['ema_mid']}/{len(candles)} ({none_counts['ema_mid']/len(candles)*100:.1f}%)")
print(f"    ema_slow: {none_counts['ema_slow']}/{len(candles)} ({none_counts['ema_slow']/len(candles)*100:.1f}%)")

# Check if ALL are None (this would be the bug!)
if none_counts['ema_fast'] == len(candles):
    print("\n[ERROR] ALL ema_fast values are None! This is the bug!")
elif none_counts['ema_mid'] == len(candles):
    print("\n[ERROR] ALL ema_mid values are None! This is the bug!")
elif none_counts['ema_slow'] == len(candles):
    print("\n[ERROR] ALL ema_slow values are None! This is the bug!")
else:
    print("\n[OK] EMAs have valid values in the response")
