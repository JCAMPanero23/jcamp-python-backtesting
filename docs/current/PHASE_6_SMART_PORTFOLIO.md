# Phase 6: Smart Portfolio Viewer Implementation Plan

**Status:** In Progress - Part 1.1 Active
**Estimated Total Effort:** 16-22 hours
**Branch:** phase6-multi-pair (both repos)
**Created:** November 30, 2025
**Last Updated:** December 1, 2025

---

## Executive Summary

This plan implements a **Smart Portfolio Viewer** that:
- Runs backtests on multiple currency pairs simultaneously
- Displays one pair at a time with intelligent auto-switching based on trade activity
- Enforces portfolio-level position limits (default 3 concurrent trades, configurable)
- Prioritizes trades using CSM (Currency Strength Meter) when multiple signals compete
- Refactors Simple Test strategy to use EMA crossover + H1 confirmation

**Key Design Decisions:**
- **NOT a 2x2 grid** - Use existing single-chart layout with functional pair tabs
- Auto-switch chart display when new trades open on different pairs
- Backend parallel execution with new `/run-multi` and `/ohlc-multi` endpoints
- Extract rendering services for code reusability and maintainability
- Preserve all Phase 5.3 bug fixes (M1 viewport positioning, EMA interpolation)

---

## Architecture Overview

### Current (Single-Pair Viewer)
```
ChartViewerWindow (monolithic, 1,633 lines)
├─ State Management (19 fields for single pair)
├─ Playback Control (timer, speed, pause/resume)
├─ Rendering (candles, EMAs, trades) - INLINE, not reusable
├─ Viewport Management (M1→M15 conversion) - INLINE
├─ UI: Single chart + pair tabs (empty placeholders, lines 290-301)
└─ Trade Tracking: per-pair only
```

### Proposed (Smart Portfolio Viewer)
```
ChartViewerWindow (refactored to multi-pair, ~2,000 lines)
├─ Multi-Pair Data Management
│   ├─ Dictionary<symbol, OhlcData> - All pairs loaded simultaneously
│   ├─ Dictionary<symbol, M1Data> - M1 data per pair (auto-loaded)
│   ├─ _currentSymbol - Currently displayed pair (auto-switches)
│   └─ _portfolioTrades - Aggregated trades across all pairs
│
├─ Portfolio-Level Logic (NEW)
│   ├─ Max concurrent trades (default 3, configurable via Settings)
│   ├─ CSM-based trade prioritization (strongest signals get slots)
│   ├─ Trade allocation tracking (which slots are open/occupied)
│   └─ Cross-pair metrics (total R, portfolio win rate, strategy tally)
│
├─ Smart Auto-Switching (NEW)
│   ├─ Switch to pair when new trade opens
│   ├─ User can manually override via pair tabs
│   ├─ Synchronized playback across all pairs (single timeline)
│   └─ Each tab shows pair symbol + active trade count badge
│
└─ UI: Functional Pair Tabs
    ├─ TabControl SelectionChanged event (switch displayed pair)
    ├─ Single ScottPlot (renders currently selected pair)
    ├─ Sidebar shows aggregated data:
    │   ├─ Combined trades (all pairs, sorted by time)
    │   ├─ Active trades panel (all pairs)
    │   ├─ Portfolio metrics (total R, overall win rate)
    │   └─ Per-strategy tally (Trend Rider: +12R, Simple Test: -2R)
    └─ Settings panel (max concurrent trades slider)
```

### Backend Architecture (NEW)
```
BacktestEngine (multi-pair execution)
├─ POST /api/v1/backtest/run-multi
│   ├─ Input: List[BacktestRequest] (EURUSD, GBPUSD, USDJPY)
│   ├─ Executes backtests with portfolio-level position limits
│   ├─ CSM-based trade prioritization across pairs
│   └─ Output: Dict[symbol, taskId]
│
├─ GET /api/v1/backtest/ohlc-multi?task_ids=...
│   ├─ Input: "EURUSD:task1,GBPUSD:task2,USDJPY:task3"
│   ├─ Retrieves OHLC + trades for all pairs
│   └─ Output: Dict[symbol, OhlcData]
│
└─ PortfolioTradeAllocator (NEW service)
    ├─ Tracks open position slots (default 3 concurrent max)
    ├─ Evaluates competing signals by CSM strength
    ├─ Allocates trades FIFO with CSM tie-breaking
    └─ Rejects signals when all slots occupied
```

---

## Implementation Phases

---

## Phase 6 Part 1: Update Simple Test Strategy (2-3 hours)

**Objective:** Add EMA crossover logic with H1 confirmation

### Part 1.1 Modify Simple Test Strategy (1.5-2 hours) - CURRENT

**File:** `D:\JcampFxTrading\jcamp-python-backtesting\src\strategies\simple_test.py`

**Current Logic:** Time-based alternating BUY/SELL signals (lines 55-107)

**New Logic:**
- **Entry Signal:** M15 EMA 20 crosses M15 EMA 50
- **Confirmation:** H1 EMAs must align in same direction
- **BUY:** M15 fast crosses above mid + H1 fast > H1 mid
- **SELL:** M15 fast crosses below mid + H1 fast < H1 mid

**Implementation:**
```python
def generate_signal(self, df, current_idx, csm_data, regime):
    """
    EMA crossover strategy with H1 confirmation
    """
    # Need at least 2 bars for crossover detection
    if current_idx < 1:
        return 'NONE', 0.0, {'reason': 'Insufficient bars'}

    # Get M15 EMA values (current and previous)
    curr_fast = self._get_indicator(df, current_idx, 'ema_fast')  # EMA 20
    curr_mid = self._get_indicator(df, current_idx, 'ema_mid')   # EMA 50
    prev_fast = self._get_indicator(df, current_idx - 1, 'ema_fast')
    prev_mid = self._get_indicator(df, current_idx - 1, 'ema_mid')

    # Validate all indicators exist
    if None in [curr_fast, curr_mid, prev_fast, prev_mid]:
        return 'NONE', 0.0, {'reason': 'Missing M15 EMAs'}

    # Detect M15 crossover
    signal = 'NONE'
    if prev_fast < prev_mid and curr_fast >= curr_mid:
        signal = 'BUY'  # Bullish crossover
    elif prev_fast > prev_mid and curr_fast <= curr_mid:
        signal = 'SELL'  # Bearish crossover

    if signal == 'NONE':
        return signal, 0.0, {'reason': 'No crossover detected'}

    # H1 EMA Confirmation
    h1_fast = self._get_indicator(df, current_idx, 'ema_20_h1')
    h1_mid = self._get_indicator(df, current_idx, 'ema_50_h1')

    if h1_fast is None or h1_mid is None:
        return 'NONE', 0.0, {'reason': 'Missing H1 EMAs'}

    # Check H1 alignment
    h1_aligned = (h1_fast > h1_mid and signal == 'BUY') or \
                 (h1_fast < h1_mid and signal == 'SELL')

    if not h1_aligned:
        return 'NONE', 0.0, {
            'reason': f'H1 EMA misalignment',
            'm15_signal': signal,
            'h1_fast': h1_fast,
            'h1_mid': h1_mid
        }

    # Calculate confidence based on crossover strength
    crossover_distance = abs(curr_fast - curr_mid)
    atr = self._get_indicator(df, current_idx, 'atr')
    if atr and atr > 0:
        confidence = min(90.0, 60.0 + (crossover_distance / atr) * 30.0)
    else:
        confidence = 75.0

    details = {
        'signal_type': 'EMA_CROSSOVER',
        'm15_fast': curr_fast,
        'm15_mid': curr_mid,
        'h1_fast': h1_fast,
        'h1_mid': h1_mid,
        'crossover_strength': crossover_distance,
        'regime': regime
    }

    return signal, confidence, details
```

### Part 1.2 Test Simple Strategy Changes (0.5-1 hour)

**Testing:**
```bash
cd D:\JcampFxTrading\jcamp-python-backtesting
python -m pytest tests/test_phase2.py::test_simple_test_strategy -v
```

**Manual Test:**
- Run single-pair backtest with Simple Test strategy
- Verify trades only occur on EMA crossovers
- Check H1 confirmation is enforced
- Review trade details in results JSON

---

## Phase 6 Part 2: Backend Portfolio API (5-7 hours)

**Objective:** Create multi-pair execution with portfolio-level position limits

### Part 2.1 Create Portfolio Trade Allocator (2-3 hours)

**File:** `D:\JcampFxTrading\jcamp-python-backtesting\src\portfolio_allocator.py` (NEW)

**Responsibilities:**
- Track open position slots (configurable limit, default 3)
- Evaluate competing signals by CSM strength
- Allocate trades FIFO with CSM tie-breaking

**Implementation:**
```python
class PortfolioTradeAllocator:
    def __init__(self, max_concurrent_trades=3):
        self.max_concurrent_trades = max_concurrent_trades
        self.open_trades = []  # List of (symbol, entry_time, csm_strength)

    def can_allocate_trade(self, symbol, signal_time, csm_diff):
        """
        Check if trade can be allocated based on portfolio limits

        Returns: (can_allocate: bool, reason: str)
        """
        # Remove closed trades (simulate time-based management)
        self._cleanup_closed_trades(signal_time)

        # Check if slots available
        if len(self.open_trades) < self.max_concurrent_trades:
            return True, f"Slot available ({len(self.open_trades)}/{self.max_concurrent_trades})"

        # All slots occupied - check CSM prioritization
        weakest_trade = min(self.open_trades, key=lambda t: abs(t[2]))  # Lowest CSM strength

        if abs(csm_diff) > abs(weakest_trade[2]):
            # Current signal is stronger - replace weakest
            return True, f"Replacing weaker trade (CSM {csm_diff:.2f} > {weakest_trade[2]:.2f})"

        return False, f"All slots occupied, signal too weak (CSM {csm_diff:.2f})"

    def allocate_trade(self, symbol, entry_time, csm_diff):
        """Record trade allocation"""
        self.open_trades.append((symbol, entry_time, csm_diff))

    def close_trade(self, symbol, exit_time):
        """Remove trade from tracking"""
        self.open_trades = [t for t in self.open_trades if not (t[0] == symbol and t[1] <= exit_time)]
```

### Part 2.2 Create Multi-Pair API Endpoints (2-3 hours)

**File:** `D:\JcampFxTrading\jcamp-python-backtesting\src\api\routes\backtest.py`

#### Endpoint 1: POST `/api/v1/backtest/run-multi`

```python
@router.post("/run-multi")
async def run_multi_backtest(request: MultiBacktestRequest) -> Dict[str, str]:
    """
    Execute multiple backtests with portfolio-level position management

    Input:
    {
        "requests": [
            {symbol: "EURUSD", strategy: "simple_test", ...},
            {symbol: "GBPUSD", strategy: "simple_test", ...},
            {symbol: "USDJPY", strategy: "simple_test", ...}
        ],
        "max_concurrent_trades": 3
    }

    Output:
    {
        "EURUSD": "task_uuid_1",
        "GBPUSD": "task_uuid_2",
        "USDJPY": "task_uuid_3"
    }
    """
    from src.portfolio_allocator import PortfolioTradeAllocator

    allocator = PortfolioTradeAllocator(request.max_concurrent_trades)

    # Execute backtests with shared allocator
    task_ids = {}
    for req in request.requests:
        task_id = str(uuid.uuid4())

        # Run backtest with portfolio allocator
        backtest_service.run_backtest_with_portfolio(
            request=req,
            task_id=task_id,
            allocator=allocator
        )

        task_ids[req.symbol] = task_id

    return task_ids
```

#### Endpoint 2: GET `/api/v1/backtest/ohlc-multi`

```python
@router.get("/ohlc-multi")
async def get_multi_ohlc(task_ids: str) -> Dict[str, OhlcData]:
    """
    Retrieve OHLC data for multiple pairs

    Input: task_ids = "EURUSD:task1,GBPUSD:task2,USDJPY:task3"

    Output:
    {
        "EURUSD": {candles: [...], trades: [...]},
        "GBPUSD": {candles: [...], trades: [...]},
        "USDJPY": {candles: [...], trades: [...]}
    }
    """
    # Parse task_ids string
    task_map = {}
    for pair_task in task_ids.split(','):
        symbol, task_id = pair_task.split(':')
        task_map[symbol] = task_id

    # Retrieve OHLC for each pair in parallel
    results = {}
    tasks = [
        backtest_service.get_ohlc_data(task_id)
        for task_id in task_map.values()
    ]
    ohlc_data_list = await asyncio.gather(*tasks)

    for symbol, ohlc_data in zip(task_map.keys(), ohlc_data_list):
        results[symbol] = ohlc_data

    return results
```

### Part 2.3 Update Backtest Service (1 hour)

**File:** `D:\JcampFxTrading\jcamp-python-backtesting\src\api\services\backtest_service.py`

**New Method:**
```python
def run_backtest_with_portfolio(request: BacktestRequest, task_id: str, allocator: PortfolioTradeAllocator):
    """
    Execute backtest with portfolio-level position limits

    Modifies strategy.generate_signal() to check allocator before entry
    """
    # Standard backtest execution
    engine = BacktestEngine(request)

    # Inject allocator into strategy
    engine.strategy.portfolio_allocator = allocator

    # Run backtest (strategy will consult allocator on each signal)
    results = engine.run()

    # Store results
    _results_cache[task_id] = results

    return task_id
```

### Part 2.4 Update Models (0.5 hour)

**File:** `D:\JcampFxTrading\jcamp-python-backtesting\src\api\models\requests.py`

```python
class MultiBacktestRequest(BaseModel):
    requests: List[BacktestRequest]
    max_concurrent_trades: int = 3  # Default portfolio limit
```

---

## Phase 6 Part 3: Extract C# Services (3-4 hours)

**Objective:** Extract rendering logic for code reusability

### Part 3.1 Create ChartRenderingService (1.5-2 hours)

**File:** `D:\JcampFxTrading\CSMMonitor\JcampForexTrader\Services\ChartRenderingService.cs` (NEW)

**Methods (extract from ChartViewerWindow.xaml.cs):**

```csharp
public class ChartRenderingService
{
    // From lines 658-688
    public List<IPlottable> RenderCandlesticks(
        WpfPlot plot,
        List<CandleData> candles,
        int maxIndex)
    {
        // Exact copy from ChartViewerWindow
        // Uses sequential indices (0, 1, 2...) to eliminate weekend gaps
    }

    // From lines 711-784
    public List<IPlottable> RenderEmaSet(
        WpfPlot plot,
        List<CandleData> candles,
        string timeframe,  // "M15" or "H1"
        bool isVisible)
    {
        // Exact copy - filters NaN/Infinity, renders with color/pattern
    }

    // From lines 798-835
    public List<IPlottable> RenderClosedTrades(
        WpfPlot plot,
        List<TradeWithLevels> closedTrades,
        Dictionary<DateTime, int> indexMap,
        int currentBarIndex)
    {
        // Exact copy - plots entry/exit lines + labels
    }

    // From lines 837-926
    public List<IPlottable> RenderActiveTrades(
        WpfPlot plot,
        List<TradeWithLevels> activeTrades,
        Dictionary<DateTime, int> indexMap,
        int currentBarIndex,
        double currentClose)
    {
        // Exact copy - plots TP/SL lines + position markers
    }
}
```

**Critical:** Copy exact logic, preserve all Phase 5.3 bug fixes

### Part 3.2 Create ChartViewportManager (1-1.5 hours)

**File:** `D:\JcampFxTrading\CSMMonitor\JcampForexTrader\Services\ChartViewportManager.cs` (NEW)

**Methods:**

```csharp
public class ChartViewportManager
{
    // From lines 608-611 (playback viewport)
    public AxisLimits CalculatePlaybackViewport(
        int currentBarIndex,
        double currentXRange,
        PlaybackMode playbackMode,
        int totalBars)
    {
        // CRITICAL: M1→M15 conversion (Phase 5.3 bug fix)
        double currentM15Index = playbackMode == PlaybackMode.RealM1
            ? currentBarIndex / 15.0  // Lines 379, 423
            : currentBarIndex;

        // Position at 80% from left edge
        double barPosition = currentM15Index - (currentXRange * 0.80);
        double xLeft = Math.Max(0, barPosition);
        double xRight = xLeft + currentXRange;

        // Clamp to valid range (commit f951fc0)
        if (xLeft < 0 || xRight > totalBars)
        {
            xLeft = Math.Max(0, totalBars - 96);
            xRight = xLeft + 96;
        }

        return new AxisLimits(xLeft, xRight, yMin, yMax);
    }

    // From lines 632-654 (paused viewport)
    public AxisLimits RestoreSavedViewport(
        AxisLimits? savedLimits,
        int currentBarIndex,
        int totalBars)
    {
        // Exact copy - restore user's zoom level
    }
}
```

**Critical:** Preserve M1→M15 conversion logic (commits 2309b9d, ed49bc2, f951fc0, ec96f47)

### Part 3.3 Update ChartViewerWindow to Use Services (0.5-1 hour)

**File:** `D:\JcampFxTrading\CSMMonitor\JcampForexTrader\ChartViewerWindow.xaml.cs`

**Changes:**
- Add service fields:
  ```csharp
  private readonly ChartRenderingService _renderingService;
  private readonly ChartViewportManager _viewportManager;
  ```
- Replace inline rendering calls with service calls
- Verify identical behavior (screenshot comparison test)

---

## Phase 6 Part 4: Frontend Multi-Pair Viewer (5-7 hours)

**Objective:** Make pair tabs functional and add auto-switching logic

### Part 4.1 Update ChartViewerWindow for Multi-Pair (3-4 hours)

**File:** `D:\JcampFxTrading\CSMMonitor\JcampForexTrader\ChartViewerWindow.xaml.cs`

**New Fields:**
```csharp
// Multi-pair data
private Dictionary<string, OhlcData> _multiOhlcData;
private Dictionary<string, List<CandleData>> _multiM1Data;
private string _currentSymbol;  // Currently displayed pair
private int _maxConcurrentTrades = 3;  // Portfolio limit

// Portfolio tracking
private List<TradeWithLevels> _portfolioTrades = new List<TradeWithLevels>();
private Dictionary<string, int> _strategyTally = new Dictionary<string, int>();
```

**New Methods:**
```csharp
private void SwitchToSymbol(string symbol)
{
    if (!_multiOhlcData.ContainsKey(symbol))
        return;

    _currentSymbol = symbol;
    _ohlcData = _multiOhlcData[symbol];

    // Re-render chart for new symbol
    RenderChartUpToBar(_currentBarIndex);

    // Update tab selection
    UpdateTabSelection(symbol);
}

private void AutoSwitchOnTradeOpen()
{
    // Called during playback when new trade opens
    // Find pair with most recent trade entry
    var recentTrade = _portfolioTrades
        .OrderByDescending(t => t.GetEntryTime())
        .FirstOrDefault();

    if (recentTrade != null && recentTrade.Symbol != _currentSymbol)
    {
        SwitchToSymbol(recentTrade.Symbol);
    }
}

private void PopulatePortfolioMetrics()
{
    // Aggregate metrics across all pairs
    double totalR = _portfolioTrades.Sum(t => t.RMultiple);
    int totalTrades = _portfolioTrades.Count;
    int wins = _portfolioTrades.Count(t => t.RMultiple > 0);
    double winRate = totalTrades > 0 ? (wins / (double)totalTrades) * 100 : 0;

    // Update UI labels
    TotalRLabel.Text = $"Total R: {totalR:F2}";
    WinRateLabel.Text = $"Win Rate: {winRate:F1}%";

    // Per-strategy tally
    foreach (var kvp in _strategyTally)
    {
        StrategyTallyPanel.Children.Add(new TextBlock
        {
            Text = $"{kvp.Key}: {kvp.Value:+0;-0}R"
        });
    }
}
```

**Playback Integration:**
```csharp
private void PlaybackTimer_Tick(object sender, EventArgs e)
{
    // Advance all pairs synchronously
    foreach (var symbol in _multiOhlcData.Keys)
    {
        var ohlcData = _multiOhlcData[symbol];

        // Check for new trades at current bar
        var newTrades = ohlcData.Trades
            .Where(t => t.GetEntryBarIndex() == _currentBarIndex)
            .ToList();

        if (newTrades.Any())
        {
            // Auto-switch to pair with new trade
            AutoSwitchOnTradeOpen();
        }
    }

    // Render currently selected pair
    RenderChartUpToBar(_currentBarIndex);

    // Update portfolio metrics
    PopulatePortfolioMetrics();
}
```

### Part 4.2 Update XAML for Functional Tabs (1 hour)

**File:** `D:\JcampFxTrading\CSMMonitor\JcampForexTrader\ChartViewerWindow.xaml`

**Changes (lines 290-301):**

```xml
<TabControl Grid.Row="1" x:Name="PairTabControl"
            Background="#1E1E1E" BorderThickness="0" Padding="5,0"
            SelectionChanged="PairTabControl_SelectionChanged">

    <TabItem Header="EURUSD (0)" x:Name="EurusdTab"
             Background="#2D2D30" Foreground="White" FontSize="12">
        <!-- Tab header shows active trade count -->
    </TabItem>

    <TabItem Header="GBPUSD (1)" x:Name="GbpusdTab"
             Background="#2D2D30" Foreground="#888888" FontSize="12">
    </TabItem>

    <TabItem Header="USDJPY (0)" x:Name="UsdjpyTab"
             Background="#2D2D30" Foreground="#888888" FontSize="12">
    </TabItem>
</TabControl>
```

**Code-Behind:**
```csharp
private void PairTabControl_SelectionChanged(object sender, SelectionChangedEventArgs e)
{
    if (PairTabControl.SelectedItem is TabItem selectedTab)
    {
        string symbol = selectedTab.Header.ToString().Split(' ')[0];  // Extract "EURUSD" from "EURUSD (1)"
        SwitchToSymbol(symbol);
    }
}

private void UpdateTabHeaders()
{
    // Update tab headers with active trade count
    EurusdTab.Header = $"EURUSD ({GetActiveTradeCount("EURUSD")})";
    GbpusdTab.Header = $"GBPUSD ({GetActiveTradeCount("GBPUSD")})";
    UsdjpyTab.Header = $"USDJPY ({GetActiveTradeCount("USDJPY")})";
}
```

### Part 4.3 Update Sidebar Panels (1 hour)

**File:** `D:\JcampFxTrading\CSMMonitor\JcampForexTrader\ChartViewerWindow.xaml`

**Changes:**

```xml
<TabControl Grid.Row="0" Grid.Column="1">
    <!-- Active Trades (all pairs) -->
    <TabItem Header="Active Trades (All Pairs)">
        <DataGrid x:Name="ActiveTradesGrid" ItemsSource="{Binding ActiveTrades}">
            <DataGrid.Columns>
                <DataGridTextColumn Header="Symbol" Binding="{Binding Symbol}"/>
                <DataGridTextColumn Header="Entry" Binding="{Binding GetEntryTime}"/>
                <DataGridTextColumn Header="R-Multiple" Binding="{Binding GetLiveRMultiple}"/>
            </DataGrid.Columns>
        </DataGrid>
    </TabItem>

    <!-- Combined Trades -->
    <TabItem Header="Closed Trades (All Pairs)">
        <DataGrid x:Name="CombinedTradesGrid"/>
    </TabItem>

    <!-- Portfolio Metrics -->
    <TabItem Header="Portfolio Metrics">
        <StackPanel>
            <TextBlock x:Name="TotalRLabel" Text="Total R: 0.00"/>
            <TextBlock x:Name="WinRateLabel" Text="Win Rate: 0.0%"/>
            <TextBlock x:Name="MaxConcurrentLabel" Text="Max Concurrent: 3"/>
            <Slider x:Name="MaxConcurrentSlider" Minimum="1" Maximum="10" Value="3"/>
        </StackPanel>
    </TabItem>

    <!-- Strategy Tally -->
    <TabItem Header="Strategy Performance">
        <StackPanel x:Name="StrategyTallyPanel"/>
    </TabItem>
</TabControl>
```

### Part 4.4 Update C# API Client (0.5 hour)

**File:** `D:\JcampFxTrading\CSMMonitor\JcampForexTrader\BacktestApiClient.cs`

**New Methods:**
```csharp
public async Task<Dictionary<string, string>> RunMultiBacktestAsync(
    List<BacktestRequest> requests,
    int maxConcurrentTrades = 3)
{
    var requestBody = new
    {
        requests = requests,
        max_concurrent_trades = maxConcurrentTrades
    };

    var response = await _httpClient.PostAsJsonAsync("/api/v1/backtest/run-multi", requestBody);
    return await response.Content.ReadFromJsonAsync<Dictionary<string, string>>();
}

public async Task<Dictionary<string, OhlcData>> GetMultiOhlcDataAsync(
    Dictionary<string, string> taskIds)
{
    string taskIdsParam = string.Join(",", taskIds.Select(kvp => $"{kvp.Key}:{kvp.Value}"));
    var response = await _httpClient.GetAsync($"/api/v1/backtest/ohlc-multi?task_ids={taskIdsParam}");
    return await response.Content.ReadFromJsonAsync<Dictionary<string, OhlcData>>();
}
```

---

## Phase 6 Part 5: Integration & Testing (2-3 hours)

### Part 5.1 Update BacktestWindow (1 hour)

**File:** `D:\JcampFxTrading\CSMMonitor\JcampForexTrader\BacktestWindow.xaml.cs`

**Changes:**
```csharp
private async void ViewChartButton_Click(object sender, RoutedEventArgs e)
{
    // Build multi-pair request (default: all 3 pairs)
    var symbols = new[] { "EURUSD", "GBPUSD", "USDJPY" };
    var requests = symbols.Select(symbol => new BacktestRequest
    {
        Symbol = symbol,
        Strategy = StrategyComboBox.SelectedValue.ToString(),
        StartDate = StartDatePicker.SelectedDate.Value,
        EndDate = EndDatePicker.SelectedDate.Value,
        // ... other params
    }).ToList();

    // Execute multi-backtest
    var taskIds = await _apiClient.RunMultiBacktestAsync(requests, maxConcurrentTrades: 3);

    // Wait for completion
    await WaitForMultiBacktestCompletion(taskIds);

    // Retrieve OHLC data for all pairs
    var multiOhlcData = await _apiClient.GetMultiOhlcDataAsync(taskIds);

    // Auto-load M1 data for all pairs
    var multiM1Data = await _apiClient.GetMultiOhlcM1DataAsync(taskIds);

    // Launch chart viewer
    var chartViewer = new ChartViewerWindow(multiOhlcData, multiM1Data, taskIds);
    chartViewer.Show();
}
```

### Part 5.2 Testing Checklist (1-2 hours)

**Strategy Tests:**
- [ ] Simple Test strategy generates trades on EMA crossovers only
- [ ] H1 confirmation is enforced (no trades when H1 misaligned)
- [ ] Compare trade count vs. old time-based logic (should be fewer trades)

**Portfolio Tests:**
- [ ] Max 3 concurrent trades enforced across all pairs
- [ ] CSM prioritization works (stronger signals get slots)
- [ ] Trades rejected when slots full (check logs)

**Frontend Tests:**
- [ ] Chart auto-switches when new trade opens on different pair
- [ ] User can manually click pair tabs to override
- [ ] Tab headers show correct active trade counts
- [ ] Portfolio metrics aggregate correctly (total R, win rate)
- [ ] Strategy tally displays per-strategy performance

**Regression Tests:**
- [ ] M1 playback positions current bar at 80% (Phase 5.3 bug fix preserved)
- [ ] EMAs render identically to single-pair viewer
- [ ] Viewport zoom preserved during pause/resume
- [ ] No visual differences in single-pair mode

**Performance Tests:**
- [ ] Multi-pair backtest completes in reasonable time (< 5 seconds for 3 pairs)
- [ ] Playback is smooth (no lag during auto-switching)
- [ ] M1 data loading doesn't block UI

---

## File-by-File Summary

### New Files to Create

| File | Lines | Purpose |
|------|-------|---------|
| `src/portfolio_allocator.py` | ~200 | Portfolio-level trade allocation |
| `Services/ChartRenderingService.cs` | ~300 | Extracted rendering methods |
| `Services/ChartViewportManager.cs` | ~150 | Viewport calculation logic |

**Total New Code:** ~650 lines

### Files to Modify

| File | Lines Changed | Changes |
|------|---------------|---------|
| `simple_test.py` | ~80 | Add EMA crossover logic |
| `backtest.py` (Python) | +120 | Add `/run-multi` and `/ohlc-multi` endpoints |
| `backtest_service.py` (Python) | +60 | Add portfolio-aware backtest execution |
| `requests.py` (Python) | +15 | Add `MultiBacktestRequest` model |
| `ChartViewerWindow.xaml.cs` | +400 | Multi-pair data, auto-switching, portfolio metrics |
| `ChartViewerWindow.xaml` | +80 | Functional tabs, portfolio panels |
| `BacktestApiClient.cs` | +40 | Add multi-pair API methods |
| `BacktestWindow.xaml.cs` | +60 | Multi-pair launch logic |

**Total Modified Code:** ~855 lines

---

## Risk Mitigation

### Risk 1: M1 Viewport Bug Regression
**Mitigation:** ChartViewportManager copies exact logic from lines 379, 423 (M1→M15 conversion). Visual regression test before/after extraction.

### Risk 2: Portfolio Allocator Complexity
**Mitigation:** Unit test portfolio allocator independently. Test with 2, 3, 5 concurrent trades. Verify CSM prioritization logic.

### Risk 3: Auto-Switching UX Issues
**Mitigation:** Make auto-switching optional (user can disable). Always allow manual tab override. Add visual indicator when auto-switch occurs.

### Risk 4: Performance Degradation
**Mitigation:** Profile playback timer (target < 50ms per tick). Load M1 data asynchronously. Render only currently selected pair.

---

## Critical Notes

**Phase 5.3 Bug Fixes to Preserve:**
1. M1→M15 coordinate conversion: `currentM15Index = currentBarIndex / 15.0`
2. Viewport positioning every frame during M1 playback (commit ec96f47)
3. Left==0 condition removed from viewport reset logic (commit f951fc0)
4. H1 EMA values pre-calculated in Python (no lookahead bias)

**CSM Integration:**
- CSM already calculated in `src/csm_calculator.py` (400 lines)
- DataFrame columns: `csm_base`, `csm_quote`, `csm_diff`
- Use `csm_diff` for trade prioritization (stronger differential = higher priority)

**Simple Strategy Requirements:**
- M15 EMA 20/50 crossover for entry signal
- H1 EMA 20/50 alignment for confirmation
- If H1 misaligned, reject signal (return 'NONE')

---

## Success Criteria

- [ ] Simple Test strategy uses EMA crossover + H1 confirmation
- [ ] Portfolio enforces max 3 concurrent trades (configurable)
- [ ] CSM prioritization allocates slots to strongest signals
- [ ] Chart auto-switches to pair when new trade opens
- [ ] User can manually override auto-switching via pair tabs
- [ ] Tab headers show active trade count badges
- [ ] Portfolio metrics aggregate across all pairs
- [ ] Strategy tally displays per-strategy performance
- [ ] All Phase 5.3 bug fixes preserved (M1 viewport, EMAs)
- [ ] Single-pair viewer still works (backward compatible)

---

**End of Plan**
