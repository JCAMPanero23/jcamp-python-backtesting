"""
═══════════════════════════════════════════════════════════════════════════════
PHASE 1 VALIDATION TEST SUITE
═══════════════════════════════════════════════════════════════════════════════
Validates:
1. Configuration loading
2. Data loader functionality
3. CSM calculation accuracy
4. Integration between components

Expected Output:
✅ All modules load correctly
✅ EURUSD data loaded successfully
✅ CSM values calculated (0-100 range)
✅ CSM differentials computed
✅ Ready for Phase 2 (Regime Detection)
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
from datetime import datetime, timedelta

# Fix import paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'config'))
sys.path.insert(0, os.path.join(project_root, 'src'))

# Import Phase 1 modules
from mt5_settings import *
from data_loader import DataLoader
from csm_calculator import CSMCalculator

def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "═"*80)
    print(f" {title}")
    print("═"*80 + "\n")

def print_test(test_num: int, description: str):
    """Print test header"""
    print(f"\n{'─'*80}")
    print(f"TEST {test_num}: {description}")
    print(f"{'─'*80}")

def print_result(passed: bool, message: str = ""):
    """Print test result"""
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"{status}{' - ' + message if message else ''}")

def main():
    """Run Phase 1 validation tests"""
    
    print_section("PHASE 1 VALIDATION TEST SUITE")
    print("Testing: Configuration, Data Loader, CSM Calculator")
    print("Target: Validate core infrastructure before strategies")
    
    # Test counters
    tests_passed = 0
    tests_failed = 0
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 1: Configuration Validation
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(1, "Configuration Validation")
    
    try:
        # Validate basic settings
        assert INITIAL_BALANCE > 0, "Invalid initial balance"
        assert 0 < RISK_PERCENT <= 100, "Invalid risk percent"
        assert len(CSM_PAIRS) == 15, "CSM must have 15 pairs"
        assert len(CSM_CURRENCIES) == 8, "CSM must have 8 currencies"
        
        print(f"Initial Balance: ${INITIAL_BALANCE:,.2f}")
        print(f"Risk Per Trade: {RISK_PERCENT}%")
        print(f"CSM Pairs: {len(CSM_PAIRS)}")
        print(f"CSM Currencies: {', '.join(CSM_CURRENCIES)}")
        print(f"Trend Rider Min Confidence: {TREND_RIDER_MIN_CONFIDENCE}%")
        print(f"Daily Loss Limit: {DAILY_LOSS_LIMIT_R}R")
        
        print_result(True, "Configuration valid")
        tests_passed += 1
        
    except AssertionError as e:
        print_result(False, str(e))
        tests_failed += 1
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 2: Data Loader - Single Pair
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(2, "Data Loader - Load EURUSD M1 Data")
    
    try:
        loader = DataLoader(data_dir="data")
        
        eurusd_m1 = loader.load_pair_data('EURUSD', 2024)
        
        # Validate data
        assert len(eurusd_m1) > 0, "No data loaded"
        assert 'open' in eurusd_m1.columns, "Missing OHLC columns"
        assert 'high' in eurusd_m1.columns, "Missing OHLC columns"
        assert 'low' in eurusd_m1.columns, "Missing OHLC columns"
        assert 'close' in eurusd_m1.columns, "Missing OHLC columns"
        
        start_date, end_date = loader.get_date_range(eurusd_m1)
        
        print(f"Loaded: {len(eurusd_m1):,} M1 bars")
        print(f"Date Range: {start_date} → {end_date}")
        print(f"Price Range: {eurusd_m1['low'].min():.5f} - {eurusd_m1['high'].max():.5f}")
        print(f"Columns: {eurusd_m1.columns.tolist()}")
        
        print_result(True, f"{len(eurusd_m1):,} bars loaded successfully")
        tests_passed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
        return  # Can't continue without data
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 3: Data Loader - Resampling
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(3, "Data Loader - Resample to H1")
    
    try:
        eurusd_h1 = loader.resample_to_timeframe(eurusd_m1, 'H1')
        
        # Validate resampling
        assert len(eurusd_h1) > 0, "Resampling failed"
        assert len(eurusd_h1) < len(eurusd_m1), "H1 should have fewer bars than M1"
        
        ratio = len(eurusd_m1) / len(eurusd_h1)
        
        print(f"M1 bars: {len(eurusd_m1):,}")
        print(f"H1 bars: {len(eurusd_h1):,}")
        print(f"Ratio: {ratio:.1f}x (expected ~60x)")
        
        # Check ratio is reasonable (should be ~60 for perfect M1→H1)
        assert 50 < ratio < 70, f"Unexpected resampling ratio: {ratio:.1f}"
        
        print_result(True, f"Resampled to {len(eurusd_h1):,} H1 bars")
        tests_passed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 4: Data Loader - Multiple Pairs
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(4, "Data Loader - Load Multiple Pairs for CSM")
    
    try:
        # Load subset of CSM pairs for testing (loading all 15 takes time)
        test_pairs = ['EURUSD', 'GBPUSD']
        
        multi_data = loader.load_multiple_pairs(test_pairs, 2024, 'H1')
        
        # Validate
        assert len(multi_data) > 0, "No pairs loaded"
        
        print(f"Loaded {len(multi_data)} pairs:")
        for pair, df in multi_data.items():
            print(f"  {pair}: {len(df):,} H1 bars")
        
        print_result(True, f"{len(multi_data)}/{len(test_pairs)} pairs loaded")
        tests_passed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
        multi_data = {}  # Ensure we have a dict for next tests
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 5: CSM Calculator - Initialization
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(5, "CSM Calculator - Initialization")
    
    try:
        csm = CSMCalculator()
        
        # Check initial state
        assert not csm.data_valid, "CSM should not be valid initially"
        assert len(csm.currency_strengths) == 8, "Should have 8 currencies"
        
        print(f"Lookback Hours: {csm.lookback_hours}")
        print(f"Calculation Period: {csm.calculation_period}H")
        print(f"Currencies: {', '.join(CSM_CURRENCIES)}")
        print(f"Initial strengths: {csm.currency_strengths}")
        
        print_result(True, "CSM initialized successfully")
        tests_passed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
        return
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 6: CSM Calculator - Calculate Strengths
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(6, "CSM Calculator - Calculate Currency Strengths")
    
    try:
        # Calculate CSM at a specific time (mid-year)
        test_time = datetime(2024, 6, 1, 12, 0, 0)
        
        success = csm.update_csm(multi_data, test_time, 'H1')
        
        assert success, "CSM calculation failed"
        assert csm.data_valid, "CSM should be valid after calculation"
        
        # Get all strengths
        strengths = csm.get_all_strengths()
        
        # Validate strengths are in range [0, 100]
        for curr, strength in strengths.items():
            assert 0 <= strength <= 100, f"{curr} strength out of range: {strength}"
        
        print(f"Calculation Time: {test_time}")
        print(f"Currency Strengths:")
        for curr in CSM_CURRENCIES:
            strength = csm.get_currency_strength(curr)
            print(f"  {curr}: {strength:6.2f}")
        
        strongest, str_val = csm.get_strongest_currency()
        weakest, weak_val = csm.get_weakest_currency()
        
        print(f"\nStrongest: {strongest} ({str_val:.2f})")
        print(f"Weakest: {weakest} ({weak_val:.2f})")
        print(f"Range: {str_val - weak_val:.2f}")
        
        print_result(True, "CSM calculated successfully")
        tests_passed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 7: CSM Calculator - Differentials
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(7, "CSM Calculator - Calculate Differentials")
    
    try:
        test_pairs_diff = ['EURUSD', 'GBPUSD']
        
        print("CSM Differentials (Base - Quote):")
        for pair in test_pairs_diff:
            diff = csm.get_csm_differential(pair)
            base, quote = get_base_quote(pair)
            base_str = csm.get_currency_strength(base)
            quote_str = csm.get_currency_strength(quote)
            
            print(f"  {pair}: {diff:+7.2f} ({base}:{base_str:.2f} - {quote}:{quote_str:.2f})")
            
            # Validate differential calculation
            expected_diff = base_str - quote_str
            assert abs(diff - expected_diff) < 0.01, f"Differential calculation error for {pair}"
        
        print_result(True, "Differentials calculated correctly")
        tests_passed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 8: CSM Calculator - Time Series
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(8, "CSM Calculator - Time Series Calculation")
    
    try:
        # Calculate CSM at multiple time points
        test_times = [
            datetime(2024, 1, 15, 12, 0, 0),  # January (ranging)
            datetime(2024, 6, 15, 12, 0, 0),  # June (mid-year)
            datetime(2024, 10, 15, 12, 0, 0), # October (trending)
        ]
        
        print("CSM Evolution Over Time:")
        for test_time in test_times:
            csm.update_csm(multi_data, test_time, 'H1')
            strongest, str_val = csm.get_strongest_currency()
            weakest, weak_val = csm.get_weakest_currency()
            
            print(f"\n{test_time.strftime('%Y-%m-%d')}:")
            print(f"  Strongest: {strongest} ({str_val:.2f})")
            print(f"  Weakest: {weakest} ({weak_val:.2f})")
            print(f"  EURUSD Diff: {csm.get_csm_differential('EURUSD'):+.2f}")
        
        print_result(True, "Time series calculation successful")
        tests_passed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
    
    # ═══════════════════════════════════════════════════════════════════════════
    # FINAL SUMMARY
    # ═══════════════════════════════════════════════════════════════════════════
    print_section("PHASE 1 TEST RESULTS")
    
    total_tests = tests_passed + tests_failed
    pass_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    print(f"Tests Failed: {tests_failed}/{total_tests}")
    print(f"Pass Rate: {pass_rate:.1f}%")
    
    if tests_failed == 0:
        print("\n" + "🎉 "*20)
        print("ALL PHASE 1 TESTS PASSED!")
        print("✅ Configuration loaded successfully")
        print("✅ Data loader working correctly")
        print("✅ CSM calculator operational")
        print("\n🚀 READY FOR PHASE 2: REGIME DETECTION")
        print("🎉 "*20)
    else:
        print("\n⚠️  SOME TESTS FAILED - PLEASE REVIEW ERRORS ABOVE")
    
    print("\n" + "═"*80 + "\n")
    
    return tests_failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
