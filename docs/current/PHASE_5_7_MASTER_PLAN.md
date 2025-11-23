# Master Plan: Phase 5-7 Implementation

**Created:** November 22, 2025
**Status:** Planned - Awaiting Implementation
**Priority:** High
**Estimated Total Effort:** 25-35 hours

---

## Overview

This master plan covers the completion of Phase 5 chart viewer enhancements, strategy validation against MT5, multi-pair backtesting capabilities, and comprehensive strategy improvements.

---

## **PHASE 5: Chart Viewer Fixes + Strategy Validation**

### **Part 1: Critical Bug Fixes** (1-2 hours)

#### 1.1 Fix Manual Progress Slider ⚡ **BLOCKING**
**Issue:** Progress slider can't be manually dragged - only responds to play/pause button

**Implementation:**
- Add `ProgressSlider_ValueChanged` event handler
- Detect manual vs programmatic slider changes
- Update `_currentBarIndex` (M15 mode) or `_m1BarIndex` (M1 mode)
- Call appropriate render method to update chart
- Prevent feedback loop (slider update triggering another update)

**Files:**
- `ChartViewerWindow.xaml` - Add `ValueChanged` event to ProgressSlider
- `ChartViewerWindow.xaml.cs` - Implement handler logic

```csharp
private bool _isManualSliderChange = false;

private void ProgressSlider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
{
    if (_isManualSliderChange) return; // Prevent feedback loop

    int newIndex = (int)e.NewValue;

    if (_playbackMode == PlaybackMode.RealM1 && _m1DataLoaded)
    {
        _m1BarIndex = newIndex;
        AdvanceToM1Bar(_m1BarIndex);
    }
    else
    {
        _currentBarIndex = newIndex;
        AdvanceToBar(_currentBarIndex);
    }
}
```

---

#### 1.2 Fix Reset Button ⚡ **BLOCKING**
**Issue:** Reset button doesn't work after recent changes

**Implementation:**
- Reset `_currentBarIndex` and `_m1BarIndex` to 0
- Clear all chart plottables
- Reset performance tracking (cumulative R, wins, losses)
- Restore initial viewport settings
- Update progress slider to position 0

**Files:**
- `ChartViewerWindow.xaml.cs` - Update `ResetButton_Click()` method

```csharp
private void ResetButton_Click(object sender, RoutedEventArgs e)
{
    StopPlayback();

    _currentBarIndex = 0;
    _m1BarIndex = 0;
    _cumulativeR = 0.0;
    _winsCount = 0;
    _lossesCount = 0;
    _activeTrades.Clear();

    _isManualSliderChange = true;
    ProgressSlider.Value = 0;
    _isManualSliderChange = false;

    if (_playbackMode == PlaybackMode.RealM1 && _m1DataLoaded)
        AdvanceToM1Bar(0);
    else
        AdvanceToBar(0);

    UpdateProgressText();
}
```

---

#### 1.3 Fix Zoom Scale Preservation 🔧 **IMPORTANT**
**Issue:** When smart viewport Y-axis moves to follow price, the zoom level (Y-range) resets to default

**Root Cause:**
Current code calls `SetLimitsY(min, max)` which sets a fixed range, overriding user's zoom

**Solution:**
- Calculate current Y-range (zoom level) before adjusting
- When following price, shift the Y-center but preserve the Y-range
- Only apply default range on initial load or explicit reset

**Implementation:**
```csharp
// In RenderM1ChartUpToBar and RenderChartUpToBar
if (shouldFollow || currentLimits.Bottom == 0)
{
    double currentYRange;

    if (currentLimits.Bottom == 0)
    {
        // Initial state - use default range
        currentYRange = _ohlcData.PipSize * 100; // 100 pips
    }
    else
    {
        // Preserve current zoom level
        currentYRange = currentLimits.Top - currentLimits.Bottom;
    }

    // Center on current price, keep range
    plot.Axes.SetLimitsY(
        currentPrice - currentYRange / 2,
        currentPrice + currentYRange / 2
    );
}
```

**Files:**
- `ChartViewerWindow.xaml.cs` - Modify viewport following logic in both render methods

---

### **Part 2: Timeframe Switching (H1/H4)** (2-3 hours)

#### 2.1 Implement Timeframe Aggregation

**Goal:** Enable users to view charts in M15, H1, or H4 timeframes

**Aggregation Logic:**
- **M15 → H1:** Combine 4 consecutive M15 bars into 1 H1 bar
- **M15 → H4:** Combine 16 consecutive M15 bars into 1 H4 bar

**OHLC Rules:**
- Open = First bar's Open
- High = Maximum of all Highs
- Low = Minimum of all Lows
- Close = Last bar's Close
- Volume = Sum of all Volumes (if applicable)

**Implementation:**

```csharp
private List<CandleData> AggregateToH1(List<CandleData> m15Bars)
{
    var h1Bars = new List<CandleData>();

    for (int i = 0; i < m15Bars.Count; i += 4)
    {
        if (i + 3 >= m15Bars.Count) break;

        var fourBars = m15Bars.GetRange(i, 4);
        var h1Bar = new CandleData
        {
            Timestamp = fourBars[0].Timestamp,
            Open = fourBars[0].Open,
            High = fourBars.Max(c => c.High),
            Low = fourBars.Min(c => c.Low),
            Close = fourBars[3].Close,
            EmaFast = null,  // Recalculate separately
            EmaMid = null,
            EmaSlow = null,
            Rsi = null,
            Adx = null
        };
        h1Bars.Add(h1Bar);
    }

    return h1Bars;
}

private List<CandleData> AggregateToH4(List<CandleData> m15Bars)
{
    var h4Bars = new List<CandleData>();

    for (int i = 0; i < m15Bars.Count; i += 16)
    {
        if (i + 15 >= m15Bars.Count) break;

        var sixteenBars = m15Bars.GetRange(i, 16);
        var h4Bar = new CandleData
        {
            Timestamp = sixteenBars[0].Timestamp,
            Open = sixteenBars[0].Open,
            High = sixteenBars.Max(c => c.High),
            Low = sixteenBars.Min(c => c.Low),
            Close = sixteenBars[15].Close,
            EmaFast = null,
            EmaMid = null,
            EmaSlow = null,
            Rsi = null,
            Adx = null
        };
        h4Bars.Add(h4Bar);
    }

    return h4Bars;
}
```

---

#### 2.2 Wire Up Timeframe Radio Buttons

**Current State:** Radio buttons exist in UI but have no event handlers

**Implementation:**
```xml
<!-- In ChartViewerWindow.xaml -->
<RadioButton Content="M15" IsChecked="True"
             Checked="Timeframe_Changed" GroupName="Timeframe"/>
<RadioButton Content="H1"
             Checked="Timeframe_Changed" GroupName="Timeframe"/>
<RadioButton Content="H4"
             Checked="Timeframe_Changed" GroupName="Timeframe"/>
```

```csharp
// In ChartViewerWindow.xaml.cs
private ChartTimeframe _selectedTimeframe = ChartTimeframe.M15;
private List<CandleData> _displayedCandles;

private void Timeframe_Changed(object sender, RoutedEventArgs e)
{
    var radioButton = sender as RadioButton;
    if (radioButton == null) return;

    switch (radioButton.Content.ToString())
    {
        case "M15":
            _selectedTimeframe = ChartTimeframe.M15;
            _displayedCandles = _ohlcData.Candles;
            break;
        case "H1":
            _selectedTimeframe = ChartTimeframe.H1;
            _displayedCandles = AggregateToH1(_ohlcData.Candles);
            break;
        case "H4":
            _selectedTimeframe = ChartTimeframe.H4;
            _displayedCandles = AggregateToH4(_ohlcData.Candles);
            break;
    }

    RecalculateIndicators();
    UpdateGridSpacing();
    RefreshChart();
}
```

---

#### 2.3 Recalculate Indicators for New Timeframe

**Important:** EMAs calculated on M15 data are NOT valid for H1/H4 timeframes

**Approach:** Calculate EMAs directly on aggregated bars

```csharp
private void RecalculateIndicators()
{
    if (_displayedCandles == null || _displayedCandles.Count == 0) return;

    // Simple EMA calculation (exponential moving average)
    CalculateEMA(_displayedCandles, 20, c => c.EmaFast);
    CalculateEMA(_displayedCandles, 50, c => c.EmaMid);
    CalculateEMA(_displayedCandles, 100, c => c.EmaSlow);
}

private void CalculateEMA(List<CandleData> candles, int period, Action<CandleData, double> setter)
{
    // EMA calculation logic
    // Multiplier = 2 / (period + 1)
    // EMA = (Close - EMA_prev) * Multiplier + EMA_prev
}
```

---

#### 2.4 Update Grid Spacing

**Goal:** Adjust X-axis grid lines based on timeframe

```csharp
private void UpdateGridSpacing()
{
    double hoursInterval;

    switch (_selectedTimeframe)
    {
        case ChartTimeframe.M15:
            hoursInterval = 1.0; // 1 hour intervals
            break;
        case ChartTimeframe.H1:
            hoursInterval = 6.0; // 6 hour intervals
            break;
        case ChartTimeframe.H4:
            hoursInterval = 24.0; // 24 hour intervals (1 day)
            break;
    }

    // Update plot grid configuration
    // (Implementation depends on ScottPlot API)
}
```

**Files:**
- `ChartViewerWindow.xaml` - Wire up radio button events
- `ChartViewerWindow.xaml.cs` - Aggregation methods, indicator recalc, grid update

---

### **Part 3: UX Enhancements** (1-2 hours)

#### 3.1 Skip Weekend Gaps

**Goal:** Jump from Friday 23:00 to Monday 00:00 during playback (skip Sat/Sun)

**Implementation:**
```csharp
private DateTime GetNextTradingTime(DateTime currentTime)
{
    // If Friday after 23:00 or Saturday/Sunday, jump to Monday 00:00
    if (currentTime.DayOfWeek == DayOfWeek.Friday && currentTime.Hour >= 23)
    {
        return currentTime.Date.AddDays(3 - (int)currentTime.DayOfWeek);
    }
    else if (currentTime.DayOfWeek == DayOfWeek.Saturday)
    {
        return currentTime.Date.AddDays(2);
    }
    else if (currentTime.DayOfWeek == DayOfWeek.Sunday)
    {
        return currentTime.Date.AddDays(1);
    }

    return currentTime;
}

// In playback timer tick
var nextTime = GetNextTradingTime(currentTime);
// Skip bars until we reach nextTime
```

**Files:**
- `ChartViewerWindow.xaml.cs` - Add weekend skip logic to playback

---

#### 3.2 Recent Trades Sidebar Redesign

**Current:** Single panel with active trades and last 5 recent trades mixed

**Proposed:** 3-section tabbed or stacked layout

**Section 1: Active Trades**
- Shows currently open positions
- Live R-multiple updates
- Entry price, current price, TP, SL

**Section 2: Technical Indicators**
- Current RSI, ADX values
- EMA alignment status
- Market regime

**Section 3: Recent Trades (Scrollable)**
- Scrollable list of closed trades
- Not limited to last 5
- Show last 20-30 trades with scroll
- Color-coded: Green (wins), Red (losses)
- Click to highlight on chart

**Implementation:**
```xml
<!-- In ChartViewerWindow.xaml -->
<TabControl Grid.Column="1">
    <TabItem Header="Active Trades">
        <ListView x:Name="ActiveTradesList" .../>
    </TabItem>
    <TabItem Header="Indicators">
        <StackPanel x:Name="IndicatorsPanel" .../>
    </TabItem>
    <TabItem Header="Recent Trades">
        <ListView x:Name="RecentTradesList"
                  ScrollViewer.VerticalScrollBarVisibility="Auto"
                  MaxHeight="400"/>
    </TabItem>
</TabControl>
```

**Files:**
- `ChartViewerWindow.xaml` - Redesign right panel with TabControl
- `ChartViewerWindow.xaml.cs` - Update trade tracking, populate lists

---

### **Part 4: Add Pending Trade to Simple Strategy** (3-4 hours)

#### 4.1 Pending Order Types

**New Enum:**
```python
class PendingOrderType(str, Enum):
    BUY_STOP = "BUY_STOP"      # Buy when price goes above level
    SELL_STOP = "SELL_STOP"    # Sell when price goes below level
    BUY_LIMIT = "BUY_LIMIT"    # Buy when price comes down to level
    SELL_LIMIT = "SELL_LIMIT"  # Sell when price comes up to level
```

---

#### 4.2 Strategy Logic

**Simple Strategy Pending Order Conditions:**

**Buy Stop Example:**
- Detect bullish trend formation
- Place Buy Stop order 10 pips above current high
- Activate when price breaks above
- Cancel if not triggered within 5 bars

**Sell Limit Example:**
- Detect resistance level
- Place Sell Limit at resistance
- Activate when price touches level
- Cancel if not triggered within 10 bars

---

#### 4.3 Implementation

**File:** `src/strategies/simple_strategy.py`

```python
class SimpleStrategy:
    def __init__(self):
        self.pending_orders = []

    def place_pending_order(self, order_type, price, bars_valid=10):
        """Place a pending order"""
        order = {
            'type': order_type,
            'price': price,
            'placed_at': self.current_bar,
            'expires_at': self.current_bar + bars_valid,
            'status': 'pending'
        }
        self.pending_orders.append(order)
        return order

    def check_pending_orders(self, current_bar, current_price):
        """Check if any pending orders should be activated or cancelled"""
        for order in self.pending_orders:
            if order['status'] != 'pending':
                continue

            # Check expiration
            if current_bar >= order['expires_at']:
                order['status'] = 'cancelled'
                continue

            # Check activation
            if order['type'] == PendingOrderType.BUY_STOP:
                if current_price >= order['price']:
                    self.activate_order(order, current_price)
            elif order['type'] == PendingOrderType.SELL_STOP:
                if current_price <= order['price']:
                    self.activate_order(order, current_price)
            # ... similar for BUY_LIMIT and SELL_LIMIT

    def activate_order(self, order, activation_price):
        """Activate pending order as market order"""
        order['status'] = 'activated'
        order['activated_at'] = self.current_bar
        order['activation_price'] = activation_price
        # Execute as regular trade
```

**Files:**
- `src/strategies/simple_strategy.py` - Add pending order logic
- `src/backtest_engine.py` - Track pending orders separately
- `src/api/models/responses.py` - Add pending order fields to TradeRecord

---

### **Part 5: MT5 EA Copy + Results Comparison** (4-6 hours)

#### 5.1 Convert Simple Strategy to MT5 EA

**Goal:** Create MQL5 Expert Advisor that exactly matches Python Simple Strategy

**File:** `SimpleStrategy.mq5` (NEW)

**Key Components:**
1. **Input Parameters:**
   - EMA periods (20, 50, 100)
   - RSI period (14)
   - ADX period (14)
   - Risk per trade (2%)
   - Max positions (2)

2. **Indicator Handles:**
   ```cpp
   int emaFastHandle, emaMidHandle, emaSlowHandle;
   int rsiHandle, adxHandle;
   ```

3. **Entry Logic (Match Python):**
   - EMA alignment check
   - RSI overbought/oversold
   - ADX trend strength
   - Exact same conditions as Python

4. **Exit Logic (Match Python):**
   - TP at +3R
   - SL at -1R
   - Trailing stop logic (if applicable)

5. **Position Sizing:**
   - Match Python risk calculation
   - Same lot size formula

---

#### 5.2 Run MT5 Backtest

**Parameters:**
- Symbol: EURUSD
- Period: 2024.01.01 - 2024.01.31
- Timeframe: M15
- Initial Balance: $10,000
- Spread: Current broker spread
- Commission: $0 (or match broker)

**Export Results:**
- Save as CSV: `MT5_SimpleStrategy_EURUSD_Jan2024.csv`
- Include: Entry time, Exit time, Profit, R-multiple

---

#### 5.3 Results Comparison Script

**File:** `scripts/compare_mt5_results.py` (NEW)

```python
import pandas as pd

def compare_results(python_results_csv, mt5_results_csv):
    """
    Compare Python backtest results with MT5 backtest results
    """
    py_df = pd.read_csv(python_results_csv)
    mt5_df = pd.read_csv(mt5_results_csv)

    comparison = {
        'total_trades': {
            'python': len(py_df),
            'mt5': len(mt5_df),
            'diff': abs(len(py_df) - len(mt5_df)),
            'diff_pct': abs(len(py_df) - len(mt5_df)) / len(py_df) * 100
        },
        'win_rate': {
            'python': (py_df['r_multiple'] > 0).sum() / len(py_df) * 100,
            'mt5': (mt5_df['profit'] > 0).sum() / len(mt5_df) * 100,
        },
        'total_r': {
            'python': py_df['r_multiple'].sum(),
            'mt5': mt5_df['r_multiple'].sum(),
        },
        # ... more metrics
    }

    # Generate report
    print("=" * 50)
    print("PYTHON vs MT5 BACKTEST COMPARISON")
    print("=" * 50)
    # ... format and print comparison

    # Check if within acceptable threshold
    success = comparison['total_trades']['diff_pct'] < 5
    return success, comparison
```

**Success Criteria:**
- Total trades difference: <5%
- Win rate difference: <3%
- Total R difference: <10%

---

## **PHASE 6: Multi-Pair Backtesting** (6-8 hours)

### Overview
Enable running backtests across multiple currency pairs simultaneously and viewing aggregated results.

---

### 6.1 Python API Multi-Pair Endpoint

**File:** `src/api/routes/backtest.py`

**New Endpoint:**
```python
@router.post("/multi-run", tags=["Backtest"])
async def run_multi_pair_backtest(
    request: MultiPairBacktestRequest,
    background_tasks: BackgroundTasks
):
    """
    Run backtest across multiple currency pairs

    - Accepts array of symbols
    - Runs backtests in parallel
    - Returns aggregated results
    """
    task_id = str(uuid.uuid4())

    # Create task for each pair
    for symbol in request.symbols:
        sub_task_id = f"{task_id}_{symbol}"
        backtest_service.create_task(sub_task_id, {
            **request.dict(),
            'symbol': symbol
        })
        background_tasks.add_task(
            backtest_service.execute_backtest,
            sub_task_id
        )

    # Create aggregate task
    backtest_service.create_aggregate_task(task_id, request.symbols)

    return MultiPairBacktestResponse(
        task_id=task_id,
        symbols=request.symbols,
        status="queued"
    )
```

---

### 6.2 Parallel Execution

**File:** `src/backtest_engine.py`

**Enhancement:** Support running multiple symbols concurrently

```python
async def run_multi_pair_backtest(symbols, config):
    """
    Run backtests for multiple pairs in parallel
    """
    import asyncio

    tasks = []
    for symbol in symbols:
        task = asyncio.create_task(
            run_single_backtest_async(symbol, config)
        )
        tasks.append(task)

    # Wait for all to complete
    results = await asyncio.gather(*tasks)

    # Aggregate results
    aggregated = aggregate_results(results)
    return aggregated
```

---

### 6.3 Results Aggregation

**Aggregate Metrics:**
- Total trades (sum across all pairs)
- Average win rate (weighted by trades per pair)
- Total R (sum across all pairs)
- Max drawdown (worst across all pairs)
- Profit factor (aggregate wins / aggregate losses)

**Per-Pair Breakdown:**
- Individual metrics for each pair
- Best performing pair
- Worst performing pair

---

### 6.4 C# UI Multi-Select

**File:** `BacktestWindow.xaml`

**Replace Symbol ComboBox with CheckBoxes:**
```xml
<GroupBox Header="Select Symbols" Margin="10">
    <StackPanel>
        <CheckBox x:Name="EURUSD_Check" Content="EURUSD" IsChecked="True"/>
        <CheckBox x:Name="GBPUSD_Check" Content="GBPUSD"/>
        <CheckBox x:Name="USDJPY_Check" Content="USDJPY"/>
        <CheckBox x:Name="AUDUSD_Check" Content="AUDUSD"/>
        <CheckBox x:Name="USDCAD_Check" Content="USDCAD"/>
        <CheckBox x:Name="NZDUSD_Check" Content="NZDUSD"/>
    </StackPanel>
</GroupBox>
```

---

### 6.5 Aggregated Results Display

**File:** `BacktestWindow.xaml`

**New Tab: Multi-Pair Results**
```xml
<TabItem Header="Multi-Pair Summary">
    <Grid>
        <!-- Aggregated Metrics Panel -->
        <GroupBox Header="Portfolio Metrics" Grid.Row="0">
            <StackPanel>
                <TextBlock Text="{Binding TotalTradesAllPairs}"/>
                <TextBlock Text="{Binding AggregateWinRate}"/>
                <TextBlock Text="{Binding TotalRAllPairs}"/>
            </StackPanel>
        </GroupBox>

        <!-- Per-Pair Breakdown DataGrid -->
        <DataGrid x:Name="PairBreakdownGrid" Grid.Row="1"
                  AutoGenerateColumns="False">
            <DataGrid.Columns>
                <DataGridTextColumn Header="Pair" Binding="{Binding Symbol}"/>
                <DataGridTextColumn Header="Trades" Binding="{Binding TotalTrades}"/>
                <DataGridTextColumn Header="Win Rate" Binding="{Binding WinRate}"/>
                <DataGridTextColumn Header="Total R" Binding="{Binding TotalR}"/>
                <DataGridTextColumn Header="Drawdown" Binding="{Binding MaxDrawdown}"/>
            </DataGrid.Columns>
        </DataGrid>
    </Grid>
</TabItem>
```

**Files:**
- `src/api/routes/backtest.py` - Multi-pair endpoint
- `src/api/models/requests.py` - MultiPairBacktestRequest model
- `src/api/models/responses.py` - MultiPairBacktestResponse model
- `src/backtest_engine.py` - Parallel execution logic
- `BacktestWindow.xaml` - Multi-select UI
- `BacktestWindow.xaml.cs` - Handle multi-pair request/response

---

## **PHASE 7: Strategy Fixes & Enhancements** (8-10 hours)

### 7.1 Trend Rider Enhancements

#### 7.1.1 Trailing Stop Logic

**Goal:** Lock in profits as trade moves favorably

**Implementation:**
```python
def update_trailing_stop(self, trade, current_price):
    """
    Move stop loss to lock in profits

    Rules:
    - When trade reaches +1R, move SL to breakeven (entry price)
    - When trade reaches +2R, move SL to +1R
    - Continue trailing at 1R intervals
    """
    r_multiple = self.calculate_r_multiple(trade, current_price)

    if r_multiple >= 1.0 and trade['stop_loss'] < trade['entry_price']:
        # Move to breakeven
        trade['stop_loss'] = trade['entry_price']
        trade['trailing_active'] = True

    elif r_multiple >= 2.0:
        # Trail at 1R
        new_sl = trade['entry_price'] + (trade['entry_price'] - trade['initial_stop'])
        if new_sl > trade['stop_loss']:
            trade['stop_loss'] = new_sl
```

**File:** `src/strategies/trend_rider.py`

---

#### 7.1.2 Multi-Timeframe Confirmation

**Goal:** Confirm M15 signal with H1 trend alignment

**Implementation:**
```python
def check_higher_timeframe_alignment(self, m15_signal):
    """
    Check if H1 timeframe confirms M15 signal

    - Aggregate last 4 M15 bars to H1
    - Check H1 EMA alignment
    - Only take trade if both timeframes align
    """
    h1_bar = self.aggregate_to_h1(self.bars[-4:])
    h1_trend = self.detect_trend(h1_bar)

    return h1_trend == m15_signal['direction']
```

---

#### 7.1.3 Breakeven Logic

**Implementation:**
```python
def move_to_breakeven(self, trade, current_price):
    """
    Move SL to entry price once +1R is reached
    """
    r_multiple = self.calculate_r_multiple(trade, current_price)

    if r_multiple >= 1.0 and not trade.get('breakeven_set'):
        trade['stop_loss'] = trade['entry_price']
        trade['breakeven_set'] = True
        trade['exit_reason'] = 'Breakeven set'
```

**File:** `src/strategies/trend_rider.py`

---

### 7.2 Range Rider Enhancements

#### 7.2.1 Better Range Detection

**Current:** Simple high/low detection
**Enhanced:** Statistical range identification

**Implementation:**
```python
def detect_range(self, lookback=50):
    """
    Detect trading range using statistical methods

    - Calculate ATR (Average True Range)
    - Identify consolidation zones (low volatility)
    - Mark support/resistance levels
    """
    atr = self.calculate_atr(lookback)
    current_atr = atr[-1]
    avg_atr = np.mean(atr)

    # Range detected if ATR is below average
    if current_atr < avg_atr * 0.7:
        range_high = max(self.bars[-lookback:], key=lambda x: x['high'])['high']
        range_low = min(self.bars[-lookback:], key=lambda x: x['low'])['low']
        return {
            'in_range': True,
            'high': range_high,
            'low': range_low,
            'width': range_high - range_low
        }

    return {'in_range': False}
```

---

#### 7.2.2 Dynamic TP/SL Based on Range Width

**Goal:** Adjust profit targets based on range size

**Implementation:**
```python
def calculate_range_targets(self, range_info):
    """
    Set TP/SL based on range width

    - TP at 80% of range width from entry
    - SL at 30% of range width from entry
    """
    range_width = range_info['width']

    return {
        'tp_distance': range_width * 0.8,
        'sl_distance': range_width * 0.3
    }
```

**File:** `src/strategies/range_rider.py`

---

### 7.3 Risk Management Improvements

#### 7.3.1 Max Daily Loss Limit

**File:** `src/risk_manager.py` (NEW)

```python
class RiskManager:
    def __init__(self, max_daily_loss_pct=5.0):
        self.max_daily_loss_pct = max_daily_loss_pct
        self.daily_pnl = 0.0
        self.last_reset_date = None

    def check_daily_loss_limit(self, current_date, balance):
        """
        Check if daily loss limit has been reached

        Returns: True if can trade, False if limit reached
        """
        # Reset daily PnL at start of new day
        if current_date != self.last_reset_date:
            self.daily_pnl = 0.0
            self.last_reset_date = current_date

        max_loss = balance * (self.max_daily_loss_pct / 100)

        if abs(self.daily_pnl) >= max_loss:
            return False  # Stop trading for the day

        return True

    def record_trade_result(self, profit):
        self.daily_pnl += profit
```

---

#### 7.3.2 Correlation Filter

**Goal:** Avoid trading highly correlated pairs simultaneously (e.g., EURUSD + GBPUSD)

**Implementation:**
```python
CORRELATION_MATRIX = {
    'EURUSD': {'GBPUSD': 0.85, 'USDCHF': -0.90},
    'GBPUSD': {'EURUSD': 0.85},
    # ... more pairs
}

def check_correlation_conflict(self, new_pair, active_pairs):
    """
    Check if new trade would conflict with active trades

    Returns: True if safe to trade, False if high correlation
    """
    for active_pair in active_pairs:
        correlation = CORRELATION_MATRIX.get(new_pair, {}).get(active_pair, 0)

        if abs(correlation) > 0.75:
            return False  # High correlation, skip trade

    return True
```

**File:** `src/risk_manager.py`

---

### 7.4 Performance Optimizations

#### 7.4.1 Cache Indicator Calculations

**Problem:** Recalculating EMAs/RSI/ADX every bar is inefficient

**Solution:** Incremental calculation + caching

```python
class IndicatorCache:
    def __init__(self):
        self.ema_cache = {}
        self.rsi_cache = {}

    def get_ema(self, period, bars):
        """
        Get EMA from cache or calculate incrementally
        """
        cache_key = f"ema_{period}"

        if cache_key in self.ema_cache:
            # Calculate only latest bar
            return self.update_ema_incremental(
                self.ema_cache[cache_key],
                bars[-1],
                period
            )
        else:
            # Full calculation on first call
            ema = self.calculate_ema_full(bars, period)
            self.ema_cache[cache_key] = ema
            return ema
```

**File:** `src/indicators.py`

---

### 7.5 New Strategy Development

#### 7.5.1 Breakout Strategy

**Concept:** Trade range breakouts with volume confirmation

**Entry Conditions:**
- Detect consolidation range (using Range Rider logic)
- Wait for price to break above resistance or below support
- Confirm with increased volume/momentum
- Enter on breakout bar close

**Exit Conditions:**
- TP at 2x range width
- SL at opposite side of range
- Trail after +1R

**File:** `src/strategies/breakout_strategy.py` (NEW)

---

#### 7.5.2 Mean Reversion Strategy

**Concept:** Trade extreme oversold/overbought conditions

**Entry Conditions:**
- RSI < 30 (oversold) → Buy
- RSI > 70 (overbought) → Sell
- Stochastic confirms (both K and D in extreme)
- Price touching Bollinger Band

**Exit Conditions:**
- RSI returns to 50 (mean)
- TP at +2R
- SL at -1R

**File:** `src/strategies/mean_reversion_strategy.py` (NEW)

---

## Timeline Summary

| Phase | Part | Description | Hours | Priority |
|-------|------|-------------|-------|----------|
| 5.1 | 1 | Progress Slider Fix | 0.5 | 🔥 Critical |
| 5.1 | 2 | Reset Button Fix | 0.5 | 🔥 Critical |
| 5.1 | 3 | Zoom Preservation | 1 | 🔥 Critical |
| 5.2 | - | H1/H4 Timeframes | 2-3 | ⚡ High |
| 5.3 | 1 | Weekend Skip | 1 | 📊 Medium |
| 5.3 | 2 | Sidebar Redesign | 1 | 📊 Medium |
| 5.4 | - | Pending Orders | 3-4 | 📈 High |
| 5.5 | - | MT5 Validation | 4-6 | ✅ High |
| 6 | - | Multi-Pair | 6-8 | 🎯 Medium |
| 7.1 | - | Trend Rider | 2-3 | 🚀 Medium |
| 7.2 | - | Range Rider | 2-3 | 🚀 Medium |
| 7.3 | - | Risk Management | 2-3 | 🛡️ High |
| 7.4 | - | Optimizations | 1-2 | ⚡ Medium |
| 7.5 | - | New Strategies | 3-4 | 🎯 Low |
| **TOTAL** | | | **28-40 hours** | |

---

## Success Criteria

### Phase 5 Complete ✅
- [ ] Progress slider works manually
- [ ] Reset button restores initial state
- [ ] Zoom level preserved during price following
- [ ] H1 and H4 timeframes display correctly
- [ ] EMAs recalculated for each timeframe
- [ ] Weekend gaps skipped during playback
- [ ] Sidebar shows 3 sections with scrollable trades
- [ ] Pending orders implemented and tested
- [ ] MT5 backtest shows <5% discrepancy with Python

### Phase 6 Complete ✅
- [ ] Can select and run 6 pairs simultaneously
- [ ] Aggregated results display correctly
- [ ] Per-pair breakdown available
- [ ] Performance acceptable (<30s for all pairs)

### Phase 7 Complete ✅
- [ ] Trailing stops working in Trend Rider
- [ ] Multi-timeframe confirmation implemented
- [ ] Range detection improved in Range Rider
- [ ] Daily loss limit enforced
- [ ] Correlation filter prevents overexposure
- [ ] Indicator caching improves performance >50%
- [ ] 2 new strategies implemented and tested

---

## Next Steps

1. **Review and Approve Plan** ✅ (Current step)
2. **Start Phase 5.1** - Critical bug fixes
3. **Test each phase** before moving to next
4. **Document findings** after MT5 comparison
5. **Iterate on strategies** based on backtest results

---

**Document Status:** Draft - Awaiting Approval
**Created By:** Claude Code
**Date:** November 22, 2025
**Related Documents:**
- NEXT_SESSION_PLAN.md
- BugfixesEnhancementsAndSuggestion_22-11-2025.txt
- SESSION_START.md
- STATUS.md
