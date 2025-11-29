# MT5-Style Chart Viewer Implementation Guide

## ✅ COMPLETED: Python API Enhancement

### New OHLC Endpoint
**Endpoint**: `GET /api/v1/backtest/{task_id}/ohlc`

Returns comprehensive candlestick data for chart visualization:
```json
{
  "symbol": "EURUSD",
  "start_date": "2024-11-01",
  "end_date": "2024-11-30",
  "candles": [
    {
      "timestamp": "2024-11-01T00:00:00",
      "open": 1.0850,
      "high": 1.0870,
      "low": 1.0840,
      "close": 1.0860,
      "ema_fast": 1.0855,
      "ema_mid": 1.0852,
      "ema_slow": 1.0848,
      "rsi": 55.2,
      "adx": 28.5
    },
    // ... more candles
  ],
  "trades": [
    {
      "ticket_number": 12345,
      "strategy": "RANGE_RIDER",
      "side": "SELL",
      "entry_time": "2024-11-07T04:00:00",
      "exit_time": "2024-11-07T09:00:00",
      "entry_price": 1.07368,
      "exit_price": 1.07588,
      "stop_loss": 1.07588,
      "take_profit": 1.07148,
      "r_multiple": -1.0,
      "is_win": false
    },
    // ... more trades
  ],
  "pip_size": 0.0001,
  "decimal_places": 5
}
```

### Files Modified
- `src/api/routes/backtest.py` - Added `/ohlc` endpoint
- `src/api/services/backtest_service.py` - Added `_prepare_ohlc_data()` method
- `src/backtest_engine.py` - Stores df and indicators for chart access

## ✅ COMPLETED: C# Data Models

### Files Created
**`OhlcModels.cs`** - Complete data models with:
- `OhlcData` - Main container for OHLC data
- `CandleData` - Individual candlestick bar
- `TradeWithLevels` - Trade data with TP/SL levels
- `ChartColors` - Dark theme color palette

### Dark Theme Color Scheme
```csharp
// Exact colors as specified
BullishBody: RGB(0, 255, 0)       // Bright green
BullishWick: RGB(0, 153, 0)       // 30% darker
BearishBody: RGB(255, 0, 0)       // Red
BearishWick: RGB(153, 0, 0)       // 30% darker
Background:  RGB(0, 0, 0)         // Black
Grid:        RGBA(204,204,204,204) // 80% grey
TPBox:       RGBA(0,255,0,191)    // Green 75% opacity
SLBox:       RGBA(255,0,0,191)    // Red 75% opacity
```

## 🔨 NEXT STEPS: C# Chart Viewer Implementation

### Step 1: Install ScottPlot NuGet Package

In Visual Studio:
1. Right-click on JcampForexTrader project
2. Select "Manage NuGet Packages"
3. Search for "ScottPlot.WPF"
4. Install `ScottPlot.WPF` (version 5.0+)

Or via Package Manager Console:
```powershell
Install-Package ScottPlot.WPF
```

### Step 2: Create ChartViewerWindow (To Be Implemented)

**Required Components:**

1. **ChartViewerWindow.xaml**
   - Dark theme window
   - TabControl for multi-symbol support
   - ScottPlot WpfPlot control for chart
   - Playback controls (Play/Pause, Speed slider, Progress bar)
   - Buttons: "Open HTML Charts", "Close"

2. **ChartViewerWindow.xaml.cs**
   - Fetch OHLC data from API
   - Render candlesticks with custom colors
   - Draw TP/SL boxes for active trades
   - Draw closed trade lines (green wins, red losses)
   - Implement bar-by-bar playback animation
   - Update live R-multiple during playback

3. **Trade Visualization Requirements:**

**Active Trades:**
```
┌────────────────────┐
│ TP: 1.0850        │ ← Green box (75% opacity)
│ +2.5R (+125 pips) │
└────────────────────┘
     │
     ●  Entry: 1.0800
     │  #12345 TREND_RIDER
     │  Live: +1.2R
     │
┌────────────────────┐
│ SL: 1.0750        │ ← Red box (75% opacity)
│ -1.0R (-50 pips)  │
└────────────────────┘
```

**Closed Trades:**
```
      #12345 +2.4R
      ↓ (text on top)
Entry ●━━━━━━━━━━━━━● Exit  (green dashed line for wins)
1.0800              1.0920

      #12346 -1.0R
      ↓
Entry ●━━━━━━━━━━━━━● Exit  (red dashed line for losses)
1.0800              1.0750
```

### Step 3: Update BacktestApiClient

Add method to fetch OHLC data:
```csharp
public async Task<OhlcData> GetOhlcDataAsync(string taskId)
{
    var response = await _httpClient.GetAsync($"/api/v1/backtest/{taskId}/ohlc");
    response.EnsureSuccessStatusCode();

    var content = await response.Content.ReadAsStringAsync();
    return JsonConvert.DeserializeObject<OhlcData>(content);
}
```

### Step 4: Modify BacktestWindow

Add "View Chart Playback" button:
```xaml
<Button x:Name="ViewChartButton" Content="View Chart Playback"
        Click="ViewChartButton_Click"
        Background="#007ACC" Foreground="White"
        Height="35" Margin="10,5"/>
```

Add click handler:
```csharp
private async void ViewChartButton_Click(object sender, RoutedEventArgs e)
{
    try
    {
        // Get task ID from current backtest
        string taskId = GetCurrentTaskId();

        // Fetch OHLC data
        var ohlcData = await _apiClient.GetOhlcDataAsync(taskId);

        // Launch chart viewer window
        var chartViewer = new ChartViewerWindow(ohlcData);
        chartViewer.Show();
    }
    catch (Exception ex)
    {
        MessageBox.Show($"Failed to load chart: {ex.Message}",
                      "Error", MessageBoxButton.OK, MessageBoxImage.Error);
    }
}
```

## 📋 Implementation Checklist

### Python API (✅ Complete)
- [x] Add OHLC endpoint `/api/v1/backtest/{task_id}/ohlc`
- [x] Prepare candlestick data with indicators
- [x] Include trade data with TP/SL levels
- [x] Store OHLC data in backtest task

### C# Data Layer (✅ Complete)
- [x] Create `OhlcModels.cs` with data classes
- [x] Define `ChartColors` constants
- [x] Add helper methods (GetPipsToTP, GetLiveRMultiple, etc.)

### C# UI Layer (⏳ To Do)
- [ ] Install ScottPlot.WPF NuGet package
- [ ] Create `ChartViewerWindow.xaml`
- [ ] Create `ChartViewerWindow.xaml.cs`
- [ ] Implement candlestick rendering
- [ ] Implement TP/SL box visualization
- [ ] Implement closed trade lines
- [ ] Add playback controls
- [ ] Add speed slider
- [ ] Add multi-symbol tabs
- [ ] Update `BacktestApiClient` with GetOhlcData method
- [ ] Update `BacktestWindow` with "View Chart" button

## 🎨 ScottPlot Implementation Example

### Basic Candlestick Chart Setup
```csharp
// In ChartViewerWindow.xaml.cs
private void InitializeChart()
{
    var plot = WpfPlot1.Plot;

    // Set dark theme
    plot.Style(ScottPlot.Style.Black);
    plot.XAxis.Color(ChartColors.Grid);
    plot.YAxis.Color(ChartColors.Grid);

    // Add candlesticks
    foreach (var candle in _ohlcData.Candles)
    {
        var ohlc = new ScottPlot.OHLC(
            candle.Open, candle.High, candle.Low, candle.Close,
            candle.GetDateTime(), TimeSpan.FromHours(1)
        );

        // Custom colors
        var color = candle.IsBullish ?
            System.Drawing.Color.FromArgb(0, 255, 0) :  // Green
            System.Drawing.Color.FromArgb(255, 0, 0);   // Red

        plot.AddCandlesticks(new[] { ohlc }, color);
    }

    // Add EMA lines
    if (_ohlcData.Candles.Any(c => c.EmaFast.HasValue))
    {
        var emaFastData = _ohlcData.Candles
            .Where(c => c.EmaFast.HasValue)
            .Select(c => c.EmaFast.Value)
            .ToArray();

        plot.AddScatterLines(
            DataGen.Consecutive(emaFastData.Length),
            emaFastData,
            System.Drawing.Color.FromArgb(41, 98, 255),
            label: "EMA Fast"
        );
    }

    WpfPlot1.Refresh();
}
```

### Trade Visualization Example
```csharp
private void DrawTrade(TradeWithLevels trade, int currentBarIndex)
{
    var plot = WpfPlot1.Plot;

    if (!trade.IsClosed)
    {
        // Active trade - draw TP/SL boxes
        DrawTPSLBoxes(trade);
    }
    else
    {
        // Closed trade - draw result line
        var color = trade.IsWin ?
            System.Drawing.Color.FromArgb(0, 255, 0) :  // Green
            System.Drawing.Color.FromArgb(255, 0, 0);   // Red

        var line = plot.AddLine(
            GetBarIndex(trade.GetEntryTime()),
            trade.EntryPrice,
            GetBarIndex(trade.GetExitTime().Value),
            trade.ExitPrice.Value,
            color,
            2,
            LineStyle.Dash
        );

        // Add label
        plot.AddText(
            $"#{trade.TicketNumber} {trade.RMultiple:+0.00}R",
            GetBarIndex(trade.GetExitTime().Value),
            trade.ExitPrice.Value,
            color: System.Drawing.Color.White
        );
    }
}
```

## 🚀 Quick Start

1. **Test the API endpoint:**
```bash
curl http://localhost:8000/api/v1/backtest/{task_id}/ohlc
```

2. **Install ScottPlot in Visual Studio**

3. **Create ChartViewerWindow** following the structure above

4. **Add "View Chart" button** to BacktestWindow

5. **Test with a completed backtest**

## 📚 Resources

- **ScottPlot Documentation**: https://scottplot.net/cookbook/5.0/
- **ScottPlot Financial Charts**: https://scottplot.net/cookbook/5.0/financial/
- **WPF Tutorial**: https://scottplot.net/quickstart/wpf/

## ⚠️ Notes

- The Python API is fully functional and tested
- OHLC data includes all necessary information for visualization
- C# models match the Python API response format
- Color scheme matches your exact specifications
- Ready for C# chart viewer implementation

The foundation is complete - the chart viewer implementation is now ready to begin!
