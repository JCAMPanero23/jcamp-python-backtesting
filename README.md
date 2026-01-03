# 🚀 JCAMP Python Backtesting Engine

**Advanced Forex Trading Strategy Backtesting & Optimization Platform**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 **Overview**

This Python-based backtesting engine replicates and extends the functionality of the JCAMP Forex Trading System (MT5 EA), providing:

- ⚡ **30-600x faster backtesting** than MT5 Strategy Tester
- 🎯 **Advanced parameter optimization** (Grid Search, Random Search, Walk-Forward)
- 📊 **Professional-grade analytics** beyond MT5 capabilities
- 🔄 **Multi-pair testing** with one-click comparison
- 🤖 **ML-ready foundation** for future AI integration
- 🌐 **REST API** for seamless C# Monitor App integration

---

## 🎯 **Key Features**

### **Core Backtesting Engine**
- Complete replication of MT5 v1.96 trading logic
- Trend Rider strategy implementation
- Range Rider strategy implementation
- Dynamic regime detection (Trending/Ranging/Transitional)
- Advanced asymmetric trailing stop system
- Multi-layer risk management

### **Technical Indicators**
- Currency Strength Meter (CSM) - 8 currencies, 15 pairs
- EMA (Fast/Slow alignment)
- ADX (Trend strength)
- RSI (Momentum with extended thresholds)
- ATR (Volatility-based stops)
- Support/Resistance detection

### **Performance Analytics**
- R-multiple tracking
- Win rate by strategy
- Profit factor calculation
- Drawdown analysis ($ and R)
- Sharpe ratio
- Monthly/yearly breakdowns
- Trade-by-trade analysis

### **Optimization Tools**
- Grid search (exhaustive parameter testing)
- Random search (large parameter spaces)
- Walk-forward analysis (robustness validation)
- Parallel processing for speed
- Results export (JSON, CSV, HTML)

### **API Server**
- FastAPI REST endpoints
- Real-time backtest progress tracking
- JSON response format
- Swagger/OpenAPI documentation
- CORS support for C# integration

---

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────┐
│           JCAMP PYTHON BACKTESTING ENGINE           │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Core Processing:                                   │
│  ├─ Data Loader (CSV/Parquet)                      │
│  ├─ Timeframe Converter (M1→H1/M15/M5)             │
│  ├─ Technical Indicators (EMA/ADX/RSI/ATR)         │
│  ├─ CSM Calculator (Currency Strength)             │
│  └─ Regime Detector (Trending/Ranging)             │
│                                                     │
│  Strategy Engines:                                  │
│  ├─ Trend Rider (EMA alignment + CSM)              │
│  ├─ Range Rider (Boundary detection)               │
│  └─ Impulse Pullback (Optional)                    │
│                                                     │
│  Risk & Position Management:                        │
│  ├─ Position Sizing (2% risk)                      │
│  ├─ Stop Loss/Take Profit (ATR-based)              │
│  ├─ Advanced Trailing Stops (3-phase asymmetric)   │
│  ├─ Daily Loss Limits (-6R)                        │
│  └─ Multi-position Coordination                    │
│                                                     │
│  Analytics & Export:                                │
│  ├─ Performance Analyzer (R-multiple, metrics)     │
│  ├─ Trade Logger (detailed logs)                   │
│  ├─ Equity Curve Generator                         │
│  └─ Results Exporter (JSON/CSV/HTML)               │
│                                                     │
│  Optimization:                                      │
│  ├─ Parameter Grid Search                          │
│  ├─ Walk-Forward Analysis                          │
│  └─ Multi-pair Comparison                          │
│                                                     │
│  API Server:                                        │
│  ├─ FastAPI REST Endpoints                         │
│  ├─ Background Task Processing                     │
│  ├─ Progress Tracking                              │
│  └─ C# Monitor App Integration                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🔗 **Symbolic Link Setup: CSMMonitor Integration**

### **Overview**

The `CSMMonitor` folder is a **symbolic link** to the C# WPF monitoring application repository. This allows seamless cross-project development between the Python backtesting engine and the C# monitoring interface.

### **C# Project Location**

**Project Directory:**
```
D:\JcampFxTrading\CSMMonitor
```

**Previous Location (OneDrive - deprecated):**
```
C:\Users\jcamp\OneDrive\Documents\Visual Studio 2022\Projects\CSMMonitor
```

**Git Repository:**
```
https://github.com/JCAMPanero23/CSMMonitor
```

### **Access Control**

**Read/Write Permissions:**
- Full read/write access to all files in the CSMMonitor directory
- Both Python and C# projects now reside in `D:\JcampFxTrading`
- Git operations (commit, push, pull) should be performed within the CSMMonitor directory

**Important Notes:**
- The C# project was migrated from OneDrive to avoid file sync conflicts
- Both projects now share the same parent directory for easier management
- Visual Studio and Claude Code can both access files without OneDrive interference

### **Git Workflow for CSMMonitor**

When working on the C# monitoring application through this project:

```bash
# Navigate to CSMMonitor directory
cd CSMMonitor

# Check status
git status

# Stage changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main
```

### **Integration Benefits**

- **Unified Workspace:** Work on both Python and C# projects in one location
- **Version Control:** Maintain separate git histories for each project
- **API Development:** Easily test API endpoints from C# while developing in Python
- **Rapid Iteration:** Make changes to the C# UI and see immediate results with Python backend

### **Caution**

⚠️ **Warning:** Deleting or modifying the symbolic link does NOT delete the original C# project. However, be careful when using file operations that might follow symbolic links unexpectedly.

---

## 📦 **Installation**

### **Prerequisites**
- Python 3.10 or higher
- pip package manager
- Git (for version control)

### **Quick Start**

```bash
# Clone the repository
git clone https://github.com/yourusername/jcamp-python-backtesting.git
cd jcamp-python-backtesting

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python scripts/verify_installation.py
```

### **Development Installation**

```bash
# Install with development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests to verify setup
pytest tests/
```

---

## 🚀 **Quick Start Guide**

### **1. Prepare Historical Data**

Place your MT5 exported CSV files in the data directory:

```
data/
├── EURUSD_sml/
│   └── 2024_M1.csv
├── GBPUSD_sml/
│   └── 2024_M1.csv
└── [other pairs...]
```

**Expected CSV Format:**
```
<DATE>    <TIME>     <OPEN>   <HIGH>   <LOW>    <CLOSE>  <TICKVOL> <VOL> <SPREAD>
2024.01.01 00:00:00  1.10450  1.10520  1.10430  1.10500  1000      0     15
```

### **2. Run a Simple Backtest**

```python
from src.engine.backtest_engine import BacktestEngine
from src.strategies.trend_rider import TrendRiderStrategy

# Configure backtest
config = {
    'symbol': 'EURUSD',
    'start_date': '2024-01-01',
    'end_date': '2024-12-31',
    'initial_balance': 10000,
    'strategy': 'both'  # trend_rider, range_rider, or both
}

# Run backtest
engine = BacktestEngine(config)
results = engine.run()

# Display results
print(f"Total R-Multiple: {results.total_r:.2f}")
print(f"Win Rate: {results.win_rate:.2%}")
print(f"Total Trades: {results.total_trades}")
```

### **3. Start API Server**

```bash
# Start FastAPI server
python scripts/run_server.py

# Server runs on http://localhost:8000
# API documentation: http://localhost:8000/docs
```

### **4. Run Parameter Optimization**

```python
from src.optimization.parameter_optimizer import ParameterOptimizer

# Define parameter ranges
param_ranges = {
    'min_confidence': [60, 65, 70, 75],
    'min_csm_diff': [10, 12.5, 15, 17.5, 20],
    'adx_threshold': [25, 28, 30, 32, 35]
}

# Run optimization
optimizer = ParameterOptimizer()
results = optimizer.grid_search(param_ranges, metric='total_r')

# Display best parameters
print("Best Parameters:")
for param, value in results.best_params.items():
    print(f"  {param}: {value}")
print(f"Best R-Multiple: {results.best_score:.2f}")
```

---

## 📖 **Usage Examples**

### **Example 1: Basic Backtest**

```python
# examples/basic_backtest.py
from src.engine.backtest_engine import BacktestEngine

# Simple EURUSD backtest
engine = BacktestEngine({
    'symbol': 'EURUSD',
    'start_date': '2024-01-01',
    'end_date': '2024-12-31'
})

results = engine.run()
results.print_summary()
results.export_csv('results/eurusd_2024.csv')
```

### **Example 2: Multi-Pair Comparison**

```python
# examples/multi_pair_comparison.py
from src.engine.backtest_engine import BacktestEngine

pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'EURJPY', 'AUDUSD']
results = {}

for pair in pairs:
    engine = BacktestEngine({
        'symbol': pair,
        'start_date': '2024-01-01',
        'end_date': '2024-12-31'
    })
    results[pair] = engine.run()

# Compare results
for pair, result in results.items():
    print(f"{pair}: {result.total_r:.2f}R ({result.total_trades} trades)")
```

### **Example 3: Walk-Forward Analysis**

```python
# examples/walk_forward.py
from src.optimization.walk_forward import WalkForwardAnalyzer

analyzer = WalkForwardAnalyzer()
results = analyzer.run(
    symbol='EURUSD',
    periods=5,  # 5 time periods
    optimize_metric='total_r'
)

results.plot_degradation()
results.export_report('results/walk_forward_report.html')
```

---

## 🔧 **Configuration**

### **Backtest Configuration**

Edit `config/backtest_config.json`:

```json
{
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
```

### **API Server Configuration**

Edit `config/api_config.json`:

```json
{
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
```

---

## 🧪 **Testing**

### **Run All Tests**

```bash
# Run full test suite
pytest

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_indicators.py

# Run with verbose output
pytest -v
```

### **Test Categories**

```bash
# Unit tests (fast)
pytest tests/unit/

# Integration tests (slower)
pytest tests/integration/

# Validation tests (compare to MT5)
pytest tests/validation/
```

---

## 📊 **Performance Benchmarks**

### **Speed Comparison (EURUSD Full Year 2024)**

| Method | Time | Speedup |
|--------|------|---------|
| MT5 Strategy Tester | 15-30 min | 1x |
| Python (vectorized) | 3-10 sec | **90-600x** |
| Python (cached) | 1-2 sec | **450-1800x** |

### **Optimization Comparison (100 Parameter Combinations)**

| Method | Time | Tests/Hour |
|--------|------|------------|
| MT5 Manual | 25-50 hours | 2-4 |
| Python Grid Search | 5-15 min | **400-1200** |

---

## 🔌 **API Documentation**

### **Endpoints**

**POST /backtest/run**
```json
{
  "symbol": "EURUSD",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "strategy": "both",
  "parameters": {
    "min_confidence": 65.0,
    "min_csm_diff": 15.0
  }
}
```

**Response:**
```json
{
  "task_id": "abc123",
  "status": "running"
}
```

**GET /backtest/status/{task_id}**

**Response:**
```json
{
  "task_id": "abc123",
  "status": "complete",
  "progress": 100,
  "message": "Backtest completed successfully"
}
```

**GET /backtest/results/{task_id}**

**Response:**
```json
{
  "total_r": 18.53,
  "win_rate": 0.5185,
  "total_trades": 162,
  "trend_rider": {
    "trades": 124,
    "win_rate": 0.492,
    "total_r": 11.95
  },
  "range_rider": {
    "trades": 37,
    "win_rate": 0.622,
    "total_r": 6.58
  },
  "trades": [...],
  "equity_curve": [...]
}
```

### **Multi-Pair Backtest**

**Endpoint:** `POST /api/v1/backtest/multi-pair`

Test multiple currency pairs with selected strategies simultaneously.

**Request Body:**
```json
{
  "pairs": ["EURUSD", "GBPUSD", "USDJPY"],
  "strategies": ["trend_rider", "range_rider"],
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "timeframe": "M15",
  "config": {
    "initial_balance": 10000.0,
    "risk_percent": 2.0,
    "max_concurrent_positions": 2,
    "min_confidence": 50.0,
    "take_profit_r": 2.0
  }
}
```

**Response:**
```json
{
  "task_id": "abc123-def456",
  "status": "queued"
}
```

**Get Results:** `GET /api/v1/backtest/multi-pair/{task_id}/results`

**Response includes:**
- Aggregate performance metrics across all pairs
- Trades merged chronologically
- Breakdown by strategy (`strategy_breakdown`)
- Breakdown by pair (`pair_breakdown`)
- Equity curve with cumulative R

Full API documentation: http://localhost:8000/docs

---

## 🤝 **Integration with C# Monitor App**

The Python backtesting engine integrates seamlessly with the JCAMP C# Monitor App via REST API.

### **C# Integration Example**

```csharp
// In your C# Monitor App
var backtestService = new BacktestService("http://localhost:8000");

var config = new BacktestConfig
{
    Symbol = "EURUSD",
    StartDate = "2024-01-01",
    EndDate = "2024-12-31",
    Strategy = "both"
};

string taskId = await backtestService.StartBacktest(config);

while (true)
{
    var status = await backtestService.GetStatus(taskId);
    if (status.IsComplete) break;
    
    UpdateProgressBar(status.Progress);
    await Task.Delay(1000);
}

var results = await backtestService.GetResults(taskId);
DisplayResults(results);
```

---

## 📁 **Project Structure**

```
jcamp-python-backtesting/
├── src/
│   ├── backtest_engine.py      # Main backtesting engine
│   ├── data_loader.py          # Data loading & timeframe conversion
│   ├── csm_calculator.py       # Currency Strength Meter
│   ├── indicators.py           # EMA, ADX, RSI, ATR
│   ├── regime_detector.py      # Trending/Ranging detection
│   ├── position_manager.py     # Position tracking
│   ├── performance_tracker.py  # Analytics & metrics
│   ├── strategies/             # Trading strategies
│   │   ├── trend_rider.py
│   │   └── range_rider.py
│   ├── visualization/          # Chart generation
│   │   └── chart_generator.py
│   └── api/                    # REST API server
│       ├── main.py
│       ├── models/
│       ├── routes/
│       └── services/
├── tests/                      # Test suite
│   ├── test_phase1.py          # Data loader & CSM tests
│   ├── test_phase2.py          # Indicators & regime tests
│   ├── test_phase3.py          # Strategy tests
│   ├── test_phase4.py          # Backtest engine tests
│   ├── samples/                # Sample data files
│   └── outputs/                # Test outputs (gitignored)
├── docs/
│   ├── current/                # Current documentation
│   └── archive/                # Historical/archived docs
├── charts/                     # Generated charts (gitignored)
├── data/                       # Historical data (gitignored)
├── scripts/
│   └── start_api_server.py     # API server launcher
├── START_ALL.bat               # Launch API + C# app
├── START_API_SERVER.bat        # Launch API only
├── START_MONITOR_APP.bat       # Launch C# app only
├── STATUS.md                   # Project status tracking
└── CSMMonitor/                 # Symbolic link to C# app
```

---

## 🗺️ **Roadmap**

### **Version 1.0 (Current - Nov 21, 2025)**
- ✅ Core backtesting engine
- ✅ Trend Rider & Range Rider strategies
- ✅ Basic parameter optimization
- ✅ REST API server with chart visualization
- ✅ CSV data loading
- ✅ Windows compatibility (Unicode fix)
- ✅ Batch launcher scripts (.bat files)

### **Version 1.1 (Next)**
- ⏳ Walk-forward analysis
- ⏳ Monte Carlo simulation
- ⏳ Enhanced visualizations
- ⏳ Parquet data support

### **Version 2.0 (Future)**
- 🔮 Machine learning integration
- 🔮 Strategy auto-generation
- 🔮 Cloud deployment support
- 🔮 Real-time optimization
- 🔮 Multi-strategy portfolios

---

## 🐛 **Troubleshooting**

### **Common Issues**

**Issue: "Module not found" errors**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Issue: "Data not found" errors**
```bash
# Verify data path in config/backtest_config.json
# Ensure CSV files are in correct location
# Check CSV format matches expected structure
```

**Issue: API server won't start**
```bash
# Check if port 8000 is available
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Try different port
python scripts/run_server.py --port 8001
```

---

## 📚 **Documentation**

### **Current Documentation**
- [Project Status](STATUS.md) - Comprehensive project status and metrics
- [Chart Viewer Issues](docs/current/CHART_VIEWER_ISSUES.md) - C# integration issues
- [Chart Viewer Implementation](docs/current/CHART_VIEWER_IMPLEMENTATION_GUIDE.md) - Integration guide
- [API Documentation](http://localhost:8000/docs) - Auto-generated Swagger docs (when server running)

### **Planned Documentation** ⏳
- Installation Guide (docs/Installation.md)
- User Guide (docs/User_Guide.md)
- Developer Guide (docs/Developer_Guide.md)
- Validation Report (docs/Validation_Report.md)

---

## 🤝 **Contributing**

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 **License**

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- MetaQuotes for MetaTrader 5 platform
- FastAPI framework for excellent API capabilities
- Pandas/NumPy communities for data processing tools
- TA-Lib for technical analysis indicators

---

## 📞 **Support**

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/jcamp-python-backtesting/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/jcamp-python-backtesting/discussions)

---

## 🎯 **Quick Links**

- [🚀 Quick Start](#-quick-start-guide)
- [📖 Examples](#-usage-examples)
- [🔧 Configuration](#-configuration)
- [🧪 Testing](#-testing)
- [🔌 API Docs](#-api-documentation)

---

**Built with ❤️ for the JCAMP Forex Trading System**

*Empowering traders with institutional-grade backtesting capabilities*
