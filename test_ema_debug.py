"""
Quick test to check if EMAs exist in dataframe after warmup changes
"""
import sys
import os

# Add both the project root and config directory
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'config'))

import pandas as pd
from src.data_loader import DataLoader
from src.indicators import TechnicalIndicators

# Simulate what run_backtest does
print("Testing warmup logic and EMA preservation...")

# Step 1: Load and prepare data (like prepare_data)
loader = DataLoader()
indicators_calc = TechnicalIndicators()

df_m1 = loader.load_pair_data('EURUSD', '2024')
df_full = loader.resample_to_timeframe(df_m1, 'M15')

# Calculate EMAs
print("\n[1] Calculating EMAs on full dataset...")
df_full['ema_fast'] = indicators_calc.calculate_ema(df_full, 20)
df_full['ema_mid'] = indicators_calc.calculate_ema(df_full, 50)
df_full['ema_slow'] = indicators_calc.calculate_ema(df_full, 100)

print(f"    Full dataset: {len(df_full)} bars")
print(f"    Columns: {df_full.columns.tolist()}")
print(f"    EMAs present: ema_fast={('ema_fast' in df_full.columns)}, ema_mid={('ema_mid' in df_full.columns)}, ema_slow={('ema_slow' in df_full.columns)}")

# Step 2: Apply warmup slicing (like run_backtest)
print("\n[2] Applying warmup slicing logic...")
start_date = '2024-01-01'
WARMUP_BARS = 500

start_timestamp = pd.Timestamp(start_date)
start_idx = df_full.index.get_indexer([start_timestamp], method='bfill')[0]
warmup_start_idx = max(0, start_idx - WARMUP_BARS)

print(f"    start_idx: {start_idx}")
print(f"    warmup_start_idx: {warmup_start_idx}")
print(f"    Slicing from bar {warmup_start_idx} to end...")

df = df_full.iloc[warmup_start_idx:]

print(f"    Sliced dataset: {len(df)} bars")
print(f"    Columns after slicing: {df.columns.tolist()}")
print(f"    EMAs present after slice: ema_fast={('ema_fast' in df.columns)}, ema_mid={('ema_mid' in df.columns)}, ema_slow={('ema_slow' in df.columns)}")

# Check if EMAs exist in engine.df
print("\n" + "="*70)
print("CHECKING DATAFRAME COLUMNS")
print("="*70)

df = engine.df
print(f"\nDataframe shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nEMA columns present:")
print(f"  - ema_fast: {'ema_fast' in df.columns}")
print(f"  - ema_mid: {'ema_mid' in df.columns}")
print(f"  - ema_slow: {'ema_slow' in df.columns}")

if 'ema_fast' in df.columns:
    print(f"\nFirst 10 bars EMA values:")
    for i in range(min(10, len(df))):
        row = df.iloc[i]
        print(f"  Bar {i}: EMA20={row['ema_fast']:.5f} | EMA50={row['ema_mid']:.5f} | EMA100={row['ema_slow']:.5f}")

    print(f"\nLast 10 bars EMA values:")
    for i in range(max(0, len(df)-10), len(df)):
        row = df.iloc[i]
        print(f"  Bar {i}: EMA20={row['ema_fast']:.5f} | EMA50={row['ema_mid']:.5f} | EMA100={row['ema_slow']:.5f}")

    # Check for NaN values
    import pandas as pd
    ema_fast_nans = df['ema_fast'].isna().sum()
    ema_mid_nans = df['ema_mid'].isna().sum()
    ema_slow_nans = df['ema_slow'].isna().sum()

    print(f"\nNaN counts:")
    print(f"  - ema_fast: {ema_fast_nans}/{len(df)} ({ema_fast_nans/len(df)*100:.1f}%)")
    print(f"  - ema_mid: {ema_mid_nans}/{len(df)} ({ema_mid_nans/len(df)*100:.1f}%)")
    print(f"  - ema_slow: {ema_slow_nans}/{len(df)} ({ema_slow_nans/len(df)*100:.1f}%)")
else:
    print("\n[ERROR] EMA columns NOT FOUND in dataframe!")
    print("This is the root cause of the bug.")

print("\n" + "="*70)
