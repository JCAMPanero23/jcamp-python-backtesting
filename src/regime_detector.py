"""
═══════════════════════════════════════════════════════════════════════════════
REGIME DETECTOR - Market Condition Classification
═══════════════════════════════════════════════════════════════════════════════
Classifies market conditions as TRENDING, RANGING, or TRANSITIONAL based on
multiple technical indicators. Enhanced with MT5-inspired components.

Classification Method (Competitive Scoring):
- Calculate TRENDING score (sum of component contributions)
- Calculate RANGING score (inverse of components)
- If scores within 5% → TRANSITIONAL
- If trending% >= 55% → TRENDING
- If ranging% >= 55% → RANGING
- Otherwise → TRANSITIONAL

Scoring Components (0-25 points each):
1. ADX Strength (25 points) - Trend strength measurement
2. EMA Alignment (25 points) - Trend direction consistency
3. ATR Volatility (25 points) - Expanding/contracting volatility
4. Price Action (25 points) - Recent bar patterns (higher highs/lows, candle bodies)

Total: 100 points available, split between trending vs ranging
═══════════════════════════════════════════════════════════════════════════════
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
from datetime import datetime
from enum import Enum
import sys
import os

# Add directories to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'config'))
sys.path.insert(0, os.path.join(project_root, 'src'))

from mt5_settings import *
from indicators import TechnicalIndicators

class RegimeType(Enum):
    """Market regime classification"""
    TRENDING = "TRENDING"
    RANGING = "RANGING"
    TRANSITIONAL = "TRANSITIONAL"

class RegimeDetector:
    """
    Detect market regime (Trending vs Ranging) based on technical indicators
    """
    
    def __init__(self,
                 trending_threshold: float = TRENDING_THRESHOLD_PERCENT,
                 ranging_threshold: float = RANGING_THRESHOLD_PERCENT,
                 min_adx_trending: float = MIN_ADX_FOR_TRENDING,
                 min_ema_separation: float = MIN_EMA_SEPARATION,
                 atr_lookback_bars: int = ATR_LOOKBACK_BARS,
                 atr_expanding_threshold: float = ATR_EXPANDING_THRESHOLD,
                 atr_contracting_threshold: float = ATR_CONTRACTING_THRESHOLD,
                 price_action_lookback: int = PRICE_ACTION_LOOKBACK,
                 strong_body_threshold: float = STRONG_BODY_THRESHOLD,
                 weak_body_threshold: float = WEAK_BODY_THRESHOLD,
                 close_scores_threshold: float = CLOSE_SCORES_THRESHOLD,
                 verbose_logging: bool = VERBOSE_REGIME_LOGGING):
        """
        Initialize regime detector

        Args:
            trending_threshold: Score >= this = TRENDING (default 55%)
            ranging_threshold: Score >= this = RANGING (default 55%)
            min_adx_trending: Min ADX for trending regime (default 30.0)
            min_ema_separation: Min EMA separation % (default 0.40%)
            atr_lookback_bars: ATR average lookback period (default 48)
            atr_expanding_threshold: ATR ratio for expanding volatility (default 1.2)
            atr_contracting_threshold: ATR ratio for contracting volatility (default 0.8)
            price_action_lookback: Bars to analyze for price action (default 10)
            strong_body_threshold: Body/range ratio for strong trending (default 0.6)
            weak_body_threshold: Body/range ratio for ranging (default 0.3)
            close_scores_threshold: If scores within this %, mark TRANSITIONAL (default 5.0)
            verbose_logging: Enable detailed component logging (default False)
        """
        self.trending_threshold = trending_threshold
        self.ranging_threshold = ranging_threshold
        self.min_adx_trending = min_adx_trending
        self.min_ema_separation = min_ema_separation
        self.atr_lookback_bars = atr_lookback_bars
        self.atr_expanding_threshold = atr_expanding_threshold
        self.atr_contracting_threshold = atr_contracting_threshold
        self.price_action_lookback = price_action_lookback
        self.strong_body_threshold = strong_body_threshold
        self.weak_body_threshold = weak_body_threshold
        self.close_scores_threshold = close_scores_threshold
        self.verbose_logging = verbose_logging

        # Initialize indicators calculator
        self.indicators = TechnicalIndicators()

        # Regime history
        self.regime_history = []
        self.last_detection_time = None
        
    def detect_regime(self, df: pd.DataFrame, 
                     current_time: Optional[datetime] = None) -> Dict:
        """
        Detect current market regime
        
        Args:
            df: DataFrame with OHLC data (H1 timeframe recommended)
            current_time: Current datetime (for logging)
            
        Returns:
            Dictionary with regime classification and details
        """
        # Calculate all indicators
        indicators = self.indicators.calculate_all_indicators(df)

        # Calculate regime score components
        adx_score = self._score_adx(indicators['adx_14'])
        ema_score = self._score_ema_alignment(indicators)
        atr_score = self._score_atr_volatility(df, indicators)
        price_action_score = self._score_price_action(df)

        # Calculate component contributions to TRENDING
        trending_score = adx_score + ema_score + atr_score + price_action_score

        # Calculate component contributions to RANGING
        # (inverse scoring - components score LOW for ranging)
        ranging_score = (25 - adx_score) + (25 - ema_score) + (25 - atr_score) + (25 - price_action_score)

        # Total available points = 100 (4 components × 25 points each)
        total_score = trending_score + ranging_score

        # Calculate percentages
        if total_score > 0:
            trending_percent = (trending_score / total_score) * 100
            ranging_percent = (ranging_score / total_score) * 100
        else:
            trending_percent = 50.0
            ranging_percent = 50.0

        # Classification with "close scores" buffer
        score_difference = abs(trending_percent - ranging_percent)

        if score_difference < self.close_scores_threshold:
            # Scores too close = TRANSITIONAL
            regime_type = RegimeType.TRANSITIONAL
        elif trending_percent >= self.trending_threshold:
            regime_type = RegimeType.TRENDING
        elif ranging_percent >= self.ranging_threshold:
            regime_type = RegimeType.RANGING
        else:
            regime_type = RegimeType.TRANSITIONAL

        # Store trending percent as primary score for backward compatibility
        regime_score = trending_percent

        # Build result dictionary
        result = {
            'regime': regime_type,
            'score': regime_score,
            'timestamp': current_time if current_time else datetime.now(),
            'components': {
                'adx_score': adx_score,
                'ema_score': ema_score,
                'atr_score': atr_score,
                'price_action_score': price_action_score,
                'trending_score': trending_score,
                'ranging_score': ranging_score,
                'trending_percent': trending_percent,
                'ranging_percent': ranging_percent,
                'score_difference': score_difference
            },
            'indicators': indicators,
            'classification': {
                'is_trending': regime_type == RegimeType.TRENDING,
                'is_ranging': regime_type == RegimeType.RANGING,
                'is_transitional': regime_type == RegimeType.TRANSITIONAL
            }
        }
        
        # Update history
        self.regime_history.append(result)
        self.last_detection_time = result['timestamp']

        # Detailed logging for MT5 validation
        if self.verbose_logging:
            print("\n" + "="*70)
            print("REGIME DETECTION - Component Breakdown")
            print("="*70)
            print(f"Timestamp: {result['timestamp']}")
            print(f"\n--- COMPONENT SCORES (0-25 points each) ---")
            print(f"  ADX Score:          {adx_score:.2f} / 25.0")
            print(f"  EMA Alignment:      {ema_score:.2f} / 25.0")
            print(f"  ATR Volatility:     {atr_score:.2f} / 25.0")
            print(f"  Price Action:       {price_action_score:.2f} / 25.0")
            print(f"\n--- COMPETITIVE SCORING ---")
            print(f"  Trending Score:     {trending_score:.2f} / 100.0 ({trending_percent:.1f}%)")
            print(f"  Ranging Score:      {ranging_score:.2f} / 100.0 ({ranging_percent:.1f}%)")
            print(f"  Score Difference:   {score_difference:.1f}%")
            print(f"\n--- CLASSIFICATION ---")
            print(f"  Regime Type:        {regime_type.value}")
            print(f"  Threshold Check:")
            print(f"    - Trending >= {self.trending_threshold}%: {trending_percent >= self.trending_threshold}")
            print(f"    - Ranging >= {self.ranging_threshold}%: {ranging_percent >= self.ranging_threshold}")
            print(f"    - Close Scores (< {self.close_scores_threshold}%): {score_difference < self.close_scores_threshold}")
            print("="*70 + "\n")

        return result
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SCORING COMPONENTS (Each component: 0-25 points)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _score_adx(self, adx: float) -> float:
        """
        Score ADX strength (0-25 points)
        
        ADX > 30 = Strong trend (25 points)
        ADX 25-30 = Moderate trend (15-25 points)
        ADX < 25 = Weak/no trend (0-15 points)
        
        Args:
            adx: ADX value
            
        Returns:
            Score (0-25)
        """
        if adx >= self.min_adx_trending:
            # Strong trend: Full points
            # ADX 30-50 scores 25 points
            # ADX 50+ scores 25 points (capped)
            score = min(25.0, 25.0 * (adx / self.min_adx_trending))
            return min(score, 25.0)
        else:
            # Weak trend: Proportional points
            # ADX 0 = 0 points
            # ADX 30 = 25 points
            return (adx / self.min_adx_trending) * 25.0
    
    def _score_ema_alignment(self, indicators: dict) -> float:
        """
        Score EMA alignment (0-25 points)
        
        EMA separation > 0.40% = Strong alignment (25 points)
        EMA separation < 0.40% = Weak alignment (0-25 points proportional)
        
        Args:
            indicators: Dictionary with indicator values
            
        Returns:
            Score (0-25)
        """
        ema_separation = indicators['ema_separation']
        
        if ema_separation >= self.min_ema_separation:
            # Strong separation: Full points
            # Separation 0.40%+ = 25 points
            score = 25.0 * (ema_separation / self.min_ema_separation)
            return min(score, 25.0)
        else:
            # Weak separation: Proportional points
            return (ema_separation / self.min_ema_separation) * 25.0
    
    def _score_atr_volatility(self, df: pd.DataFrame, indicators: dict) -> float:
        """
        Score ATR volatility expansion/contraction (0-25 points)

        MT5 Logic (adapted for Python):
        - ATR ratio > 1.2: Expanding volatility = Trending (25 points)
        - ATR ratio < 0.8: Contracting volatility = Ranging (0 points)
        - ATR ratio 0.8-1.2: Neutral (proportional 0-25)

        ATR Ratio = Current ATR / Average ATR (lookback period)

        Args:
            df: DataFrame with price data (needed for ATR history)
            indicators: Dictionary with indicator values

        Returns:
            Score (0-25): Higher = more trending
        """
        current_atr = indicators['atr_14']

        # Calculate ATR series for historical values
        atr_series = self.indicators.calculate_atr(df, 14)

        # Calculate average ATR over lookback period
        if len(atr_series) < self.atr_lookback_bars:
            # Not enough data, use available bars
            lookback = len(atr_series)
        else:
            lookback = self.atr_lookback_bars

        atr_values = atr_series.tail(lookback)
        avg_atr = atr_values.mean()

        if avg_atr == 0 or pd.isna(avg_atr):
            return 12.5  # Neutral if no data

        # Calculate ATR ratio
        atr_ratio = current_atr / avg_atr

        # Score based on ratio
        if atr_ratio >= self.atr_expanding_threshold:
            # Expanding volatility = trending
            # Cap at 25 for ratios > 1.5
            score = 25.0 * (atr_ratio / self.atr_expanding_threshold)
            return min(score, 25.0)
        elif atr_ratio <= self.atr_contracting_threshold:
            # Contracting volatility = ranging
            return 0.0
        else:
            # Neutral zone (0.8-1.2): Linear scale
            # 0.8 → 0 points, 1.2 → 25 points
            range_width = self.atr_expanding_threshold - self.atr_contracting_threshold
            score = ((atr_ratio - self.atr_contracting_threshold) / range_width) * 25.0
            return score
    
    def _score_price_action(self, df: pd.DataFrame) -> float:
        """
        Score recent price action patterns (0-25 points)

        MT5-inspired logic (Python-optimized):
        - Analyzes last N bars for trending vs ranging behavior
        - Trending signals: Higher highs/lows, strong directional candles
        - Ranging signals: Overlapping candles, small bodies, wicks

        Args:
            df: DataFrame with OHLC data

        Returns:
            Score (0-25): Higher = more trending, Lower = more ranging
        """
        lookback = self.price_action_lookback

        if len(df) < lookback + 1:
            return 12.5  # Neutral if insufficient data

        recent_bars = df.tail(lookback)

        # Component 1: Higher Highs / Lower Lows Pattern (10 points)
        highs = recent_bars['high'].values
        lows = recent_bars['low'].values

        # Count higher highs and lower lows
        higher_highs = sum(1 for i in range(1, len(highs)) if highs[i] > highs[i-1])
        lower_lows = sum(1 for i in range(1, len(lows)) if lows[i] < lows[i-1])

        # Directional consistency: either mostly higher highs OR mostly lower lows
        max_direction = max(higher_highs, lower_lows)
        hl_score = (max_direction / (lookback - 1)) * 10.0  # 0-10 points

        # Component 2: Candle Body Strength (10 points)
        bodies = abs(recent_bars['close'] - recent_bars['open'])
        ranges = recent_bars['high'] - recent_bars['low']

        # Avoid division by zero
        body_ratios = bodies / ranges.replace(0, 1)
        avg_body_ratio = body_ratios.mean()

        # Strong bodies (ratio > 0.6) = trending
        # Weak bodies (ratio < 0.3) = ranging
        if avg_body_ratio >= self.strong_body_threshold:
            body_score = 10.0
        elif avg_body_ratio <= self.weak_body_threshold:
            body_score = 0.0
        else:
            body_score = ((avg_body_ratio - self.weak_body_threshold) /
                         (self.strong_body_threshold - self.weak_body_threshold)) * 10.0

        # Component 3: Directional Momentum (5 points)
        closes = recent_bars['close'].values
        price_change = closes[-1] - closes[0]
        price_range = max(highs) - min(lows)

        if price_range > 0:
            momentum_ratio = abs(price_change) / price_range
            momentum_score = momentum_ratio * 5.0
        else:
            momentum_score = 0.0

        # Total score (0-25)
        total_score = hl_score + body_score + momentum_score
        return min(total_score, 25.0)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # REGIME ANALYSIS & STATISTICS
    # ═══════════════════════════════════════════════════════════════════════════
    
    def analyze_period(self, df: pd.DataFrame, 
                      start_date: str, end_date: str,
                      check_interval_hours: int = REGIME_CHECK_HOURS) -> Dict:
        """
        Analyze regime over a date range
        
        Args:
            df: DataFrame with H1 OHLC data
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            check_interval_hours: Hours between regime checks
            
        Returns:
            Dictionary with regime statistics
        """
        # Filter date range
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date) + pd.Timedelta(days=1)
        
        df_period = df[(df.index >= start) & (df.index < end)].copy()
        
        if len(df_period) == 0:
            return {'error': 'No data in date range'}
        
        # Sample at regular intervals
        sample_indices = range(0, len(df_period), check_interval_hours)
        
        regime_counts = {
            RegimeType.TRENDING: 0,
            RegimeType.RANGING: 0,
            RegimeType.TRANSITIONAL: 0
        }
        
        regime_scores = []
        
        for i in sample_indices:
            if i >= len(df_period):
                break
            
            # Get data up to this point
            df_slice = df_period.iloc[:i+48] if i >= 48 else df_period.iloc[:i+1]
            
            if len(df_slice) < 14:  # Need minimum bars for indicators
                continue
            
            # Detect regime
            result = self.detect_regime(df_slice, df_period.index[i])
            
            regime_counts[result['regime']] += 1
            regime_scores.append(result['score'])
        
        total_checks = sum(regime_counts.values())
        
        if total_checks == 0:
            return {'error': 'Not enough data for analysis'}
        
        # Calculate statistics
        stats = {
            'period': f"{start_date} to {end_date}",
            'total_checks': total_checks,
            'regime_distribution': {
                'trending': regime_counts[RegimeType.TRENDING],
                'ranging': regime_counts[RegimeType.RANGING],
                'transitional': regime_counts[RegimeType.TRANSITIONAL]
            },
            'regime_percentages': {
                'trending': regime_counts[RegimeType.TRENDING] / total_checks * 100,
                'ranging': regime_counts[RegimeType.RANGING] / total_checks * 100,
                'transitional': regime_counts[RegimeType.TRANSITIONAL] / total_checks * 100
            },
            'average_score': np.mean(regime_scores),
            'dominant_regime': max(regime_counts, key=regime_counts.get),
            'regime_decisiveness': 100 - (regime_counts[RegimeType.TRANSITIONAL] / total_checks * 100)
        }
        
        return stats
    
    def get_regime_summary(self, result: Dict) -> str:
        """
        Get formatted summary of regime detection result
        
        Args:
            result: Result dictionary from detect_regime()
            
        Returns:
            Formatted string summary
        """
        regime = result['regime']
        score = result['score']
        components = result['components']
        
        summary = f"\n{'='*60}\n"
        summary += f"REGIME DETECTION: {regime.value}\n"
        summary += f"{'='*60}\n"
        summary += f"Overall Score: {score:.1f}%\n"
        summary += f"Timestamp: {result['timestamp']}\n"
        summary += f"{'-'*60}\n"
        summary += f"Component Scores (out of 25):\n"
        summary += f"  ADX Strength:      {components['adx_score']:.1f}\n"
        summary += f"  EMA Alignment:     {components['ema_score']:.1f}\n"
        summary += f"  ATR Volatility:    {components['atr_score']:.1f}\n"
        summary += f"  Price Action:      {components['price_action_score']:.1f}\n"
        summary += f"{'-'*60}\n"
        summary += f"Key Indicators:\n"
        summary += f"  ADX: {result['indicators']['adx_14']:.2f}\n"
        summary += f"  EMA Sep: {result['indicators']['ema_separation']:.2f}%\n"
        summary += f"  ATR: {result['indicators']['atr_14']:.4f}\n"
        summary += f"  +DI: {result['indicators']['plus_di']:.2f}\n"
        summary += f"  -DI: {result['indicators']['minus_di']:.2f}\n"
        summary += f"{'='*60}\n"
        
        return summary


# ═══════════════════════════════════════════════════════════════════════════════
# TESTING & VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "═"*80)
    print("REGIME DETECTOR - VALIDATION TEST")
    print("═"*80 + "\n")
    
    # Import data loader
    from data_loader import DataLoader
    
    # Load test data
    print("Loading EURUSD H1 data...")
    loader = DataLoader(data_dir="data")
    eurusd_m1 = loader.load_pair_data('EURUSD', 2024)
    eurusd_h1 = loader.resample_to_timeframe(eurusd_m1, 'H1')
    
    # Initialize regime detector
    detector = RegimeDetector()
    
    # Test 1: Current regime
    print("\n" + "-"*80)
    print("TEST 1: Current Market Regime")
    print("-"*80)
    result = detector.detect_regime(eurusd_h1)
    print(detector.get_regime_summary(result))
    
    # Test 2: January-March 2024 (Expected: RANGING)
    print("\n" + "-"*80)
    print("TEST 2: Jan-Mar 2024 Period Analysis (Expected: RANGING)")
    print("-"*80)
    stats_ranging = detector.analyze_period(eurusd_h1, '2024-01-01', '2024-03-31')
    print(f"Period: {stats_ranging['period']}")
    print(f"Total Checks: {stats_ranging['total_checks']}")
    print(f"Regime Distribution:")
    print(f"  Trending: {stats_ranging['regime_percentages']['trending']:.1f}%")
    print(f"  Ranging: {stats_ranging['regime_percentages']['ranging']:.1f}%")
    print(f"  Transitional: {stats_ranging['regime_percentages']['transitional']:.1f}%")
    print(f"Dominant Regime: {stats_ranging['dominant_regime'].value}")
    print(f"Regime Decisiveness: {stats_ranging['regime_decisiveness']:.1f}%")
    
    # Test 3: September-November 2024 (Expected: TRENDING)
    print("\n" + "-"*80)
    print("TEST 3: Sep-Nov 2024 Period Analysis (Expected: TRENDING)")
    print("-"*80)
    stats_trending = detector.analyze_period(eurusd_h1, '2024-09-01', '2024-11-30')
    print(f"Period: {stats_trending['period']}")
    print(f"Total Checks: {stats_trending['total_checks']}")
    print(f"Regime Distribution:")
    print(f"  Trending: {stats_trending['regime_percentages']['trending']:.1f}%")
    print(f"  Ranging: {stats_trending['regime_percentages']['ranging']:.1f}%")
    print(f"  Transitional: {stats_trending['regime_percentages']['transitional']:.1f}%")
    print(f"Dominant Regime: {stats_trending['dominant_regime'].value}")
    print(f"Regime Decisiveness: {stats_trending['regime_decisiveness']:.1f}%")
    
    print("\n" + "═"*80)
    print("[OK] All regime detection tests completed!")
    print("═"*80 + "\n")
