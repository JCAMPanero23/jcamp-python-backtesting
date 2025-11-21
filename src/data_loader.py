"""
═══════════════════════════════════════════════════════════════════════════════
DATA LOADER - MT5 CSV Handler
═══════════════════════════════════════════════════════════════════════════════
Handles tab-delimited MT5 M1 CSV exports and prepares data for backtesting.

Features:
- Load tab-delimited CSV files from MT5 export
- Resample M1 data to H1/M15 timeframes
- Handle broker suffix removal
- Validate data integrity
- Memory-efficient data handling

CSV Format Expected:
<DATE>    <TIME>    <OPEN>    <HIGH>    <LOW>    <CLOSE>    <TICKVOL>    <VOL>    <SPREAD>
2024.01.02    00:03:00    1.10439    1.10440    1.10439    1.10440    8    0    40
═══════════════════════════════════════════════════════════════════════════════
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mt5_settings import *

class DataLoader:
    """
    Load and prepare MT5 CSV data for backtesting
    """
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize data loader
        
        Args:
            data_dir: Root directory containing pair subdirectories
        """
        self.data_dir = Path(data_dir)
        self.loaded_data = {}  # Cache for loaded dataframes
        
    def load_pair_data(self, pair: str, year: int = 2024) -> pd.DataFrame:
        """
        Load M1 data for a currency pair
        
        Args:
            pair: Currency pair (e.g., 'EURUSD')
            year: Year to load
            
        Returns:
            DataFrame with OHLC data
        """
        # Check cache first
        cache_key = f"{pair}_{year}_M1"
        if cache_key in self.loaded_data:
            print(f"[OK] Loading {pair} from cache")
            return self.loaded_data[cache_key].copy()
        
        # Build file path: data/EURUSD_sml/2024_M1.csv
        pair_dir = self.data_dir / f"{pair}{BROKER_SUFFIX}"
        csv_file = pair_dir / f"{year}_M1.csv"
        
        if not csv_file.exists():
            raise FileNotFoundError(f"Data file not found: {csv_file}")
        
        print(f"[LOAD] Loading {pair} data from {csv_file}...")
        
        # Load tab-delimited CSV
        df = pd.read_csv(csv_file, sep='\t')
        
        # Validate columns
        expected_cols = ['<DATE>', '<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', 
                        '<TICKVOL>', '<VOL>', '<SPREAD>']
        if list(df.columns) != expected_cols:
            raise ValueError(f"Unexpected columns in {csv_file}: {df.columns.tolist()}")
        
        # Combine date and time into datetime index
        df['datetime'] = pd.to_datetime(df['<DATE>'] + ' ' + df['<TIME>'], 
                                       format='%Y.%m.%d %H:%M:%S')
        df.set_index('datetime', inplace=True)
        
        # Rename columns to standard format (remove <>)
        df.rename(columns={
            '<OPEN>': 'open',
            '<HIGH>': 'high',
            '<LOW>': 'low',
            '<CLOSE>': 'close',
            '<TICKVOL>': 'tick_volume',
            '<VOL>': 'volume',
            '<SPREAD>': 'spread'
        }, inplace=True)
        
        # Drop original date/time columns
        df.drop(columns=['<DATE>', '<TIME>'], inplace=True)
        
        # Sort by datetime (should already be sorted, but ensure it)
        df.sort_index(inplace=True)
        
        # Add pair column
        df['pair'] = pair
        
        # Validate data
        self._validate_ohlc(df, pair)
        
        # Cache the data
        self.loaded_data[cache_key] = df.copy()
        
        print(f"[OK] Loaded {len(df):,} M1 bars for {pair}")
        print(f"  Date range: {df.index[0]} to {df.index[-1]}")
        print(f"  Price range: {df['low'].min():.5f} - {df['high'].max():.5f}")
        
        return df
    
    def resample_to_timeframe(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """
        Resample M1 data to higher timeframe (H1, M15, etc.)
        
        Args:
            df: M1 DataFrame
            timeframe: Target timeframe ('H1', 'M15', 'D1', etc.)
            
        Returns:
            Resampled DataFrame
        """
        # Map timeframe codes to pandas resample rules
        timeframe_map = {
            'M1': '1T',   # 1 minute
            'M5': '5T',   # 5 minutes
            'M15': '15T', # 15 minutes
            'M30': '30T', # 30 minutes
            'H1': '1H',   # 1 hour
            'H4': '4H',   # 4 hours
            'D1': '1D',   # 1 day
        }
        
        if timeframe not in timeframe_map:
            raise ValueError(f"Unsupported timeframe: {timeframe}")
        
        rule = timeframe_map[timeframe]
        
        print(f"[TIME]  Resampling to {timeframe}...")
        
        # Resample using OHLC aggregation
        resampled = df.resample(rule).agg({
            'open': 'first',      # First price in period
            'high': 'max',        # Highest price in period
            'low': 'min',         # Lowest price in period
            'close': 'last',      # Last price in period
            'tick_volume': 'sum', # Sum of tick volumes
            'volume': 'sum',      # Sum of volumes
            'spread': 'mean',     # Average spread
            'pair': 'first'       # Keep pair name
        })
        
        # Remove any rows with NaN (incomplete periods)
        resampled.dropna(subset=['open', 'high', 'low', 'close'], inplace=True)
        
        print(f"[OK] Resampled to {len(resampled):,} {timeframe} bars")
        
        return resampled
    
    def load_multiple_pairs(self, pairs: List[str], year: int = 2024, 
                           timeframe: str = 'H1') -> Dict[str, pd.DataFrame]:
        """
        Load data for multiple pairs
        
        Args:
            pairs: List of currency pairs
            year: Year to load
            timeframe: Target timeframe
            
        Returns:
            Dictionary of {pair: DataFrame}
        """
        print(f"\n{'═'*80}")
        print(f"LOADING {len(pairs)} PAIRS - {timeframe} TIMEFRAME")
        print(f"{'═'*80}\n")
        
        data_dict = {}
        
        for pair in pairs:
            try:
                # Load M1 data
                df_m1 = self.load_pair_data(pair, year)
                
                # Resample to target timeframe
                if timeframe != 'M1':
                    df = self.resample_to_timeframe(df_m1, timeframe)
                else:
                    df = df_m1
                
                data_dict[pair] = df
                print()  # Blank line between pairs
                
            except Exception as e:
                print(f"[ERROR] Error loading {pair}: {e}")
                continue
        
        print(f"{'═'*80}")
        print(f"[OK] Successfully loaded {len(data_dict)}/{len(pairs)} pairs")
        print(f"{'═'*80}\n")
        
        return data_dict
    
    def _validate_ohlc(self, df: pd.DataFrame, pair: str):
        """
        Validate OHLC data integrity
        
        Args:
            df: DataFrame to validate
            pair: Pair name for error messages
        """
        # Check for NaN values
        nan_count = df[['open', 'high', 'low', 'close']].isna().sum().sum()
        if nan_count > 0:
            print(f"[WARN]  Warning: {nan_count} NaN values found in {pair} OHLC data")
        
        # Check OHLC relationships (high >= low, etc.)
        invalid_hl = (df['high'] < df['low']).sum()
        invalid_oh = (df['open'] > df['high']).sum()
        invalid_ol = (df['open'] < df['low']).sum()
        invalid_ch = (df['close'] > df['high']).sum()
        invalid_cl = (df['close'] < df['low']).sum()
        
        total_invalid = invalid_hl + invalid_oh + invalid_ol + invalid_ch + invalid_cl
        
        if total_invalid > 0:
            print(f"[WARN]  Warning: {total_invalid} invalid OHLC relationships in {pair}")
            print(f"    High < Low: {invalid_hl}")
            print(f"    Open > High: {invalid_oh}")
            print(f"    Open < Low: {invalid_ol}")
            print(f"    Close > High: {invalid_ch}")
            print(f"    Close < Low: {invalid_cl}")
        
        # Check for duplicate timestamps
        duplicates = df.index.duplicated().sum()
        if duplicates > 0:
            print(f"[WARN]  Warning: {duplicates} duplicate timestamps in {pair}")
            # Remove duplicates, keep last
            df = df[~df.index.duplicated(keep='last')]
        
        # Check for gaps in M1 data (should be continuous)
        time_diff = df.index.to_series().diff()
        expected_diff = pd.Timedelta(minutes=1)
        gaps = (time_diff > expected_diff * 5).sum()  # Gaps > 5 minutes
        if gaps > 0:
            print(f"[WARN]  Info: {gaps} gaps detected in {pair} M1 data (weekends/holidays expected)")
    
    def get_date_range(self, df: pd.DataFrame) -> Tuple[datetime, datetime]:
        """Get start and end dates from DataFrame"""
        return df.index[0], df.index[-1]
    
    def get_bar_at_time(self, df: pd.DataFrame, target_time: datetime) -> Optional[pd.Series]:
        """
        Get the bar at or before a specific time
        
        Args:
            df: DataFrame to search
            target_time: Target datetime
            
        Returns:
            Series representing the bar, or None if not found
        """
        if target_time < df.index[0] or target_time > df.index[-1]:
            return None
        
        # Find the nearest bar at or before target_time
        idx = df.index.searchsorted(target_time, side='right') - 1
        if idx < 0:
            return None
        
        return df.iloc[idx]
    
    def filter_by_date_range(self, df: pd.DataFrame, 
                            start_date: str, end_date: str) -> pd.DataFrame:
        """
        Filter DataFrame by date range
        
        Args:
            df: DataFrame to filter
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            Filtered DataFrame
        """
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        
        filtered = df[(df.index >= start) & (df.index <= end)]
        
        print(f"📅 Filtered to {start_date} → {end_date}")
        print(f"   {len(filtered):,} bars ({len(filtered)/len(df)*100:.1f}% of original)")
        
        return filtered


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING & VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "═"*80)
    print("DATA LOADER - VALIDATION TEST")
    print("═"*80 + "\n")
    
    # Initialize loader
    loader = DataLoader(data_dir="D:/JcampFxTrading/jcamp-python-backtesting/data")
    
    # Test 1: Load single pair M1 data
    print("TEST 1: Load EURUSD M1 data")
    print("-"*80)
    try:
        eurusd_m1 = loader.load_pair_data('EURUSD', 2024)
        print(f"[OK] Test 1 PASSED")
        print(f"  Shape: {eurusd_m1.shape}")
        print(f"  Columns: {eurusd_m1.columns.tolist()}")
        print(f"\nFirst 3 bars:")
        print(eurusd_m1.head(3))
        print(f"\nLast 3 bars:")
        print(eurusd_m1.tail(3))
    except Exception as e:
        print(f"[X] Test 1 FAILED: {e}")
    
    print("\n" + "-"*80)
    print("TEST 2: Resample to H1")
    print("-"*80)
    try:
        eurusd_h1 = loader.resample_to_timeframe(eurusd_m1, 'H1')
        print(f"[OK] Test 2 PASSED")
        print(f"  M1 bars: {len(eurusd_m1):,}")
        print(f"  H1 bars: {len(eurusd_h1):,}")
        print(f"  Ratio: {len(eurusd_m1)/len(eurusd_h1):.1f}x")
        print(f"\nFirst H1 bar:")
        print(eurusd_h1.head(1))
    except Exception as e:
        print(f"[X] Test 2 FAILED: {e}")
    
    print("\n" + "-"*80)
    print("TEST 3: Load multiple pairs")
    print("-"*80)
    try:
        test_pairs = ['EURUSD', 'GBPUSD']
        multi_data = loader.load_multiple_pairs(test_pairs, 2024, 'H1')
        print(f"[OK] Test 3 PASSED")
        for pair, df in multi_data.items():
            print(f"  {pair}: {len(df):,} H1 bars")
    except Exception as e:
        print(f"[X] Test 3 FAILED: {e}")
    
    print("\n" + "-"*80)
    print("TEST 4: Date range filtering")
    print("-"*80)
    try:
        jan_mar = loader.filter_by_date_range(eurusd_h1, '2024-01-01', '2024-03-31')
        print(f"[OK] Test 4 PASSED")
        print(f"  Filtered bars: {len(jan_mar):,}")
        print(f"  Date range: {jan_mar.index[0]} to {jan_mar.index[-1]}")
    except Exception as e:
        print(f"[X] Test 4 FAILED: {e}")
    
    print("\n" + "═"*80)
    print("ALL TESTS COMPLETE")
    print("═"*80 + "\n")
