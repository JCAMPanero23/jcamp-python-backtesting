"""
Test what API returns for Feb 1-29 backtest with warmup
"""
import sys
import os
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'config'))

import pandas as pd
from src.backtest_engine import BacktestEngine

# Simulate backtest for Feb 1-29 (like user's test)
engine = BacktestEngine(
    initial_balance=10000.0,
    risk_percent=2.0,
    max_positions=2,
    timeframe='M15'
)

start_date = '2024-02-01'
end_date = '2024-02-29'

print(f"{'='*70}")
print(f"Testing backtest: {start_date} to {end_date}")
print(f"{'='*70}\n")

# This is what the API does
from src.data_loader import DataLoader
from src.indicators import TechnicalIndicators

loader = DataLoader()
indicators_calc = TechnicalIndicators()

df_m1 = loader.load_pair_data('EURUSD', '2024')
df_full = loader.resample_to_timeframe(df_m1, 'M15')

# Calculate EMAs
df_full['ema_fast'] = indicators_calc.calculate_ema(df_full, 20)
df_full['ema_mid'] = indicators_calc.calculate_ema(df_full, 50)
df_full['ema_slow'] = indicators_calc.calculate_ema(df_full, 100)

# Apply warmup logic
WARMUP_BARS = 500

start_timestamp = pd.Timestamp(start_date)
start_idx = df_full.index.get_indexer([start_timestamp], method='bfill')[0]
warmup_start_idx = max(0, start_idx - WARMUP_BARS)

actual_warmup_bars = start_idx - warmup_start_idx
print(f"Warmup bars: {actual_warmup_bars} (requested {WARMUP_BARS})")
print(f"Warmup start: {df_full.index[warmup_start_idx]}")
print(f"Backtest start: {df_full.index[start_idx]}\n")

# Slice dataframe (this is what goes into engine.df)
df = df_full.iloc[warmup_start_idx:]

# Filter end date
end_timestamp = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
df = df[df.index <= end_timestamp]

print(f"Total bars in API response: {len(df)}")
print(f"Date range: {df.index[0]} to {df.index[-1]}")
print(f"Backtest start index: {start_idx - warmup_start_idx}\n")

# Check what C# will receive
print(f"{'='*70}")
print(f"WHAT C# RECEIVES")
print(f"{'='*70}\n")

# Simulate JSON response (like _prepare_ohlc_data does)
candles = []
for idx, row in df.iterrows():
    candle = {
        "timestamp": idx.isoformat(),
        "ema_fast": float(row.get('ema_fast', 0)) if not pd.isna(row.get('ema_fast', 0)) else None,
        "ema_mid": float(row.get('ema_mid', 0)) if not pd.isna(row.get('ema_mid', 0)) else None,
        "ema_slow": float(row.get('ema_slow', 0)) if not pd.isna(row.get('ema_slow', 0)) else None,
    }
    candles.append(candle)

print(f"C# receives: {len(candles)} candles")
print(f"StartDate in JSON: '{start_date}'")
print(f"EndDate in JSON: '{end_date}'")
print(f"First candle timestamp: {candles[0]['timestamp']}")
print(f"Last candle timestamp: {candles[-1]['timestamp']}\n")

print(f"First 5 candles (warmup period):")
for i in range(min(5, len(candles))):
    c = candles[i]
    print(f"  {i}: {c['timestamp']} | EMA20={c['ema_fast']} | EMA50={c['ema_mid']} | EMA100={c['ema_slow']}")

print(f"\nCandles around backtest start (index {start_idx - warmup_start_idx}):")
backtest_start_idx = start_idx - warmup_start_idx
for i in range(max(0, backtest_start_idx-2), min(len(candles), backtest_start_idx+3)):
    c = candles[i]
    marker = " <-- BACKTEST START (where trading begins)" if i == backtest_start_idx else ""
    print(f"  {i}: {c['timestamp']} | EMA20={c['ema_fast']:.5f} | EMA50={c['ema_mid']:.5f} | EMA100={c['ema_slow']:.5f}{marker}")

print(f"\n{'='*70}")
print(f"CONCLUSION")
print(f"{'='*70}\n")
print(f"✅ Python sends ALL {len(candles)} candles including warmup")
print(f"✅ First candle is from {candles[0]['timestamp'][:10]} (NOT {start_date}!)")
print(f"✅ StartDate in JSON is '{start_date}' but candles start earlier")
print(f"\n⚠️ C# MUST display ALL candles, not filter by StartDate!")
print(f"⚠️ Otherwise warmup bars won't show and EMAs will appear delayed")
