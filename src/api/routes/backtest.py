"""
Backtest API Endpoints
Core routes for backtest execution and results retrieval
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import List
import uuid

from src.api.models.requests import BacktestRequest, ConfigValidationRequest
from src.api.models.responses import (
    BacktestResponse,
    BacktestStatus,
    BacktestResults,
    BacktestSummary,
    BacktestListItem,
    ValidationResponse
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
