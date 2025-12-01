"""
Simple Test Strategy - EMA Crossover with H1 Confirmation

This strategy is designed for testing and debugging the chart viewer.
It generates trades with fixed risk/reward parameters based on EMA crossovers.

Entry Logic:
- M15 EMA 20 crosses M15 EMA 50
- H1 EMA 20/50 must align in the same direction for confirmation
- BUY: M15 fast crosses above mid + H1 fast > H1 mid
- SELL: M15 fast crosses below mid + H1 fast < H1 mid

Exit Logic:
- Fixed 5 pip stop loss
- Fixed 10 pip take profit
- Perfect 2:1 reward-to-risk ratio

Author: JCAMP
Purpose: Chart viewer testing and EMA crossover validation
"""

from typing import Dict, Tuple
import pandas as pd
from .base_strategy import BaseStrategy


class SimpleTestStrategy(BaseStrategy):
    """
    Simple test strategy with EMA crossover + H1 confirmation and fixed 5 pip SL / 10 pip TP.

    Entry Conditions:
    - M15 EMA 20 crosses M15 EMA 50
    - H1 EMA 20/50 alignment confirms direction
    - Fixed risk/reward: 5 pip SL, 10 pip TP (2:1 R:R)

    This strategy uses actual technical indicators but maintains fixed risk parameters
    for consistent testing of the chart visualization and backtest engine.
    """

    def __init__(self, config: Dict):
        super().__init__(config)

        # Fixed SL/TP in pips
        self.stop_loss_pips = 5
        self.take_profit_pips = 10

        # Convert pips to price (for 4-decimal pairs like EURUSD)
        self.pip_size = 0.0001

    def get_strategy_name(self) -> str:
        """Return strategy identifier."""
        return "SIMPLE_TEST"

    def generate_signal(
        self,
        df: pd.DataFrame,
        current_idx: int,
        csm_data: Dict,
        regime: str
    ) -> Tuple[str, float, Dict]:
        """
        Generate signals based on M15 EMA crossover with H1 confirmation.

        Entry Conditions:
        - M15 EMA 20 crosses M15 EMA 50
        - H1 EMA 20/50 must align in same direction
        - BUY: M15 fast crosses above mid + H1 fast > H1 mid
        - SELL: M15 fast crosses below mid + H1 fast < H1 mid

        Args:
            df: Price data DataFrame with indicators
            current_idx: Current bar index
            csm_data: CSM indicator data
            regime: Market regime

        Returns:
            Tuple of (signal, confidence, details):
            - signal: 'BUY', 'SELL', or 'NONE'
            - confidence: Based on crossover strength (60-90%)
            - details: Crossover metrics and confirmation status
        """
        # Need at least 2 bars for crossover detection
        if current_idx < 1:
            return 'NONE', 0.0, {'reason': 'Insufficient bars (need at least 2)'}

        # Get M15 EMA values (current and previous)
        curr_fast = self._get_indicator(df, current_idx, 'ema_fast')  # EMA 20
        curr_mid = self._get_indicator(df, current_idx, 'ema_mid')   # EMA 50
        prev_fast = self._get_indicator(df, current_idx - 1, 'ema_fast')
        prev_mid = self._get_indicator(df, current_idx - 1, 'ema_mid')

        # Validate all M15 indicators exist
        if None in [curr_fast, curr_mid, prev_fast, prev_mid]:
            return 'NONE', 0.0, {'reason': 'Missing M15 EMAs'}

        # Detect M15 crossover
        signal = 'NONE'
        if prev_fast < prev_mid and curr_fast >= curr_mid:
            signal = 'BUY'  # Bullish crossover
        elif prev_fast > prev_mid and curr_fast <= curr_mid:
            signal = 'SELL'  # Bearish crossover

        if signal == 'NONE':
            return signal, 0.0, {'reason': 'No crossover detected'}

        # H1 EMA Confirmation
        h1_fast = self._get_indicator(df, current_idx, 'ema_20_h1')
        h1_mid = self._get_indicator(df, current_idx, 'ema_50_h1')

        if h1_fast is None or h1_mid is None:
            return 'NONE', 0.0, {
                'reason': 'Missing H1 EMAs',
                'm15_signal': signal,
                'note': 'H1 confirmation required but EMAs not available'
            }

        # Check H1 alignment
        h1_aligned = (h1_fast > h1_mid and signal == 'BUY') or \
                     (h1_fast < h1_mid and signal == 'SELL')

        if not h1_aligned:
            return 'NONE', 0.0, {
                'reason': 'H1 EMA misalignment',
                'm15_signal': signal,
                'h1_fast': float(h1_fast),
                'h1_mid': float(h1_mid),
                'h1_relationship': 'fast > mid' if h1_fast > h1_mid else 'fast < mid',
                'required': 'fast > mid for BUY' if signal == 'BUY' else 'fast < mid for SELL'
            }

        # Calculate confidence based on crossover strength
        crossover_distance = abs(curr_fast - curr_mid)
        atr = self._get_indicator(df, current_idx, 'atr')

        if atr and atr > 0:
            # Confidence: 60% base + up to 30% based on crossover strength relative to ATR
            # Stronger crossovers (larger distance relative to ATR) get higher confidence
            strength_factor = min(1.0, crossover_distance / (atr * 0.5))  # 0.5 ATR = 100% factor
            confidence = min(90.0, 60.0 + (strength_factor * 30.0))
        else:
            confidence = 75.0  # Default mid-range confidence

        # Get current price for logging
        close = self._get_current_price(df, current_idx)

        # Build details for logging
        details = {
            'signal_type': 'EMA_CROSSOVER',
            'close': float(close),
            'm15_fast': float(curr_fast),
            'm15_mid': float(curr_mid),
            'prev_fast': float(prev_fast),
            'prev_mid': float(prev_mid),
            'h1_fast': float(h1_fast),
            'h1_mid': float(h1_mid),
            'h1_aligned': h1_aligned,
            'crossover_distance': float(crossover_distance),
            'atr': float(atr) if atr else None,
            'crossover_strength_pct': float((crossover_distance / atr * 100)) if atr and atr > 0 else None,
            'regime': regime,
            'strategy': 'SIMPLE_TEST',
            'stop_loss_pips': self.stop_loss_pips,
            'take_profit_pips': self.take_profit_pips
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
        Return fixed confidence score for testing.

        Returns:
            Tuple of (confidence_percent, component_scores):
            - confidence_percent: 75.0 (fixed)
            - component_scores: Simple breakdown
        """
        confidence = 75.0
        component_scores = {
            'total_points': 75.0,
            'max_points': 100.0,
            'confidence_percent': 75.0,
            'note': 'Fixed confidence for testing'
        }
        return confidence, component_scores

    def get_stop_loss(
        self,
        df: pd.DataFrame,
        current_idx: int,
        signal: str
    ) -> float:
        """
        Return fixed 5 pip stop loss distance.

        Args:
            df: Price data (not used)
            current_idx: Current bar index (not used)
            signal: Trade direction (not used)

        Returns:
            Stop loss distance in price points (0.0005 for EURUSD)
        """
        return self.stop_loss_pips * self.pip_size  # 5 pips = 0.0005

    def get_take_profit(
        self,
        df: pd.DataFrame,
        current_idx: int,
        signal: str
    ) -> float:
        """
        Return fixed 10 pip take profit distance.

        This is a custom method not in BaseStrategy.
        BacktestEngine needs to support calling this method.

        Args:
            df: Price data (not used)
            current_idx: Current bar index (not used)
            signal: Trade direction (not used)

        Returns:
            Take profit distance in price points (0.001 for EURUSD)
        """
        return self.take_profit_pips * self.pip_size  # 10 pips = 0.001

    def should_filter_signal(
        self,
        signal: str,
        confidence: float,
        regime: str
    ) -> bool:
        """
        Never filter signals in test strategy.

        Returns:
            False (always allow signals through)
        """
        return False  # Never filter
