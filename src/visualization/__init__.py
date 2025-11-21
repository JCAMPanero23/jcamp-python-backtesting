"""
Visualization module for backtest results.
Provides candlestick charts, equity curves, and trade visualization.
"""

from .chart_generator import (
    generate_candlestick_chart,
    generate_equity_curve,
    save_charts_to_html
)

__all__ = [
    'generate_candlestick_chart',
    'generate_equity_curve',
    'save_charts_to_html'
]
