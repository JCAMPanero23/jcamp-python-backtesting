"""
Example 2: Multi-Pair Comparison

This example runs backtests on multiple pairs and compares results.
"""

from src.engine.backtest_engine import BacktestEngine


def main():
    """Run multi-pair comparison."""
    
    pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'EURJPY', 'AUDUSD']
    
    print("Multi-Pair Backtest Comparison")
    print("=" * 80)
    print()
    
    results = {}
    
    for pair in pairs:
        print(f"Testing {pair}...")
        
        config = {
            'symbol': pair,
            'start_date': '2024-01-01',
            'end_date': '2024-12-31'
        }
        
        engine = BacktestEngine(config)
        results[pair] = engine.run()
        
        print(f"  Complete: {results[pair].total_r:+.2f}R")
        print()
    
    # Display comparison
    print("=" * 80)
    print("COMPARISON RESULTS")
    print("=" * 80)
    print(f"{'Pair':<10} {'Total R':>10} {'Trades':>8} {'Win Rate':>10} {'PF':>8}")
    print("-" * 80)
    
    for pair, result in sorted(results.items(), key=lambda x: x[1].total_r, reverse=True):
        print(f"{pair:<10} {result.total_r:>+9.2f}R {result.total_trades:>7} "
              f"{result.win_rate:>9.1%} {result.profit_factor:>7.2f}")
    
    print("=" * 80)


if __name__ == "__main__":
    main()
