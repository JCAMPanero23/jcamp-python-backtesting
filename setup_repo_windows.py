#!/usr/bin/env python3
"""
JCAMP Python Backtesting Engine - Repository Setup Script (Windows Compatible)

This script initializes the complete project structure for the
JCAMP Python Backtesting Engine.

Usage:
    python setup_repo_windows.py

Author: JCAMP Trading System
Date: 2025-11-15
"""

import os
import sys
from pathlib import Path


def create_directory_structure():
    """Create all necessary directories for the project."""
    
    print("Creating directory structure...")
    
    directories = [
        # Source code directories
        "src",
        "src/core",
        "src/strategies",
        "src/risk",
        "src/engine",
        "src/optimization",
        "src/api",
        
        # Test directories
        "tests",
        "tests/unit",
        "tests/integration",
        "tests/validation",
        "tests/data",
        
        # Configuration
        "config",
        
        # Data directories
        "data",
        "data/samples",
        "data/EURUSD_sml",
        "data/GBPUSD_sml",
        "data/USDJPY_sml",
        "data/EURJPY",
        "data/AUDUSD_sml",
        "data/USDCHF",
        "data/GBPJPY_sml",
        
        # Results
        "results",
        "results/backtests",
        "results/optimization",
        "results/exports",
        
        # Cache
        "cache",
        
        # Logs
        "logs",
        
        # Documentation
        "docs",
        "docs/images",
        "docs/examples",
        
        # Scripts
        "scripts",
        
        # Examples
        "examples",
        
        # Notebooks (optional)
        "notebooks",
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        print(f"  [OK] Created: {directory}/")
    
    print(f"[SUCCESS] Created {len(directories)} directories")


def create_init_files():
    """Create __init__.py files for Python packages."""
    
    print("\nCreating __init__.py files...")
    
    packages = [
        "src",
        "src/core",
        "src/strategies",
        "src/risk",
        "src/engine",
        "src/optimization",
        "src/api",
        "tests",
        "tests/unit",
        "tests/integration",
        "tests/validation",
    ]
    
    for package in packages:
        init_file = Path(package) / "__init__.py"
        
        # Create appropriate __init__.py content based on package
        if package == "src":
            content = '''"""
JCAMP Python Backtesting Engine

A high-performance backtesting and optimization platform for forex trading strategies.
"""

__version__ = "1.0.0"
__author__ = "JCAMP Trading System"
__license__ = "MIT"

# Package-level imports will go here
'''
        else:
            # Extract package name for docstring
            pkg_name = package.split('/')[-1].replace('_', ' ').title()
            content = f'''"""
{pkg_name} module for JCAMP Backtesting Engine.
"""
'''
        
        # CRITICAL FIX: Use UTF-8 encoding explicitly
        init_file.write_text(content, encoding='utf-8')
        print(f"  [OK] Created: {init_file}")
    
    print(f"[SUCCESS] Created {len(packages)} __init__.py files")


def create_gitkeep_files():
    """Create .gitkeep files in empty directories."""
    
    print("\nCreating .gitkeep files...")
    
    directories_needing_gitkeep = [
        "data",
        "data/samples",
        "data/EURUSD_sml",
        "data/GBPUSD_sml",
        "data/USDJPY_sml",
        "data/EURJPY",
        "data/AUDUSD_sml",
        "data/USDCHF",
        "data/GBPJPY_sml",
        "results",
        "results/backtests",
        "results/optimization",
        "results/exports",
        "cache",
        "logs",
        "tests/data",
    ]
    
    for directory in directories_needing_gitkeep:
        gitkeep_file = Path(directory) / ".gitkeep"
        gitkeep_file.write_text("# This file keeps the directory in git\n", encoding='utf-8')
        print(f"  [OK] Created: {gitkeep_file}")
    
    print(f"[SUCCESS] Created {len(directories_needing_gitkeep)} .gitkeep files")


def create_config_templates():
    """Create template configuration files."""
    
    print("\nCreating configuration templates...")
    
    # Backtest configuration template
    backtest_config = Path("config/backtest_config.json")
    backtest_config_content = """{
  "data": {
    "historical_data_path": "data/",
    "cache_enabled": true,
    "cache_path": "cache/"
  },
  
  "backtest": {
    "initial_balance": 10000,
    "leverage": 50,
    "commission_per_lot": 0,
    "slippage_points": 1
  },
  
  "strategies": {
    "trend_rider": {
      "enabled": true,
      "min_confidence": 65.0,
      "min_csm_differential": 15.0,
      "adx_threshold": 25.0,
      "rsi_buy_max": 65.0,
      "rsi_sell_min": 35.0
    },
    
    "range_rider": {
      "enabled": true,
      "min_confidence": 65,
      "min_quality_score": 25,
      "max_adx": 30.0,
      "boundary_proximity_pips": 15.0
    }
  },
  
  "risk_management": {
    "risk_percent": 2.0,
    "max_positions": 2,
    "daily_loss_limit_r": -6.0,
    "use_advanced_trailing": true
  }
}
"""
    backtest_config.write_text(backtest_config_content, encoding='utf-8')
    print(f"  [OK] Created: {backtest_config}")
    
    # API configuration template
    api_config = Path("config/api_config.json")
    api_config_content = """{
  "server": {
    "host": "localhost",
    "port": 8000,
    "workers": 4,
    "reload": false
  },
  
  "cors": {
    "allow_origins": ["http://localhost:*"],
    "allow_methods": ["GET", "POST"],
    "allow_headers": ["*"]
  },
  
  "logging": {
    "level": "INFO",
    "file": "logs/api_server.log"
  }
}
"""
    api_config.write_text(api_config_content, encoding='utf-8')
    print(f"  [OK] Created: {api_config}")
    
    print("[SUCCESS] Created configuration templates")


def create_readme_for_data():
    """Create README in data directory with instructions."""
    
    print("\nCreating data directory README...")
    
    data_readme = Path("data/README.md")
    
    # CRITICAL FIX: Removed special Unicode characters (arrows)
    readme_content = """# Historical Data Directory

This directory contains historical forex data for backtesting.

## Directory Structure

```
data/
|-- EURUSD_sml/      # EURUSD historical data
|-- GBPUSD_sml/      # GBPUSD historical data
|-- USDJPY_sml/      # USDJPY historical data
|-- EURJPY/          # EURJPY historical data
|-- AUDUSD_sml/      # AUDUSD historical data
|-- USDCHF/          # USDCHF historical data
|-- GBPJPY_sml/      # GBPJPY historical data
```

## Data Format

### CSV Format (M1 Bars)

```
<DATE>    <TIME>     <OPEN>   <HIGH>   <LOW>    <CLOSE>  <TICKVOL> <VOL> <SPREAD>
2024.01.01 00:00:00  1.10450  1.10520  1.10430  1.10500  1000      0     15
2024.01.01 00:01:00  1.10500  1.10580  1.10490  1.10550  1200      0     16
```

### Required Fields

- `DATE`: Trading date (YYYY.MM.DD)
- `TIME`: Bar time (HH:MM:SS)
- `OPEN`: Opening price (5 decimals for most pairs)
- `HIGH`: Highest price in bar
- `LOW`: Lowest price in bar
- `CLOSE`: Closing price
- `TICKVOL`: Tick volume
- `VOL`: Real volume (usually 0 for forex)
- `SPREAD`: Spread in points

## How to Export from MT5

1. Open MT5 terminal
2. Go to Tools > History Center (F2)
3. Select symbol (e.g., EURUSD.sml)
4. Select M1 timeframe
5. Click "Export" button
6. Save as CSV format
7. Place in appropriate directory

## File Naming Convention

- `SYMBOL_TIMEFRAME_STARTDATE_ENDDATE.csv`
- Example: `EURUSD_sml_M1_20240101_20241231.csv`

Or simply:
- `2024_M1.csv` (inside symbol directory)

## Notes

- Data files are gitignored due to size
- Keep at least full year 2024 data for validation
- M1 data will be converted to H1, M15, M5 automatically
- Ensure no gaps in data for accurate backtesting
"""
    
    # CRITICAL FIX: Use UTF-8 encoding
    data_readme.write_text(readme_content, encoding='utf-8')
    print(f"  [OK] Created: {data_readme}")
    
    print("[SUCCESS] Created data directory documentation")


def create_example_scripts():
    """Create example usage scripts."""
    
    print("\nCreating example scripts...")
    
    # Example 1: Basic backtest
    example1 = Path("examples/basic_backtest.py")
    example1_content = '''"""
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
'''
    example1.write_text(example1_content, encoding='utf-8')
    print(f"  [OK] Created: {example1}")
    
    # Example 2: Multi-pair comparison
    example2 = Path("examples/multi_pair_comparison.py")
    example2_content = '''"""
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
'''
    example2.write_text(example2_content, encoding='utf-8')
    print(f"  [OK] Created: {example2}")
    
    print("[SUCCESS] Created example scripts")


def print_next_steps():
    """Print instructions for next steps."""
    
    print("\n" + "=" * 80)
    print("SUCCESS! REPOSITORY SETUP COMPLETE!")
    print("=" * 80)
    
    print("""
Next Steps:

1. INITIALIZE GIT REPOSITORY:
   
   git init
   git add .
   git commit -m "Initial repository structure"

2. CREATE GITHUB REPOSITORY (Optional):
   
   - Go to GitHub and create new repository: jcamp-python-backtesting
   - Link to remote:
     git remote add origin https://github.com/YOUR_USERNAME/jcamp-python-backtesting.git
     git branch -M main
     git push -u origin main

3. SET UP VIRTUAL ENVIRONMENT:
   
   python -m venv venv
   
   # Windows:
   venv\\Scripts\\activate
   
   # Linux/Mac:
   source venv/bin/activate

4. INSTALL DEPENDENCIES:
   
   pip install -r requirements.txt
   
   # Or for development:
   pip install -r requirements-dev.txt

5. ADD HISTORICAL DATA:
   
   - Place your MT5 CSV exports in data/ directories
   - Example: data/EURUSD_sml/2024_M1.csv

6. START DEVELOPMENT:
   
   - Review README.md for project overview
   - Check CONTRIBUTING.md for development guidelines
   - See examples/ for usage examples

Ready to build!
""")


def main():
    """Main setup function."""
    
    print("\n" + "=" * 80)
    print("JCAMP PYTHON BACKTESTING ENGINE - REPOSITORY SETUP (Windows)")
    print("=" * 80)
    print()
    
    try:
        create_directory_structure()
        create_init_files()
        create_gitkeep_files()
        create_config_templates()
        create_readme_for_data()
        create_example_scripts()
        print_next_steps()
        
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] Error during setup: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
