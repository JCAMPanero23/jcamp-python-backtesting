"""
Range Rider Strategy - Mean reversion in ranging markets
Matches MT5 v1.96 logic for support/resistance edge trading

Target Performance: +6.86R (18W/10L trades)
"""

from typing import Dict, Tuple, Optional
import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class RangeRiderStrategy(BaseStrategy):
    """
    Range Rider Strategy implementation.
    
    Strategy Concept:
    - Trade mean reversion at range edges
    - Identify support/resistance levels
    - Enter when price reaches extremes
    - Quick exits at break-even (+0.5R)
    - Max hold time: 48 hours
    
    Entry Requirements:
    - Regime must be RANGING
    - Price at support (buy) or resistance (sell)
    - RSI oversold/overbought confirmation
    - Minimum range width requirement
    """
    
    def __init__(self, config: Dict):
        """
        Initialize Range Rider strategy.
        
        Args:
            config: Dictionary with strategy parameters
        """
        super().__init__(config)
        
        # Load configuration
        self.min_confidence = config.get('range_min_confidence', 60.0)
        self.stop_loss_atr_multiple = config.get('range_stop_loss_atr', 1.0)
        self.break_even_r = config.get('range_break_even_r', 0.5)
        self.max_hold_hours = config.get('range_max_hold_hours', 48)
        self.min_range_width_atr = config.get('range_min_width_atr', 2.0)
        self.edge_proximity_pct = config.get('range_edge_proximity_pct', 5.0)
        
        # RSI thresholds
        self.rsi_oversold = config.get('rsi_oversold', 30.0)
        self.rsi_overbought = config.get('rsi_overbought', 70.0)
        
    def get_strategy_name(self) -> str:
        """Return strategy identifier."""
        return "RANGE_RIDER"
    
    def generate_signal(
        self,
        df: pd.DataFrame,
        current_idx: int,
        csm_data: Dict,
        regime: str
    ) -> Tuple[str, float, Dict]:
        """
        Generate Range Rider signal.
        
        Args:
            df: DataFrame with OHLC and indicators
            current_idx: Current bar index
            csm_data: Currency strength meter data
            regime: Current market regime
            
        Returns:
            Tuple of (signal, confidence, details)
        """
        # Only trade in RANGING regime
        # Handle both string and enum values
        regime_str = str(regime).split('.')[-1] if hasattr(regime, 'value') else regime
        if regime_str != 'RANGING':
            return 'NONE', 0.0, {'filtered_reason': f'{regime_str} regime (need RANGING)'}
        
        # Calculate confidence score
        confidence, component_scores = self.calculate_confidence(
            df, current_idx, csm_data, regime
        )
        
        # Identify support/resistance levels
        support, resistance = self._find_support_resistance(df, current_idx)
        
        if support is None or resistance is None:
            return 'NONE', 0.0, {'filtered_reason': 'No valid range detected'}
        
        # Check range width
        range_width = resistance - support
        atr = self._get_indicator(df, current_idx, 'atr')
        
        if atr is not None and range_width < (atr * self.min_range_width_atr):
            return 'NONE', 0.0, {'filtered_reason': 'Range too narrow'}
        
        # Get current price and RSI
        close = self._get_current_price(df, current_idx)
        rsi = self._get_indicator(df, current_idx, 'rsi')
        
        # Determine signal based on edge proximity
        signal = 'NONE'
        
        # Check if at support (buy signal)
        distance_to_support = abs(close - support) / support * 100.0
        if distance_to_support <= self.edge_proximity_pct:
            if rsi is not None and rsi <= self.rsi_oversold:
                signal = 'BUY'
            elif confidence >= self.min_confidence:
                signal = 'BUY'
        
        # Check if at resistance (sell signal)
        distance_to_resistance = abs(close - resistance) / resistance * 100.0
        if distance_to_resistance <= self.edge_proximity_pct:
            if rsi is not None and rsi >= self.rsi_overbought:
                signal = 'SELL'
            elif confidence >= self.min_confidence:
                signal = 'SELL'
        
        # Build details
        details = {
            'component_scores': component_scores,
            'support': support,
            'resistance': resistance,
            'range_width': range_width,
            'distance_to_support_pct': distance_to_support,
            'distance_to_resistance_pct': distance_to_resistance,
            'rsi': rsi,
            'regime': regime
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
        Calculate Range Rider confidence score.
        
        Component Breakdown:
        1. Range Quality (40 points): Clear support/resistance
        2. Edge Proximity (30 points): How close to edge
        3. Mean Reversion Setup (20 points): RSI confirmation
        4. Regime Strength (10 points): How RANGING is the market
        
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
        max_points = 100.0
        
        # ============================================================
        # COMPONENT 1: RANGE QUALITY (40 points)
        # ============================================================
        range_points, range_details = self._score_range_quality(df, current_idx)
        component_scores['range_quality'] = range_points
        component_scores['range_details'] = range_details
        total_points += range_points
        
        # ============================================================
        # COMPONENT 2: EDGE PROXIMITY (30 points)
        # ============================================================
        edge_points, edge_details = self._score_edge_proximity(df, current_idx)
        component_scores['edge_proximity'] = edge_points
        component_scores['edge_details'] = edge_details
        total_points += edge_points
        
        # ============================================================
        # COMPONENT 3: MEAN REVERSION SETUP (20 points)
        # ============================================================
        reversion_points, rsi_value = self._score_mean_reversion(df, current_idx)
        component_scores['mean_reversion'] = reversion_points
        component_scores['rsi'] = rsi_value
        total_points += reversion_points
        
        # ============================================================
        # COMPONENT 4: REGIME STRENGTH (10 points)
        # ============================================================
        regime_points = self._score_regime_strength(df, current_idx, regime)
        component_scores['regime_strength'] = regime_points
        total_points += regime_points
        
        # Calculate confidence percentage
        confidence_percent = (total_points / max_points) * 100.0
        
        # Add summary
        component_scores['total_points'] = total_points
        component_scores['max_points'] = max_points
        component_scores['confidence_percent'] = confidence_percent
        
        return confidence_percent, component_scores
    
    def _score_range_quality(self, df: pd.DataFrame, current_idx: int) -> Tuple[float, Dict]:
        """
        Score range quality (40 points max).
        
        Checks:
        - Clear support/resistance levels
        - Range width (not too narrow)
        - Number of touches on boundaries
        
        Returns:
            Tuple of (points, details_dict)
        """
        support, resistance = self._find_support_resistance(df, current_idx)
        
        if support is None or resistance is None:
            return 0.0, {'valid_range': False}
        
        range_width = resistance - support
        atr = self._get_indicator(df, current_idx, 'atr')
        
        points = 20.0  # Base points for valid range
        
        # Score based on range width
        if atr is not None:
            width_ratio = range_width / atr
            if width_ratio >= 3.0:
                points = 40.0  # Wide, clear range
            elif width_ratio >= 2.0:
                points = 35.0  # Good range
            elif width_ratio >= 1.5:
                points = 25.0  # Acceptable range
        
        details = {
            'valid_range': True,
            'support': support,
            'resistance': resistance,
            'range_width': range_width,
            'width_ratio': range_width / atr if atr else 0.0
        }
        
        return points, details
    
    def _score_edge_proximity(self, df: pd.DataFrame, current_idx: int) -> Tuple[float, Dict]:
        """
        Score edge proximity (30 points max).
        
        Closer to support/resistance = higher score
        
        Returns:
            Tuple of (points, details_dict)
        """
        support, resistance = self._find_support_resistance(df, current_idx)
        
        if support is None or resistance is None:
            return 0.0, {'at_edge': False}
        
        close = self._get_current_price(df, current_idx)
        
        # Calculate distances
        distance_to_support = abs(close - support) / support * 100.0
        distance_to_resistance = abs(close - resistance) / resistance * 100.0
        
        # Score based on proximity to either edge
        min_distance = min(distance_to_support, distance_to_resistance)
        
        if min_distance <= 2.0:
            points = 30.0  # Very close to edge
        elif min_distance <= 5.0:
            points = 25.0  # Close to edge
        elif min_distance <= 10.0:
            points = 15.0  # Moderate distance
        else:
            points = 5.0  # Far from edges
        
        details = {
            'at_edge': min_distance <= self.edge_proximity_pct,
            'distance_to_support_pct': distance_to_support,
            'distance_to_resistance_pct': distance_to_resistance,
            'min_distance': min_distance
        }
        
        return points, details
    
    def _score_mean_reversion(self, df: pd.DataFrame, current_idx: int) -> Tuple[float, float]:
        """
        Score mean reversion setup (20 points max).
        
        Uses RSI to confirm oversold/overbought conditions:
        - RSI <= 30 or >= 70: 20 points (strong)
        - RSI <= 40 or >= 60: 15 points (moderate)
        - RSI 40-60: 5 points (weak)
        
        Returns:
            Tuple of (points, rsi_value)
        """
        rsi = self._get_indicator(df, current_idx, 'rsi')
        
        if rsi is None:
            return 10.0, 50.0  # Neutral if no RSI
        
        if rsi <= 30.0 or rsi >= 70.0:
            points = 20.0  # Strong oversold/overbought
        elif rsi <= 40.0 or rsi >= 60.0:
            points = 15.0  # Moderate
        else:
            points = 5.0  # Weak setup
        
        return points, rsi
    
    def _score_regime_strength(self, df: pd.DataFrame, current_idx: int, regime: str) -> float:
        """
        Score regime strength (10 points max).
        
        Stronger RANGING regime = higher confidence
        Uses ADX (lower ADX = more ranging)
        
        Returns:
            Points (0-10)
        """
        if regime != 'RANGING':
            return 0.0
        
        adx = self._get_indicator(df, current_idx, 'adx')
        
        if adx is None:
            return 5.0
        
        # Lower ADX = better for range trading
        if adx < 20.0:
            return 10.0  # Strong ranging
        elif adx < 25.0:
            return 7.0  # Good ranging
        elif adx < 30.0:
            return 4.0  # Weak ranging
        else:
            return 0.0  # Not really ranging
    
    def _find_support_resistance(
        self,
        df: pd.DataFrame,
        current_idx: int,
        lookback: int = 48
    ) -> Tuple[Optional[float], Optional[float]]:
        """
        Identify support and resistance levels.
        
        Uses recent swing highs/lows over lookback period
        
        Args:
            df: DataFrame with OHLC data
            current_idx: Current bar index
            lookback: Number of bars to look back
            
        Returns:
            Tuple of (support_level, resistance_level) or (None, None)
        """
        # Ensure we have enough history
        start_idx = max(0, current_idx - lookback)
        
        if start_idx >= current_idx:
            return None, None
        
        # Get recent price data
        recent_data = df.iloc[start_idx:current_idx + 1]
        
        if len(recent_data) < 10:
            return None, None
        
        # Find support (recent lows)
        support = recent_data['low'].min()
        
        # Find resistance (recent highs)
        resistance = recent_data['high'].max()
        
        # Validate range
        if resistance <= support:
            return None, None
        
        # Ensure minimum range width
        range_width = resistance - support
        if range_width < support * 0.001:  # At least 0.1% width
            return None, None
        
        return support, resistance
    
    def get_stop_loss(
        self,
        df: pd.DataFrame,
        current_idx: int,
        signal: str
    ) -> float:
        """
        Calculate stop loss distance.
        
        Uses ATR-based stop loss: 1.0 x ATR
        (Tighter than Trend Rider since we're range trading)
        
        Args:
            df: DataFrame with indicators
            current_idx: Current bar index
            signal: Trade direction
            
        Returns:
            Stop loss distance in price points
        """
        atr = self._get_indicator(df, current_idx, 'atr')
        
        if atr is None:
            # Fallback: 0.3% of price (tighter for range trading)
            close = self._get_current_price(df, current_idx)
            return close * 0.003
        
        return atr * self.stop_loss_atr_multiple
    
    def should_filter_signal(
        self,
        signal: str,
        confidence: float,
        regime: str
    ) -> bool:
        """
        Determine if Range Rider signal should be filtered.
        
        Filtering rules:
        - Must be in RANGING regime
        - Must meet minimum confidence (60%)
        
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
        
        # Range Rider only trades in RANGING regime
        if regime != 'RANGING':
            return True
        
        return False
    
    def should_close_position(
        self,
        entry_price: float,
        current_price: float,
        entry_time: pd.Timestamp,
        current_time: pd.Timestamp,
        signal_direction: str,
        stop_loss_distance: float
    ) -> Tuple[bool, str]:
        """
        Determine if position should be closed.
        
        Range Rider specific rules:
        1. Break-even exit at +0.5R
        2. Max hold time: 48 hours
        
        Args:
            entry_price: Entry price
            current_price: Current price
            entry_time: Entry timestamp
            current_time: Current timestamp
            signal_direction: 'BUY' or 'SELL'
            stop_loss_distance: Original stop loss distance
            
        Returns:
            Tuple of (should_close, reason)
        """
        # Calculate current profit
        if signal_direction == 'BUY':
            profit_distance = current_price - entry_price
        else:  # SELL
            profit_distance = entry_price - current_price
        
        current_r = profit_distance / stop_loss_distance
        
        # Check break-even exit
        if current_r >= self.break_even_r:
            return True, f'Break-even exit at +{current_r:.2f}R'
        
        # Check max hold time
        hours_held = (current_time - entry_time).total_seconds() / 3600.0
        if hours_held >= self.max_hold_hours:
            return True, f'Max hold time reached ({hours_held:.1f} hours)'
        
        return False, ''
