"""
═══════════════════════════════════════════════════════════════════════════════
CURRENCY STRENGTH METER (CSM) CALCULATOR - FIXED VERSION
═══════════════════════════════════════════════════════════════════════════════
Bug Fix: Properly initialize price_change_24h and handle missing data
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import sys
import os

# Add config directory to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'config'))

from mt5_settings import *

class CSMCalculator:
    """
    Currency Strength Meter - calculates relative strength of 8 major currencies
    """
    
    def __init__(self, lookback_hours: int = CSM_LOOKBACK_HOURS):
        """
        Initialize CSM calculator
        
        Args:
            lookback_hours: Hours to look back for strength calculation (default 48)
        """
        self.lookback_hours = lookback_hours
        self.calculation_period = CSM_CALCULATION_PERIOD  # 24H for price changes
        
        # Initialize currency strength data structure
        self.currency_strengths = {curr: 0.0 for curr in CSM_CURRENCIES}
        self.strength_changes_24h = {curr: 0.0 for curr in CSM_CURRENCIES}
        self.last_update = None
        self.data_valid = False
        
        # Pair data cache
        self.pair_data = {pair: {} for pair in CSM_PAIRS}
        
    def update_csm(self, pair_dataframes: Dict[str, pd.DataFrame], 
                   current_time: datetime, 
                   timeframe: str = 'H1') -> bool:
        """
        Update CSM values based on current market data
        
        Args:
            pair_dataframes: Dict of {pair: DataFrame} with OHLC data
            current_time: Current datetime for calculation
            timeframe: Timeframe of data ('H1', 'M15', etc.)
            
        Returns:
            True if CSM updated successfully, False otherwise
        """
        # Reset strength values to neutral (50.0)
        for curr in CSM_CURRENCIES:
            self.currency_strengths[curr] = 50.0
            self.strength_changes_24h[curr] = 0.0
        
        # Calculate bars needed based on timeframe
        bars_needed = self._calculate_bars_needed(timeframe)
        bars_24h = bars_needed // 2  # 24H ago is halfway through 48H lookback
        
        # Step 1: Calculate 24H price changes for all 15 pairs
        for pair in CSM_PAIRS:
            # ✅ INITIALIZE PAIR DATA WITH DEFAULTS
            self.pair_data[pair] = {
                'current_price': 0.0,
                'price_24h_ago': 0.0,
                'price_48h_ago': 0.0,
                'price_change_24h': 0.0,  # ✅ ALWAYS INITIALIZE THIS
                'data_available': False
            }
            
            if pair not in pair_dataframes:
                # Data not available - already initialized to zeros
                continue
            
            df = pair_dataframes[pair]
            
            # Get price data at specific time points
            try:
                # Find current bar
                current_bar = self._get_bar_at_time(df, current_time)
                if current_bar is None:
                    continue
                
                # Find 24H ago bar
                time_24h_ago = current_time - timedelta(hours=24)
                bar_24h_ago = self._get_bar_at_time(df, time_24h_ago)
                if bar_24h_ago is None:
                    continue
                
                # Find 48H ago bar (for future use if needed)
                time_48h_ago = current_time - timedelta(hours=48)
                bar_48h_ago = self._get_bar_at_time(df, time_48h_ago)
                
                # Update pair data
                self.pair_data[pair]['current_price'] = current_bar['close']
                self.pair_data[pair]['price_24h_ago'] = bar_24h_ago['close']
                self.pair_data[pair]['price_48h_ago'] = bar_48h_ago['close'] if bar_48h_ago is not None else 0.0
                self.pair_data[pair]['data_available'] = True
                
                # Calculate 24H price change (percentage)
                if bar_24h_ago['close'] > 0:
                    price_change = (current_bar['close'] - bar_24h_ago['close']) / bar_24h_ago['close']
                    self.pair_data[pair]['price_change_24h'] = price_change
                
            except Exception as e:
                print(f"⚠️  Error processing {pair}: {e}")
                continue
        
        # Step 2: Distribute strength changes to currencies
        for pair in CSM_PAIRS:
            # ✅ CHECK IF DATA IS AVAILABLE BEFORE PROCESSING
            if not self.pair_data[pair].get('data_available', False):
                continue
            
            # ✅ SAFELY GET PRICE CHANGE (already initialized)
            price_change = self.pair_data[pair]['price_change_24h']
            
            if price_change == 0.0:
                continue
            
            # Get weight for this pair (EURUSD, GBPUSD, GBPNZD = 1.5, others = 1.0)
            weight = get_pair_weight(pair)
            
            # Calculate strength change (MT5 formula)
            # strength_change = price_change * 100.0 * 2.0 * weight
            strength_change = price_change * CSM_STRENGTH_MULTIPLIER * CSM_WEIGHT_FACTOR * weight
            
            # Extract base and quote currencies
            base, quote = get_base_quote(pair)
            
            # Distribute strength:
            # If EURUSD goes up 1% → EUR gains strength, USD loses strength
            # base += strength_change, quote -= strength_change
            if base in self.currency_strengths and quote in self.currency_strengths:
                self.currency_strengths[base] += strength_change
                self.strength_changes_24h[base] += strength_change
                
                self.currency_strengths[quote] -= strength_change
                self.strength_changes_24h[quote] -= strength_change
        
        # Step 3: Normalize strength values to 0-100 scale
        self._normalize_strengths()
        
        # Mark data as valid
        self.data_valid = True
        self.last_update = current_time
        
        return True
    
    def _normalize_strengths(self):
        """
        Normalize currency strengths to 0-100 scale using min-max normalization
        (Exact MT5 v1.96 logic from NormalizeStrengthValues())
        """
        # Find min and max strength values
        strength_values = list(self.currency_strengths.values())
        min_strength = min(strength_values)
        max_strength = max(strength_values)
        
        strength_range = max_strength - min_strength
        
        # Only normalize if range is significant (> 0.001)
        if strength_range > CSM_NORMALIZATION_THRESHOLD:
            # Normalize each currency to 0-100 scale
            for curr in CSM_CURRENCIES:
                normalized = ((self.currency_strengths[curr] - min_strength) / strength_range) * 100.0
                self.currency_strengths[curr] = normalized
                
                # Also normalize 24h changes (for future reference)
                if strength_range > 0:
                    self.strength_changes_24h[curr] = (self.strength_changes_24h[curr] / strength_range) * 100.0
        else:
            # No significant range - set all to neutral (50.0)
            for curr in CSM_CURRENCIES:
                self.currency_strengths[curr] = 50.0
                self.strength_changes_24h[curr] = 0.0
    
    def get_currency_strength(self, currency: str) -> float:
        """
        Get current strength for a specific currency
        
        Args:
            currency: Currency code (e.g., 'USD', 'EUR')
            
        Returns:
            Strength value (0-100), or 50.0 if invalid/neutral
        """
        if not self.data_valid:
            return 50.0
        
        return self.currency_strengths.get(currency, 50.0)
    
    def get_csm_differential(self, pair: str) -> float:
        """
        Calculate CSM differential for a currency pair
        Differential = base_strength - quote_strength
        
        Args:
            pair: Currency pair (e.g., 'EURUSD')
            
        Returns:
            Differential value (-100 to +100)
        """
        if not self.data_valid:
            return 0.0
        
        # Remove broker suffix if present
        clean_pair = pair.replace(BROKER_SUFFIX, '')
        
        # Extract base and quote currencies
        base, quote = get_base_quote(clean_pair)
        
        # Calculate differential
        base_strength = self.get_currency_strength(base)
        quote_strength = self.get_currency_strength(quote)
        
        return base_strength - quote_strength
    
    def get_all_strengths(self) -> Dict[str, float]:
        """Get all current currency strengths"""
        return self.currency_strengths.copy()
    
    def get_strongest_currency(self) -> Tuple[str, float]:
        """Get the strongest currency and its strength value"""
        if not self.data_valid:
            return ('NONE', 50.0)
        
        strongest = max(self.currency_strengths.items(), key=lambda x: x[1])
        return strongest
    
    def get_weakest_currency(self) -> Tuple[str, float]:
        """Get the weakest currency and its strength value"""
        if not self.data_valid:
            return ('NONE', 50.0)
        
        weakest = min(self.currency_strengths.items(), key=lambda x: x[1])
        return weakest
    
    def get_strength_summary(self) -> str:
        """Get formatted summary of all currency strengths"""
        if not self.data_valid:
            return "CSM data not valid"
        
        summary = "\n" + "="*60 + "\n"
        summary += "CURRENCY STRENGTH METER\n"
        summary += "="*60 + "\n"
        summary += f"Last Update: {self.last_update}\n"
        summary += "-"*60 + "\n"
        
        # Sort currencies by strength (descending)
        sorted_currencies = sorted(self.currency_strengths.items(), 
                                  key=lambda x: x[1], reverse=True)
        
        for curr, strength in sorted_currencies:
            # Create visual bar
            bar_length = int(strength / 5)  # 0-100 → 0-20 chars
            bar = "█" * bar_length
            
            summary += f"{curr}: {strength:6.2f} {bar}\n"
        
        summary += "-"*60 + "\n"
        strongest, str_val = self.get_strongest_currency()
        weakest, weak_val = self.get_weakest_currency()
        summary += f"Strongest: {strongest} ({str_val:.2f})\n"
        summary += f"Weakest: {weakest} ({weak_val:.2f})\n"
        summary += f"Range: {str_val - weak_val:.2f}\n"
        summary += "="*60 + "\n"
        
        return summary
    
    def _calculate_bars_needed(self, timeframe: str) -> int:
        """Calculate number of bars needed for lookback period"""
        timeframe_hours = {
            'M1': 1/60, 'M5': 5/60, 'M15': 15/60, 'M30': 30/60,
            'H1': 1, 'H4': 4, 'D1': 24
        }
        
        hours_per_bar = timeframe_hours.get(timeframe, 1)
        bars_needed = int(np.ceil(self.lookback_hours / hours_per_bar)) + 1
        
        return bars_needed
    
    def _get_bar_at_time(self, df: pd.DataFrame, target_time: datetime) -> Optional[pd.Series]:
        """
        Get the bar at or before a specific time
        
        Args:
            df: DataFrame to search
            target_time: Target datetime
            
        Returns:
            Series representing the bar, or None if not found
        """
        if len(df) == 0:
            return None
        
        if target_time < df.index[0] or target_time > df.index[-1]:
            return None
        
        # Find the nearest bar at or before target_time
        idx = df.index.searchsorted(target_time, side='right') - 1
        if idx < 0:
            return None
        
        return df.iloc[idx]
    
    def diagnose_csm(self) -> str:
        """Get diagnostic information about CSM calculation"""
        diag = "\n" + "="*60 + "\n"
        diag += "CSM DIAGNOSTICS\n"
        diag += "="*60 + "\n"
        diag += f"Data Valid: {self.data_valid}\n"
        diag += f"Last Update: {self.last_update}\n"
        diag += f"Lookback Hours: {self.lookback_hours}\n"
        diag += "-"*60 + "\n"
        diag += "PAIR DATA (24H Price Changes):\n"
        diag += "-"*60 + "\n"
        
        for pair in CSM_PAIRS:
            if pair in self.pair_data and self.pair_data[pair].get('data_available', False):
                change = self.pair_data[pair]['price_change_24h']
                weight = get_pair_weight(pair)
                diag += f"{pair:8s}: {change:+.4%} (weight: {weight:.1f})\n"
            else:
                diag += f"{pair:8s}: NO DATA\n"
        
        diag += "="*60 + "\n"
        return diag


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING & VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "═"*80)
    print("CSM CALCULATOR - VALIDATION TEST")
    print("═"*80 + "\n")
    
    # This test requires data_loader.py to be working
    from data_loader import DataLoader
    
    # Initialize
    print("Initializing...")
    loader = DataLoader(data_dir="data")
    csm = CSMCalculator()
    
    # Load data for CSM pairs (we'll test with a subset for speed)
    print("\nLoading CSM pair data...")
    test_pairs = ['EURUSD', 'GBPUSD']
    
    try:
        pair_data = loader.load_multiple_pairs(test_pairs, 2024, 'H1')
        
        # Test CSM calculation at different time points
        print("\n" + "-"*80)
        print("TEST 1: CSM Calculation - Mid-Year (June 1, 2024)")
        print("-"*80)
        
        test_time = datetime(2024, 6, 1, 12, 0, 0)
        success = csm.update_csm(pair_data, test_time, 'H1')
        
        if success:
            print("✓ CSM calculation successful")
            print(csm.get_strength_summary())
            print(csm.diagnose_csm())
            
            # Test differential calculation
            print("\n" + "-"*80)
            print("TEST 2: CSM Differentials")
            print("-"*80)
            for pair in ['EURUSD', 'GBPUSD']:
                diff = csm.get_csm_differential(pair)
                base, quote = get_base_quote(pair)
                base_str = csm.get_currency_strength(base)
                quote_str = csm.get_currency_strength(quote)
                print(f"{pair}: {diff:+7.2f} ({base}:{base_str:.2f} - {quote}:{quote_str:.2f})")
            
            print("\n✓ All tests completed successfully!")
            
        else:
            print("✗ CSM calculation failed")
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "═"*80)
    print("TEST COMPLETE")
    print("═"*80 + "\n")
