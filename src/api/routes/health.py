"""
Health and Information Endpoints
Server status and system information
"""

import time
from fastapi import APIRouter
from src.api.models.responses import HealthResponse, InfoResponse
from src.api import __version__
from pathlib import Path

router = APIRouter()

# Track server start time
START_TIME = time.time()

@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint

    Returns server health status and uptime
    """
    uptime = int(time.time() - START_TIME)

    return HealthResponse(
        status="ok",
        version=__version__,
        uptime_seconds=uptime
    )


@router.get("/info", response_model=InfoResponse, tags=["Health"])
async def system_info():
    """
    System information endpoint

    Returns API capabilities, supported symbols, and data availability
    """
    # Check data directory for available symbols
    data_dir = Path(__file__).parent.parent.parent.parent / "data"
    available_symbols = {}

    if data_dir.exists():
        for symbol_dir in data_dir.iterdir():
            if symbol_dir.is_dir() and symbol_dir.suffix == ".sml":
                symbol = symbol_dir.stem
                # Check for data files
                csv_files = list(symbol_dir.glob("*.csv"))
                if csv_files:
                    # Get date range from filenames (e.g., 2024_M1.csv)
                    years = [f.stem.split('_')[0] for f in csv_files]
                    available_symbols[symbol] = f"{min(years)}-01-01 to {max(years)}-12-31"

    return InfoResponse(
        version=__version__,
        features=[
            "backtesting",
            "multi-strategy",
            "multi-pair",
            "performance-analytics",
            "optimization (coming soon)"
        ],
        supported_symbols=["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD", "NZDUSD", "EURGBP", "EURJPY"],
        supported_strategies=["trend_rider", "range_rider", "both"],
        data_available=available_symbols if available_symbols else {"EURUSD": "2024-01-01 to 2024-12-31"}
    )
