"""
Backtest API Endpoints
Core routes for backtest execution and results retrieval
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from typing import List
import uuid
import os

from src.api.models.requests import BacktestRequest, ConfigValidationRequest, MultiPairBacktestRequest
from src.api.models.responses import (
    BacktestResponse,
    BacktestStatus,
    BacktestResults,
    BacktestSummary,
    BacktestListItem,
    ValidationResponse,
    MultiPairBacktestResults
)
from src.api.services.backtest_service import BacktestService

router = APIRouter()

# Create service instance (singleton for now)
backtest_service = BacktestService()


@router.post("/run", response_model=BacktestResponse, tags=["Backtest"])
async def run_backtest(request: BacktestRequest, background_tasks: BackgroundTasks):
    """
    Start a new backtest (runs asynchronously)

    - **symbol**: Trading pair (EURUSD, GBPUSD, etc.)
    - **start_date**: Start date (YYYY-MM-DD)
    - **end_date**: End date (YYYY-MM-DD)
    - **strategy**: Strategy to run (trend_rider, range_rider, or both)
    - **initial_balance**: Starting balance (default: 10000.0)
    - **risk_percent**: Risk per trade percentage (default: 2.0)
    - **max_positions**: Max concurrent positions (default: 2)
    - **parameters**: Optional strategy parameters

    Returns task_id for tracking progress
    """
    # Generate unique task ID
    task_id = str(uuid.uuid4())

    # Create task
    backtest_service.create_task(task_id, request)

    # Execute in background
    background_tasks.add_task(backtest_service.execute_backtest, task_id)

    return BacktestResponse(task_id=task_id, status="queued")


@router.post("/multi-pair", response_model=BacktestResponse, tags=["Backtest"])
async def run_multi_pair_backtest(request: MultiPairBacktestRequest, background_tasks: BackgroundTasks):
    """
    Start a multi-pair backtest (runs asynchronously)

    Tests multiple currency pairs with selected strategies simultaneously.
    Merges results chronologically and provides aggregate statistics.

    - **pairs**: List of trading pairs (e.g., ["EURUSD", "GBPUSD", "USDJPY"])
    - **strategies**: Strategies to run (e.g., ["trend_rider", "range_rider"])
    - **start_date**: Start date (YYYY-MM-DD)
    - **end_date**: End date (YYYY-MM-DD)
    - **config**: Configuration object with:
        - initial_balance: Starting balance (default: 10000.0)
        - risk_percent: Risk per trade percentage (default: 2.0)
        - max_concurrent_positions: Max positions across ALL pairs (default: 2)
        - min_confidence: Minimum confidence threshold (default: 50.0)
        - take_profit_r: Take profit target in R (default: 2.0)

    Returns task_id for tracking progress
    """
    # Generate unique task ID
    task_id = str(uuid.uuid4())

    # Create task
    backtest_service.create_task(task_id, request)

    # Execute in background
    background_tasks.add_task(backtest_service.execute_multi_pair_backtest, task_id)

    return BacktestResponse(task_id=task_id, status="queued")


@router.get("/multi-pair/{task_id}/results", response_model=MultiPairBacktestResults, tags=["Backtest"])
async def get_multi_pair_results(task_id: str):
    """
    Get complete multi-pair backtest results

    Returns aggregate performance metrics, trades merged chronologically,
    and breakdowns by pair and strategy.

    **Note**: This endpoint returns large amounts of data for multi-pair backtests.
    """
    result = backtest_service.get_task_results(task_id)

    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    if result["status"] != "complete":
        raise HTTPException(
            status_code=409,
            detail=f"Backtest not complete. Current status: {result['status']}"
        )

    return result["data"]


@router.get("/{task_id}/status", response_model=BacktestStatus, tags=["Backtest"])
async def get_backtest_status(task_id: str):
    """
    Get backtest status and progress

    Returns current status, progress percentage, and estimated time remaining
    """
    status = backtest_service.get_task_status(task_id)

    if not status:
        raise HTTPException(status_code=404, detail="Task not found")

    return status


@router.get("/{task_id}/results", response_model=BacktestResults, tags=["Backtest"])
async def get_backtest_results(task_id: str):
    """
    Get complete backtest results

    Returns full performance metrics, trade list, equity curve, and strategy breakdown

    **Note**: This endpoint returns large amounts of data. Use /summary for metrics only.
    """
    result = backtest_service.get_task_results(task_id)

    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    if result["status"] != "complete":
        raise HTTPException(
            status_code=409,
            detail=f"Backtest not complete. Current status: {result['status']}"
        )

    return result["data"]


@router.get("/{task_id}/summary", response_model=BacktestSummary, tags=["Backtest"])
async def get_backtest_summary(task_id: str):
    """
    Get abbreviated backtest results (metrics only)

    Returns key performance metrics without trade list or equity curve.
    Much faster than /results for large backtests.
    """
    summary = backtest_service.get_task_summary(task_id)

    if not summary:
        raise HTTPException(status_code=404, detail="Task not found or not complete")

    return summary


@router.get("/list", response_model=List[BacktestListItem], tags=["Backtest"])
async def list_backtests():
    """
    List all backtests

    Returns a list of all backtest tasks with their current status
    """
    return backtest_service.list_tasks()


@router.get("/{task_id}/charts", response_class=HTMLResponse, tags=["Backtest"])
async def get_backtest_charts(task_id: str):
    """
    Get interactive backtest charts (HTML page)

    Returns an HTML page with candlestick chart showing trades
    and equity curve with performance metrics.
    """
    task = backtest_service.tasks.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["status"] != "complete":
        raise HTTPException(
            status_code=409,
            detail=f"Backtest not complete. Current status: {task['status']}"
        )

    chart_path = task.get("chart_path")
    if not chart_path or not os.path.exists(chart_path):
        raise HTTPException(
            status_code=404,
            detail="Charts not available for this backtest"
        )

    # Return HTML file content
    with open(chart_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    return HTMLResponse(content=html_content)


@router.get("/{task_id}/ohlc", tags=["Backtest"])
async def get_backtest_ohlc(task_id: str):
    """
    Get OHLC candlestick data for chart visualization

    Returns candlestick data (open, high, low, close), indicators,
    and active/closed trade information for visual chart playback.
    """
    task = backtest_service.tasks.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["status"] != "complete":
        raise HTTPException(
            status_code=409,
            detail=f"Backtest not complete. Current status: {task['status']}"
        )

    ohlc_data = task.get("ohlc_data")
    if not ohlc_data:
        raise HTTPException(
            status_code=404,
            detail="OHLC data not available for this backtest"
        )

    return ohlc_data


@router.get("/{task_id}/ohlc-m1", tags=["Backtest"])
async def get_backtest_ohlc_m1(task_id: str):
    """
    Get M1 (1-minute) OHLC candlestick data for enhanced playback

    Returns M1-level candlestick data for smooth chart playback.
    This provides 15x more granular price movement than M15 data.
    """
    task = backtest_service.tasks.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["status"] != "complete":
        raise HTTPException(
            status_code=409,
            detail=f"Backtest not complete. Current status: {task['status']}"
        )

    # Get M1 OHLC data
    m1_data = backtest_service.get_m1_ohlc_data(task_id)

    if not m1_data:
        raise HTTPException(
            status_code=404,
            detail="M1 data not available for this backtest"
        )

    return m1_data


@router.delete("/{task_id}", tags=["Backtest"])
async def delete_backtest(task_id: str):
    """
    Delete a backtest task

    Removes task from memory. Cannot delete running tasks.
    """
    task = backtest_service.get_task_status(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["status"] == "running":
        raise HTTPException(
            status_code=409,
            detail="Cannot delete running task. Wait for completion or cancellation."
        )

    success = backtest_service.delete_task(task_id)

    return {"success": success, "message": f"Task {task_id} deleted"}


@router.post("/validate", response_model=ValidationResponse, tags=["Configuration"])
async def validate_config(request: ConfigValidationRequest):
    """
    Validate a backtest configuration

    Checks if configuration is valid before running backtest
    """
    errors = []

    config = request.config

    # Validate date range
    if config.start_date >= config.end_date:
        errors.append("start_date must be before end_date")

    # Validate year matches
    start_year = config.start_date[:4]
    end_year = config.end_date[:4]
    if start_year != end_year:
        errors.append("start_date and end_date must be in the same year (current limitation)")

    # Additional validations can be added here

    return ValidationResponse(
        valid=len(errors) == 0,
        errors=errors
    )



@router.post("/multi-pair", response_model=BacktestResponse, tags=["Backtest"])
async def run_multi_pair_backtest(
    request: MultiPairBacktestRequest,
    background_tasks: BackgroundTasks
):
    """
    Start a multi-pair backtest (runs asynchronously)
    
    - **pairs**: List of currency pairs (e.g., ["EURUSD", "GBPUSD", "USDJPY"])
    - **strategies**: List of strategies (e.g., ["trend_rider", "range_rider"])
    - **start_date**: Start date (YYYY-MM-DD)
    - **end_date**: End date (YYYY-MM-DD)
    - **timeframe**: Chart timeframe (default: M15)
    - **config**: Backtest configuration (balance, risk, positions, etc.)
    
    Returns task_id for tracking progress
    """
    # Generate unique task ID
    task_id = str(uuid.uuid4())
    
    # Create task
    backtest_service.create_task(task_id, request)
    
    # Execute in background
    background_tasks.add_task(backtest_service.execute_multi_pair_backtest, task_id)
    
    return BacktestResponse(task_id=task_id, status="queued")


@router.get("/multi-pair/{task_id}/results", tags=["Backtest"])
async def get_multi_pair_results(task_id: str):
    """
    Get complete multi-pair backtest results
    
    Returns:
    - All trades chronologically sorted
    - Overall statistics
    - Per-pair breakdown
    - Per-strategy breakdown
    - Equity curve
    - Chart data for each pair
    """
    result = backtest_service.get_task_results(task_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if result["status"] != "complete":
        raise HTTPException(
            status_code=409,
            detail=f"Backtest not complete. Current status: {result['status']}"
        )
    
    return result["data"]
