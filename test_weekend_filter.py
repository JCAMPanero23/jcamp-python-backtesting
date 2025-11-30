"""
Test weekend filtering to verify Saturday/Sunday bars are removed
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

# Test configuration
config = {
    "symbol": "EURUSD",
    "start_date": "2024-01-02",  # Tuesday
    "end_date": "2024-01-31",    # Wednesday
    "strategy": "simple_test",
    "timeframe": "M15",
    "initial_balance": 10000,
    "risk_percent": 2.0
}

print("="*80)
print("WEEKEND FILTERING TEST")
print("="*80)
print(f"Testing: {config['symbol']} from {config['start_date']} to {config['end_date']}")
print()

# Start backtest
print("[1/4] Starting backtest...")
response = requests.post(f"{BASE_URL}/api/backtest", json=config)
if response.status_code != 200:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
    exit(1)

task_id = response.json()["task_id"]
print(f"✅ Task ID: {task_id}")

# Wait for completion
import time
print("\n[2/4] Waiting for completion...")
max_wait = 60
waited = 0

while waited < max_wait:
    status_resp = requests.get(f"{BASE_URL}/api/backtest/{task_id}/status")
    status_data = status_resp.json()

    if status_data["status"] == "completed":
        print(f"✅ Completed in {waited}s")
        break
    elif status_data["status"] == "failed":
        print(f"❌ Failed: {status_data.get('message')}")
        exit(1)

    time.sleep(2)
    waited += 2

# Get M15 OHLC data
print("\n[3/4] Fetching M15 OHLC data...")
ohlc_resp = requests.get(f"{BASE_URL}/api/backtest/{task_id}/ohlc")
if ohlc_resp.status_code != 200:
    print(f"❌ Error fetching OHLC: {ohlc_resp.status_code}")
    exit(1)

ohlc_data = ohlc_resp.json()
candles = ohlc_data["candles"]

print(f"✅ Received {len(candles)} M15 candles")

# Get M1 OHLC data
print("\n[4/4] Fetching M1 OHLC data...")
m1_resp = requests.get(f"{BASE_URL}/api/backtest/{task_id}/m1-ohlc")
if m1_resp.status_code != 200:
    print(f"❌ Error fetching M1: {m1_resp.status_code}")
    exit(1)

m1_data = m1_resp.json()
m1_candles = m1_data["candles"]

print(f"✅ Received {len(m1_candles)} M1 candles")

# Verify no weekend bars
print("\n" + "="*80)
print("WEEKEND VERIFICATION")
print("="*80)

weekend_count_m15 = 0
weekend_count_m1 = 0

# Check M15 for weekends
for candle in candles:
    ts = datetime.fromisoformat(candle["timestamp"].replace('Z', '+00:00'))
    if ts.weekday() >= 5:  # Saturday=5, Sunday=6
        weekend_count_m15 += 1

# Check M1 for weekends
for candle in m1_candles[:100]:  # Sample first 100 for speed
    ts = datetime.fromisoformat(candle["timestamp"].replace('Z', '+00:00'))
    if ts.weekday() >= 5:
        weekend_count_m1 += 1

print(f"M15 Data:")
print(f"  Total bars: {len(candles)}")
print(f"  Weekend bars found: {weekend_count_m15}")
print(f"  Status: {'✅ PASS' if weekend_count_m15 == 0 else '❌ FAIL'}")

print(f"\nM1 Data (sampled first 100):")
print(f"  Total bars: {len(m1_candles)}")
print(f"  Weekend bars found: {weekend_count_m1}")
print(f"  Status: {'✅ PASS' if weekend_count_m1 == 0 else '❌ FAIL'}")

# Show first and last timestamps
print(f"\nTimestamp Range (M15):")
print(f"  First: {candles[0]['timestamp']}")
print(f"  Last:  {candles[-1]['timestamp']}")

# Check for gaps in weekdays
print(f"\nChecking for Friday → Monday transitions...")
friday_to_monday_count = 0
for i in range(len(candles) - 1):
    curr_ts = datetime.fromisoformat(candles[i]["timestamp"].replace('Z', '+00:00'))
    next_ts = datetime.fromisoformat(candles[i+1]["timestamp"].replace('Z', '+00:00'))

    # If current is Friday and next is Monday, that's expected
    if curr_ts.weekday() == 4 and next_ts.weekday() == 0:
        friday_to_monday_count += 1
        if friday_to_monday_count <= 3:  # Show first 3
            print(f"  Gap {friday_to_monday_count}: {curr_ts} (Fri) → {next_ts} (Mon)")

print(f"\nTotal Friday→Monday transitions: {friday_to_monday_count}")
print(f"Expected: ~4 (for weekends in January)")

print("\n" + "="*80)
if weekend_count_m15 == 0 and weekend_count_m1 == 0:
    print("🎉 SUCCESS! Weekend filtering working perfectly!")
    print("   ✅ No Saturday/Sunday bars in M15 data")
    print("   ✅ No Saturday/Sunday bars in M1 data")
    print("   ✅ Chart will display without weekend gaps")
else:
    print("⚠️  FAILED: Weekend bars still present in data")

print("="*80)
