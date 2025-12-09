# MT5 Indicator Export Instructions

## Goal
Export MT5 indicator values for validation against Python implementation

## Test Data Range
- Symbol: EURUSD
- Timeframe: H1
- Date Range: 2024-12-01 00:00 to 2024-12-07 23:59 (1 week)
- Expected bars: ~120 H1 bars

## Method: Add Print Statements to MT5 EA

### Step 1: Open MT5 EA in MetaEditor

1. Open MetaTrader 5
2. Press F4 to open MetaEditor
3. Open `Jcamp_BacktestEA.mq5`

### Step 2: Find OnInit() Function

Locate the `OnInit()` function (should be around line 200-300)

### Step 3: Add Indicator Export Code

Add this code to the **END** of the `OnInit()` function, right before the `return(INIT_SUCCEEDED);` line:

```mql5
//==============================================================================
// PYTHON VALIDATION: Export Indicator Values
//==============================================================================
// Export H1 indicator values for Python validation (Dec 1-7, 2024)
// This code will print indicator values for the first 10 H1 bars
// TODO: Remove this code block after validation complete
//==============================================================================

if (_Symbol == "EURUSD" && AnalysisTimeframe == PERIOD_H1)
{
   Print("==============================================================================");
   Print("PYTHON VALIDATION - Exporting H1 Indicator Values");
   Print("Date Range: 2024-12-01 to 2024-12-07");
   Print("==============================================================================");

   // Get indicator handles
   int atr_handle = iATR(_Symbol, PERIOD_H1, ATRPeriod);
   int ema20_handle = iMA(_Symbol, PERIOD_H1, 20, 0, MODE_EMA, PRICE_CLOSE);
   int ema50_handle = iMA(_Symbol, PERIOD_H1, 50, 0, MODE_EMA, PRICE_CLOSE);
   int ema100_handle = iMA(_Symbol, PERIOD_H1, 100, 0, MODE_EMA, PRICE_CLOSE);
   int adx_handle = iADX(_Symbol, PERIOD_H1, 14);
   int rsi_handle = iRSI(_Symbol, PERIOD_H1, 14, PRICE_CLOSE);

   // Copy last 10 bars
   double atr_buffer[];
   double ema20_buffer[];
   double ema50_buffer[];
   double ema100_buffer[];
   double adx_buffer[];
   double plus_di_buffer[];
   double minus_di_buffer[];
   double rsi_buffer[];
   double close_buffer[];

   ArraySetAsSeries(atr_buffer, true);
   ArraySetAsSeries(ema20_buffer, true);
   ArraySetAsSeries(ema50_buffer, true);
   ArraySetAsSeries(ema100_buffer, true);
   ArraySetAsSeries(adx_buffer, true);
   ArraySetAsSeries(plus_di_buffer, true);
   ArraySetAsSeries(minus_di_buffer, true);
   ArraySetAsSeries(rsi_buffer, true);
   ArraySetAsSeries(close_buffer, true);

   CopyBuffer(atr_handle, 0, 0, 10, atr_buffer);
   CopyBuffer(ema20_handle, 0, 0, 10, ema20_buffer);
   CopyBuffer(ema50_handle, 0, 0, 10, ema50_buffer);
   CopyBuffer(ema100_handle, 0, 0, 10, ema100_buffer);
   CopyBuffer(adx_handle, 0, 0, 10, adx_buffer);           // ADX main line
   CopyBuffer(adx_handle, 1, 0, 10, plus_di_buffer);       // +DI line
   CopyBuffer(adx_handle, 2, 0, 10, minus_di_buffer);      // -DI line
   CopyBuffer(rsi_handle, 0, 0, 10, rsi_buffer);
   CopyClose(_Symbol, PERIOD_H1, 0, 10, close_buffer);

   // Print header
   Print("Timestamp,Close,ATR,EMA20,EMA50,EMA100,ADX,+DI,-DI,RSI");

   // Print last 10 bars
   for (int i = 0; i < 10; i++)
   {
      datetime bar_time = iTime(_Symbol, PERIOD_H1, i);
      string timestamp = TimeToString(bar_time, TIME_DATE|TIME_MINUTES);

      PrintFormat("%s,%.5f,%.5f,%.5f,%.5f,%.5f,%.2f,%.2f,%.2f,%.2f",
                  timestamp,
                  close_buffer[i],
                  atr_buffer[i],
                  ema20_buffer[i],
                  ema50_buffer[i],
                  ema100_buffer[i],
                  adx_buffer[i],
                  plus_di_buffer[i],
                  minus_di_buffer[i],
                  rsi_buffer[i]);
   }

   Print("==============================================================================");
   Print("Export complete. Copy lines above to CSV file for validation.");
   Print("==============================================================================");

   // Release handles
   IndicatorRelease(atr_handle);
   IndicatorRelease(ema20_handle);
   IndicatorRelease(ema50_handle);
   IndicatorRelease(ema100_handle);
   IndicatorRelease(adx_handle);
   IndicatorRelease(rsi_handle);
}

//==============================================================================
// END PYTHON VALIDATION CODE - Remove after validation complete
//==============================================================================
```

### Step 4: Run EA in MT5 Strategy Tester

1. Compile the EA (F7)
2. Open Strategy Tester (Ctrl+R)
3. Settings:
   - Expert: `Jcamp_BacktestEA`
   - Symbol: `EURUSD`
   - Period: `H1`
   - Date: `2024.12.01` to `2024.12.07`
   - Optimization: **Visual mode OFF** (faster)
4. Click **Start**
5. Wait for backtest to complete

### Step 5: Copy Indicator Values from Expert Log

1. Open **Experts** tab (bottom of MT5)
2. Look for the CSV output between the `=====` lines
3. Copy all lines that start with timestamps (e.g., `2024.12.01 00:00,1.05234,...`)
4. Paste into file: `tests/fixtures/mt5_reference_data.csv`

Example output format:
```
Timestamp,Close,ATR,EMA20,EMA50,EMA100,ADX,+DI,-DI,RSI
2024.12.07 23:00,1.05234,0.00142,1.05234,1.05189,1.05456,24.50,18.30,12.70,52.30
2024.12.07 22:00,1.05256,0.00141,1.05237,1.05191,1.05453,24.80,18.70,12.50,53.10
...
```

### Step 6: Update Test File

1. Open `tests/test_indicator_accuracy.py`
2. Replace placeholder values in `mt5_values` dictionaries with actual MT5 data
3. Format timestamps as: `'2024-12-07 23:00:00'` (add seconds)

Example:
```python
mt5_values = {
    '2024-12-07 23:00:00': 0.00142,  # ATR from MT5 export
    '2024-12-07 22:00:00': 0.00141,
    # ... more values
}
```

### Step 7: Run Validation Tests

```bash
cd D:\JcampFxTrading\jcamp-python-backtesting
python tests/test_indicator_accuracy.py
```

## Expected Results

All tests should pass with tolerances:
- **ATR**: ±0.00001 (5 decimal places)
- **EMA**: ±0.00001 (5 decimal places)
- **ADX/+DI/-DI**: ±0.1 (1 decimal place)
- **RSI**: ±0.1 (1 decimal place)

## Troubleshooting

### Issue: No output in Experts tab
- **Solution**: Check that `Print()` statements are not filtered. Right-click Experts tab → enable all message types

### Issue: Indicator values show 0.00000 or empty
- **Solution**: Increase warmup bars. The EA may need 100+ bars before indicators have valid values. Run backtest from 2024-01-01 to ensure warmup.

### Issue: Timestamps don't match
- **Solution**: MT5 uses broker server time. Check timezone offset. Python uses UTC time from CSV files.

## Alternative: Manual Screenshots

If automated export is too complex:

1. Run MT5 Strategy Tester with **Visual mode ON**
2. Pause at 5-10 random bars in date range
3. Take screenshots showing:
   - Current bar timestamp
   - ATR(14) value
   - EMA(20, 50, 100) values
   - ADX(14), +DI, -DI values
   - RSI(14) value
4. Manually transcribe values to test file

## After Validation Complete

**IMPORTANT**: Remove the indicator export code block from the EA to avoid performance overhead in production.

---

**File created**: 2024-12-09
**Purpose**: Python indicator validation against MT5 EA reference
**Status**: Ready for user execution
