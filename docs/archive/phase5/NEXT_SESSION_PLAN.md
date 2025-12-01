Mult# Next Session Plan: Chart Viewer Playback Enhancements

**Created:** November 22, 2025
**Status:** Planned - Ready for Implementation
**Priority:** High
**Estimated Effort:** 10-16 hours

---

## Overview

Enhance the C# chart viewer with smooth playback capabilities, multiple timeframe support, and improved speed controls for a more realistic trading visualization experience.

---

## Objectives

1. **M1-Level Movement Precision** - Add smooth, realistic price movement
2. **Timeframe Support** - Enable H1 and H4 timeframe viewing
3. **Speed Control Enhancement** - Extend playback speed range to 1-20x

---

## User Requirements

### 1. Movement Precision (Dual-Mode Approach)

**Option A: Real M1 Data Mode**
- Load actual M1 (1-minute) bars from data source
- Most accurate representation of price movement
- Requires M1 data files available
- 15x more granular than M15

**Option B: Simulated OHLC Mode**
- Animate each M15 bar's OHLC progression: Open → High → Low → Close
- Creates realistic bar formation without needing M1 data
- 4 intermediate steps per M15 bar
- Good balance of smoothness and simplicity

**Implementation:** Make it optional via UI toggle

### 2. Timeframe Switching

**Approach:** Client-side conversion (aggregate M15 data)

**Supported Timeframes:**
- M15 (current, base data)
- H1 (aggregate 4 M15 bars)
- H4 (aggregate 16 M15 bars)

**Aggregation Rules:**
- Open = First bar's Open
- High = Maximum of all Highs
- Low = Minimum of all Lows
- Close = Last bar's Close
- Volume = Sum of all Volumes (if applicable)

### 3. Speed Slider Range

**Current:** 1-5x
**Target:** 1-20x

**Suggested Scale:**
- 1x - Real-time (or as close as possible)
- 5x - 5 times faster
- 10x - 10 times faster
- 15x - 15 times faster
- 20x - 20 times faster

**Consider:** Logarithmic scaling for smoother control at higher speeds

---

## Implementation Plan

### Phase 1: Python API Enhancements

#### File: `src/api/routes/backtest.py`

**New Endpoints:**
```python
@router.get("/backtest/ohlc-m1/{task_id}")
async def get_m1_ohlc_data(task_id: str):
    """Get M1 OHLC data for enhanced playback"""
    # Return M1 bars for the backtest period
    pass
```

**Enhanced Endpoint:**
```python
@router.get("/backtest/ohlc/{task_id}")
async def get_ohlc_data(task_id: str, timeframe: str = "M15"):
    """Get OHLC data with optional timeframe parameter"""
    # Support: M1, M15, H1, H4
    pass
```

#### File: `src/api/services/backtest_service.py`

**New Methods:**
- `load_m1_data(symbol, start_date, end_date)` - Load M1 bars
- `aggregate_to_h1(m15_bars)` - Convert M15 to H1
- `aggregate_to_h4(m15_bars)` - Convert M15 to H4

#### File: `src/api/models/requests.py`

**New Enum:**
```python
class Timeframe(str, Enum):
    M1 = "M1"
    M15 = "M15"
    H1 = "H1"
    H4 = "H4"
```

---

### Phase 2: C# Data Models Enhancement

#### New File: `Models/PlaybackMode.cs`

```csharp
public enum PlaybackMode
{
    Standard,           // Jump between bars (current behavior)
    RealM1,            // Use real M1 data for smooth movement
    SimulatedOHLC      // Simulate OHLC progression
}

public enum ChartTimeframe
{
    M15,
    H1,
    H4
}
```

#### Update File: `Models/OhlcData.cs`

```csharp
public class OhlcData
{
    // ... existing properties ...

    public ChartTimeframe Timeframe { get; set; }
    public List<Candle> M1Candles { get; set; }  // For Real M1 mode

    // Aggregation method
    public List<Candle> AggregateToH1() { ... }
    public List<Candle> AggregateToH4() { ... }
}
```

---

### Phase 3: C# Chart Viewer - Movement Precision

#### File: `ChartViewerWindow.xaml.cs`

**New Properties:**
```csharp
private PlaybackMode _playbackMode = PlaybackMode.SimulatedOHLC;
private int _subBarIndex = 0;  // For OHLC simulation
private int _m1BarIndex = 0;   // For Real M1 mode
```

**New Method: Simulated OHLC Playback**
```csharp
private void PlaybackTimer_Tick_SimulatedOHLC(object sender, EventArgs e)
{
    // For each M15 bar, animate 4 steps:
    // Step 0: Open
    // Step 1: High (Open -> High)
    // Step 2: Low (High -> Low or Open -> Low depending on bar direction)
    // Step 3: Close (Low -> Close or High -> Close)

    if (_subBarIndex < 4)
    {
        // Render intermediate price position
        UpdateChartWithSubBar(_currentBarIndex, _subBarIndex);
        _subBarIndex++;
    }
    else
    {
        // Move to next M15 bar
        _currentBarIndex++;
        _subBarIndex = 0;
    }
}
```

**New Method: Real M1 Playback**
```csharp
private void PlaybackTimer_Tick_RealM1(object sender, EventArgs e)
{
    // Playback through M1 bars
    // Every 15 M1 bars = 1 M15 bar

    if (_m1BarIndex < _ohlcData.M1Candles.Count)
    {
        UpdateChartWithM1Bar(_m1BarIndex);
        _m1BarIndex++;
    }
}
```

**New Method: Load M1 Data**
```csharp
private async Task LoadM1DataAsync()
{
    // Call API: GET /backtest/ohlc-m1/{taskId}
    var response = await _httpClient.GetAsync($"{ApiBaseUrl}/backtest/ohlc-m1/{_taskId}");
    var m1Data = await response.Content.ReadFromJsonAsync<OhlcDataResponse>();
    _ohlcData.M1Candles = m1Data.Candles;
}
```

---

### Phase 4: Timeframe Conversion (Client-Side)

#### File: `ChartViewerWindow.xaml.cs`

**New Property:**
```csharp
private ChartTimeframe _selectedTimeframe = ChartTimeframe.M15;
```

**New Method: Aggregate M15 to H1**
```csharp
private List<Candle> AggregateToH1(List<Candle> m15Bars)
{
    var h1Bars = new List<Candle>();

    for (int i = 0; i < m15Bars.Count; i += 4)
    {
        if (i + 3 >= m15Bars.Count) break;

        var fourBars = m15Bars.GetRange(i, 4);
        var h1Bar = new Candle
        {
            Time = fourBars[0].Time,
            Open = fourBars[0].Open,
            High = fourBars.Max(b => b.High),
            Low = fourBars.Min(b => b.Low),
            Close = fourBars[3].Close
        };
        h1Bars.Add(h1Bar);
    }

    return h1Bars;
}
```

**New Method: Aggregate M15 to H4**
```csharp
private List<Candle> AggregateToH4(List<Candle> m15Bars)
{
    // Similar to H1 but aggregate 16 bars instead of 4
    // ... implementation ...
}
```

**Update Method: OnTimeframeChanged**
```csharp
private void TimeframeComboBox_SelectionChanged(object sender, EventArgs e)
{
    _selectedTimeframe = (ChartTimeframe)TimeframeComboBox.SelectedItem;

    switch (_selectedTimeframe)
    {
        case ChartTimeframe.M15:
            _displayedCandles = _ohlcData.Candles;
            break;
        case ChartTimeframe.H1:
            _displayedCandles = AggregateToH1(_ohlcData.Candles);
            break;
        case ChartTimeframe.H4:
            _displayedCandles = AggregateToH4(_ohlcData.Candles);
            break;
    }

    // Recalculate EMAs for new timeframe
    RecalculateIndicators();

    // Update grid spacing
    UpdateGridSpacing();

    // Refresh chart
    RefreshChart();
}
```

**Update Method: Grid Spacing Based on Timeframe**
```csharp
private void UpdateGridSpacing()
{
    int barInterval;

    switch (_selectedTimeframe)
    {
        case ChartTimeframe.M15:
            barInterval = 2;  // 30 minutes (current)
            break;
        case ChartTimeframe.H1:
            barInterval = 6;  // 6 hours
            break;
        case ChartTimeframe.H4:
            barInterval = 6;  // 24 hours (1 day)
            break;
    }

    // Update X-axis tick generation with new interval
    // ... implementation ...
}
```

---

### Phase 5: Speed Slider Enhancement

#### File: `ChartViewerWindow.xaml`

**Update Slider Control:**
```xml
<Slider x:Name="SpeedSlider"
        Minimum="1"
        Maximum="20"
        Value="5"
        TickFrequency="1"
        TickPlacement="BottomRight"
        Width="200"/>

<TextBlock x:Name="SpeedLabel"
           Text="Speed: 5x"
           Margin="10,0,0,0"/>
```

#### File: `ChartViewerWindow.xaml.cs`

**Update Method: Speed Slider Changed**
```csharp
private void SpeedSlider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
{
    int speed = (int)e.NewValue;
    SpeedLabel.Text = $"Speed: {speed}x";
    UpdatePlaybackSpeed();
}

private void UpdatePlaybackSpeed()
{
    int speed = (int)SpeedSlider.Value;

    // Base interval for M15 at 1x speed
    int baseInterval = 1000;  // 1 second per bar at 1x

    // Adjust based on playback mode
    if (_playbackMode == PlaybackMode.SimulatedOHLC)
    {
        // 4 steps per M15 bar
        baseInterval = baseInterval / 4;
    }
    else if (_playbackMode == PlaybackMode.RealM1)
    {
        // 15 M1 bars per M15 bar
        baseInterval = baseInterval / 15;
    }

    // Apply speed multiplier
    int interval = baseInterval / speed;

    _playbackTimer.Interval = TimeSpan.FromMilliseconds(interval);
}
```

---

### Phase 6: UI/UX Updates

#### File: `ChartViewerWindow.xaml`

**New Controls to Add:**

```xml
<!-- Timeframe Selector -->
<ComboBox x:Name="TimeframeComboBox"
          SelectionChanged="TimeframeComboBox_SelectionChanged"
          SelectedIndex="0">
    <ComboBoxItem Content="M15"/>
    <ComboBoxItem Content="H1"/>
    <ComboBoxItem Content="H4"/>
</ComboBox>

<!-- Playback Mode Toggle -->
<StackPanel Orientation="Horizontal" Margin="10,5">
    <TextBlock Text="Playback Mode:" VerticalAlignment="Center" Margin="0,0,10,0"/>
    <RadioButton x:Name="StandardModeRadio"
                 Content="Standard"
                 GroupName="PlaybackMode"
                 Checked="PlaybackMode_Changed"/>
    <RadioButton x:Name="SimulatedModeRadio"
                 Content="Simulated OHLC"
                 GroupName="PlaybackMode"
                 IsChecked="True"
                 Checked="PlaybackMode_Changed"
                 Margin="10,0,0,0"/>
    <RadioButton x:Name="RealM1ModeRadio"
                 Content="Real M1 Data"
                 GroupName="PlaybackMode"
                 Checked="PlaybackMode_Changed"
                 Margin="10,0,0,0"/>
</StackPanel>

<!-- Status Indicator -->
<TextBlock x:Name="PlaybackStatusText"
           Text="Mode: Simulated OHLC | Timeframe: M15 | Speed: 5x"
           Margin="10,5"/>
```

---

## Testing Plan

### Unit Tests
1. **Timeframe Aggregation:**
   - Test M15 → H1 conversion (verify 4 bars combine correctly)
   - Test M15 → H4 conversion (verify 16 bars combine correctly)
   - Test OHLC values: Open, High, Low, Close accuracy

2. **Playback Modes:**
   - Test Standard mode (current behavior)
   - Test Simulated OHLC mode (4-step animation)
   - Test Real M1 mode (15 M1 bars per M15 bar)

### Integration Tests
1. Load M15 data and switch to H1 - verify chart updates
2. Load M15 data and switch to H4 - verify chart updates
3. Enable Real M1 mode - verify API call and data loading
4. Test speed slider at 1x, 5x, 10x, 20x - verify smooth playback

### Visual Tests
1. Verify EMAs recalculate correctly for H1/H4
2. Verify grid spacing adjusts for each timeframe
3. Verify trade markers display at correct positions across timeframes
4. Verify X-axis labels show appropriate time intervals

---

## Files to Modify

### Python Backend
- `src/api/routes/backtest.py` - New M1 endpoint, timeframe parameter
- `src/api/services/backtest_service.py` - M1 loading, aggregation logic
- `src/api/models/requests.py` - Timeframe enum
- `src/data_loader.py` - M1 data loading (if not already supported)

### C# Frontend
- `ChartViewerWindow.xaml.cs` - Core playback logic, mode switching
- `ChartViewerWindow.xaml` - UI controls (timeframe selector, mode toggle, speed slider)
- `Models/OhlcData.cs` - Data structures for M1 and aggregation
- `Models/PlaybackMode.cs` - NEW: Enums for modes and timeframes
- `Services/TimeframeConverter.cs` - NEW: Aggregation helper methods

---

## Technical Considerations

### Performance
- **M1 Data:** 15x more data points - ensure efficient rendering
- **Real-time Updates:** Consider caching aggregated H1/H4 bars
- **Memory:** M1 data for full year could be significant - consider lazy loading

### Trade Positioning
- Trades entered on M15 need to map correctly to H1/H4
- Entry price horizontal lines should remain at same price levels
- TP/SL lines should persist across timeframe changes

### EMA Recalculation
- EMAs are timeframe-specific
- EMA(20) on M15 ≠ EMA(20) on H1
- Need to recalculate EMAs when timeframe changes
- Consider server-side EMA calculation for accuracy

---

## Open Questions

1. **M1 Data Availability:**
   - Do we have M1 data files for EURUSD?
   - Are they in the same format as M15 data?

2. **API Performance:**
   - How large will M1 dataset be?
   - Should we implement pagination or streaming?

3. **EMA Calculation:**
   - Server-side or client-side for H1/H4?
   - Impact on performance?

4. **Trade Execution Timing:**
   - How to display trades that execute mid-bar in H1/H4?
   - Show entry time precisely or snap to bar?

---

## Success Criteria

- [ ] User can toggle between Standard, Simulated OHLC, and Real M1 playback modes
- [ ] User can switch between M15, H1, H4 timeframes
- [ ] Speed slider ranges from 1-20x with smooth control
- [ ] Chart updates correctly when changing timeframes (EMAs, grid, labels)
- [ ] Trade markers display at correct positions across all timeframes
- [ ] Playback is smooth and responsive at all speed levels
- [ ] All modes tested and verified working

---

## Next Steps for Implementation Session

1. Start with Python API enhancements (M1 endpoint, timeframe parameter)
2. Implement client-side timeframe aggregation (M15→H1, M15→H4)
3. Add UI controls (timeframe selector, mode toggle, speed slider)
4. Implement Simulated OHLC mode (easier than Real M1)
5. Test timeframe switching with existing M15 data
6. Implement Real M1 mode (requires M1 data availability)
7. Full integration testing

---

**Documented by:** Claude Code
**Review Status:** Ready for next session
**Related Documents:**
- STATUS.md
- CHART_VIEWER_ISSUES.md
- SESSION_START.md
