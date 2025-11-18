"""
JCAMP Python Backtesting - Strategy Package
Implements Trend Rider and Range Rider strategies matching MT5 v1.96 logic
"""

from .base_strategy import BaseStrategy
from .trend_rider import TrendRiderStrategy
from .range_rider import RangeRiderStrategy

__all__ = ['BaseStrategy', 'TrendRiderStrategy', 'RangeRiderStrategy']
