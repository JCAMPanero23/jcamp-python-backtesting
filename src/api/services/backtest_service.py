"""
Backtest Service Layer
Orchestrates backtest execution and task management
"""

import time
import traceback
import os
from typing import Dict, Optional, List
from datetime import datetime
from src.backtest_engine import BacktestEngine
from src.position_manager import PositionManager
from src.visualization.chart_generator import (
    generate_candlestick_chart,
    generate_equity_curve,
    save_charts_to_html
)
from src.api.models.requests import BacktestRequest
from src.api.models.responses import (
    BacktestStatus,
    BacktestResults,
    BacktestSummary,
    BacktestListItem,
    TradeRecord,
    StrategyBreakdown,
    EquityPoint
)


class BacktestService:
    """
    Manages backtest tasks and execution
    """

    def __init__(self):
        """Initialize service with in-memory task storage"""
        self.tasks: Dict[str, Dict] = {}

        # Create charts directory if it doesn't exist
        self.charts_dir = os.path.join(os.getcwd(), "charts")
        os.makedirs(self.charts_dir, exist_ok=True)

    def create_task(self, task_id: str, request: BacktestRequest):
        """Create a new backtest task"""
        self.tasks[task_id] = {
            "task_id": task_id,
            "status": "queued",
            "progress": 0.0,
            "message": "Task queued",
            "request": request.dict(),
            "created_at": datetime.utcnow().isoformat() + "Z",
            "started_at": None,
            "completed_at": None,
            "results": None,
            "error": None
        }

    async def execute_backtest(self, task_id: str):
        """
        Execute backtest in background

        This runs asynchronously via FastAPI BackgroundTasks
        """
        try:
            task = self.tasks.get(task_id)
            if not task:
                return

            # Mark as running
            task["status"] = "running"
            task["started_at"] = datetime.utcnow().isoformat() + "Z"
            task["message"] = "Initializing backtest..."

            # Get request parameters
            request = task["request"]

            # Initialize backtest engine
            engine = BacktestEngine(
                initial_balance=request.get("initial_balance", 10000.0),
                risk_percent=request.get("risk_percent", 2.0),
                max_positions=request.get("max_positions", 2),
                timeframe=request.get("timeframe", "M15")
            )

            # Extract year from start_date
            year = request["start_date"][:4]

            # Update progress
            task["progress"] = 10.0
            task["message"] = "Loading data..."

            # Run backtest
            # Convert strategy field to strategies list
            strategy_param = request.get("strategy", "both")
            if strategy_param == "both":
                strategies_list = ["trend_rider", "range_rider"]
            else:
                strategies_list = [strategy_param]

            results = engine.run_backtest(
                symbol=request["symbol"],
                year=year,
                start_date=request["start_date"],
                end_date=request["end_date"],
                strategies=strategies_list
            )

            task["progress"] = 90.0
            task["message"] = "Processing results..."

            # Transform results to API response format
            api_results = self._transform_results(task_id, request, results)

            # Generate charts
            task["progress"] = 95.0
            task["message"] = "Generating charts..."
            chart_path = self._generate_charts(task_id, request, results, api_results, engine)
            api_results["chart_url"] = f"/api/v1/backtest/{task_id}/charts"

            # Prepare OHLC data for chart viewer
            task["progress"] = 97.0
            task["message"] = "Preparing OHLC data..."
            # Phase 1.1: Pass pre-calculated H1 dataframe to avoid duplicate calculation
            ohlc_data = self._prepare_ohlc_data(request, api_results, engine, engine.df_h1)

            # Prepare M1 OHLC data for enhanced playback
            task["progress"] = 98.0
            task["message"] = "Preparing M1 data for enhanced playback..."
            # Phase 1.2: Pass pre-loaded M1 dataframe to avoid duplicate disk read
            m1_ohlc_data = self._prepare_m1_ohlc_data(request, engine, engine.df_m1)

            # Mark as complete
            task["status"] = "complete"
            task["progress"] = 100.0
            task["message"] = "Backtest completed successfully"
            task["completed_at"] = datetime.utcnow().isoformat() + "Z"
            task["results"] = api_results
            task["chart_path"] = chart_path
            task["ohlc_data"] = ohlc_data
            task["m1_ohlc_data"] = m1_ohlc_data

        except Exception as e:
            # Mark as failed
            task["status"] = "failed"
            task["message"] = f"Backtest failed: {str(e)}"
            task["error"] = {
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            print(f"Backtest {task_id} failed: {e}")
            traceback.print_exc()

    async def execute_multi_pair_backtest(self, task_id: str):
        """
        Execute multi-pair backtest in background.

        Runs separate backtests for each pair, then merges trades chronologically
        and calculates aggregate statistics.
        """
        try:
            task = self.tasks.get(task_id)
            if not task:
                return

            # Mark as running
            task["status"] = "running"
            task["started_at"] = datetime.utcnow().isoformat() + "Z"
            task["message"] = "Starting multi-pair backtest..."
            task["progress"] = 0.0

            # Get request parameters
            request = task["request"]
            pairs = request["pairs"]
            strategies = request["strategies"]
            config = request["config"]

            print(f"\n[MULTI-PAIR] Starting backtest for {len(pairs)} pairs × {len(strategies)} strategies")
            print(f"[MULTI-PAIR] Pairs: {', '.join(pairs)}")
            print(f"[MULTI-PAIR] Strategies: {', '.join(strategies)}")
            print(f"[MULTI-PAIR] Date range: {request['start_date']} to {request['end_date']}")

            # Track progress
            total_backtests = len(pairs) * len(strategies)
            completed_backtests = 0

            # Storage for all results
            all_trades = []
            pair_results = {}  # pair -> {strategy -> results}
            strategy_results = {}  # strategy -> aggregated results

            # Run backtest for each pair + strategy combination
            for pair in pairs:
                pair_results[pair] = {}

                for strategy in strategies:
                    task["progress"] = (completed_backtests / total_backtests) * 90.0
                    task["message"] = f"Processing {pair} - {strategy}..."
                    print(f"\n[MULTI-PAIR] [{completed_backtests + 1}/{total_backtests}] Running {pair} - {strategy}")

                    # Initialize backtest engine
                    engine = BacktestEngine(
                        initial_balance=config.get("initial_balance", 10000.0),
                        risk_percent=config.get("risk_percent", 2.0),
                        max_positions=config.get("max_concurrent_positions", 2),
                        timeframe=request.get("timeframe", "M15")
                    )

                    # Extract year from start_date
                    year = request["start_date"][:4]

                    # Run backtest for this pair+strategy
                    results = engine.run_backtest(
                        symbol=pair,
                        year=year,
                        start_date=request["start_date"],
                        end_date=request["end_date"]
                    )

                    # Store results
                    pair_results[pair][strategy] = results

                    # Add trades to master list (with pair info)
                    for trade in results.get("trades", []):
                        trade_copy = trade.copy()
                        trade_copy["symbol"] = pair
                        all_trades.append(trade_copy)

                    completed_backtests += 1
                    print(f"[MULTI-PAIR] ✓ {pair} - {strategy}: {results['performance']['total_trades']} trades, {results['performance']['total_r']:.2f}R")

            # Sort all trades chronologically
            task["progress"] = 92.0
            task["message"] = "Merging trades chronologically..."
            print(f"\n[MULTI-PAIR] Merging {len(all_trades)} trades chronologically...")

            all_trades.sort(key=lambda t: t["entry_time"])

            # Calculate aggregate statistics
            task["progress"] = 95.0
            task["message"] = "Calculating statistics..."
            print(f"[MULTI-PAIR] Calculating aggregate statistics...")

            aggregate_stats = self._calculate_multi_pair_statistics(
                all_trades,
                pair_results,
                pairs,
                strategies,
                config.get("initial_balance", 10000.0)
            )

            # Transform to API format
            task["progress"] = 98.0
            task["message"] = "Formatting results..."

            api_results = self._transform_multi_pair_results(
                task_id,
                request,
                all_trades,
                aggregate_stats
            )

            # Mark as complete
            task["status"] = "complete"
            task["progress"] = 100.0
            task["message"] = f"Multi-pair backtest completed: {len(all_trades)} trades across {len(pairs)} pairs"
            task["completed_at"] = datetime.utcnow().isoformat() + "Z"
            task["results"] = api_results

            print(f"\n[MULTI-PAIR] ✅ COMPLETE")
            print(f"[MULTI-PAIR] Total trades: {len(all_trades)}")
            print(f"[MULTI-PAIR] Total R: {aggregate_stats['total_r']:.2f}")
            print(f"[MULTI-PAIR] Win rate: {aggregate_stats['win_rate']:.1f}%")
            print(f"[MULTI-PAIR] Final balance: ${aggregate_stats['final_balance']:.2f}")

        except Exception as e:
            # Mark as failed
            task["status"] = "failed"
            task["message"] = f"Multi-pair backtest failed: {str(e)}"
            task["error"] = {
                "error": str(e),
                "traceback": traceback.format_exc()
            }
            print(f"[MULTI-PAIR] ❌ FAILED: {e}")
            traceback.print_exc()

    def _calculate_multi_pair_statistics(
        self,
        all_trades: List[Dict],
        pair_results: Dict,
        pairs: List[str],
        strategies: List[str],
        initial_balance: float
    ) -> Dict:
        """
        Calculate aggregate statistics across all pairs and strategies.

        Returns:
            Dictionary with overall stats, pair breakdowns, and strategy breakdowns
        """
        import numpy as np

        # Overall statistics
        total_trades = len(all_trades)
        wins = sum(1 for t in all_trades if t.get("r_multiple", 0) > 0)
        losses = sum(1 for t in all_trades if t.get("r_multiple", 0) < 0)
        total_r = sum(t.get("r_multiple", 0) for t in all_trades)
        avg_r = total_r / total_trades if total_trades > 0 else 0
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0

        r_multiples = [t.get("r_multiple", 0) for t in all_trades if t.get("r_multiple") is not None]
        max_r = max(r_multiples) if r_multiples else 0
        min_r = min(r_multiples) if r_multiples else 0

        # Calculate P&L
        total_pl = sum(t.get("profit_loss", 0) for t in all_trades if t.get("profit_loss"))
        final_balance = initial_balance + total_pl
        return_pct = (total_pl / initial_balance * 100) if initial_balance > 0 else 0

        # Profit factor
        winning_pl = sum(t.get("profit_loss", 0) for t in all_trades if t.get("profit_loss", 0) > 0)
        losing_pl = abs(sum(t.get("profit_loss", 0) for t in all_trades if t.get("profit_loss", 0) < 0))
        profit_factor = (winning_pl / losing_pl) if losing_pl > 0 else 0

        # Drawdown (simplified - track equity curve)
        equity = initial_balance
        peak_equity = initial_balance
        max_drawdown_dollars = 0
        max_drawdown_pct = 0

        for trade in all_trades:
            pl = trade.get("profit_loss", 0)
            if pl:
                equity += pl
                if equity > peak_equity:
                    peak_equity = equity
                drawdown = peak_equity - equity
                if drawdown > max_drawdown_dollars:
                    max_drawdown_dollars = drawdown
                    max_drawdown_pct = (drawdown / peak_equity * 100) if peak_equity > 0 else 0

        # Consecutive wins/losses
        consecutive_wins = 0
        consecutive_losses = 0
        max_consecutive_wins = 0
        max_consecutive_losses = 0

        for trade in all_trades:
            r = trade.get("r_multiple", 0)
            if r > 0:
                consecutive_wins += 1
                consecutive_losses = 0
                max_consecutive_wins = max(max_consecutive_wins, consecutive_wins)
            elif r < 0:
                consecutive_losses += 1
                consecutive_wins = 0
                max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)

        # Sharpe ratio (simplified - assumes daily returns)
        if r_multiples and len(r_multiples) > 1:
            sharpe_ratio = np.mean(r_multiples) / np.std(r_multiples) if np.std(r_multiples) > 0 else 0
        else:
            sharpe_ratio = 0

        # Strategy breakdowns
        strategy_breakdown = {}
        for strategy in strategies:
            # Normalize: request has 'trend_rider', trades have 'TREND_RIDER'
            strategy_upper = strategy.upper()
            strategy_trades = [t for t in all_trades if t.get("strategy", "").upper() == strategy_upper]

            if strategy_trades:
                strat_wins = sum(1 for t in strategy_trades if t.get("r_multiple", 0) > 0)
                strat_losses = sum(1 for t in strategy_trades if t.get("r_multiple", 0) < 0)
                strat_total_r = sum(t.get("r_multiple", 0) for t in strategy_trades)
                strat_total_pl = sum(t.get("profit_loss", 0) for t in strategy_trades if t.get("profit_loss"))

                strategy_breakdown[strategy] = {
                    "trades": len(strategy_trades),
                    "wins": strat_wins,
                    "losses": strat_losses,
                    "total_r": strat_total_r,
                    "total_pl": strat_total_pl,
                    "win_rate": (strat_wins / len(strategy_trades) * 100) if strategy_trades else 0,
                    "avg_r": (strat_total_r / len(strategy_trades)) if strategy_trades else 0
                }

        # Pair breakdowns
        pair_breakdown = {}
        for pair in pairs:
            pair_trades = [t for t in all_trades if t.get("symbol") == pair]

            if pair_trades:
                pair_wins = sum(1 for t in pair_trades if t.get("r_multiple", 0) > 0)
                pair_losses = sum(1 for t in pair_trades if t.get("r_multiple", 0) < 0)
                pair_total_r = sum(t.get("r_multiple", 0) for t in pair_trades)
                pair_total_pl = sum(t.get("profit_loss", 0) for t in pair_trades if t.get("profit_loss"))

                pair_breakdown[pair] = {
                    "pair": pair,
                    "trades": len(pair_trades),
                    "wins": pair_wins,
                    "losses": pair_losses,
                    "total_r": pair_total_r,
                    "total_pl": pair_total_pl,
                    "win_rate": (pair_wins / len(pair_trades) * 100) if pair_trades else 0,
                    "avg_r": (pair_total_r / len(pair_trades)) if pair_trades else 0
                }

        return {
            "initial_balance": initial_balance,
            "final_balance": final_balance,
            "net_profit": total_pl,
            "return_pct": return_pct,
            "total_trades": total_trades,
            "winning_trades": wins,
            "losing_trades": losses,
            "win_rate": win_rate,
            "total_r": total_r,
            "avg_r": avg_r,
            "max_r": max_r,
            "min_r": min_r,
            "max_drawdown_pct": max_drawdown_pct,
            "max_drawdown_dollars": max_drawdown_dollars,
            "profit_factor": profit_factor,
            "sharpe_ratio": sharpe_ratio,
            "max_consecutive_wins": max_consecutive_wins,
            "max_consecutive_losses": max_consecutive_losses,
            "strategy_breakdown": strategy_breakdown,
            "pair_breakdown": pair_breakdown
        }

    def _transform_multi_pair_results(
        self,
        task_id: str,
        request: Dict,
        all_trades: List[Dict],
        aggregate_stats: Dict
    ) -> Dict:
        """
        Transform multi-pair results to API response format.
        """
        # Transform trades
        api_trades = []
        for trade in all_trades:
            api_trades.append({
                "position_id": trade["position_id"],
                "symbol": trade["symbol"],
                "side": trade["side"],
                "strategy": trade["strategy"],
                "confidence": trade.get("confidence", 0.0),
                "regime": trade.get("regime", "UNKNOWN"),
                "entry_time": trade["entry_time"].isoformat() if isinstance(trade["entry_time"], datetime) else trade["entry_time"],
                "exit_time": trade["exit_time"].isoformat() if trade.get("exit_time") and isinstance(trade["exit_time"], datetime) else trade.get("exit_time"),
                "entry_price": trade["entry_price"],
                "exit_price": trade.get("exit_price"),
                "stop_loss": trade.get("initial_stop"),
                "take_profit": trade.get("initial_tp"),
                "r_multiple": trade.get("r_multiple"),
                "profit_loss": trade.get("profit_loss"),
                "exit_reason": trade.get("exit_reason")
            })

        # Build equity curve (chronological cumulative R)
        api_equity = []
        cumulative_r = 0
        balance = aggregate_stats["initial_balance"]

        for trade in all_trades:
            if trade.get("exit_time"):
                r_mult = trade.get("r_multiple", 0)
                pl = trade.get("profit_loss", 0)
                cumulative_r += r_mult
                balance += pl

                api_equity.append({
                    "timestamp": trade["exit_time"].isoformat() if isinstance(trade["exit_time"], datetime) else trade["exit_time"],
                    "balance": balance,
                    "r_multiple": r_mult,
                    "cumulative_r": cumulative_r,
                    "strategy": trade.get("strategy", "UNKNOWN")
                })

        return {
            "task_id": task_id,
            "pairs": request["pairs"],
            "strategies": request["strategies"],
            "start_date": request["start_date"],
            "end_date": request["end_date"],
            "initial_balance": aggregate_stats["initial_balance"],
            "final_balance": aggregate_stats["final_balance"],
            "net_profit": aggregate_stats["net_profit"],
            "return_pct": aggregate_stats["return_pct"],
            "total_trades": aggregate_stats["total_trades"],
            "winning_trades": aggregate_stats["winning_trades"],
            "losing_trades": aggregate_stats["losing_trades"],
            "win_rate": aggregate_stats["win_rate"],
            "total_r": aggregate_stats["total_r"],
            "avg_r": aggregate_stats["avg_r"],
            "max_r": aggregate_stats["max_r"],
            "min_r": aggregate_stats["min_r"],
            "max_drawdown_pct": aggregate_stats["max_drawdown_pct"],
            "max_drawdown_dollars": aggregate_stats["max_drawdown_dollars"],
            "profit_factor": aggregate_stats["profit_factor"],
            "sharpe_ratio": aggregate_stats["sharpe_ratio"],
            "max_consecutive_wins": aggregate_stats["max_consecutive_wins"],
            "max_consecutive_losses": aggregate_stats["max_consecutive_losses"],
            "strategy_breakdown": aggregate_stats["strategy_breakdown"],
            "pair_breakdown": aggregate_stats["pair_breakdown"],
            "trades": api_trades,
            "equity_curve": api_equity
        }

    def _transform_results(self, task_id: str, request: Dict, results: Dict) -> Dict:
        """Transform BacktestEngine results to API response format"""

        performance = results["performance"]
        strategies = results.get("strategies", {})
        trades_list = results.get("trades", [])
        equity = results.get("equity_curve", [])

        # Transform trades
        api_trades = []
        for trade in trades_list:
            api_trades.append({
                "position_id": trade["position_id"],
                "symbol": trade["symbol"],
                "side": trade["side"],
                "strategy": trade["strategy"],
                "confidence": trade.get("confidence", 0.0),
                "regime": trade.get("regime", "UNKNOWN"),
                "entry_time": trade["entry_time"].isoformat() if isinstance(trade["entry_time"], datetime) else trade["entry_time"],
                "exit_time": trade["exit_time"].isoformat() if trade.get("exit_time") and isinstance(trade["exit_time"], datetime) else trade.get("exit_time"),
                "entry_price": trade["entry_price"],
                "exit_price": trade.get("exit_price"),
                "stop_loss": trade.get("initial_stop"),
                "take_profit": trade.get("initial_tp"),
                "r_multiple": trade.get("r_multiple"),
                "profit_loss": trade.get("profit_loss"),
                "exit_reason": trade.get("exit_reason")
            })

        # Transform equity curve
        api_equity = []
        for point in equity:
            api_equity.append({
                "timestamp": point["timestamp"].isoformat() if isinstance(point["timestamp"], datetime) else point["timestamp"],
                "balance": point["balance"],
                "r_multiple": point.get("r_multiple", 0.0),
                "cumulative_r": point.get("cumulative_r", 0.0),
                "strategy": point.get("strategy", "UNKNOWN")
            })

        # Transform strategy breakdown
        def transform_strategy(strat_data):
            if not strat_data:
                return None
            return {
                "trades": strat_data["trades"],
                "wins": strat_data["wins"],
                "losses": strat_data["losses"],
                "total_r": strat_data["total_r"],
                "total_pl": strat_data.get("total_pl", 0.0),
                "win_rate": strat_data.get("win_rate", 0.0),
                "avg_r": strat_data.get("avg_r", 0.0)
            }

        return {
            "task_id": task_id,
            "symbol": request["symbol"],
            "start_date": request["start_date"],
            "end_date": request["end_date"],
            "strategy": request.get("strategy", "both"),
            "initial_balance": performance["initial_balance"],
            "final_balance": performance["final_balance"],
            "net_profit": performance["net_profit"],
            "return_pct": performance["return_pct"],
            "total_trades": performance["total_trades"],
            "winning_trades": performance["winning_trades"],
            "losing_trades": performance["losing_trades"],
            "win_rate": performance["win_rate"],
            "total_r": performance["total_r"],
            "avg_r": performance.get("avg_r", 0.0),
            "max_r": performance.get("max_r", 0.0),
            "min_r": performance.get("min_r", 0.0),
            "max_drawdown_pct": performance.get("max_drawdown_pct", 0.0),
            "max_drawdown_dollars": performance.get("max_drawdown_dollars", 0.0),
            "profit_factor": performance.get("profit_factor", 0.0),
            "sharpe_ratio": performance.get("sharpe_ratio", 0.0),
            "max_consecutive_wins": performance.get("max_consecutive_wins", 0),
            "max_consecutive_losses": performance.get("max_consecutive_losses", 0),
            "trend_rider": transform_strategy(strategies.get("TREND_RIDER")),
            "range_rider": transform_strategy(strategies.get("RANGE_RIDER")),
            "trades": api_trades,
            "equity_curve": api_equity
        }

    def _generate_charts(
        self,
        task_id: str,
        request: Dict,
        engine_results: Dict,
        api_results: Dict,
        engine: 'BacktestEngine'
    ) -> str:
        """
        Generate interactive charts for backtest results.

        Returns path to saved HTML file
        """
        try:
            import pandas as pd

            # Get OHLC data from engine
            df = engine.df.copy()

            # Extract indicators from dataframe
            indicators = {}
            if 'ema_fast' in df.columns:
                indicators['EMA_Fast'] = df['ema_fast']
            if 'ema_mid' in df.columns:
                indicators['EMA_Mid'] = df['ema_mid']
            if 'ema_slow' in df.columns:
                indicators['EMA_Slow'] = df['ema_slow']
            if 'rsi' in df.columns:
                indicators['RSI'] = df['rsi']
            if 'adx' in df.columns:
                indicators['ADX'] = df['adx']

            # Generate candlestick chart
            candlestick_fig = generate_candlestick_chart(
                df=df,
                trades=api_results['trades'],
                indicators=indicators,
                symbol=request['symbol'],
                title_suffix=f"({request['start_date']} to {request['end_date']})"
            )

            # Generate equity curve
            equity_fig = generate_equity_curve(
                equity_data=api_results['equity_curve'],
                trades=api_results['trades'],
                initial_balance=request.get('initial_balance', 10000.0),
                symbol=request['symbol']
            )

            # Save charts to HTML
            chart_filename = f"backtest_{task_id}.html"
            chart_path = os.path.join(self.charts_dir, chart_filename)
            save_charts_to_html(candlestick_fig, equity_fig, chart_path)

            print(f"[OK] Charts generated: {chart_path}")
            return chart_path

        except Exception as e:
            print(f"[WARN] Chart generation failed: {e}")
            traceback.print_exc()
            return None

    def _prepare_ohlc_data(
        self,
        request: Dict,
        api_results: Dict,
        engine: 'BacktestEngine',
        df_h1: 'pd.DataFrame'
    ) -> Dict:
        """
        Prepare OHLC candlestick data for C# chart viewer.

        Returns comprehensive data for visual playback including:
        - Candlestick OHLC data
        - Indicator values (EMAs, RSI, ADX)
        - Trade information with TP/SL levels
        """
        try:
            import pandas as pd

            # Get OHLC dataframe from engine
            df_full = engine.df.copy()

            # CRITICAL FIX: Calculate H1 EMAs on FULL dataset (with warmup) for accurate values
            # Then skip warmup bars before sending to C#
            backtest_start_idx = getattr(engine, 'backtest_start_idx', 0)

            print(f"\n[OHLC DATA] Full dataset: {len(df_full)} bars (includes warmup)")

            # Phase 1.1: Use pre-calculated H1 EMAs from engine (eliminates 120-180s duplicate calculation)
            # H1 EMAs were already calculated in backtest_engine.py using vectorized operations
            # This df_full already contains the interpolated ema_20_h1, ema_50_h1, ema_100_h1 columns
            print(f"[PERF] Using pre-calculated H1 EMAs from engine (saved 120-180s)")

            # Now filter to backtest period (skip warmup)
            df = df_full.iloc[backtest_start_idx:].copy()
            print(f"[OHLC DATA] After warmup skip: {len(df)} bars")

            # WEEKEND FILTERING: Remove Saturday and Sunday bars for cleaner visualization
            # In pandas, dayofweek: Monday=0, Tuesday=1, ..., Saturday=5, Sunday=6
            bars_before_weekend_filter = len(df)
            df = df[df.index.dayofweek < 5]  # Keep only Mon-Fri (0-4)
            bars_after_weekend_filter = len(df)
            weekend_bars_removed = bars_before_weekend_filter - bars_after_weekend_filter

            print(f"[OHLC DATA] Weekend filtering: Removed {weekend_bars_removed} bars (Sat/Sun)")
            print(f"[OHLC DATA] Sending to C#: {len(df)} bars (weekdays only)")

            # DEBUG: Print last 5 bars to see if EMAs exist
            print(f"[DEBUG] Last 5 bars EMA status:")
            for i in range(-5, 0):
                idx = df.index[i]
                row = df.iloc[i]
                print(f"  Bar {i}: {idx} | M15_EMA20={row.get('ema_fast', 'MISSING')} | H1_EMA100={row.get('ema_100_h1', 'MISSING')}")

            # Prepare candlestick data
            candles = []
            for idx, row in df.iterrows():
                candle = {
                    "timestamp": idx.isoformat() if isinstance(idx, datetime) else idx,
                    "open": float(row['open']),
                    "high": float(row['high']),
                    "low": float(row['low']),
                    "close": float(row['close']),
                    # M15 EMAs
                    "ema_fast": float(row.get('ema_fast', 0)) if not pd.isna(row.get('ema_fast', 0)) else None,
                    "ema_mid": float(row.get('ema_mid', 0)) if not pd.isna(row.get('ema_mid', 0)) else None,
                    "ema_slow": float(row.get('ema_slow', 0)) if not pd.isna(row.get('ema_slow', 0)) else None,
                    # H1 EMAs (pre-calculated with warmup)
                    "ema_20_h1": float(row.get('ema_20_h1', 0)) if not pd.isna(row.get('ema_20_h1', 0)) else None,
                    "ema_50_h1": float(row.get('ema_50_h1', 0)) if not pd.isna(row.get('ema_50_h1', 0)) else None,
                    "ema_100_h1": float(row.get('ema_100_h1', 0)) if not pd.isna(row.get('ema_100_h1', 0)) else None,
                    # Other indicators
                    "rsi": float(row.get('rsi', 50)) if not pd.isna(row.get('rsi', 50)) else 50.0,
                    "adx": float(row.get('adx', 0)) if not pd.isna(row.get('adx', 0)) else None
                }
                candles.append(candle)

            # Prepare trade data with TP/SL levels
            trades_with_levels = []
            for trade in api_results['trades']:
                r_mult = trade.get('r_multiple', 0)
                trade_data = {
                    "ticket_number": int(trade['position_id']),
                    "symbol": str(trade['symbol']),
                    "side": str(trade['side']),
                    "strategy": str(trade['strategy']),
                    "entry_time": str(trade['entry_time']),
                    "exit_time": str(trade['exit_time']) if trade.get('exit_time') else None,
                    "entry_price": float(trade['entry_price']),
                    "exit_price": float(trade['exit_price']) if trade.get('exit_price') else None,
                    "stop_loss": float(trade.get('stop_loss')) if trade.get('stop_loss') else None,
                    "take_profit": float(trade.get('take_profit')) if trade.get('take_profit') else None,
                    "r_multiple": float(r_mult) if r_mult is not None else None,
                    "profit_loss": float(trade.get('profit_loss')) if trade.get('profit_loss') else None,
                    "exit_reason": str(trade.get('exit_reason')) if trade.get('exit_reason') else None,
                    "is_win": bool(float(r_mult) > 0) if r_mult is not None else False
                }
                trades_with_levels.append(trade_data)

            result = {
                "symbol": request['symbol'],
                "start_date": request['start_date'],
                "end_date": request['end_date'],
                "timeframe": request.get('timeframe', 'M15'),
                "candles": candles,
                "trades": trades_with_levels,
                "pip_size": 0.0001,  # For most pairs
                "decimal_places": 5
            }

            print(f"[OK] OHLC data prepared: {len(candles)} candles, {len(trades_with_levels)} trades")
            return result

        except Exception as e:
            print(f"[WARN] OHLC data preparation failed: {e}")
            traceback.print_exc()
            return {
                "symbol": request.get('symbol', 'UNKNOWN'),
                "candles": [],
                "trades": [],
                "error": str(e)
            }

    def _prepare_m1_ohlc_data(
        self,
        request: Dict,
        engine: 'BacktestEngine',
        df_m1: 'pd.DataFrame'
    ) -> Dict:
        """
        Prepare M1 (1-minute) OHLC data for enhanced chart playback.

        Returns M1-level candlestick data for smooth price movement visualization.
        """
        try:
            # Phase 1.2: Use pre-loaded M1 dataframe from engine (eliminates 30-60s disk I/O)
            # M1 data was already loaded in backtest_engine.py, no need to reload from CSV
            print(f"[PERF] Using pre-loaded M1 data from engine (saved 30-60s disk I/O)")
            symbol = request["symbol"]
            m1_df = df_m1  # Already loaded and passed from engine

            # Filter M1 data to EXACT same timestamp range as M15 data (after warmup)
            # This ensures M1 and M15 data are perfectly aligned
            import pandas as pd

            # Get the actual M15 dataframe from engine (after warmup skip)
            backtest_start_idx = getattr(engine, 'backtest_start_idx', 0)
            m15_df = engine.df.iloc[backtest_start_idx:].copy()

            # WEEKEND FILTERING: Filter weekends from M15 reference data
            # This must match the filtering done in _prepare_ohlc_data
            m15_bars_before = len(m15_df)
            m15_df = m15_df[m15_df.index.dayofweek < 5]  # Keep Mon-Fri only
            m15_bars_after = len(m15_df)
            print(f"[M1 DEBUG] M15 weekend filter: {m15_bars_before} -> {m15_bars_after} bars ({m15_bars_before - m15_bars_after} weekends removed)")

            # Use M15 timestamps to filter M1 data
            m15_start_time = m15_df.index[0]
            m15_end_time = m15_df.index[-1]

            print(f"\n{'='*80}")
            print(f"[M1 DEBUG] M15 DATAFRAME ANALYSIS")
            print(f"{'='*80}")
            print(f"[M1 DEBUG] Total M15 bars (after warmup skip): {len(m15_df)}")
            print(f"[M1 DEBUG] M15 start time: {m15_start_time}")
            print(f"[M1 DEBUG] M15 end time:   {m15_end_time}")
            print(f"[M1 DEBUG] First 3 M15 timestamps:")
            for i in range(min(3, len(m15_df))):
                print(f"  [{i}] {m15_df.index[i]}")
            print(f"[M1 DEBUG] Last 3 M15 timestamps:")
            for i in range(max(0, len(m15_df)-3), len(m15_df)):
                print(f"  [{i}] {m15_df.index[i]}")

            # Filter M1 to match M15 range EXACTLY (each M15 bar contains 15 M1 bars)
            # M15 bar at 10:00 contains M1 bars from 10:00 to 10:14
            # So we need M1 bars from m15_start_time to m15_end_time + 14 minutes
            m1_end_time = m15_end_time + pd.Timedelta(minutes=14)

            print(f"\n[M1 DEBUG] RAW M1 DATA BEFORE FILTERING")
            print(f"[M1 DEBUG] Total raw M1 bars loaded: {len(m1_df)}")
            print(f"[M1 DEBUG] Raw M1 first timestamp: {m1_df.index[0]}")
            print(f"[M1 DEBUG] Raw M1 last timestamp:  {m1_df.index[-1]}")

            print(f"\n[M1 DEBUG] FILTERING M1 DATA")
            print(f"[M1 DEBUG] Filter range: {m15_start_time} to {m1_end_time}")

            m1_df_filtered = m1_df.loc[m15_start_time:m1_end_time]

            print(f"\n[M1 DEBUG] FILTERED M1 DATA RESULTS (BEFORE FORWARD-FILL)")
            print(f"[M1 DEBUG] Filtered M1 bars: {len(m1_df_filtered)}")
            print(f"[M1 DEBUG] Expected M1 bars: {len(m15_df) * 15} ({len(m15_df)} M15 × 15)")
            print(f"[M1 DEBUG] Missing M1 bars: {(len(m15_df) * 15) - len(m1_df_filtered)}")
            print(f"[M1 DEBUG] Filtered M1 first timestamp: {m1_df_filtered.index[0]}")
            print(f"[M1 DEBUG] Filtered M1 last timestamp:  {m1_df_filtered.index[-1]}")

            # Check if we're missing M1 bars at the end
            if len(m1_df_filtered) < len(m15_df) * 15:
                missing_count = (len(m15_df) * 15) - len(m1_df_filtered)
                missing_m15_equivalent = missing_count / 15
                print(f"\n[M1 DEBUG] [WARN] WARNING: Missing {missing_count} M1 bars ({missing_m15_equivalent:.1f} M15 bars equivalent)")

                # Check last 5 M15 bars to see which ones have missing M1 data
                print(f"[M1 DEBUG] Checking last 5 M15 bars for M1 coverage:")
                for i in range(max(0, len(m15_df)-5), len(m15_df)):
                    m15_ts = m15_df.index[i]
                    m15_end_ts = m15_ts + pd.Timedelta(minutes=14)
                    m1_in_period = m1_df_filtered.loc[m15_ts:m15_end_ts]
                    print(f"  M15[{i}] {m15_ts}: {len(m1_in_period)} M1 bars (expected 15)")
                    if len(m1_in_period) < 15:
                        # Show which M1 bars are present
                        expected_times = [m15_ts + pd.Timedelta(minutes=j) for j in range(15)]
                        actual_times = m1_in_period.index.tolist()
                        missing_times = [t for t in expected_times if t not in actual_times]
                        if missing_times:
                            print(f"    MISSING M1 timestamps: {[str(t) for t in missing_times]}")

                # Check if the raw M1 file has data beyond m1_end_time
                m1_beyond_filter = m1_df.loc[m1_end_time:]
                print(f"\n[M1 DEBUG] Raw M1 bars AFTER filter end time ({m1_end_time}): {len(m1_beyond_filter)}")
                if len(m1_beyond_filter) > 0:
                    print(f"[M1 DEBUG] So the raw CSV HAS more M1 data available")
                    print(f"[M1 DEBUG] Next 5 M1 timestamps after filter:")
                    for i, ts in enumerate(m1_beyond_filter.index[:5]):
                        print(f"    [{i}] {ts}")
                else:
                    print(f"[M1 DEBUG] Raw CSV file ENDS at the filter end time - no more data available")

            print(f"{'='*80}\n")

            # FORWARD-FILL missing M1 bars to ensure perfect alignment with EMAs
            # This is critical for chart visualization - EMAs must align with M1 candlesticks
            print(f"[M1 DEBUG] APPLYING FORWARD-FILL TO ELIMINATE GAPS")

            # Build M1 index from M15 bars (15 M1 bars per M15 bar)
            # Note: M1 timestamps can spill into weekends even from Friday M15 bars (e.g., Fri 23:45 → Sat 00:13)
            # We'll filter weekends from the final M1 index after generation
            m1_timestamps = []
            for m15_timestamp in m15_df.index:
                # Each M15 bar at time T contains M1 bars from T to T+14 minutes
                for minute_offset in range(15):
                    m1_ts = m15_timestamp + pd.Timedelta(minutes=minute_offset)
                    m1_timestamps.append(m1_ts)

            complete_m1_index = pd.DatetimeIndex(m1_timestamps)

            # CRITICAL FIX: Filter out weekend M1 bars
            # Even though M15 bars are weekend-filtered, M1 timestamps can spill into Saturday/Sunday
            # Example: Friday 23:45 M15 bar generates M1 bars from 23:45-23:59, which includes Saturday 00:00-00:13
            m1_index_before_weekend_filter = len(complete_m1_index)
            complete_m1_index = complete_m1_index[complete_m1_index.dayofweek < 5]  # Keep Mon-Fri only
            m1_weekend_bars_removed = m1_index_before_weekend_filter - len(complete_m1_index)

            print(f"[M1 DEBUG] Complete index length (before weekend filter): {m1_index_before_weekend_filter} bars")
            print(f"[M1 DEBUG] Weekend filtering: Removed {m1_weekend_bars_removed} M1 bars that fell on Sat/Sun")
            print(f"[M1 DEBUG] Complete index length (after weekend filter): {len(complete_m1_index)} bars")
            print(f"[M1 DEBUG] Original data length: {len(m1_df_filtered)} bars")
            print(f"[M1 DEBUG] Bars to be filled: {len(complete_m1_index) - len(m1_df_filtered)}")

            # Reindex with forward-fill (missing bars use previous bar's close as OHLC)
            m1_df_filled = m1_df_filtered.reindex(complete_m1_index)

            # Forward-fill OHLC data (each missing bar copies previous bar's close)
            # Use .ffill() instead of deprecated fillna(method='ffill')
            m1_df_filled = m1_df_filled.ffill()

            # Backward-fill any remaining NaN values at the start (if first bar has no data)
            m1_df_filled = m1_df_filled.bfill()

            # Drop any remaining NaN values as a final safety measure
            nan_count_before = m1_df_filled.isnull().sum().sum()
            if nan_count_before > 0:
                print(f"[M1 DEBUG] Dropping {nan_count_before} remaining NaN values after ffill/bfill")
                m1_df_filled = m1_df_filled.dropna()

            # Verify no NaN values remain
            if m1_df_filled.isnull().any().any():
                print(f"[M1 WARN] [WARN] NaN values remain after forward-fill!")
                print(f"[M1 WARN] First NaN at index: {m1_df_filled[m1_df_filled.isnull().any(axis=1)].index[0]}")
            else:
                print(f"[M1 DEBUG] [OK] Forward-fill complete - no NaN values")

            print(f"[M1 DEBUG] Final M1 bar count after forward-fill: {len(m1_df_filled)}")
            print(f"[M1 DEBUG] Expected bar count: {len(complete_m1_index)} (weekend-filtered M1 index)")

            if len(m1_df_filled) == len(complete_m1_index):
                print(f"[M1 DEBUG] [OK] PERFECT ALIGNMENT: {len(m1_df_filled)} bars = expected weekend-filtered count")
            else:
                print(f"[M1 WARN] [WARN] Alignment mismatch: {len(m1_df_filled)} ≠ {len(complete_m1_index)}")

            print(f"{'='*80}\n")

            # Use filled dataframe for candlestick generation
            # Weekends are excluded via explicit dayofweek filtering on the complete_m1_index
            m1_df_filtered = m1_df_filled

            print(f"[M1 DEBUG] Ready for candlestick generation: {len(m1_df_filtered)} weekday-only M1 bars")
            print(f"{'='*80}\n")

            # Prepare candlestick data (simplified - no indicators for M1)
            candles = []
            for idx, row in m1_df_filtered.iterrows():
                candle = {
                    "timestamp": idx.isoformat() if isinstance(idx, datetime) else idx,
                    "open": float(row['open']),
                    "high": float(row['high']),
                    "low": float(row['low']),
                    "close": float(row['close'])
                }
                candles.append(candle)

            result = {
                "symbol": symbol,
                "start_date": str(m15_start_time),
                "end_date": str(m15_end_time),
                "timeframe": "M1",
                "candles": candles,
                "pip_size": 0.0001,
                "decimal_places": 5
            }

            print(f"[OK] M1 OHLC data prepared: {len(candles)} M1 candles")
            return result

        except Exception as e:
            print(f"[WARN] M1 OHLC data preparation failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                "symbol": request.get('symbol', 'UNKNOWN'),
                "timeframe": "M1",
                "candles": [],
                "error": str(e)
            }

    def get_m1_ohlc_data(self, task_id: str) -> Optional[Dict]:
        """Get M1 OHLC data for a completed backtest"""
        task = self.tasks.get(task_id)
        if not task:
            return None

        return task.get("m1_ohlc_data")

    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Get current status of a task"""
        task = self.tasks.get(task_id)
        if not task:
            return None

        return {
            "task_id": task_id,
            "status": task["status"],
            "progress": task["progress"],
            "message": task["message"],
            "eta_seconds": None,  # TODO: Implement ETA calculation
            "started_at": task.get("started_at"),
            "completed_at": task.get("completed_at")
        }

    def get_task_results(self, task_id: str) -> Optional[Dict]:
        """Get complete results of a task"""
        task = self.tasks.get(task_id)
        if not task:
            return None

        return {
            "status": task["status"],
            "data": task.get("results")
        }

    def get_task_summary(self, task_id: str) -> Optional[Dict]:
        """Get abbreviated results (metrics only)"""
        task = self.tasks.get(task_id)
        if not task or task["status"] != "complete":
            return None

        results = task["results"]
        return {
            "task_id": task_id,
            "symbol": results["symbol"],
            "start_date": results["start_date"],
            "end_date": results["end_date"],
            "strategy": results["strategy"],
            "total_trades": results["total_trades"],
            "total_r": results["total_r"],
            "win_rate": results["win_rate"],
            "final_balance": results["final_balance"],
            "max_drawdown_pct": results["max_drawdown_pct"]
        }

    def list_tasks(self) -> list:
        """List all tasks"""
        task_list = []
        for task_id, task in self.tasks.items():
            item = {
                "task_id": task_id,
                "symbol": task["request"]["symbol"],
                "strategy": task["request"].get("strategy", "both"),
                "status": task["status"],
                "created_at": task["created_at"],
                "total_r": None
            }

            if task["status"] == "complete" and task.get("results"):
                item["total_r"] = task["results"]["total_r"]

            task_list.append(item)

        # Sort by creation time (newest first)
        task_list.sort(key=lambda x: x["created_at"], reverse=True)

        return task_list

    def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    async def execute_multi_pair_backtest(self, task_id: str):
        """Execute multi-pair backtest in background."""
        try:
            task = self.tasks.get(task_id)
            if not task:
                return
            task['status'] = 'running'
            task['started_at'] = datetime.utcnow().isoformat() + 'Z'
            task['message'] = 'Initializing multi-pair backtest...'
            request = task['request']
            pairs = request['pairs']
            config = request['config']
            all_pair_results = {}
            pair_engines = {}
            total_pairs = len(pairs)


            # ARCHITECTURAL LIMITATION (Phase 8.6):
            # Pairs are processed SEQUENTIALLY, not chronologically bar-by-bar.
            # This means:
            #   1. EURUSD backtest runs completely (all bars, all trades)
            #   2. Then GBPUSD backtest runs completely
            #   3. Trades are merged chronologically after the fact
            #
            # IMPACT:
            #   - Position slots may not be managed realistically
            #   - First pair processed gets priority for position slots
            #   - Does not simulate true live trading conditions
            #
            # TODO (Phase 8.7): Implement true chronological bar-by-bar orchestrator
            #   - Advance all pairs simultaneously by timestamp
            #   - Evaluate strategies chronologically across pairs
            #   - Implement signal priority resolution when multiple pairs signal
            #   - Estimate: 16-24 hours development + testing

            # Create shared PositionManager for all pairs (respects global limit)
            shared_position_manager = PositionManager(config["max_concurrent_positions"])
            print(f"[MULTI-PAIR] Created shared PositionManager with max_positions={config['max_concurrent_positions']}")

            for idx, symbol in enumerate(pairs):
                task['progress'] = 10.0 + (idx / total_pairs) * 70.0
                task['message'] = f'Running backtest for {symbol} ({idx+1}/{total_pairs})...'
                engine = BacktestEngine(
                    initial_balance=config['initial_balance'],
                    risk_percent=config['risk_percent'] * 100,
                    max_positions=config['max_concurrent_positions'],
                    timeframe=request.get('timeframe', 'M15'),
                    position_manager=shared_position_manager
                )
                year = request['start_date'][:4]
                try:
                    results = engine.run_backtest(
                        symbol=symbol,
                        year=year,
                        start_date=request['start_date'],
                        end_date=request['end_date'],
                        strategies=request.get('strategies')
                    )
                    all_pair_results[symbol] = results
                    pair_engines[symbol] = engine
                    print(f'[OK] {symbol} backtest complete: {results["performance"]["total_trades"]} trades')
                except Exception as e:
                    print(f'[ERROR] {symbol} backtest failed: {e}')
                    all_pair_results[symbol] = {'error': str(e), 'performance': self._get_empty_performance(), 'trades': [], 'equity_curve': []}
            task['progress'] = 85.0
            task['message'] = 'Merging results across pairs...'
            api_results = self._merge_multi_pair_results(task_id=task_id, request=request, pair_results=all_pair_results, pair_engines=pair_engines)
            task['status'] = 'complete'
            task['progress'] = 100.0
            task['message'] = 'Multi-pair backtest completed successfully'
            task['completed_at'] = datetime.utcnow().isoformat() + 'Z'
            task['results'] = api_results
        except Exception as e:
            task['status'] = 'failed'
            task['message'] = f'Multi-pair backtest failed: {str(e)}'
            task['error'] = {'error': str(e), 'traceback': traceback.format_exc()}
            print(f'Multi-pair backtest {task_id} failed: {e}')
            traceback.print_exc()

    def _merge_multi_pair_results(self, task_id: str, request: dict, pair_results: dict, pair_engines: dict) -> dict:
        """Merge results from multiple pairs into unified response."""
        all_trades = []
        for symbol, results in pair_results.items():
            if "error" in results:
                continue
            trades_list = results.get("trades", [])
            for trade in trades_list:
                api_trade = {
                    "position_id": trade["position_id"],
                    "symbol": trade["symbol"],
                    "side": self._convert_side_to_csharp(trade["side"]),
                    "strategy": self._convert_strategy_to_csharp(trade["strategy"]),
                    "confidence": trade.get("confidence", 0.0),
                    "regime": trade.get("regime", "UNKNOWN"),
                    "entry_time": self._format_timestamp(trade["entry_time"]),
                    "exit_time": self._format_timestamp(trade.get("exit_time")),
                    "entry_price": trade["entry_price"],
                    "exit_price": trade.get("exit_price"),
                    "stop_loss": trade.get("initial_stop"),
                    "take_profit": trade.get("initial_tp"),
                    "r_multiple": trade.get("r_multiple"),
                    "profit_loss": trade.get("profit_loss"),
                    "exit_reason": trade.get("exit_reason")
                }
                all_trades.append(api_trade)
        all_trades.sort(key=lambda t: t["exit_time"] if t["exit_time"] else t["entry_time"])
        overall_stats = self._calculate_overall_statistics(all_trades, request["config"]["initial_balance"])
        pair_breakdown = {}
        for symbol in request["pairs"]:
            pair_trades = [t for t in all_trades if t["symbol"] == symbol]
            pair_breakdown[symbol] = self._calculate_pair_statistics(pair_trades)
        strategy_breakdown = {}
        for strategy in ["TREND_RIDER", "RANGE_RIDER"]:
            strat_trades = [t for t in all_trades if t["strategy"] == strategy]
            if strat_trades:
                strategy_breakdown[strategy] = self._calculate_strategy_statistics(strat_trades)
        equity_curve = self._build_unified_equity_curve(all_trades, request["config"]["initial_balance"])
        pair_chart_data = {}
        for symbol, engine in pair_engines.items():
            if symbol in pair_results and "error" not in pair_results[symbol]:
                pair_chart_data[symbol] = self._prepare_pair_chart_data(symbol=symbol, engine=engine, request=request)
        return {
            "task_id": task_id,
            "pairs": request["pairs"],
            "strategies": request["strategies"],
            "start_date": request["start_date"],
            "end_date": request["end_date"],
            "timeframe": request.get("timeframe", "M15"),
            "trades": all_trades,
            "statistics": overall_stats,
            "equity_curve": equity_curve,
            "pair_breakdown": pair_breakdown,
            "strategy_breakdown": strategy_breakdown,
            "pair_chart_data": pair_chart_data
        }

    def _convert_side_to_csharp(self, side: str) -> str:
        """Convert BUY/SELL to LONG/SHORT for C# compatibility"""
        mapping = {"BUY": "LONG", "SELL": "SHORT", "LONG": "LONG", "SHORT": "SHORT"}
        return mapping.get(side, side)

    def _convert_strategy_to_csharp(self, strategy: str) -> str:
        """Convert strategy name to C# format"""
        mapping = {"SIMPLE_TEST": "SIMPLE_TEST", "TREND_RIDER": "TREND_RIDER", "RANGE_RIDER": "RANGE_RIDER", "trend_rider": "TREND_RIDER", "range_rider": "RANGE_RIDER"}
        return mapping.get(strategy, strategy.upper())

    def _format_timestamp(self, timestamp):
        """Format timestamp to ISO format for C#"""
        if timestamp is None:
            return None
        if isinstance(timestamp, datetime):
            return timestamp.isoformat()
        if isinstance(timestamp, str):
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                return dt.isoformat()
            except:
                return timestamp
        return str(timestamp)

    def _calculate_overall_statistics(self, trades: list, initial_balance: float) -> dict:
        """Calculate overall statistics from all trades"""
        if not trades:
            return self._get_empty_overall_stats(initial_balance)
        total_trades = len(trades)
        wins = len([t for t in trades if t.get("r_multiple", 0) and t["r_multiple"] > 0])
        losses = len([t for t in trades if t.get("r_multiple", 0) and t["r_multiple"] < 0])
        total_r = sum([t.get("r_multiple", 0) or 0 for t in trades])
        avg_r = total_r / total_trades if total_trades > 0 else 0
        r_multiples = [t.get("r_multiple", 0) or 0 for t in trades]
        max_r = max(r_multiples) if r_multiples else 0
        min_r = min(r_multiples) if r_multiples else 0
        total_pl = sum([t.get("profit_loss", 0) or 0 for t in trades])
        final_balance = initial_balance + total_pl
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        return_percent = (total_pl / initial_balance * 100) if initial_balance > 0 else 0
        running_balance = initial_balance
        peak_balance = initial_balance
        max_drawdown_dollars = 0
        for trade in trades:
            running_balance += trade.get("profit_loss", 0) or 0
            if running_balance > peak_balance:
                peak_balance = running_balance
            drawdown = peak_balance - running_balance
            if drawdown > max_drawdown_dollars:
                max_drawdown_dollars = drawdown
        max_drawdown_pct = -(max_drawdown_dollars / peak_balance * 100) if peak_balance > 0 else 0
        if r_multiples and len(r_multiples) > 1:
            import numpy as np
            r_std = float(np.std(r_multiples))
            sharpe_ratio = avg_r / r_std if r_std > 0 else 0
        else:
            sharpe_ratio = 0
        return {
            "total_trades": total_trades,
            "wins": wins,
            "losses": losses,
            "win_rate": round(win_rate, 1),
            "total_r": round(total_r, 2),
            "avg_r": round(avg_r, 2),
            "max_r": round(max_r, 2),
            "min_r": round(min_r, 2),
            "max_drawdown": round(-max_drawdown_dollars, 2),
            "max_drawdown_pct": round(max_drawdown_pct, 1),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "initial_balance": initial_balance,
            "final_balance": round(final_balance, 2),
            "net_profit": round(total_pl, 2),
            "return_percent": round(return_percent, 1)
        }

    def _calculate_pair_statistics(self, trades: list) -> dict:
        """Calculate statistics for a single pair"""
        if not trades:
            return {"trades": 0, "wins": 0, "losses": 0, "win_rate": 0.0, "total_r": 0.0, "avg_r": 0.0, "net_profit": 0.0}
        total_trades = len(trades)
        wins = len([t for t in trades if t.get("r_multiple", 0) and t["r_multiple"] > 0])
        losses = len([t for t in trades if t.get("r_multiple", 0) and t["r_multiple"] < 0])
        total_r = sum([t.get("r_multiple", 0) or 0 for t in trades])
        avg_r = total_r / total_trades if total_trades > 0 else 0
        total_pl = sum([t.get("profit_loss", 0) or 0 for t in trades])
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        return {"trades": total_trades, "wins": wins, "losses": losses, "win_rate": round(win_rate, 1), "total_r": round(total_r, 2), "avg_r": round(avg_r, 2), "net_profit": round(total_pl, 2)}

    def _calculate_strategy_statistics(self, trades: list) -> dict:
        """Calculate statistics for a single strategy"""
        return self._calculate_pair_statistics(trades)

    def _build_unified_equity_curve(self, trades: list, initial_balance: float) -> list:
        """Build chronological equity curve from all trades"""
        if not trades:
            return []
        equity_curve = []
        running_balance = initial_balance
        cumulative_r = 0
        if trades:
            first_time = trades[0]["entry_time"]
            equity_curve.append({"timestamp": first_time, "balance": initial_balance, "r_multiple": 0.0, "cumulative_r": 0.0, "strategy": "START"})
        for trade in trades:
            if trade.get("exit_time"):
                running_balance += trade.get("profit_loss", 0) or 0
                cumulative_r += trade.get("r_multiple", 0) or 0
                equity_curve.append({"timestamp": trade["exit_time"], "balance": round(running_balance, 2), "r_multiple": round(trade.get("r_multiple", 0) or 0, 2), "cumulative_r": round(cumulative_r, 2), "strategy": trade["strategy"]})
        return equity_curve

    def _prepare_pair_chart_data(self, symbol: str, engine, request: dict) -> dict:
        """Prepare chart data (OHLC + indicators) for a single pair"""
        try:
            import pandas as pd
            backtest_start_idx = getattr(engine, 'backtest_start_idx', 0)
            df_m15 = engine.df.iloc[backtest_start_idx:].copy()
            df_m15 = df_m15[df_m15.index.dayofweek < 5]
            m15_candles = []
            for idx, row in df_m15.iterrows():
                candle = {
                    "timestamp": idx.isoformat() if isinstance(idx, pd.Timestamp) else str(idx),
                    "open": float(row['open']),
                    "high": float(row['high']),
                    "low": float(row['low']),
                    "close": float(row['close']),
                    "ema_fast": float(row.get('ema_fast', 0)) if not pd.isna(row.get('ema_fast', 0)) else None,
                    "ema_mid": float(row.get('ema_mid', 0)) if not pd.isna(row.get('ema_mid', 0)) else None,
                    "ema_slow": float(row.get('ema_slow', 0)) if not pd.isna(row.get('ema_slow', 0)) else None,
                    "rsi": float(row.get('rsi', 50)) if not pd.isna(row.get('rsi', 50)) else 50.0,
                    "adx": float(row.get('adx', 0)) if not pd.isna(row.get('adx', 0)) else None
                }
                m15_candles.append(candle)
            m1_candles = self._prepare_m1_candles_simplified(symbol, request, engine)
            return {"symbol": symbol, "m15_candles": m15_candles, "m1_candles": m1_candles}
        except Exception as e:
            print(f"[WARN] Chart data preparation failed for {symbol}: {e}")
            return {"symbol": symbol, "m15_candles": [], "m1_candles": []}

    def _prepare_m1_candles_simplified(self, symbol: str, request: dict, engine) -> list:
        """Simplified M1 candle preparation"""
        try:
            from src.data_loader import DataLoader
            import pandas as pd
            import traceback
            
            print(f"[M1-LOAD] Starting M1 data preparation for {symbol}")
            
            # Reuse engine's DataLoader instead of creating new one (prevents state corruption)
            loader = engine.loader
            year = int(request["start_date"][:4])
            
            print(f"[M1-LOAD] Loading M1 data for {symbol}, year={year}")
            m1_df = loader.load_pair_data(symbol, year=year)
            print(f"[M1-LOAD] Loaded {len(m1_df)} M1 candles for {symbol}")
            
            backtest_start_idx = getattr(engine, 'backtest_start_idx', 0)
            m15_df = engine.df.iloc[backtest_start_idx:].copy()
            m15_df = m15_df[m15_df.index.dayofweek < 5]
            m15_start = m15_df.index[0]
            m15_end = m15_df.index[-1]
            m1_end = m15_end + pd.Timedelta(minutes=14)
            
            print(f"[M1-LOAD] Filtering M1 data: {m15_start} to {m1_end}")
            m1_filtered = m1_df.loc[m15_start:m1_end]
            m1_filtered = m1_filtered[m1_filtered.index.dayofweek < 5]
            print(f"[M1-LOAD] Filtered to {len(m1_filtered)} M1 candles for {symbol}")
            
            m1_candles = []
            for idx, row in m1_filtered.iterrows():
                candle = {"timestamp": idx.isoformat() if isinstance(idx, pd.Timestamp) else str(idx), "open": float(row['open']), "high": float(row['high']), "low": float(row['low']), "close": float(row['close'])}
                m1_candles.append(candle)
            
            print(f"[M1-LOAD] Successfully prepared {len(m1_candles)} M1 candles for {symbol}")
            return m1_candles
        except Exception as e:
            import traceback
            print(f"[ERROR] M1 data preparation failed for {symbol}: {e}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            return []

    def _get_empty_performance(self) -> dict:
        """Return empty performance dict for failed pairs"""
        return {"initial_balance": 0, "final_balance": 0, "total_trades": 0, "winning_trades": 0, "losing_trades": 0, "win_rate": 0, "total_r": 0}

    def _get_empty_overall_stats(self, initial_balance: float) -> dict:
        """Return empty overall statistics"""
        return {"total_trades": 0, "wins": 0, "losses": 0, "win_rate": 0.0, "total_r": 0.0, "avg_r": 0.0, "max_r": 0.0, "min_r": 0.0, "max_drawdown": 0.0, "max_drawdown_pct": 0.0, "sharpe_ratio": 0.0, "initial_balance": initial_balance, "final_balance": initial_balance, "net_profit": 0.0, "return_percent": 0.0}
