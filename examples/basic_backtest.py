"""
Example 1: Basic Backtesting

This example shows how to run a simple backtest on EURUSD.
"""

from src.engine.backtest_engine import BacktestEngine


def main():
    """Run basic backtest example."""
    
    # Configure backtest
    config = {
        'symbol': 'EURUSD',
        'start_date': '2024-01-01',
        'end_date': '2024-12-31',
        'initial_balance': 10000,
        'strategy': 'both'  # trend_rider, range_rider, or both
    }
    
    print("Starting EURUSD backtest...")
    print(f"Period: {config['start_date']} to {config['end_date']}")
    print()
    
    # Run backtest
    engine = BacktestEngine(config)
    results = engine.run()
    
    # Display results
    print("=" * 60)
    print("BACKTEST RESULTS")
    print("=" * 60)
    print(f"Total R-Multiple:        {results.total_r:+.2f}R")
    print(f"Total Trades:            {results.total_trades}")
    print(f"Win Rate:                {results.win_rate:.2%}")
    print(f"Profit Factor:           {results.profit_factor:.2f}")
    print(f"Max Drawdown:            ${results.max_drawdown:,.2f}")
    print()
    print("Strategy Breakdown:")
    print(f"  Trend Rider:  {results.trend_rider_r:+.2f}R ({results.trend_rider_trades} trades)")
    print(f"  Range Rider:  {results.range_rider_r:+.2f}R ({results.range_rider_trades} trades)")
    print("=" * 60)
    
    # Export results
    results.export_csv('results/backtests/eurusd_2024_basic.csv')
    print()
    print("Results exported to: results/backtests/eurusd_2024_basic.csv")


if __name__ == "__main__":
    main()
