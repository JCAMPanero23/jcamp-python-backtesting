#!/usr/bin/env python3
"""
Start the JCAMP Backtesting API Server
"""

import uvicorn
import sys
import io
from pathlib import Path

# Fix Windows encoding for Unicode output
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    print("=" * 70)
    print("  JCAMP BACKTESTING API SERVER")
    print("=" * 70)
    print("\n>> Starting server...")
    print(">> API Documentation: http://localhost:8000/docs")
    print(">> Health Check: http://localhost:8000/api/v1/health")
    print(">> System Info: http://localhost:8000/api/v1/info")
    print("\n>> Press CTRL+C to stop\n")
    print("=" * 70)

    try:
        uvicorn.run(
            "src.api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n>> Server stopped by user")
    except Exception as e:
        print(f"\n\n>> Error starting server: {e}")
        sys.exit(1)
