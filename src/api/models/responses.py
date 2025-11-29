"""
Pydantic Response Models
Structured responses for API endpoints
"""

from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime


class BacktestResponse(BaseModel):
    """Response when starting a backtest"""

    task_id: str
    status: str  # queued, running, complete, failed

    class Config:
        json_json_schema_extra = {
            "example": {
                "task_id": "abc123-def456-ghi789",
                "status": "queued"
            }
        }


class BacktestStatus(BaseModel):
    """Current status of a backtest task"""

    task_id: str
    status: str  # queued, running, complete, failed
    progress: float  # 0-100
    message: Optional[str] = None
    eta_seconds: Optional[int] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    class Config:
        json_json_schema_extra = {
            "example": {
                "task_id": "abc123-def456-ghi789",
                "status": "running",
                "progress": 45.2,
                "message": "Processing bar 2,819 of 6,240",
                "eta_seconds": 125,
                "started_at": "2024-11-19T14:30:00Z",
                "completed_at": None
            }
        }


class TradeRecord(BaseModel):
    """Individual trade record"""

    position_id: int
    symbol: str
    side: str  # BUY or SELL
    strategy: str  # TREND_RIDER or RANGE_RIDER
    confidence: float
    regime: str  # TRENDING, RANGING, TRANSITIONAL
    entry_time: str
    exit_time: Optional[str]
    entry_price: float
    exit_price: Optional[float]
    stop_loss: float
    take_profit: Optional[float]
    r_multiple: Optional[float]
    profit_loss: Optional[float]
    exit_reason: Optional[str]

    class Config:
        json_json_schema_extra = {
            "example": {
                "position_id": 1,
                "symbol": "EURUSD",
                "side": "BUY",
                "strategy": "TREND_RIDER",
                "confidence": 75.0,
                "regime": "TRENDING",
                "entry_time": "2024-01-05T12:00:00",
                "exit_time": "2024-01-05T18:00:00",
                "entry_price": 1.10500,
                "exit_price": 1.10750,
                "stop_loss": 1.10200,
                "take_profit": 1.11000,
                "r_multiple": 0.83,
                "profit_loss": 250.0,
                "exit_reason": "BREAK_EVEN"
            }
        }


class StrategyBreakdown(BaseModel):
    """Performance breakdown by strategy"""

    trades: int
    wins: int
    losses: int
    total_r: float
    total_pl: float
    win_rate: float
    avg_r: float

    class Config:
        json_json_schema_extra = {
            "example": {
                "trades": 78,
                "wins": 42,
                "losses": 36,
                "total_r": 9.18,
                "total_pl": 918.0,
                "win_rate": 53.8,
                "avg_r": 0.12
            }
        }


class EquityPoint(BaseModel):
    """Single point on equity curve"""

    timestamp: str
    balance: float
    r_multiple: float
    cumulative_r: float
    strategy: str

    class Config:
        json_json_schema_extra = {
            "example": {
                "timestamp": "2024-01-05T18:00:00",
                "balance": 10250.0,
                "r_multiple": 0.83,
                "cumulative_r": 2.5,
                "strategy": "TREND_RIDER"
            }
        }


class BacktestResults(BaseModel):
    """Complete backtest results"""

    task_id: str
    symbol: str
    start_date: str
    end_date: str
    strategy: str
    initial_balance: float
    final_balance: float
    net_profit: float
    return_pct: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_r: float
    avg_r: float
    max_r: float
    min_r: float
    max_drawdown_pct: float
    max_drawdown_dollars: float
    profit_factor: float
    sharpe_ratio: float
    max_consecutive_wins: int
    max_consecutive_losses: int
    trend_rider: Optional[StrategyBreakdown] = None
    range_rider: Optional[StrategyBreakdown] = None
    trades: List[TradeRecord]
    equity_curve: List[EquityPoint]

    class Config:
        json_json_schema_extra = {
            "example": {
                "task_id": "abc123-def456-ghi789",
                "symbol": "EURUSD",
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "strategy": "both",
                "initial_balance": 10000.0,
                "final_balance": 11603.0,
                "net_profit": 1603.0,
                "return_pct": 16.03,
                "total_trades": 149,
                "winning_trades": 77,
                "losing_trades": 72,
                "win_rate": 51.7,
                "total_r": 16.03,
                "avg_r": 0.11,
                "max_r": 3.5,
                "min_r": -1.0,
                "max_drawdown_pct": 18.5,
                "max_drawdown_dollars": 1850.0,
                "profit_factor": 1.45,
                "sharpe_ratio": 1.23,
                "max_consecutive_wins": 7,
                "max_consecutive_losses": 5,
                "trend_rider": {
                    "trades": 78,
                    "wins": 42,
                    "losses": 36,
                    "total_r": 9.18,
                    "total_pl": 918.0,
                    "win_rate": 53.8,
                    "avg_r": 0.12
                },
                "range_rider": {
                    "trades": 71,
                    "wins": 35,
                    "losses": 36,
                    "total_r": 6.86,
                    "total_pl": 686.0,
                    "win_rate": 49.3,
                    "avg_r": 0.10
                },
                "trades": [],
                "equity_curve": []
            }
        }


class BacktestSummary(BaseModel):
    """Abbreviated backtest results (metrics only, no trades/equity)"""

    task_id: str
    symbol: str
    start_date: str
    end_date: str
    strategy: str
    total_trades: int
    total_r: float
    win_rate: float
    final_balance: float
    max_drawdown_pct: float

    class Config:
        json_json_schema_extra = {
            "example": {
                "task_id": "abc123-def456-ghi789",
                "symbol": "EURUSD",
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "strategy": "both",
                "total_trades": 149,
                "total_r": 16.03,
                "win_rate": 51.7,
                "final_balance": 11603.0,
                "max_drawdown_pct": 18.5
            }
        }


class BacktestListItem(BaseModel):
    """Single item in backtest list"""

    task_id: str
    symbol: str
    strategy: str
    status: str
    created_at: str
    total_r: Optional[float] = None

    class Config:
        json_json_schema_extra = {
            "example": {
                "task_id": "abc123-def456-ghi789",
                "symbol": "EURUSD",
                "strategy": "both",
                "status": "complete",
                "created_at": "2024-11-19T14:30:00Z",
                "total_r": 16.03
            }
        }


class ErrorResponse(BaseModel):
    """Structured error response"""

    error_code: str
    message: str
    details: Optional[Dict] = None

    class Config:
        json_json_schema_extra = {
            "example": {
                "error_code": "INVALID_SYMBOL",
                "message": "Symbol XXXUSD is not supported",
                "details": {
                    "valid_symbols": ["EURUSD", "GBPUSD", "USDJPY"]
                }
            }
        }


class HealthResponse(BaseModel):
    """Server health check response"""

    status: str  # ok, degraded, down
    version: str
    uptime_seconds: int

    class Config:
        json_json_schema_extra = {
            "example": {
                "status": "ok",
                "version": "1.0.0",
                "uptime_seconds": 3600
            }
        }


class InfoResponse(BaseModel):
    """System information response"""

    version: str
    features: List[str]
    supported_symbols: List[str]
    supported_strategies: List[str]
    data_available: Dict[str, str]  # symbol -> date range

    class Config:
        json_json_schema_extra = {
            "example": {
                "version": "1.0.0",
                "features": ["backtesting", "optimization", "multi-pair"],
                "supported_symbols": ["EURUSD", "GBPUSD", "USDJPY"],
                "supported_strategies": ["trend_rider", "range_rider", "both"],
                "data_available": {
                    "EURUSD": "2024-01-01 to 2024-12-31",
                    "GBPUSD": "2024-01-01 to 2024-12-31"
                }
            }
        }


class ValidationResponse(BaseModel):
    """Configuration validation response"""

    valid: bool
    errors: List[str] = []

    class Config:
        json_json_schema_extra = {
            "example": {
                "valid": False,
                "errors": [
                    "start_date must be before end_date",
                    "risk_percent must be between 0.1 and 10.0"
                ]
            }
        }
