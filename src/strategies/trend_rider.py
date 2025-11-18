"""
Trend Rider Strategy - Confidence-based trend following
Matches MT5 v1.96 logic with 135-point scoring system

Target Performance: +9.18R (60W/61L trades)
"""

from typing import Dict, Tuple
import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class TrendRiderStrategy(BaseStrategy):
    """
    Trend Rider Strategy implementation.
    
    Scoring System (135 points total):
    - EMA Alignment: 50 points (trend consistency)
    - ADX Strength: 25 points (trend power)
    - Momentum: 50 points (directional strength)
    - CSM Support: 10 points (currency strength alignment)
    
    Entry Requirements:
    - Minimum confidence: 65%
    - Minimum CSM differential: 15.0
    - Regime: Must be TRENDING (not filtered in RANGING)
    """
    
    def __init__(self, config: Dict):
        """
        Initialize Trend Rider strategy.
        
        Args:
            config: Dictionary with strategy parameters
        """
        super().__init__(config)
        
        # Load configuration
        self.min_confidence = config.get('trend_min_confidence', 65.0)
        self.min_csm_differential = config.get('trend_min_csm_diff', 15.0)
        self.stop_loss_atr_multiple = config.get('trend_stop_loss_atr', 1.2)
        self.adx_strong_threshold = config.get('adx_strong_trend', 30.0)
        self.ema_separation_min = config.get('ema_separation_min', 0.40)
        
    def get_strategy_name(self) -> str:
        """Return strategy identifier."""
        return "TREND_RIDER"
    
    def generate_signal(
        self,
        df: pd.DataFrame,
        current_idx: int,
        csm_data: Dict,
        regime: str
    ) -> Tuple[str, float, Dict]:
        """
        Generate Trend Rider signal.
        
        Args:
            df: DataFrame with OHLC and indicators
            current_idx: Current bar index
            csm_data: Currency strength meter data
            regime: Current market regime
            
        Returns:
            Tuple of (signal, confidence, details)
        """
        # Calculate confidence score
        confidence, component_scores = self.calculate_confidence(
            df, current_idx, csm_data, regime
        )
        
        # Get CSM differential
        csm_diff = csm_data.get('differential', 0.0)
        
        # Determine signal direction
        signal = 'NONE'
        
        # Check minimum requirements
        if confidence >= self.min_confidence and abs(csm_diff) >= self.min_csm_differential:
            # Determine direction from CSM and EMA alignment
            if csm_diff > 0 and component_scores.get('ema_direction') == 'BULLISH':
                signal = 'BUY'
            elif csm_diff < 0 and component_scores.get('ema_direction') == 'BEARISH':
                signal = 'SELL'
        
        # Filter by regime (adaptive behavior)
        if regime == 'RANGING' and self.config.get('filter_ranging', True):
            signal = 'NONE'
            component_scores['filtered_reason'] = 'RANGING regime'
        
        # Build details
        details = {
            'component_scores': component_scores,
            'csm_differential': csm_diff,
            'regime': regime,
            'min_confidence': self.min_confidence,
            'min_csm_differential': self.min_csm_differential
        }
        
        return signal, confidence, details
    
    def calculate_confidence(
        self,
        df: pd.DataFrame,
        current_idx: int,
        csm_data: Dict,
        regime: str
    ) -> Tuple[float, Dict]:
        """
        Calculate 135-point confidence score.
        
        Component Breakdown:
        1. EMA Alignment (50 points): Trend consistency
        2. ADX Strength (25 points): Trend power
        3. Momentum (50 points): Directional strength
        4. CSM Support (10 points): Currency strength alignment
        
        Args:
            df: DataFrame with indicators
            current_idx: Current bar index
            csm_data: Currency strength data
            regime: Market regime
            
        Returns:
            Tuple of (total_confidence_percent, component_scores)
        """
        component_scores = {}
        total_points = 0.0
        max_points = 135.0
        
        # ============================================================
        # COMPONENT 1: EMA ALIGNMENT (50 points)
        # ============================================================
        ema_points, ema_details = self._score_ema_alignment(df, current_idx)
        component_scores['ema_alignment'] = ema_points
        component_scores['ema_direction'] = ema_details['direction']
        component_scores['ema_separation'] = ema_details['separation_pct']
        total_points += ema_points
        
        # ============================================================
        # COMPONENT 2: ADX STRENGTH (25 points)
        # ============================================================
        adx_points, adx_value = self._score_adx_strength(df, current_idx)
        component_scores['adx_strength'] = adx_points
        component_scores['adx_value'] = adx_value
        total_points += adx_points
        
        # ============================================================
        # COMPONENT 3: MOMENTUM (50 points)
        # ============================================================
        momentum_points, momentum_details = self._score_momentum(df, current_idx)
        component_scores['momentum'] = momentum_points
        component_scores['momentum_direction'] = momentum_details['direction']
        component_scores['momentum_strength'] = momentum_details['strength']
        total_points += momentum_points
        
        # ============================================================
        # COMPONENT 4: CSM SUPPORT (10 points)
        # ============================================================
        csm_points, csm_alignment = self._score_csm_support(csm_data, ema_details['direction'])
        component_scores['csm_support'] = csm_points
        component_scores['csm_alignment'] = csm_alignment
        total_points += csm_points
        
        # Calculate confidence percentage
        confidence_percent = (total_points / max_points) * 100.0
        
        # Add summary
        component_scores['total_points'] = total_points
        component_scores['max_points'] = max_points
        component_scores['confidence_percent'] = confidence_percent
        
        return confidence_percent, component_scores
    
    def _score_ema_alignment(self, df: pd.DataFrame, current_idx: int) -> Tuple[float, Dict]:
        """
        Score EMA alignment (50 points max).
        
        Scoring:
        - Perfect alignment (fast > mid > slow): 50 points
        - Partial alignment: 25-40 points
        - Mixed/choppy: 0-20 points
        - Separation bonus: +10 points if >0.40%
        
        Returns:
            Tuple of (points, details_dict)
        """
        ema_fast = self._get_indicator(df, current_idx, 'ema_fast')
        ema_mid = self._get_indicator(df, current_idx, 'ema_mid')
        ema_slow = self._get_indicator(df, current_idx, 'ema_slow')
        close = self._get_current_price(df, current_idx)
        
        if None in [ema_fast, ema_mid, ema_slow]:
            return 0.0, {'direction': 'NEUTRAL', 'separation_pct': 0.0}
        
        points = 0.0
        direction = 'NEUTRAL'
        
        # Check alignment
        bullish_aligned = (close > ema_fast > ema_mid > ema_slow)
        bearish_aligned = (close < ema_fast < ema_mid < ema_slow)
        
        if bullish_aligned:
            points = 50.0
            direction = 'BULLISH'
        elif bearish_aligned:
            points = 50.0
            direction = 'BEARISH'
        else:
            # Partial alignment
            if close > ema_fast and ema_fast > ema_mid:
                points = 35.0
                direction = 'BULLISH'
            elif close < ema_fast and ema_fast < ema_mid:
                points = 35.0
                direction = 'BEARISH'
            elif close > ema_fast:
                points = 20.0
                direction = 'BULLISH'
            elif close < ema_fast:
                points = 20.0
                direction = 'BEARISH'
        
        # Calculate separation (fast to slow)
        separation_pct = abs((ema_fast - ema_slow) / ema_slow * 100.0)
        
        # Bonus for strong separation
        if separation_pct >= self.ema_separation_min and direction != 'NEUTRAL':
            points = min(50.0, points + 10.0)
        
        details = {
            'direction': direction,
            'separation_pct': separation_pct,
            'bullish_aligned': bullish_aligned,
            'bearish_aligned': bearish_aligned
        }
        
        return points, details
    
    def _score_adx_strength(self, df: pd.DataFrame, current_idx: int) -> Tuple[float, float]:
        """
        Score ADX strength (25 points max).
        
        Scoring:
        - ADX >= 30: 25 points (strong trend)
        - ADX 25-30: 20 points (moderate trend)
        - ADX 20-25: 15 points (weak trend)
        - ADX < 20: 5 points (no trend)
        
        Returns:
            Tuple of (points, adx_value)
        """
        adx = self._get_indicator(df, current_idx, 'adx')
        
        if adx is None:
            return 0.0, 0.0
        
        if adx >= 30.0:
            points = 25.0
        elif adx >= 25.0:
            points = 20.0
        elif adx >= 20.0:
            points = 15.0
        else:
            points = 5.0
        
        return points, adx
    
    def _score_momentum(self, df: pd.DataFrame, current_idx: int) -> Tuple[float, Dict]:
        """
        Score momentum (50 points max).
        
        Uses +DI/-DI and price vs EMAs:
        - Strong directional movement: 50 points
        - Moderate momentum: 30-40 points
        - Weak momentum: 10-25 points
        
        Returns:
            Tuple of (points, details_dict)
        """
        plus_di = self._get_indicator(df, current_idx, 'plus_di')
        minus_di = self._get_indicator(df, current_idx, 'minus_di')
        close = self._get_current_price(df, current_idx)
        ema_fast = self._get_indicator(df, current_idx, 'ema_fast')
        ema_slow = self._get_indicator(df, current_idx, 'ema_slow')
        
        if None in [plus_di, minus_di, ema_fast, ema_slow]:
            return 0.0, {'direction': 'NEUTRAL', 'strength': 0.0}
        
        # Calculate directional strength
        di_diff = abs(plus_di - minus_di)
        
        # Determine direction
        if plus_di > minus_di and close > ema_fast:
            direction = 'BULLISH'
            strength = di_diff
        elif minus_di > plus_di and close < ema_fast:
            direction = 'BEARISH'
            strength = di_diff
        else:
            direction = 'NEUTRAL'
            strength = 0.0
        
        # Score based on strength
        if direction != 'NEUTRAL':
            if di_diff >= 20.0:
                points = 50.0  # Strong momentum
            elif di_diff >= 15.0:
                points = 40.0  # Good momentum
            elif di_diff >= 10.0:
                points = 30.0  # Moderate momentum
            elif di_diff >= 5.0:
                points = 20.0  # Weak momentum
            else:
                points = 10.0  # Very weak
        else:
            points = 0.0
        
        # Bonus for price distance from EMAs
        price_distance_pct = abs((close - ema_slow) / ema_slow * 100.0)
        if price_distance_pct >= 0.5 and direction != 'NEUTRAL':
            points = min(50.0, points + 10.0)
        
        details = {
            'direction': direction,
            'strength': di_diff,
            'plus_di': plus_di,
            'minus_di': minus_di
        }
        
        return points, details
    
    def _score_csm_support(self, csm_data: Dict, ema_direction: str) -> Tuple[float, str]:
        """
        Score CSM support (10 points max).
        
        Checks if currency strength aligns with EMA direction:
        - Perfect alignment: 10 points
        - Weak alignment: 5 points
        - No alignment: 0 points
        
        Returns:
            Tuple of (points, alignment_status)
        """
        csm_diff = csm_data.get('differential', 0.0)
        
        alignment = 'NONE'
        points = 0.0
        
        if ema_direction == 'BULLISH' and csm_diff > 0:
            alignment = 'ALIGNED'
            if csm_diff >= 20.0:
                points = 10.0
            elif csm_diff >= 10.0:
                points = 7.0
            else:
                points = 5.0
        elif ema_direction == 'BEARISH' and csm_diff < 0:
            alignment = 'ALIGNED'
            if csm_diff <= -20.0:
                points = 10.0
            elif csm_diff <= -10.0:
                points = 7.0
            else:
                points = 5.0
        
        return points, alignment
    
    def get_stop_loss(
        self,
        df: pd.DataFrame,
        current_idx: int,
        signal: str
    ) -> float:
        """
        Calculate stop loss distance.
        
        Uses ATR-based stop loss: 1.2 x ATR
        
        Args:
            df: DataFrame with indicators
            current_idx: Current bar index
            signal: Trade direction
            
        Returns:
            Stop loss distance in price points
        """
        atr = self._get_indicator(df, current_idx, 'atr')
        
        if atr is None:
            # Fallback: 0.5% of price
            close = self._get_current_price(df, current_idx)
            return close * 0.005
        
        return atr * self.stop_loss_atr_multiple
    
    def should_filter_signal(
        self,
        signal: str,
        confidence: float,
        regime: str
    ) -> bool:
        """
        Determine if Trend Rider signal should be filtered.
        
        Filtering rules:
        - Must meet minimum confidence (65%)
        - Can be filtered in RANGING regime (if configured)
        
        Args:
            signal: Trade signal
            confidence: Confidence score
            regime: Market regime
            
        Returns:
            True to filter (block), False to allow
        """
        # Use base class confidence check
        if super().should_filter_signal(signal, confidence, regime):
            return True
        
        # Additional Trend Rider filtering
        if regime == 'RANGING' and self.config.get('filter_ranging', True):
            return True
        
        return False
