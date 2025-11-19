"""
Backtest Service Layer
Orchestrates backtest execution and task management
"""

import time
import traceback
from typing import Dict, Optional
from datetime import datetime
from src.backtest_engine import BacktestEngine
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
                max_positions=request.get("max_positions", 2)
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

            # Mark as complete
            task["status"] = "complete"
            task["progress"] = 100.0
            task["message"] = "Backtest completed successfully"
            task["completed_at"] = datetime.utcnow().isoformat() + "Z"
            task["results"] = api_results

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
