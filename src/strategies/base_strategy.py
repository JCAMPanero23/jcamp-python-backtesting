"""
Base Strategy Class - Abstract interface for all trading strategies
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple
import pandas as pd
import numpy as np


class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    
    All strategies must implement:
    - generate_signal(): Analyze market and return buy/sell/none signal
    - calculate_confidence(): Calculate signal confidence score
    - get_stop_loss(): Calculate stop loss distance
    - get_strategy_name(): Return strategy identifier
    """
    
    def __init__(self, config: Dict):
        """
        Initialize base strategy.
        
        Args:
            config: Dictionary containing strategy parameters
        """
        self.config = config
        self.name = self.get_strategy_name()
        
    @abstractmethod
    def generate_signal(
        self,
        df: pd.DataFrame,
        current_idx: int,
        csm_data: Dict,
        regime: str
    ) -> Tuple[str, float, Dict]:
        """
        Generate trading signal for current bar.
        
        Args:
            df: DataFrame with OHLC and indicators
            current_idx: Current bar index
            csm_data: Currency strength meter data
            regime: Current market regime ('TRENDING', 'RANGING', 'TRANSITIONAL')
            
        Returns:
            Tuple of (signal, confidence, details):
                - signal: 'BUY', 'SELL', or 'NONE'
                - confidence: Confidence score 0-100
                - details: Dictionary with signal breakdown
        """
        pass
    
    @abstractmethod
    def calculate_confidence(
        self,
        df: pd.DataFrame,
        current_idx: int,
        csm_data: Dict,
        regime: str
    ) -> Tuple[float, Dict]:
        """
        Calculate confidence score for potential signal.
        
        Args:
            df: DataFrame with OHLC and indicators
            current_idx: Current bar index
            csm_data: Currency strength meter data
            regime: Current market regime
            
        Returns:
            Tuple of (confidence_score, component_scores):
                - confidence_score: Overall confidence 0-100
                - component_scores: Dictionary with score breakdown
        """
        pass
    
    @abstractmethod
    def get_stop_loss(
        self,
        df: pd.DataFrame,
        current_idx: int,
        signal: str
    ) -> float:
        """
        Calculate stop loss distance in price points.
        
        Args:
            df: DataFrame with OHLC and indicators
            current_idx: Current bar index
            signal: Trade direction ('BUY' or 'SELL')
            
        Returns:
            Stop loss distance in price points
        """
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Return strategy identifier.
        
        Returns:
            Strategy name string
        """
        pass
    
    def should_filter_signal(
        self,
        signal: str,
        confidence: float,
        regime: str
    ) -> bool:
        """
        Determine if signal should be filtered based on conditions.
        
        Args:
            signal: Trade signal ('BUY', 'SELL', or 'NONE')
            confidence: Signal confidence score
            regime: Current market regime
            
        Returns:
            True if signal should be filtered (blocked), False to allow
        """
        # No signal to filter
        if signal == 'NONE':
            return False
            
        # Check minimum confidence
        min_confidence = self.config.get('min_confidence', 60.0)
        if confidence < min_confidence:
            return True
            
        return False
    
    def get_position_size(
        self,
        account_balance: float,
        risk_percent: float,
        stop_loss_distance: float,
        point_value: float
    ) -> float:
        """
        Calculate position size based on risk parameters.
        
        Args:
            account_balance: Current account balance
            risk_percent: Risk percentage per trade (e.g., 2.0 for 2%)
            stop_loss_distance: Stop loss distance in price points
            point_value: Value per point movement
            
        Returns:
            Position size in lots
        """
        risk_amount = account_balance * (risk_percent / 100.0)
        position_size = risk_amount / (stop_loss_distance * point_value)
        
        # Round to 2 decimal places (0.01 lot minimum)
        position_size = round(position_size, 2)
        
        return max(0.01, position_size)  # Minimum 0.01 lot
    
    def format_signal_output(
        self,
        signal: str,
        confidence: float,
        details: Dict
    ) -> Dict:
        """
        Format signal output for logging and tracking.
        
        Args:
            signal: Trade signal
            confidence: Confidence score
            details: Signal details dictionary
            
        Returns:
            Formatted signal dictionary
        """
        return {
            'strategy': self.name,
            'signal': signal,
            'confidence': confidence,
            'details': details,
            'timestamp': pd.Timestamp.now()
        }
    
    def _get_current_price(self, df: pd.DataFrame, current_idx: int) -> float:
        """Helper to get current close price."""
        return df.iloc[current_idx]['close']
    
    def _get_indicator(
        self,
        df: pd.DataFrame,
        current_idx: int,
        indicator_name: str
    ) -> Optional[float]:
        """
        Helper to safely get indicator value.
        
        Args:
            df: DataFrame with indicators
            current_idx: Current bar index
            indicator_name: Name of indicator column
            
        Returns:
            Indicator value or None if not available
        """
        if indicator_name not in df.columns:
            return None
            
        value = df.iloc[current_idx][indicator_name]
        
        # Return None if NaN
        if pd.isna(value):
            return None
            
        return value
