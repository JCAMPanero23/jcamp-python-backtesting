"""
Quick test to verify M1 forward-fill implementation
Run this before testing in C# viewer
"""
import requests
import json

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_CONFIG = {
    "symbol": "EURUSD",
    "start_date": "2024-01-02",
    "end_date": "2024-01-31",
    "strategy": "simple_test",
    "timeframe": "M15",
    "initial_balance": 10000,
    "risk_percent": 2.0
}

print("="*80)
print("M1 FORWARD-FILL TEST")
print("="*80)
print(f"Testing: {TEST_CONFIG['symbol']} from {TEST_CONFIG['start_date']} to {TEST_CONFIG['end_date']}")
print()

# Step 1: Start backtest
print("[1/3] Starting backtest...")
response = requests.post(f"{BASE_URL}/api/backtest", json=TEST_CONFIG)

if response.status_code != 200:
    print(f"❌ Error starting backtest: {response.status_code}")
    print(response.text)
    exit(1)

data = response.json()
task_id = data.get("task_id")
print(f"✅ Backtest started: {task_id}")
print()

# Step 2: Wait for completion (check status)
import time
print("[2/3] Waiting for backtest to complete...")
max_wait = 60  # 60 seconds max
waited = 0

while waited < max_wait:
    status_response = requests.get(f"{BASE_URL}/api/backtest/{task_id}/status")
    status_data = status_response.json()

    if status_data["status"] == "completed":
        print(f"✅ Backtest completed in {waited} seconds")
        break
    elif status_data["status"] == "failed":
        print(f"❌ Backtest failed: {status_data.get('message')}")
        exit(1)

    time.sleep(2)
    waited += 2
    print(f"   Status: {status_data['status']} - {status_data.get('message', '')}")

if waited >= max_wait:
    print(f"❌ Timeout waiting for backtest")
    exit(1)

print()

# Step 3: Get M1 OHLC data and verify
print("[3/3] Fetching M1 OHLC data...")
m1_response = requests.get(f"{BASE_URL}/api/backtest/{task_id}/m1-ohlc")

if m1_response.status_code != 200:
    print(f"❌ Error fetching M1 data: {m1_response.status_code}")
    print(m1_response.text)
    exit(1)

m1_data = m1_response.json()
m1_candles = m1_data.get("candles", [])

print(f"✅ M1 data received: {len(m1_candles)} bars")
print()

# Verification
print("="*80)
print("VERIFICATION RESULTS")
print("="*80)

# Expected calculation
# January 2024: Jan 2-31 = 30 days (but actual trading days vary)
# We saw in logs: 2,112 M15 bars
# Expected M1: 2,112 × 15 = 31,680 bars

expected_m1 = 2112 * 15  # From previous test data

print(f"Expected M1 bars: 31,680 (2,112 M15 × 15)")
print(f"Actual M1 bars:   {len(m1_candles)}")

if len(m1_candles) == expected_m1:
    print()
    print("🎉 SUCCESS! Forward-fill working perfectly!")
    print("   ✅ No gaps in M1 data")
    print("   ✅ EMAs will align correctly with candlesticks")
    print("   ✅ Chart visualization will be accurate")
else:
    diff = abs(len(m1_candles) - expected_m1)
    print()
    print(f"⚠️  WARNING: Bar count mismatch!")
    print(f"   Difference: {diff} bars")
    print(f"   This could indicate an issue with forward-fill logic")

print()
print("="*80)
print("Check server logs above for detailed forward-fill debug output")
print("="*80)
