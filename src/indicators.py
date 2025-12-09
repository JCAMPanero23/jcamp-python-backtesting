"""
═══════════════════════════════════════════════════════════════════════════════
TECHNICAL INDICATORS - MT5 Compatible Calculations
═══════════════════════════════════════════════════════════════════════════════
Implements exact MT5 indicator calculations:
- ATR (Average True Range) - Volatility measurement
- EMA (Exponential Moving Average) - Trend direction
- ADX (Average Directional Index) - Trend strength
- +DI/-DI (Directional Indicators) - Trend direction components

All calculations match MT5 iATR, iMA, iADX functions for consistency with
the existing Jcamp_BacktestEA.mq5 v1.96 implementation.
═══════════════════════════════════════════════════════════════════════════════
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple
import sys
import os

# Add config directory to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'config'))

from mt5_settings import *

class TechnicalIndicators:
    """
    Technical indicator calculations matching MT5 implementation
    """
    
    def __init__(self):
        """Initialize indicator calculator"""
        self.indicator_cache = {}  # Cache calculated indicators
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ATR (AVERAGE TRUE RANGE) - Volatility Measurement
    # ═══════════════════════════════════════════════════════════════════════════
    
    def calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculate Average True Range (ATR)
        
        ATR measures market volatility by decomposing the entire range of prices
        for that period. Uses Wilder's smoothing (similar to EMA with alpha=1/period).
        
        Args:
            df: DataFrame with 'high', 'low', 'close' columns
            period: ATR period (default 14)
            
        Returns:
            Series with ATR values
        """
        high = df['high']
        low = df['low']
        close = df['close']
        
        # Calculate True Range components
        tr1 = high - low                          # Current high - current low
        tr2 = abs(high - close.shift(1))          # Current high - previous close
        tr3 = abs(low - close.shift(1))           # Current low - previous close
        
        # True Range is the maximum of the three
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # Calculate ATR using Wilder's smoothing (exponential moving average)
        # alpha = 1/period for Wilder's smoothing
        atr = tr.ewm(alpha=1/period, adjust=False).mean()
        
        return atr
    
    def get_atr(self, df: pd.DataFrame, period: int = 14, 
                index: int = -1) -> float:
        """
        Get ATR value at specific index (default: most recent)
        
        Args:
            df: DataFrame with OHLC data
            period: ATR period
            index: Index to get value from (-1 = most recent)
            
        Returns:
            ATR value
        """
        atr_series = self.calculate_atr(df, period)
        
        if len(atr_series) == 0:
            return 0.0
        
        return atr_series.iloc[index]
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EMA (EXPONENTIAL MOVING AVERAGE) - Trend Direction
    # ═══════════════════════════════════════════════════════════════════════════
    
    def calculate_ema(self, df: pd.DataFrame, period: int, 
                     price: str = 'close') -> pd.Series:
        """
        Calculate Exponential Moving Average (EMA)
        
        EMA gives more weight to recent prices. Responds faster to price changes
        than Simple Moving Average (SMA).
        
        Args:
            df: DataFrame with price data
            period: EMA period
            price: Price column to use ('close', 'open', 'high', 'low')
            
        Returns:
            Series with EMA values
        """
        if price not in df.columns:
            raise ValueError(f"Price column '{price}' not found in DataFrame")
        
        # Calculate EMA using pandas built-in function
        ema = df[price].ewm(span=period, adjust=False).mean()
        
        return ema
    
    def get_ema(self, df: pd.DataFrame, period: int, 
                price: str = 'close', index: int = -1) -> float:
        """
        Get EMA value at specific index
        
        Args:
            df: DataFrame with price data
            period: EMA period
            price: Price column to use
            index: Index to get value from (-1 = most recent)
            
        Returns:
            EMA value
        """
        ema_series = self.calculate_ema(df, period, price)
        
        if len(ema_series) == 0:
            return 0.0
        
        return ema_series.iloc[index]
    
    def calculate_ema_separation(self, df: pd.DataFrame, 
                                 fast_period: int = 20,
                                 slow_period: int = 50) -> float:
        """
        Calculate EMA separation percentage
        
        Measures how far apart the fast and slow EMAs are, as a percentage
        of price. Used in regime detection to identify strong trends.
        
        Args:
            df: DataFrame with price data
            fast_period: Fast EMA period (default 20)
            slow_period: Slow EMA period (default 50)
            
        Returns:
            EMA separation as percentage (0-100)
        """
        ema_fast = self.get_ema(df, fast_period)
        ema_slow = self.get_ema(df, slow_period)
        current_price = df['close'].iloc[-1]
        
        if current_price == 0:
            return 0.0
        
        # Calculate separation as percentage of price
        separation = abs(ema_fast - ema_slow) / current_price * 100.0
        
        return separation
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ADX (AVERAGE DIRECTIONAL INDEX) - Trend Strength
    # ═══════════════════════════════════════════════════════════════════════════
    
    def calculate_adx(self, df: pd.DataFrame, period: int = 14) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate ADX (Average Directional Index) and directional indicators
        
        ADX measures trend strength (0-100):
        - 0-25: Weak/absent trend (ranging)
        - 25-50: Strong trend
        - 50-75: Very strong trend
        - 75-100: Extremely strong trend
        
        Also returns +DI and -DI which indicate trend direction.
        
        Args:
            df: DataFrame with 'high', 'low', 'close' columns
            period: ADX period (default 14)
            
        Returns:
            Tuple of (adx_series, plus_di_series, minus_di_series)
        """
        high = df['high']
        low = df['low']
        close = df['close']
        
        # Calculate +DM (Positive Directional Movement)
        plus_dm = high.diff()
        plus_dm[plus_dm < 0] = 0
        
        # Calculate -DM (Negative Directional Movement)
        minus_dm = -low.diff()
        minus_dm[minus_dm < 0] = 0
        
        # When both +DM and -DM are positive, only keep the larger one
        plus_dm[plus_dm < minus_dm] = 0
        minus_dm[minus_dm < plus_dm] = 0
        
        # Calculate True Range
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # Smooth the values using Wilder's smoothing
        atr = tr.ewm(alpha=1/period, adjust=False).mean()
        plus_dm_smooth = plus_dm.ewm(alpha=1/period, adjust=False).mean()
        minus_dm_smooth = minus_dm.ewm(alpha=1/period, adjust=False).mean()
        
        # Calculate +DI and -DI (Directional Indicators)
        plus_di = 100 * plus_dm_smooth / atr
        minus_di = 100 * minus_dm_smooth / atr
        
        # Calculate DX (Directional Index)
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        
        # Handle division by zero
        dx = dx.fillna(0)
        
        # Calculate ADX (smoothed DX)
        adx = dx.ewm(alpha=1/period, adjust=False).mean()
        
        return adx, plus_di, minus_di
    
    def get_adx(self, df: pd.DataFrame, period: int = 14, 
                index: int = -1) -> float:
        """
        Get ADX value at specific index
        
        Args:
            df: DataFrame with OHLC data
            period: ADX period
            index: Index to get value from (-1 = most recent)
            
        Returns:
            ADX value
        """
        adx_series, _, _ = self.calculate_adx(df, period)
        
        if len(adx_series) == 0:
            return 0.0
        
        return adx_series.iloc[index]
    
    def get_directional_indicators(self, df: pd.DataFrame, period: int = 14,
                                   index: int = -1) -> Tuple[float, float]:
        """
        Get +DI and -DI values at specific index
        
        Args:
            df: DataFrame with OHLC data
            period: ADX period
            index: Index to get value from (-1 = most recent)
            
        Returns:
            Tuple of (plus_di, minus_di)
        """
        _, plus_di, minus_di = self.calculate_adx(df, period)
        
        if len(plus_di) == 0 or len(minus_di) == 0:
            return 0.0, 0.0
        
        return plus_di.iloc[index], minus_di.iloc[index]

    # ═══════════════════════════════════════════════════════════════════════════
    # RSI (RELATIVE STRENGTH INDEX) - Momentum Oscillator
    # ═══════════════════════════════════════════════════════════════════════════

    def calculate_rsi(self, df: pd.DataFrame, period: int = 14,
                      price: str = 'close') -> pd.Series:
        """
        Calculate RSI (Relative Strength Index)

        RSI is a momentum oscillator that measures the speed and magnitude of
        price changes. Values range from 0-100:
        - Above 70: Overbought (potential reversal down)
        - Below 30: Oversold (potential reversal up)
        - Above 50: Bullish momentum
        - Below 50: Bearish momentum

        Uses Wilder's smoothing method (same as MT5 iRSI function).

        Args:
            df: DataFrame with price data
            period: RSI period (default 14)
            price: Price column to use ('close', 'open', 'high', 'low')

        Returns:
            Series with RSI values (0-100)
        """
        if price not in df.columns:
            raise ValueError(f"Price column '{price}' not found in DataFrame")

        # Calculate price changes
        delta = df[price].diff()

        # Separate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Calculate average gain/loss using Wilder's smoothing
        # Wilder's smoothing uses alpha = 1/period (same as ATR and ADX)
        avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()

        # Calculate RS (Relative Strength)
        rs = avg_gain / avg_loss

        # Calculate RSI
        # RSI = 100 - (100 / (1 + RS))
        rsi = 100 - (100 / (1 + rs))

        # Handle division by zero (when avg_loss = 0, RSI = 100)
        rsi = rsi.fillna(100)

        return rsi

    def get_rsi(self, df: pd.DataFrame, period: int = 14,
                price: str = 'close', index: int = -1) -> float:
        """
        Get RSI value at specific index

        Args:
            df: DataFrame with price data
            period: RSI period
            price: Price column to use
            index: Index to get value from (-1 = most recent)

        Returns:
            RSI value (0-100)
        """
        rsi_series = self.calculate_rsi(df, period, price)

        if len(rsi_series) == 0:
            return 50.0  # Neutral RSI if no data

        return rsi_series.iloc[index]

    def is_rsi_overbought(self, df: pd.DataFrame, period: int = 14,
                          threshold: float = 70.0) -> bool:
        """
        Check if RSI indicates overbought condition

        Args:
            df: DataFrame with price data
            period: RSI period
            threshold: RSI threshold for overbought (default 70)

        Returns:
            True if RSI > threshold, False otherwise
        """
        rsi = self.get_rsi(df, period)
        return rsi >= threshold

    def is_rsi_oversold(self, df: pd.DataFrame, period: int = 14,
                        threshold: float = 30.0) -> bool:
        """
        Check if RSI indicates oversold condition

        Args:
            df: DataFrame with price data
            period: RSI period
            threshold: RSI threshold for oversold (default 30)

        Returns:
            True if RSI < threshold, False otherwise
        """
        rsi = self.get_rsi(df, period)
        return rsi <= threshold

    # ═══════════════════════════════════════════════════════════════════════════
    # HELPER FUNCTIONS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def is_ema_bullish(self, df: pd.DataFrame, fast_period: int = 20,
                       slow_period: int = 50) -> bool:
        """
        Check if EMAs are in bullish alignment (fast > slow)
        
        Args:
            df: DataFrame with price data
            fast_period: Fast EMA period
            slow_period: Slow EMA period
            
        Returns:
            True if bullish alignment, False otherwise
        """
        ema_fast = self.get_ema(df, fast_period)
        ema_slow = self.get_ema(df, slow_period)
        
        return ema_fast > ema_slow
    
    def is_adx_strong(self, df: pd.DataFrame, period: int = 14,
                     threshold: float = 25.0) -> bool:
        """
        Check if ADX indicates strong trend
        
        Args:
            df: DataFrame with OHLC data
            period: ADX period
            threshold: ADX threshold for strong trend (default 25)
            
        Returns:
            True if ADX > threshold, False otherwise
        """
        adx = self.get_adx(df, period)
        
        return adx >= threshold
    
    def get_trend_direction(self, df: pd.DataFrame, period: int = 14) -> int:
        """
        Get trend direction based on +DI/-DI
        
        Args:
            df: DataFrame with OHLC data
            period: ADX period
            
        Returns:
            +1 for uptrend, -1 for downtrend, 0 for neutral
        """
        plus_di, minus_di = self.get_directional_indicators(df, period)
        
        if plus_di > minus_di:
            return 1
        elif minus_di > plus_di:
            return -1
        else:
            return 0
    
    def calculate_all_indicators(self, df: pd.DataFrame) -> dict:
        """
        Calculate all indicators and return as dictionary

        Args:
            df: DataFrame with OHLC data

        Returns:
            Dictionary with all indicator values
        """
        indicators = {
            'atr_14': self.get_atr(df, 14),
            'ema_20': self.get_ema(df, 20),
            'ema_50': self.get_ema(df, 50),
            'ema_100': self.get_ema(df, 100),
            'ema_separation': self.calculate_ema_separation(df, 20, 50),
            'adx_14': self.get_adx(df, 14),
            'plus_di': 0.0,
            'minus_di': 0.0,
            'rsi_14': self.get_rsi(df, 14),
            'trend_direction': self.get_trend_direction(df, 14),
            'ema_bullish': self.is_ema_bullish(df, 20, 50),
            'adx_strong': self.is_adx_strong(df, 14, 25.0),
            'rsi_overbought': self.is_rsi_overbought(df, 14, 70.0),
            'rsi_oversold': self.is_rsi_oversold(df, 14, 30.0),
        }

        # Get +DI and -DI
        plus_di, minus_di = self.get_directional_indicators(df, 14)
        indicators['plus_di'] = plus_di
        indicators['minus_di'] = minus_di

        return indicators


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING & VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "═"*80)
    print("TECHNICAL INDICATORS - VALIDATION TEST")
    print("═"*80 + "\n")
    
    # Import data loader for testing
    sys.path.insert(0, os.path.join(project_root, 'src'))
    from data_loader import DataLoader
    
    # Load test data
    print("Loading EURUSD data...")
    loader = DataLoader(data_dir="data")
    eurusd_h1 = loader.load_pair_data('EURUSD', 2024)
    eurusd_h1 = loader.resample_to_timeframe(eurusd_h1, 'H1')
    
    # Initialize indicators
    indicators = TechnicalIndicators()
    
    # Test 1: ATR
    print("\n" + "-"*80)
    print("TEST 1: ATR Calculation")
    print("-"*80)
    atr = indicators.get_atr(eurusd_h1, 14)
    print(f"Current ATR(14): {atr:.5f}")
    print(f"ATR as percentage of price: {atr/eurusd_h1['close'].iloc[-1]*100:.2f}%")
    
    # Test 2: EMA
    print("\n" + "-"*80)
    print("TEST 2: EMA Calculation")
    print("-"*80)
    ema_20 = indicators.get_ema(eurusd_h1, 20)
    ema_50 = indicators.get_ema(eurusd_h1, 50)
    ema_sep = indicators.calculate_ema_separation(eurusd_h1, 20, 50)
    ema_bullish = indicators.is_ema_bullish(eurusd_h1, 20, 50)
    
    print(f"Current Price: {eurusd_h1['close'].iloc[-1]:.5f}")
    print(f"EMA(20): {ema_20:.5f}")
    print(f"EMA(50): {ema_50:.5f}")
    print(f"EMA Separation: {ema_sep:.2f}%")
    print(f"EMA Alignment: {'BULLISH' if ema_bullish else 'BEARISH'}")
    
    # Test 3: ADX
    print("\n" + "-"*80)
    print("TEST 3: ADX Calculation")
    print("-"*80)
    adx = indicators.get_adx(eurusd_h1, 14)
    plus_di, minus_di = indicators.get_directional_indicators(eurusd_h1, 14)
    trend_dir = indicators.get_trend_direction(eurusd_h1, 14)
    adx_strong = indicators.is_adx_strong(eurusd_h1, 14, 25.0)
    
    print(f"ADX(14): {adx:.2f}")
    print(f"+DI: {plus_di:.2f}")
    print(f"-DI: {minus_di:.2f}")
    print(f"Trend Direction: {'+1 (UP)' if trend_dir == 1 else '-1 (DOWN)' if trend_dir == -1 else '0 (NEUTRAL)'}")
    print(f"Strong Trend: {'YES' if adx_strong else 'NO'}")

    # Test 4: RSI
    print("\n" + "-"*80)
    print("TEST 4: RSI Calculation")
    print("-"*80)
    rsi = indicators.get_rsi(eurusd_h1, 14)
    rsi_overbought = indicators.is_rsi_overbought(eurusd_h1, 14, 70.0)
    rsi_oversold = indicators.is_rsi_oversold(eurusd_h1, 14, 30.0)

    print(f"RSI(14): {rsi:.2f}")
    print(f"Overbought (>70): {'YES' if rsi_overbought else 'NO'}")
    print(f"Oversold (<30): {'YES' if rsi_oversold else 'NO'}")
    momentum = 'BULLISH' if rsi > 50 else 'BEARISH' if rsi < 50 else 'NEUTRAL'
    print(f"Momentum: {momentum}")

    # Test 5: All indicators
    print("\n" + "-"*80)
    print("TEST 5: All Indicators Summary")
    print("-"*80)
    all_ind = indicators.calculate_all_indicators(eurusd_h1)
    for key, value in all_ind.items():
        if isinstance(value, bool):
            print(f"{key}: {value}")
        elif isinstance(value, int):
            print(f"{key}: {value}")
        else:
            print(f"{key}: {value:.4f}")
    
    print("\n" + "═"*80)
    print("[OK] All indicator tests completed successfully!")
    print("═"*80 + "\n")
