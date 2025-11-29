"""
JCAMP Backtesting REST API Server
FastAPI application for remote backtest execution
"""

import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.api import __version__

# Import routers
from src.api.routes import backtest, health

# Track server start time
START_TIME = time.time()

# Initialize FastAPI app
app = FastAPI(
    title="JCAMP Backtesting API",
    version=__version__,
    description="""
    REST API for Forex Trading Strategy Backtesting and Optimization

    ## Features
    - **Backtest Execution**: Run historical backtests remotely
    - **Progress Tracking**: Monitor backtest progress in real-time
    - **Results Retrieval**: Get comprehensive performance metrics
    - **Strategy Comparison**: Compare Trend Rider vs Range Rider
    - **Parameter Optimization**: Grid search and walk-forward analysis (Phase 6)

    ## Supported Symbols
    - EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, NZDUSD, EURGBP, EURJPY

    ## Supported Strategies
    - **Trend Rider**: EMA alignment + Currency Strength Meter
    - **Range Rider**: Support/Resistance trading
    - **Both**: Run both strategies simultaneously
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/openapi.json"
)

# CORS Configuration - Allow C# Monitor App
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:*",  # C# Monitor app (any port)
        "http://127.0.0.1:*",
        "http://localhost:3000",  # Common dev ports
        "http://localhost:5000",
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    print(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")

    return response

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "details": {"error": str(exc)}
        }
    )

# Include route modules
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(backtest.router, prefix="/api/v1/backtest", tags=["Backtest"])
# app.include_router(optimization.router, prefix="/api/v1/optimize", tags=["Optimization"])  # Phase 6

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """API root endpoint"""
    return {
        "name": "JCAMP Backtesting API",
        "version": __version__,
        "status": "online",
        "uptime_seconds": int(time.time() - START_TIME),
        "docs": "/docs",
        "health": "/api/v1/health"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Actions to perform on server startup"""
    print("=" * 70)
    print("  JCAMP BACKTESTING API SERVER")
    print("=" * 70)
    print(f"  Version: {__version__}")
    print(f"  Docs: http://localhost:8000/docs")
    print(f"  Health: http://localhost:8000/api/v1/health")
    print("=" * 70)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Actions to perform on server shutdown"""
    print("\nShutting down JCAMP Backtesting API Server...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
