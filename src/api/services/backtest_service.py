"""
Backtest Service Layer
Orchestrates backtest execution and task management
"""

import time
import traceback
import os
from typing import Dict, Optional
from datetime import datetime
from src.backtest_engine import BacktestEngine
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
            results = engine.run_backtest(
                symbol=request["symbol"],
                year=year,
                start_date=request["start_date"],
                end_date=request["end_date"]
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
            ohlc_data = self._prepare_ohlc_data(request, api_results, engine)

            # Prepare M1 OHLC data for enhanced playback
            task["progress"] = 98.0
            task["message"] = "Preparing M1 data for enhanced playback..."
            m1_ohlc_data = self._prepare_m1_ohlc_data(request, engine)

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

            print(f"✅ Charts generated: {chart_path}")
            return chart_path

        except Exception as e:
            print(f"[WARN]️ Chart generation failed: {e}")
            traceback.print_exc()
            return None

    def _prepare_ohlc_data(
        self,
        request: Dict,
        api_results: Dict,
        engine: 'BacktestEngine'
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
            print(f"[OHLC DATA] Calculating H1 EMAs on full dataset for accuracy...")

            # Aggregate to H1 for H1 EMA calculation
            df_h1 = df_full.resample('1H').agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last'
            }).dropna()

            # Calculate H1 EMAs using TA-Lib or simple EMA
            def calculate_ema_simple(data, period):
                """Simple EMA calculation"""
                if len(data) < period:
                    return pd.Series([None] * len(data), index=data.index)

                multiplier = 2.0 / (period + 1)
                ema = data.copy()

                # Initial SMA
                ema.iloc[:period-1] = None
                ema.iloc[period-1] = data.iloc[:period].mean()

                # Calculate EMA
                for i in range(period, len(data)):
                    ema.iloc[i] = (data.iloc[i] - ema.iloc[i-1]) * multiplier + ema.iloc[i-1]

                return ema

            df_h1['ema_20'] = calculate_ema_simple(df_h1['close'], 20)
            df_h1['ema_50'] = calculate_ema_simple(df_h1['close'], 50)
            df_h1['ema_100'] = calculate_ema_simple(df_h1['close'], 100)

            # Map H1 EMAs back to M15 bars with LINEAR INTERPOLATION for smoothness
            # Use PREVIOUS hour's H1 EMA to avoid lookahead bias
            df_full['ema_20_h1'] = None
            df_full['ema_50_h1'] = None
            df_full['ema_100_h1'] = None

            # Create a list of H1 timestamps for faster lookup
            h1_timestamps = sorted(df_h1.index.tolist())

            for i, (idx, row) in enumerate(df_full.iterrows()):
                # Find the H1 bar that COMPLETED before or at this M15 bar
                current_hour = idx.floor('1H')

                # Find the index of the COMPLETED H1 bar (previous hour)
                # A H1 bar at 14:00 completes at 15:00, so for M15 at 14:45, we use H1 from 13:00
                completed_h1_idx = None
                next_h1_idx = None

                for j, h1_ts in enumerate(h1_timestamps):
                    if h1_ts <= current_hour:
                        completed_h1_idx = j
                    if h1_ts > current_hour:
                        next_h1_idx = j
                        break

                if completed_h1_idx is not None and completed_h1_idx > 0:
                    # Use the previous H1 bar (the one that's complete)
                    prev_h1_ts = h1_timestamps[completed_h1_idx - 1] if completed_h1_idx > 0 else h1_timestamps[0]
                    curr_h1_ts = h1_timestamps[completed_h1_idx]

                    # Get EMA values for interpolation
                    prev_ema20 = df_h1.loc[prev_h1_ts, 'ema_20']
                    prev_ema50 = df_h1.loc[prev_h1_ts, 'ema_50']
                    prev_ema100 = df_h1.loc[prev_h1_ts, 'ema_100']

                    curr_ema20 = df_h1.loc[curr_h1_ts, 'ema_20']
                    curr_ema50 = df_h1.loc[curr_h1_ts, 'ema_50']
                    curr_ema100 = df_h1.loc[curr_h1_ts, 'ema_100']

                    # Calculate interpolation factor based on time within the hour
                    # M15 at 14:00 → factor = 0.0 (use previous H1)
                    # M15 at 14:15 → factor = 0.25
                    # M15 at 14:30 → factor = 0.50
                    # M15 at 14:45 → factor = 0.75
                    minutes_into_hour = idx.minute
                    factor = minutes_into_hour / 60.0

                    # Linear interpolation for smooth H1 EMAs
                    if not pd.isna(prev_ema20) and not pd.isna(curr_ema20):
                        df_full.loc[idx, 'ema_20_h1'] = prev_ema20 + (curr_ema20 - prev_ema20) * factor
                    if not pd.isna(prev_ema50) and not pd.isna(curr_ema50):
                        df_full.loc[idx, 'ema_50_h1'] = prev_ema50 + (curr_ema50 - prev_ema50) * factor
                    if not pd.isna(prev_ema100) and not pd.isna(curr_ema100):
                        df_full.loc[idx, 'ema_100_h1'] = prev_ema100 + (curr_ema100 - prev_ema100) * factor

            print(f"[OK] H1 EMAs calculated on {len(df_h1)} H1 bars and interpolated to M15")

            # Now filter to backtest period (skip warmup)
            df = df_full.iloc[backtest_start_idx:].copy()
            print(f"[OHLC DATA] Sending to C#: {len(df)} bars (warmup skipped, start from bar {backtest_start_idx})")

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

            print(f"✅ OHLC data prepared: {len(candles)} candles, {len(trades_with_levels)} trades")
            return result

        except Exception as e:
            print(f"[WARN]️ OHLC data preparation failed: {e}")
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
        engine: 'BacktestEngine'
    ) -> Dict:
        """
        Prepare M1 (1-minute) OHLC data for enhanced chart playback.

        Returns M1-level candlestick data for smooth price movement visualization.
        """
        try:
            from src.data_loader import DataLoader

            # Initialize data loader
            loader = DataLoader(data_dir="data")

            # Extract year from start_date
            year = int(request["start_date"][:4])
            symbol = request["symbol"]

            # Load M1 data
            print(f"[M1] Loading M1 data for {symbol} ({year})...")
            m1_df = loader.load_pair_data(symbol, year=year)

            # Filter to backtest date range (include entire end date through 23:59:59)
            import pandas as pd
            start_date = request["start_date"]
            end_date = request["end_date"]
            end_timestamp = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
            m1_df_filtered = m1_df.loc[start_date:end_timestamp]

            print(f"[M1] Filtered M1 data: {len(m1_df_filtered)} bars from {m1_df_filtered.index[0]} to {m1_df_filtered.index[-1]}")

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
                "start_date": start_date,
                "end_date": end_date,
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
