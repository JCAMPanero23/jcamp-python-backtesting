"""
═══════════════════════════════════════════════════════════════════════════════
REGIME DETECTOR - Market Condition Classification
═══════════════════════════════════════════════════════════════════════════════
Classifies market conditions as TRENDING, RANGING, or TRANSITIONAL based on
multiple technical indicators. Matches MT5 v1.96 regime detection logic.

Classification Thresholds:
- TRENDING: Score >= 55% (strong directional movement)
- RANGING: Score <= 40% (sideways consolidation)  
- TRANSITIONAL: Score between 40-55% (unclear regime)

Scoring Components (0-100 points each):
1. ADX Strength (25 points) - Trend strength measurement
2. EMA Alignment (25 points) - Trend direction consistency
3. Directional Movement (25 points) - +DI/-DI dominance
4. Price vs EMA (25 points) - Price position relative to moving averages

Total Score: Sum of components, normalized to 0-100%
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
                 min_ema_separation: float = MIN_EMA_SEPARATION):
        """
        Initialize regime detector
        
        Args:
            trending_threshold: Score >= this = TRENDING (default 55%)
            ranging_threshold: Score <= this = RANGING (default 40%)
            min_adx_trending: Min ADX for trending regime (default 30.0)
            min_ema_separation: Min EMA separation % (default 0.40%)
        """
        self.trending_threshold = trending_threshold
        self.ranging_threshold = ranging_threshold
        self.min_adx_trending = min_adx_trending
        self.min_ema_separation = min_ema_separation
        
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
        di_score = self._score_directional_movement(indicators)
        price_ema_score = self._score_price_vs_ema(df, indicators)
        
        # Total score (0-100 points)
        total_score = adx_score + ema_score + di_score + price_ema_score
        
        # Normalize to percentage (out of 100)
        regime_score = total_score  # Already out of 100
        
        # Classify regime
        if regime_score >= self.trending_threshold:
            regime_type = RegimeType.TRENDING
        elif regime_score <= self.ranging_threshold:
            regime_type = RegimeType.RANGING
        else:
            regime_type = RegimeType.TRANSITIONAL
        
        # Build result dictionary
        result = {
            'regime': regime_type,
            'score': regime_score,
            'timestamp': current_time if current_time else datetime.now(),
            'components': {
                'adx_score': adx_score,
                'ema_score': ema_score,
                'di_score': di_score,
                'price_ema_score': price_ema_score
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
    
    def _score_directional_movement(self, indicators: dict) -> float:
        """
        Score directional movement dominance (0-25 points)
        
        Strong +DI or -DI dominance = Trending (25 points)
        Equal +DI and -DI = Ranging (0 points)
        
        Args:
            indicators: Dictionary with indicator values
            
        Returns:
            Score (0-25)
        """
        plus_di = indicators['plus_di']
        minus_di = indicators['minus_di']
        
        # Calculate dominance ratio
        total_di = plus_di + minus_di
        
        if total_di == 0:
            return 0.0
        
        # Dominance = |+DI - -DI| / (+DI + -DI)
        dominance = abs(plus_di - minus_di) / total_di
        
        # Score: 0 (equal) to 25 (one completely dominates)
        return dominance * 25.0
    
    def _score_price_vs_ema(self, df: pd.DataFrame, indicators: dict) -> float:
        """
        Score price position vs EMAs (0-25 points)
        
        Price far from EMAs = Trending (25 points)
        Price near EMAs = Ranging (0 points)
        
        Args:
            df: DataFrame with price data
            indicators: Dictionary with indicator values
            
        Returns:
            Score (0-25)
        """
        current_price = df['close'].iloc[-1]
        ema_20 = indicators['ema_20']
        ema_50 = indicators['ema_50']
        
        # Calculate distance from EMAs as percentage
        dist_20 = abs(current_price - ema_20) / current_price * 100
        dist_50 = abs(current_price - ema_50) / current_price * 100
        
        # Average distance
        avg_distance = (dist_20 + dist_50) / 2.0
        
        # Score: 0% distance = 0 points, 2%+ distance = 25 points
        # Linear scale from 0-2%
        score = min(25.0, (avg_distance / 2.0) * 25.0)
        
        return score
    
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
        summary += f"  Directional Move:  {components['di_score']:.1f}\n"
        summary += f"  Price vs EMA:      {components['price_ema_score']:.1f}\n"
        summary += f"{'-'*60}\n"
        summary += f"Key Indicators:\n"
        summary += f"  ADX: {result['indicators']['adx_14']:.2f}\n"
        summary += f"  EMA Sep: {result['indicators']['ema_separation']:.2f}%\n"
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
