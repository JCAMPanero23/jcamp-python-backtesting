"""
JCAMP Python Backtesting - Strategy Package
Implements Trend Rider and Range Rider strategies matching MT5 v1.96 logic
Also includes SimpleTestStrategy for chart visualization testing
"""

from .base_strategy import BaseStrategy
from .trend_rider import TrendRiderStrategy
from .range_rider import RangeRiderStrategy
from .simple_test import SimpleTestStrategy

__all__ = ['BaseStrategy', 'TrendRiderStrategy', 'RangeRiderStrategy', 'SimpleTestStrategy']
