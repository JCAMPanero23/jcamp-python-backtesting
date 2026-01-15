"""
Chronological Multi-Pair Backtest Orchestrator
Phase 8.6 - Bug #2 - Phase 2

Processes multiple pairs in true chronological order (bar-by-bar),
simulating realistic live trading conditions with shared position management.
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from src.backtest_engine import BacktestEngine
from src.position_manager import PositionManager


class ChronologicalOrchestrator:
    """
    Orchestrates multi-pair backtests in chronological order.

    Instead of processing pair-by-pair (EURUSD all bars, then GBPUSD all bars),
    this advances all pairs simultaneously timestamp-by-timestamp.
    """

    def __init__(
        self,
        pairs: List[str],
        strategies: List[str],
        config: Dict,
        start_date: str,
        end_date: str,
        timeframe: str = "M15"
    ):
        """
        Initialize chronological orchestrator.

        Args:
            pairs: List of trading pairs (e.g., ['EURUSD', 'GBPUSD'])
            strategies: List of strategies (e.g., ['trend_rider', 'range_rider'])
            config: Backtest configuration dict
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            timeframe: Chart timeframe (M15, H1, H4)
        """
        self.pairs = pairs
        self.strategies = strategies
        self.config = config
        self.start_date = start_date
        self.end_date = end_date
        self.timeframe = timeframe

        # Create shared PositionManager for all pairs
        self.position_manager = PositionManager(
            max_positions=config.get("max_concurrent_positions", 2)
        )

        # Storage for pair engines and data
        self.pair_engines: Dict[str, BacktestEngine] = {}
        self.pair_data: Dict[str, pd.DataFrame] = {}
        self.pair_indices: Dict[str, int] = {}  # Track current bar index per pair

        # Global timeline
        self.global_timeline: List[Tuple[datetime, str, int]] = []

        print(f"\n[CHRONO] Chronological Orchestrator initialized")
        print(f"[CHRONO] Pairs: {', '.join(pairs)}")
        print(f"[CHRONO] Strategies: {', '.join(strategies)}")
        print(f"[CHRONO] Max positions: {config.get('max_concurrent_positions', 2)}")
        print(f"[CHRONO] Date range: {start_date} to {end_date}")

    def prepare_pair_engines(self):
        """
        Load data and create BacktestEngine for each pair.
        All engines share the same PositionManager.
        """
        print(f"\n[CHRONO] Loading data for {len(self.pairs)} pairs...")

        year = self.start_date[:4]

        for pair in self.pairs:
            print(f"[CHRONO] Loading {pair}...")

            # Create engine with shared position manager
            engine = BacktestEngine(
                initial_balance=self.config.get("initial_balance", 10000.0),
                risk_percent=self.config.get("risk_percent", 2.0),
                max_positions=self.config.get("max_concurrent_positions", 2),
                timeframe=self.timeframe,
                position_manager=self.position_manager  # SHARED!
            )

            # Prepare data (loads and prepares indicators)
            df = engine.prepare_data(
                symbol=pair,
                year=year,
                start_date=self.start_date
            )

            # Apply end date filter
            if self.end_date:
                end_timestamp = pd.Timestamp(self.end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
                df = df[df.index <= end_timestamp]

            # Store engine, data, and initialize bar index
            self.pair_engines[pair] = engine
            self.pair_data[pair] = df
            self.pair_indices[pair] = engine.backtest_start_idx  # Start after warmup

            print(f"[CHRONO] ✓ {pair}: {len(df)} bars loaded, starting at index {engine.backtest_start_idx}")

        print(f"[CHRONO] All pairs loaded successfully")

    def create_global_timeline(self):
        """
        Create chronologically sorted timeline of all bars across all pairs.

        Returns list of (timestamp, pair, bar_index) tuples sorted by timestamp.
        """
        print(f"\n[CHRONO] Creating global timeline...")

        timeline = []

        for pair in self.pairs:
            df = self.pair_data[pair]
            start_idx = self.pair_indices[pair]

            # Add each bar to timeline (starting from backtest_start_idx)
            for idx in range(start_idx, len(df)):
                timestamp = df.index[idx]
                timeline.append((timestamp, pair, idx))

        # Sort chronologically by timestamp
        timeline.sort(key=lambda x: x[0])

        self.global_timeline = timeline

        print(f"[CHRONO] ✓ Global timeline created: {len(timeline)} bars")
        print(f"[CHRONO] Timeline range: {timeline[0][0]} to {timeline[-1][0]}")

        return timeline

    def process_chronologically(self, progress_callback=None):
        """
        Process all bars chronologically across all pairs.

        Args:
            progress_callback: Optional function(current, total) for progress tracking

        Returns:
            Dictionary with backtest results
        """
        print(f"\n[CHRONO] Starting chronological processing...")
        print(f"[CHRONO] Total bars to process: {len(self.global_timeline)}")

        total_bars = len(self.global_timeline)

        for bar_num, (timestamp, pair, bar_idx) in enumerate(self.global_timeline):
            # Progress update
            if bar_num % 1000 == 0 or bar_num == total_bars - 1:
                progress_pct = (bar_num / total_bars) * 100
                print(f"[CHRONO] Progress: {bar_num}/{total_bars} ({progress_pct:.1f}%) - {timestamp} - {pair}")

                if progress_callback:
                    progress_callback(bar_num, total_bars)

            # Get engine and data for this pair
            engine = self.pair_engines[pair]
            df = self.pair_data[pair]

            # Update engine's current bar index
            engine.current_bar_index = bar_idx

            # STEP 1: Check exits for ALL pairs at current price
            # (positions can be closed by any pair's price movement)
            self._check_all_exits(timestamp)

            # STEP 2: Check entry signal for THIS specific pair
            if self.position_manager.can_open_position():
                engine._check_entries(df, bar_idx, pair)

        print(f"\n[CHRONO] Chronological processing complete!")
        print(f"[CHRONO] Total trades executed: {len(self.position_manager.closed_positions)}")

        # Compile results
        return self._compile_results()

    def _check_all_exits(self, timestamp: datetime):
        """
        Check exit conditions for all open positions at current timestamp.

        This ensures positions can be closed by any pair's price movement,
        not just the pair that opened the position.
        """
        # Get all open positions
        open_positions = list(self.position_manager.open_positions.values())

        for position in open_positions:
            # Get the pair's current data
            pair_symbol = position.symbol

            if pair_symbol not in self.pair_data:
                continue

            df = self.pair_data[pair_symbol]
            engine = self.pair_engines[pair_symbol]

            # Find bar index for this timestamp (or closest)
            try:
                bar_idx = df.index.get_indexer([timestamp], method='ffill')[0]

                if bar_idx >= 0:
                    # Use engine's exit check logic
                    engine._check_exits(df, bar_idx)
            except Exception as e:
                # Timestamp not found in this pair's data - skip
                pass

    def _compile_results(self) -> Dict:
        """
        Compile results from all pair engines.

        Returns:
            Dictionary with aggregated results
        """
        print(f"\n[CHRONO] Compiling results...")

        all_trades = []
        pair_results = {}

        # Collect trades from position manager
        for position in self.position_manager.closed_positions:
            trade = {
                "position_id": position.position_id,
                "symbol": position.symbol,
                "side": position.side.value,
                "strategy": position.strategy,
                "confidence": position.confidence,
                "regime": position.regime,
                "entry_time": position.entry_time.isoformat() if isinstance(position.entry_time, datetime) else str(position.entry_time),
                "exit_time": position.exit_time.isoformat() if isinstance(position.exit_time, datetime) else str(position.exit_time),
                "entry_price": position.entry_price,
                "exit_price": position.exit_price,
                "initial_stop": position.initial_stop_loss,
                "initial_tp": position.initial_take_profit,
                "r_multiple": position.r_multiple,
                "profit_loss": position.profit_loss,
                "exit_reason": position.exit_reason.value if position.exit_reason else None
            }
            all_trades.append(trade)

        # Sort trades chronologically
        all_trades.sort(key=lambda t: t["entry_time"])

        # Calculate statistics per pair
        for pair in self.pairs:
            pair_trades = [t for t in all_trades if t["symbol"] == pair]
            pair_results[pair] = self._calculate_pair_stats(pair_trades)

        # Calculate overall statistics
        overall_stats = self._calculate_overall_stats(all_trades)

        print(f"[CHRONO] ✓ Results compiled")
        print(f"[CHRONO] Total trades: {len(all_trades)}")
        print(f"[CHRONO] Win rate: {overall_stats['win_rate']:.1f}%")
        print(f"[CHRONO] Total R: {overall_stats['total_r']:.2f}")

        return {
            "trades": all_trades,
            "pair_results": pair_results,
            "overall_stats": overall_stats,
            "pair_engines": self.pair_engines
        }

    def _calculate_pair_stats(self, trades: List[Dict]) -> Dict:
        """Calculate statistics for a single pair."""
        if not trades:
            return {
                "total_trades": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0.0,
                "total_r": 0.0,
                "avg_r": 0.0,
                "net_profit": 0.0
            }

        wins = sum(1 for t in trades if t.get("r_multiple", 0) > 0)
        losses = len(trades) - wins
        total_r = sum(t.get("r_multiple", 0) for t in trades)
        avg_r = total_r / len(trades) if trades else 0
        net_profit = sum(t.get("profit_loss", 0) for t in trades)

        return {
            "total_trades": len(trades),
            "wins": wins,
            "losses": losses,
            "win_rate": (wins / len(trades) * 100) if trades else 0,
            "total_r": total_r,
            "avg_r": avg_r,
            "net_profit": net_profit
        }

    def _calculate_overall_stats(self, trades: List[Dict]) -> Dict:
        """Calculate overall statistics across all pairs."""
        if not trades:
            return {
                "total_trades": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0.0,
                "total_r": 0.0,
                "avg_r": 0.0,
                "max_r": 0.0,
                "min_r": 0.0,
                "net_profit": 0.0,
                "initial_balance": self.config.get("initial_balance", 10000.0),
                "final_balance": self.config.get("initial_balance", 10000.0),
                "return_percent": 0.0
            }

        wins = sum(1 for t in trades if t.get("r_multiple", 0) > 0)
        losses = len(trades) - wins
        total_r = sum(t.get("r_multiple", 0) for t in trades)
        avg_r = total_r / len(trades)
        r_values = [t.get("r_multiple", 0) for t in trades]
        max_r = max(r_values) if r_values else 0
        min_r = min(r_values) if r_values else 0
        net_profit = sum(t.get("profit_loss", 0) for t in trades)
        initial_balance = self.config.get("initial_balance", 10000.0)
        final_balance = initial_balance + net_profit
        return_pct = (net_profit / initial_balance * 100) if initial_balance > 0 else 0

        return {
            "total_trades": len(trades),
            "wins": wins,
            "losses": losses,
            "win_rate": (wins / len(trades) * 100) if trades else 0,
            "total_r": total_r,
            "avg_r": avg_r,
            "max_r": max_r,
            "min_r": min_r,
            "net_profit": net_profit,
            "initial_balance": initial_balance,
            "final_balance": final_balance,
            "return_percent": return_pct
        }
