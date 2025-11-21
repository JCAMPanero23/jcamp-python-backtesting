"""
Simple Test Strategy - Fixed SL/TP for Chart Visualization Testing

This strategy is designed for testing and debugging the chart viewer.
It generates predictable trades with fixed risk/reward parameters.

Entry Logic:
- Time-based: Enters whenever no active trade exists
- Alternates between BUY and SELL signals
- Always starts with BUY as first trade

Exit Logic:
- Fixed 5 pip stop loss
- Fixed 10 pip take profit
- Perfect 2:1 reward-to-risk ratio

Author: JCAMP
Purpose: Chart viewer testing and validation
"""

from typing import Dict, Tuple
import pandas as pd
from .base_strategy import BaseStrategy


class SimpleTestStrategy(BaseStrategy):
    """
    Simple test strategy with alternating BUY/SELL and fixed 5 pip SL / 10 pip TP.

    This strategy ignores technical indicators and market conditions.
    It's designed to create clean, predictable trade sequences for testing
    the chart visualization and backtest engine.
    """

    def __init__(self, config: Dict):
        super().__init__(config)

        # Fixed SL/TP in pips
        self.stop_loss_pips = 5
        self.take_profit_pips = 10

        # Convert pips to price (for 4-decimal pairs like EURUSD)
        self.pip_size = 0.0001

        # Track last signal for alternation (starts with None to trigger BUY first)
        self._last_signal = None

        # Simple entry cooldown (not strict 1 hour, just prevent same-bar re-entry)
        self._last_entry_idx = -1

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
        Generate alternating BUY/SELL signals regardless of market conditions.

        Args:
            df: Price data DataFrame
            current_idx: Current bar index
            csm_data: CSM indicator data (not used)
            regime: Market regime (not used)

        Returns:
            Tuple of (signal, confidence, details):
            - signal: 'BUY', 'SELL', or 'NONE'
            - confidence: Fixed at 75.0 for testing
            - details: Debug information dictionary
        """
        # Prevent re-entry on same bar
        if current_idx == self._last_entry_idx:
            return 'NONE', 0.0, {'reason': 'Same bar as last entry'}

        # Alternate signals: None -> BUY -> SELL -> BUY -> SELL ...
        if self._last_signal is None or self._last_signal == 'SELL':
            signal = 'BUY'
        else:
            signal = 'SELL'

        # Update tracking
        self._last_signal = signal
        self._last_entry_idx = current_idx

        # Get current price for logging
        close = self._get_current_price(df, current_idx)

        # Build details for logging
        details = {
            'close': close,
            'signal_sequence': signal,
            'stop_loss_pips': self.stop_loss_pips,
            'take_profit_pips': self.take_profit_pips,
            'regime': regime,
            'strategy': 'SIMPLE_TEST'
        }

        # Fixed confidence for testing
        confidence = 75.0

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
