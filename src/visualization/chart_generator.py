"""
Chart generation module for backtest visualization.
Creates interactive candlestick charts and equity curves similar to MT5 Tester.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging

logger = logging.getLogger(__name__)


def generate_candlestick_chart(
    df: pd.DataFrame,
    trades: List[Dict],
    indicators: Optional[Dict[str, pd.Series]] = None,
    symbol: str = "EURUSD",
    title_suffix: str = ""
) -> go.Figure:
    """
    Generate interactive candlestick chart with trades overlaid.

    Args:
        df: OHLC DataFrame with DateTimeIndex
        trades: List of trade dictionaries with entry/exit info
        indicators: Optional dict of indicator name -> Series
        symbol: Trading symbol for chart title
        title_suffix: Additional text for title

    Returns:
        Plotly Figure object
    """
    logger.info(f"Generating candlestick chart for {symbol} with {len(trades)} trades")

    # Create figure with secondary y-axis for volume/indicators
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3],
        subplot_titles=(f'{symbol} Price Chart {title_suffix}', 'Indicators')
    )

    # Add candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price',
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ),
        row=1, col=1
    )

    # Add EMA indicators if provided
    if indicators:
        colors = ['#EF5350', '#FF6D00', '#2962FF']  # RED (Fast), ORANGE (Mid), BLUE (Slow)
        color_idx = 0

        for name, series in indicators.items():
            if 'EMA' in name.upper() or 'MA' in name.upper():
                fig.add_trace(
                    go.Scatter(
                        x=series.index,
                        y=series.values,
                        mode='lines',
                        name=name,
                        line=dict(color=colors[color_idx % len(colors)], width=1.5),
                        opacity=0.7
                    ),
                    row=1, col=1
                )
                color_idx += 1

    # Add trade entry/exit markers
    entry_longs_x, entry_longs_y = [], []
    entry_shorts_x, entry_shorts_y = [], []
    exit_wins_x, exit_wins_y = [], []
    exit_losses_x, exit_losses_y = [], []

    for trade in trades:
        entry_time = pd.to_datetime(trade['entry_time'])
        exit_time = pd.to_datetime(trade['exit_time'])
        entry_price = trade['entry_price']
        exit_price = trade['exit_price']
        side = trade['side']
        r_multiple = trade.get('r_multiple', 0)

        # Entry markers
        if side == 'LONG':
            entry_longs_x.append(entry_time)
            entry_longs_y.append(entry_price)
        else:
            entry_shorts_x.append(entry_time)
            entry_shorts_y.append(entry_price)

        # Exit markers
        is_win = r_multiple > 0
        if is_win:
            exit_wins_x.append(exit_time)
            exit_wins_y.append(exit_price)
        else:
            exit_losses_x.append(exit_time)
            exit_losses_y.append(exit_price)

    # Add entry markers
    if entry_longs_x:
        fig.add_trace(
            go.Scatter(
                x=entry_longs_x,
                y=entry_longs_y,
                mode='markers',
                name='Long Entry',
                marker=dict(
                    symbol='triangle-up',
                    size=12,
                    color='#00E676',
                    line=dict(color='white', width=1)
                ),
                hovertemplate='<b>LONG ENTRY</b><br>Price: %{y:.5f}<br>Time: %{x}<extra></extra>'
            ),
            row=1, col=1
        )

    if entry_shorts_x:
        fig.add_trace(
            go.Scatter(
                x=entry_shorts_x,
                y=entry_shorts_y,
                mode='markers',
                name='Short Entry',
                marker=dict(
                    symbol='triangle-down',
                    size=12,
                    color='#FF6D00',
                    line=dict(color='white', width=1)
                ),
                hovertemplate='<b>SHORT ENTRY</b><br>Price: %{y:.5f}<br>Time: %{x}<extra></extra>'
            ),
            row=1, col=1
        )

    # Add exit markers
    if exit_wins_x:
        fig.add_trace(
            go.Scatter(
                x=exit_wins_x,
                y=exit_wins_y,
                mode='markers',
                name='Win Exit',
                marker=dict(
                    symbol='circle',
                    size=10,
                    color='#26a69a',
                    line=dict(color='white', width=1)
                ),
                hovertemplate='<b>WIN</b><br>Price: %{y:.5f}<br>Time: %{x}<extra></extra>'
            ),
            row=1, col=1
        )

    if exit_losses_x:
        fig.add_trace(
            go.Scatter(
                x=exit_losses_x,
                y=exit_losses_y,
                mode='markers',
                name='Loss Exit',
                marker=dict(
                    symbol='x',
                    size=10,
                    color='#ef5350',
                    line=dict(color='white', width=2)
                ),
                hovertemplate='<b>LOSS</b><br>Price: %{y:.5f}<br>Time: %{x}<extra></extra>'
            ),
            row=1, col=1
        )

    # Add RSI or other oscillators to bottom panel if provided
    if indicators:
        for name, series in indicators.items():
            if 'RSI' in name.upper() or 'ADX' in name.upper():
                fig.add_trace(
                    go.Scatter(
                        x=series.index,
                        y=series.values,
                        mode='lines',
                        name=name,
                        line=dict(width=1.5)
                    ),
                    row=2, col=1
                )

        # Add RSI reference lines if RSI present
        if any('RSI' in name.upper() for name in indicators.keys()):
            fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=2, col=1)

    # Update layout
    fig.update_layout(
        title=f'{symbol} Backtest Chart {title_suffix}',
        xaxis_rangeslider_visible=False,
        height=900,
        template='plotly_dark',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Value", row=2, col=1)

    logger.info("Candlestick chart generated successfully")
    return fig


def generate_equity_curve(
    equity_data: List[Dict],
    trades: List[Dict],
    initial_balance: float = 10000.0,
    symbol: str = "EURUSD"
) -> go.Figure:
    """
    Generate equity curve chart showing balance progression over time.

    Args:
        equity_data: List of dicts with 'timestamp' and 'balance' keys
        trades: List of trade dicts for win/loss markers
        initial_balance: Starting account balance
        symbol: Trading symbol for title

    Returns:
        Plotly Figure object
    """
    logger.info(f"Generating equity curve with {len(equity_data)} data points")

    if not equity_data:
        logger.warning("No equity data provided, creating empty chart")
        fig = go.Figure()
        fig.add_annotation(
            text="No equity data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20, color="gray")
        )
        fig.update_layout(template='plotly_dark', height=500)
        return fig

    # Convert to DataFrame for easier processing
    equity_df = pd.DataFrame(equity_data)
    equity_df['timestamp'] = pd.to_datetime(equity_df['timestamp'])
    equity_df = equity_df.set_index('timestamp')

    # Create figure with subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.5, 0.25, 0.25],
        subplot_titles=(
            f'{symbol} Equity Curve',
            'Drawdown',
            'Cumulative R-Multiples'
        )
    )

    # 1. Equity curve
    fig.add_trace(
        go.Scatter(
            x=equity_df.index,
            y=equity_df['balance'],
            mode='lines',
            name='Balance',
            line=dict(color='#2962FF', width=2),
            fill='tonexty',
            fillcolor='rgba(41, 98, 255, 0.1)'
        ),
        row=1, col=1
    )

    # Add starting balance reference line
    fig.add_hline(
        y=initial_balance,
        line_dash="dash",
        line_color="gray",
        opacity=0.5,
        annotation_text="Initial Balance",
        row=1, col=1
    )

    # 2. Drawdown calculation and plot
    running_max = equity_df['balance'].expanding().max()
    drawdown = ((equity_df['balance'] - running_max) / running_max * 100)

    fig.add_trace(
        go.Scatter(
            x=equity_df.index,
            y=drawdown,
            mode='lines',
            name='Drawdown %',
            line=dict(color='#ef5350', width=2),
            fill='tozeroy',
            fillcolor='rgba(239, 83, 80, 0.2)'
        ),
        row=2, col=1
    )

    # 3. Cumulative R-Multiple chart
    if trades:
        trade_df = pd.DataFrame(trades)
        trade_df['exit_time'] = pd.to_datetime(trade_df['exit_time'])
        trade_df = trade_df.sort_values('exit_time')
        trade_df['cumulative_r'] = trade_df['r_multiple'].cumsum()

        fig.add_trace(
            go.Scatter(
                x=trade_df['exit_time'],
                y=trade_df['cumulative_r'],
                mode='lines',
                name='Cumulative R',
                line=dict(color='#00E676', width=2)
            ),
            row=3, col=1
        )

        # Add win/loss markers
        wins = trade_df[trade_df['r_multiple'] > 0]
        losses = trade_df[trade_df['r_multiple'] <= 0]

        if not wins.empty:
            fig.add_trace(
                go.Scatter(
                    x=wins['exit_time'],
                    y=wins['cumulative_r'],
                    mode='markers',
                    name='Wins',
                    marker=dict(symbol='circle', size=6, color='#26a69a'),
                    showlegend=False
                ),
                row=3, col=1
            )

        if not losses.empty:
            fig.add_trace(
                go.Scatter(
                    x=losses['exit_time'],
                    y=losses['cumulative_r'],
                    mode='markers',
                    name='Losses',
                    marker=dict(symbol='x', size=6, color='#ef5350'),
                    showlegend=False
                ),
                row=3, col=1
            )

    # Update layout
    fig.update_layout(
        height=900,
        template='plotly_dark',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        title_text=f"{symbol} Performance Overview"
    )

    fig.update_xaxes(title_text="Date", row=3, col=1)
    fig.update_yaxes(title_text="Balance ($)", row=1, col=1)
    fig.update_yaxes(title_text="Drawdown (%)", row=2, col=1)
    fig.update_yaxes(title_text="Cumulative R", row=3, col=1)

    logger.info("Equity curve generated successfully")
    return fig


def save_charts_to_html(
    candlestick_fig: go.Figure,
    equity_fig: go.Figure,
    output_path: str
) -> str:
    """
    Save both charts to a single HTML file.

    Args:
        candlestick_fig: Candlestick chart figure
        equity_fig: Equity curve figure
        output_path: Path to save HTML file

    Returns:
        Path to saved file
    """
    logger.info(f"Saving charts to {output_path}")

    # Create HTML with both charts
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Backtest Results - JCAMP FX Trading</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                background-color: #1e1e1e;
                color: #cccccc;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
            }}
            h1 {{
                text-align: center;
                color: #007ACC;
                margin-bottom: 30px;
            }}
            .chart-container {{
                margin-bottom: 40px;
                background-color: #252526;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            }}
        </style>
    </head>
    <body>
        <h1>JCAMP Python Backtest Results</h1>

        <div class="chart-container">
            <div id="equity-chart"></div>
        </div>

        <div class="chart-container">
            <div id="candlestick-chart"></div>
        </div>

        <script>
            // Equity curve
            var equityData = {equity_fig.to_json()};
            Plotly.newPlot('equity-chart', equityData.data, equityData.layout);

            // Candlestick chart
            var candlestickData = {candlestick_fig.to_json()};
            Plotly.newPlot('candlestick-chart', candlestickData.data, candlestickData.layout);
        </script>
    </body>
    </html>
    """

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    logger.info(f"Charts saved successfully to {output_path}")
    return output_path


def generate_strategy_comparison_chart(
    strategy_breakdown: Dict[str, Dict]
) -> go.Figure:
    """
    Generate comparison chart for strategy performance.

    Args:
        strategy_breakdown: Dict with strategy names as keys and stats as values

    Returns:
        Plotly Figure object
    """
    strategies = list(strategy_breakdown.keys())

    if not strategies:
        fig = go.Figure()
        fig.add_annotation(
            text="No strategy data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20, color="gray")
        )
        fig.update_layout(template='plotly_dark', height=400)
        return fig

    # Extract metrics
    trades = [strategy_breakdown[s]['trades'] for s in strategies]
    win_rates = [strategy_breakdown[s]['win_rate'] for s in strategies]
    total_r = [strategy_breakdown[s]['total_r'] for s in strategies]

    # Create subplots
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Total Trades', 'Win Rate (%)', 'Total R-Multiple')
    )

    # Trades bar chart
    fig.add_trace(
        go.Bar(x=strategies, y=trades, name='Trades', marker_color='#2962FF'),
        row=1, col=1
    )

    # Win rate bar chart
    fig.add_trace(
        go.Bar(x=strategies, y=win_rates, name='Win Rate', marker_color='#00E676'),
        row=1, col=2
    )

    # Total R bar chart
    colors = ['#00E676' if r > 0 else '#ef5350' for r in total_r]
    fig.add_trace(
        go.Bar(x=strategies, y=total_r, name='Total R', marker_color=colors),
        row=1, col=3
    )

    fig.update_layout(
        height=400,
        template='plotly_dark',
        showlegend=False,
        title_text="Strategy Performance Comparison"
    )

    return fig
