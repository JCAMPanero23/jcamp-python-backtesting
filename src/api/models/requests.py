"""
Pydantic Request Models
Data validation for incoming API requests
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List
from datetime import datetime


class BacktestRequest(BaseModel):
    """Request model for starting a backtest"""

    symbol: str = Field(..., description="Trading pair (e.g., EURUSD)")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    strategy: str = Field("both", description="Strategy: trend_rider, range_rider, or both")
    timeframe: str = Field("M15", description="Chart timeframe: M15, H1, or H4")
    initial_balance: float = Field(10000.0, description="Starting balance in dollars")
    risk_percent: float = Field(2.0, description="Risk per trade as percentage")
    max_positions: int = Field(2, description="Maximum concurrent positions")
    parameters: Optional[Dict] = Field(None, description="Optional strategy parameters")

    @validator('symbol')
    def validate_symbol(cls, v):
        """Validate symbol is in approved list"""
        valid_symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD', 'NZDUSD', 'EURGBP', 'EURJPY']
        if v not in valid_symbols:
            raise ValueError(f'Symbol must be one of {valid_symbols}')
        return v

    @validator('strategy')
    def validate_strategy(cls, v):
        """Validate strategy selection"""
        valid_strategies = ['trend_rider', 'range_rider', 'both']
        if v not in valid_strategies:
            raise ValueError(f'Strategy must be one of {valid_strategies}')
        return v

    @validator('timeframe')
    def validate_timeframe(cls, v):
        """Validate timeframe selection"""
        valid_timeframes = ['M15', 'H1', 'H4']
        if v not in valid_timeframes:
            raise ValueError(f'Timeframe must be one of {valid_timeframes}')
        return v

    @validator('start_date', 'end_date')
    def validate_date_format(cls, v):
        """Validate date format"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v

    @validator('risk_percent')
    def validate_risk(cls, v):
        """Validate risk percentage is reasonable"""
        if not 0.1 <= v <= 10.0:
            raise ValueError('Risk percent must be between 0.1 and 10.0')
        return v

    @validator('max_positions')
    def validate_max_positions(cls, v):
        """Validate max positions is reasonable"""
        if not 1 <= v <= 10:
            raise ValueError('Max positions must be between 1 and 10')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "EURUSD",
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "strategy": "both",
                "timeframe": "M15",
                "initial_balance": 10000.0,
                "risk_percent": 2.0,
                "max_positions": 2,
                "parameters": {
                    "min_confidence": 65.0,
                    "min_csm_diff": 15.0
                }
            }
        }


class OptimizationRequest(BaseModel):
    """Request model for parameter optimization"""

    symbol: str = Field(..., description="Trading pair")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    strategy: str = Field(..., description="Strategy to optimize")
    parameter_ranges: Dict = Field(..., description="Parameter ranges to test")
    optimization_type: str = Field("grid", description="Type: grid, random, or walkforward")

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "EURUSD",
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "strategy": "trend_rider",
                "parameter_ranges": {
                    "min_confidence": [60, 65, 70, 75],
                    "min_csm_diff": [10, 15, 20, 25]
                },
                "optimization_type": "grid"
            }
        }


class ConfigValidationRequest(BaseModel):
    """Request to validate a backtest configuration"""

    config: BacktestRequest

    class Config:
        json_schema_extra = {
            "example": {
                "config": {
                    "symbol": "EURUSD",
                    "start_date": "2024-01-01",
                    "end_date": "2024-12-31",
                    "strategy": "both"
                }
            }
        }


class MultiPairBacktestRequest(BaseModel):
    """Request model for multi-pair backtest"""

    pairs: List[str] = Field(..., description="List of trading pairs (e.g., ['EURUSD', 'GBPUSD'])")
    strategies: List[str] = Field(..., description="Strategies to run: ['trend_rider', 'range_rider']")
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    timeframe: str = Field("M15", description="Chart timeframe: M15, H1, or H4")
    config: Dict = Field(..., description="Backtest configuration")

    @validator('pairs')
    def validate_pairs(cls, v):
        """Validate pairs list"""
        valid_symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD', 'NZDUSD', 'EURGBP', 'EURJPY']
        if not v or len(v) == 0:
            raise ValueError('At least one pair must be specified')
        for symbol in v:
            if symbol not in valid_symbols:
                raise ValueError(f'Symbol {symbol} must be one of {valid_symbols}')
        return v

    @validator('strategies')
    def validate_strategies(cls, v):
        """Validate strategies list"""
        valid_strategies = ['trend_rider', 'range_rider']
        if not v or len(v) == 0:
            raise ValueError('At least one strategy must be specified')
        for strategy in v:
            if strategy not in valid_strategies:
                raise ValueError(f'Strategy {strategy} must be one of {valid_strategies}')
        return v

    @validator('start_date', 'end_date')
    def validate_date_format(cls, v):
        """Validate date format"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v

    @validator('config')
    def validate_config(cls, v):
        """Validate required config fields"""
        required_fields = ['initial_balance', 'risk_percent', 'max_concurrent_positions']
        for field in required_fields:
            if field not in v:
                raise ValueError(f'Config must contain {field}')

        # Validate ranges
        if not 1000 <= v['initial_balance'] <= 1000000:
            raise ValueError('initial_balance must be between 1000 and 1000000')
        if not 0.1 <= v['risk_percent'] <= 10.0:
            raise ValueError('risk_percent must be between 0.1 and 10.0')
        if not 1 <= v['max_concurrent_positions'] <= 10:
            raise ValueError('max_concurrent_positions must be between 1 and 10')

        return v

    class Config:
        json_schema_extra = {
            "example": {
                "pairs": ["EURUSD", "GBPUSD", "USDJPY"],
                "strategies": ["trend_rider", "range_rider"],
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "timeframe": "M15",
                "config": {
                    "initial_balance": 10000.0,
                    "risk_percent": 2.0,
                    "max_concurrent_positions": 2,
                    "min_confidence": 50.0,
                    "take_profit_r": 2.0
                }
            }
        }
