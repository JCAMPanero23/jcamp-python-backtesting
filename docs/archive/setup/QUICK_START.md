# 🚀 QUICK START GUIDE
## JCAMP Python Backtesting Engine - Repository Setup

**Last Updated:** November 15, 2025  
**For:** Initial repository setup before Session 1

---

## 📦 **WHAT YOU RECEIVED**

You should have these files ready to use:

```
python-repo/
├── README.md                    # Comprehensive project documentation
├── .gitignore                   # Git exclusions for Python
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # Contribution guidelines
├── requirements.txt             # Core dependencies
├── requirements-dev.txt         # Development dependencies
└── setup_repo.py                # Automated setup script
```

---

## ⚡ **INSTALLATION - 5 MINUTES**

### **Step 1: Create Repository Directory**

```bash
# Create new project directory
mkdir jcamp-python-backtesting
cd jcamp-python-backtesting
```

### **Step 2: Copy Files**

Copy all 7 files from `python-repo/` to your new directory:

```bash
# Your directory should now look like:
jcamp-python-backtesting/
├── README.md
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
├── requirements.txt
├── requirements-dev.txt
└── setup_repo.py
```

### **Step 3: Run Setup Script**

```bash
# Run the automated setup
python setup_repo.py
```

**This creates:**
- ✅ Complete directory structure (src/, tests/, config/, etc.)
- ✅ All `__init__.py` files for Python packages
- ✅ Configuration templates
- ✅ Example scripts
- ✅ Data directory structure
- ✅ `.gitkeep` files to preserve structure

**Expected output:**
```
============================================================
JCAMP PYTHON BACKTESTING ENGINE - REPOSITORY SETUP
============================================================

📁 Creating directory structure...
  ✓ Created: src/
  ✓ Created: src/core/
  ✓ Created: src/strategies/
  ...
✅ Created 30+ directories

📝 Creating __init__.py files...
  ✓ Created: src/__init__.py
  ...
✅ Created 11 __init__.py files

📌 Creating .gitkeep files...
✅ Created .gitkeep files

⚙️ Creating configuration templates...
✅ Created configuration templates

📖 Creating data directory README...
✅ Created data directory documentation

📜 Creating example scripts...
✅ Created example scripts

============================================================
✨ REPOSITORY SETUP COMPLETE!
============================================================
```

### **Step 4: Initialize Git**

```bash
# Initialize git repository
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial repository structure"
```

### **Step 5: (Optional) Push to GitHub**

```bash
# Create repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/jcamp-python-backtesting.git
git branch -M main
git push -u origin main
```

### **Step 6: Create Virtual Environment**

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### **Step 7: Install Dependencies**

```bash
# Install core dependencies (basic usage)
pip install -r requirements.txt

# OR install development dependencies (recommended)
pip install -r requirements-dev.txt
```

**Installation will take 2-5 minutes.**

Dependencies include:
- pandas, numpy (data processing)
- fastapi, uvicorn (API server)
- pandas-ta, ta (technical indicators)
- matplotlib, plotly (visualization)
- pytest (testing)
- and more...

---

## ✅ **VERIFY INSTALLATION**

### **Check Structure:**

```bash
# List directory structure
ls -la

# You should see:
# src/           ✅
# tests/         ✅
# config/        ✅
# data/          ✅
# requirements.txt ✅
# README.md      ✅
```

### **Check Python Packages:**

```bash
# Verify installations
python -c "import pandas; import numpy; print('✅ Core packages OK')"
python -c "import fastapi; print('✅ FastAPI OK')"
python -c "import pandas_ta; print('✅ TA library OK')"
```

### **Check Git:**

```bash
# Verify git initialized
git status

# Should show:
# On branch main
# nothing to commit, working tree clean
```

---

## 📚 **NEXT STEPS**

### **Before Session 1, Prepare:**

1. **Historical Data:**
   - Export EURUSD 2024 M1 data from MT5
   - Place in `data/EURUSD_sml/2024_M1.csv`
   - Format: Same as your GBPUSD sample

2. **MT5 Baseline Results:**
   - Document your v1.96 EURUSD 2024 results:
     - Total R-multiple
     - Trade count
     - Win rate
     - Strategy breakdown

3. **Review Documentation:**
   - Read `README.md` for project overview
   - Check `CONTRIBUTING.md` for dev guidelines
   - Review integration plan document

### **Session 1 Will Build:**

```
src/core/
├── data_loader.py          # Load CSV files
├── timeframe_converter.py  # M1→H1/M15/M5
├── indicators.py           # EMA, ADX, RSI, ATR
├── csm_calculator.py       # Currency strength
└── regime_detector.py      # Trending/ranging

src/strategies/
├── trend_rider.py          # Main strategy
└── range_rider.py          # Ranging strategy

src/engine/
└── backtest_engine.py      # Main backtester
```

---

## 🗂️ **DIRECTORY GUIDE**

### **Where Things Go:**

```
jcamp-python-backtesting/
│
├── src/                    # ALL source code goes here
│   ├── core/              # Data processing & indicators
│   ├── strategies/        # Trading strategies
│   ├── risk/              # Risk management
│   ├── engine/            # Backtesting engine
│   ├── optimization/      # Parameter optimization
│   └── api/               # REST API server
│
├── tests/                 # ALL tests go here
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── validation/       # MT5 validation
│
├── config/                # Configuration files
│   ├── backtest_config.json
│   └── api_config.json
│
├── data/                  # Historical data (GITIGNORED)
│   ├── EURUSD_sml/       # Place EURUSD CSVs here
│   ├── GBPUSD_sml/       # Place GBPUSD CSVs here
│   └── [other pairs]/
│
├── results/               # Backtest results (GITIGNORED)
│   ├── backtests/        # Individual test results
│   └── optimization/     # Optimization results
│
├── logs/                  # Log files (GITIGNORED)
│
├── scripts/               # Utility scripts
│   └── run_server.py     # Start API server
│
├── examples/              # Usage examples
│   ├── basic_backtest.py
│   └── multi_pair_comparison.py
│
└── docs/                  # Documentation
    └── [to be created in Session 1]
```

---

## 🔧 **TROUBLESHOOTING**

### **Problem: setup_repo.py fails**

**Solution:**
```bash
# Ensure Python 3.10+
python --version

# If old version, use python3
python3 setup_repo.py
```

### **Problem: pip install fails**

**Solution:**
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Try again
pip install -r requirements.txt

# If specific package fails (e.g., TA-Lib)
# Use alternative (pandas-ta is already in requirements)
```

### **Problem: venv activation not working**

**Windows:**
```bash
# If execution policy error
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
venv\Scripts\activate
```

**Linux/Mac:**
```bash
# Ensure execute permission
chmod +x venv/bin/activate

# Then activate
source venv/bin/activate
```

### **Problem: Import errors after installation**

**Solution:**
```bash
# Verify venv is activated (you should see (venv) in prompt)
# If not, activate it first

# Then verify installation
pip list | grep pandas
pip list | grep fastapi

# Reinstall if needed
pip install --force-reinstall pandas fastapi
```

---

## 📞 **GET HELP**

### **Before Session 1:**

If you encounter issues:

1. **Check Python version:**
   ```bash
   python --version  # Must be 3.10+
   ```

2. **Check virtual environment:**
   ```bash
   which python      # Should point to venv/
   ```

3. **Verify file structure:**
   ```bash
   python setup_repo.py  # Re-run if needed
   ```

4. **Test basic imports:**
   ```bash
   python -c "import pandas; import numpy"
   ```

### **Ready for Session 1 When:**

✅ Repository structure created  
✅ Git initialized  
✅ Virtual environment working  
✅ Dependencies installed  
✅ EURUSD 2024 data ready  
✅ MT5 baseline results documented  

---

## 🎯 **SESSION 1 PREVIEW**

**What We'll Build:**

In Session 1 (3-4 hours), we'll create:

1. **Data Loader** - Read your CSV files
2. **Indicators** - EMA, ADX, RSI, ATR calculations
3. **CSM Calculator** - Currency strength analysis
4. **Regime Detector** - Trending/ranging classification
5. **First Backtest** - Run on EURUSD 2024

**Expected Result:**

By end of Session 1, you'll run:

```python
from src.engine.backtest_engine import BacktestEngine

engine = BacktestEngine({'symbol': 'EURUSD', 'start_date': '2024-01-01', 'end_date': '2024-12-31'})
results = engine.run()

print(f"Total R: {results.total_r:.2f}")  # Should match MT5 ±5%
```

**And see results comparable to your MT5 v1.96 baseline!** 🎉

---

## 📋 **CHECKLIST**

Before starting Session 1, ensure:

- [ ] Repository directory created
- [ ] All 7 initial files copied
- [ ] `python setup_repo.py` completed successfully
- [ ] Git initialized (`git init`, `git add .`, `git commit`)
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] EURUSD 2024 M1 data prepared
- [ ] MT5 baseline results documented
- [ ] Python 3.10+ installed
- [ ] All import tests pass

---

**🎊 YOU'RE READY TO START BUILDING!**

When all checkboxes are ✅, you're ready for Session 1!

See you in the next session where we'll build the core backtesting engine! 🚀

---

*Quick Start Guide v1.0 - Last Updated: November 15, 2025*
