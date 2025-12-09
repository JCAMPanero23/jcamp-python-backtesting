# MT5 Indicator Export - Simple Script Method

## Quick Steps (10 minutes)

### Step 1: Copy the Export Script to MT5

1. Copy the file: `D:\JcampFxTrading\MT5_Indicator_Export_Script.mq5`
2. Paste it into your MT5 Scripts folder:
   - Path: `C:\Users\jcamp\AppData\Roaming\MetaQuotes\Terminal\D0E8209F77C8CF37AD8BF550E51FF075\MQL5\Scripts\`
   - Or right-click in MT5 Navigator → Scripts → "Open Folder"

### Step 2: Run the Script in MT5

1. Open MetaTrader 5
2. Open any EURUSD chart (any timeframe)
3. In **Navigator** panel (Ctrl+N), find **Scripts** folder
4. Drag `MT5_Indicator_Export_Script` onto the EURUSD chart
5. A dialog will appear with settings:
   - **Symbol**: EURUSD (default)
   - **Timeframe**: H1 (default)
   - **Start Date**: 2024.12.01 (default)
   - **End Date**: 2024.12.07 (default)
   - **Max Bars**: 200 (default)
6. Click **OK**

### Step 3: Copy Output from Experts Log

1. Open the **Experts** tab at the bottom of MT5
2. You'll see output like this:

```
======================================================================
PYTHON VALIDATION - Exporting MT5 Indicator Values
Symbol: EURUSD
Timeframe: H1
Date Range: 2024.12.01 to 2024.12.07
======================================================================

Exporting 120 bars...

CSV FORMAT (copy lines below):
Timestamp,Close,ATR,EMA20,EMA50,EMA100,ADX,+DI,-DI,RSI
2024.12.07 23:00,1.05234,0.00142,1.05234,1.05189,1.05456,24.50,18.30,12.70,52.30
2024.12.07 22:00,1.05256,0.00141,1.05237,1.05191,1.05453,24.80,18.70,12.50,53.10
... (more lines)
```

3. **Right-click** in the Experts tab → **Copy All** (or manually select and copy the CSV lines)

### Step 4: Save to CSV File

1. Open a text editor (Notepad, VS Code, etc.)
2. Paste the copied lines
3. **Keep only the lines that start with dates** (remove the header text)
4. Make sure the first line is: `Timestamp,Close,ATR,EMA20,EMA50,EMA100,ADX,+DI,-DI,RSI`
5. Save as: `D:\JcampFxTrading\jcamp-python-backtesting\tests\fixtures\mt5_reference_data.csv`

Example CSV file format:
```csv
Timestamp,Close,ATR,EMA20,EMA50,EMA100,ADX,+DI,-DI,RSI
2024.12.07 23:00,1.05234,0.00142,1.05234,1.05189,1.05456,24.50,18.30,12.70,52.30
2024.12.07 22:00,1.05256,0.00141,1.05237,1.05191,1.05453,24.80,18.70,12.50,53.10
2024.12.07 21:00,1.05201,0.00140,1.05240,1.05193,1.05450,25.10,19.00,12.30,54.20
```

### Step 5: Run Python Validation Tests

```bash
cd D:\JcampFxTrading\jcamp-python-backtesting
python tests/test_indicator_accuracy.py
```

The tests will automatically load the MT5 reference data and compare against Python calculations.

---

## Troubleshooting

### Issue: Script not appearing in Navigator
- **Solution**: Press F4 to open MetaEditor, compile the script, then refresh Navigator

### Issue: "Could not find bars for date range"
- **Solution**: Ensure you have EURUSD H1 history data for Dec 1-7, 2024. Download data in MT5 if needed.

### Issue: Indicator values show 0.00000
- **Solution**: Wait a moment after running script (indicators need to calculate). Try running script again.

### Issue: Wrong timeframe or symbol
- **Solution**: When dragging script to chart, check the input parameters dialog and adjust before clicking OK

---

## Alternative: Use Strategy Tester

If running on live chart doesn't work:

1. Open **Strategy Tester** (Ctrl+R)
2. Select **Script** mode (not Expert Advisor)
3. Choose `MT5_Indicator_Export_Script`
4. Symbol: EURUSD
5. Period: H1
6. Date: 2024.12.01 to 2024.12.07
7. Click **Start**
8. Check Experts tab for output

---

**File created**: 2024-12-09
**Purpose**: Simplified MT5 indicator export using standalone script
**Estimated time**: 10 minutes
