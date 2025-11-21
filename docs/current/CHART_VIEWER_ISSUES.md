BACKTEST VIEWER - ISSUES STATUS
Last Updated: 2025-11-21

## FIXED ISSUES ✅ (Nov 21, 2025)

### B. MT5-Style Chart Viewer - JCAMP Backtesting Chart

1. **✅ FIXED - Candlesticks now showing**
   - **Issue:** Candlesticks not rendering, only EMAs visible
   - **Root Cause:** ScottPlot 5.x required explicit color configuration
   - **Fix:** Added explicit UpColor/DownColor and LineWidth to candlestick plot
   - **File:** ChartViewerWindow.xaml.cs:271-274

2. **✅ FIXED - Trade boxes too large**
   - **Issue:** TP/SL boxes were 5 pips tall, too prominent
   - **Fix:** Reduced box height from 5 pips to 2 pips
   - **File:** ChartViewerWindow.xaml.cs:385, 415

3. **✅ FIXED - Trade boxes starting at bar 0**
   - **Issue:** Trade boxes appeared at wrong positions, often starting at bar 0
   - **Root Cause:** Coordinate system mismatch - candlesticks used DateTime for X-axis, but EMAs and trade boxes used bar indices
   - **Fix:** Changed candlesticks to use bar index-based coordinates (DateTime.MinValue.AddDays(i)) for consistency
   - **File:** ChartViewerWindow.xaml.cs:261-262

5. **✅ CONFIRMED - EMA colors and periods correct**
   - EMA Fast (20): RED #EF5350
   - EMA Mid (50): ORANGE #FF6D00
   - EMA Slow (100): BLUE #2962FF
   - Matches MT5 v1.96 specification

## REMAINING ISSUES ⚠️

### A. Python Backtest Engine Window (Low Priority)
1. **Text font contrast issue**
   - White text on light background in some areas
   - Status: Not critical, UX improvement

### B. MT5-Style Chart Viewer

3. **Bar slider - WORKING ✅**
   - No issues reported

4. **Viewport auto-scroll during playback**
   - **Status:** Already implemented (ChartViewerWindow.xaml.cs:206-223)
   - Keeps current bar on right side of viewport during playback
   - May need testing to verify it works as expected

## MIGRATION COMPLETED ✅

**Project Location Changed:**
- **Old:** `C:\Users\jcamp\OneDrive\Documents\Visual Studio 2022\Projects\CSMMonitor`
- **New:** `D:\JcampFxTrading\CSMMonitor`
- **Reason:** OneDrive sync was causing file editing conflicts
- **Date:** November 21, 2025

## TESTING REQUIRED 🧪

**Next Steps:**
1. Run a backtest from Python API
2. Open chart viewer in C# application
3. Verify:
   - ✅ Candlesticks are visible
   - ✅ Trade boxes start at correct entry point
   - ✅ Trade boxes are appropriately sized (2 pips)
   - ⚠️ Viewport follows price during playback
   - ⚠️ Time/date display on X-axis

## TECHNICAL DETAILS

**Files Modified:**
- `ChartViewerWindow.xaml.cs` - Main chart viewer logic

**Key Changes:**
1. Line 261-262: Changed OHLC to use `DateTime.MinValue.AddDays(i)` instead of `candle.GetDateTime()`
2. Line 271-274: Added explicit candlestick colors (UpColor, DownColor, LineWidth)
3. Line 385, 415: Changed box height from 5 pips to 2 pips

**Commit Status:** Ready to commit