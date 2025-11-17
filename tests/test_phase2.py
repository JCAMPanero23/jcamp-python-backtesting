"""
═══════════════════════════════════════════════════════════════════════════════
PHASE 2 VALIDATION TEST SUITE
═══════════════════════════════════════════════════════════════════════════════
Validates:
1. Technical indicators (ATR, EMA, ADX)
2. Regime detection logic
3. Period analysis (Jan-Mar vs Sep-Nov)
4. Integration with Phase 1 components

Expected Output:
✅ ATR calculation working
✅ EMA calculation working
✅ ADX calculation working
✅ Regime detection operational
✅ Jan-Mar 2024 classified as RANGING
✅ Sep-Nov 2024 classified as TRENDING
✅ Ready for Phase 3 (Strategy Engines)
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
from datetime import datetime

# Add directories to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'config'))
sys.path.insert(0, os.path.join(project_root, 'src'))

# Import modules
from mt5_settings import *
from data_loader import DataLoader
from indicators import TechnicalIndicators
from regime_detector import RegimeDetector, RegimeType

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
    """Run Phase 2 validation tests"""
    
    print_section("PHASE 2 VALIDATION TEST SUITE")
    print("Testing: Technical Indicators & Regime Detection")
    print("Target: Accurate market regime classification")
    
    # Test counters
    tests_passed = 0
    tests_failed = 0
    
    # Load data first
    print("Loading EURUSD data for testing...")
    try:
        loader = DataLoader(data_dir="data")
        eurusd_m1 = loader.load_pair_data('EURUSD', 2024)
        eurusd_h1 = loader.resample_to_timeframe(eurusd_m1, 'H1')
        print(f"✓ Loaded {len(eurusd_h1):,} H1 bars\n")
    except Exception as e:
        print(f"✗ Failed to load data: {e}")
        return False
    
    # Initialize components
    indicators = TechnicalIndicators()
    detector = RegimeDetector()
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 1: ATR Calculation
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(1, "ATR (Average True Range) Calculation")
    
    try:
        atr = indicators.get_atr(eurusd_h1, 14)
        
        # Validate ATR is reasonable
        assert atr > 0, "ATR must be positive"
        assert atr < eurusd_h1['close'].iloc[-1] * 0.1, "ATR too high (>10% of price)"
        
        atr_pct = atr / eurusd_h1['close'].iloc[-1] * 100
        
        print(f"Current Price: {eurusd_h1['close'].iloc[-1]:.5f}")
        print(f"ATR(14): {atr:.5f}")
        print(f"ATR as % of price: {atr_pct:.2f}%")
        
        print_result(True, f"ATR={atr:.5f}")
        tests_passed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 2: EMA Calculation
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(2, "EMA (Exponential Moving Average) Calculation")
    
    try:
        ema_20 = indicators.get_ema(eurusd_h1, 20)
        ema_50 = indicators.get_ema(eurusd_h1, 50)
        ema_sep = indicators.calculate_ema_separation(eurusd_h1, 20, 50)
        
        # Validate EMAs
        assert ema_20 > 0, "EMA20 must be positive"
        assert ema_50 > 0, "EMA50 must be positive"
        assert ema_sep >= 0, "EMA separation must be non-negative"
        
        current_price = eurusd_h1['close'].iloc[-1]
        ema_bullish = ema_20 > ema_50
        
        print(f"Current Price: {current_price:.5f}")
        print(f"EMA(20): {ema_20:.5f}")
        print(f"EMA(50): {ema_50:.5f}")
        print(f"EMA Separation: {ema_sep:.2f}%")
        print(f"Alignment: {'BULLISH (20>50)' if ema_bullish else 'BEARISH (50>20)'}")
        
        print_result(True, f"EMA separation={ema_sep:.2f}%")
        tests_passed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 3: ADX Calculation
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(3, "ADX (Average Directional Index) Calculation")
    
    try:
        adx = indicators.get_adx(eurusd_h1, 14)
        plus_di, minus_di = indicators.get_directional_indicators(eurusd_h1, 14)
        
        # Validate ADX and DI
        assert 0 <= adx <= 100, "ADX must be 0-100"
        assert plus_di >= 0, "+DI must be non-negative"
        assert minus_di >= 0, "-DI must be non-negative"
        
        trend_strength = "STRONG" if adx >= 25 else "WEAK"
        trend_dir = "+DI dominant" if plus_di > minus_di else "-DI dominant"
        
        print(f"ADX(14): {adx:.2f} ({trend_strength} trend)")
        print(f"+DI: {plus_di:.2f}")
        print(f"-DI: {minus_di:.2f}")
        print(f"Direction: {trend_dir}")
        
        print_result(True, f"ADX={adx:.2f}")
        tests_passed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 4: All Indicators Integration
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(4, "All Indicators Integration")
    
    try:
        all_ind = indicators.calculate_all_indicators(eurusd_h1)
        
        # Validate all required keys present
        required_keys = ['atr_14', 'ema_20', 'ema_50', 'ema_separation', 
                        'adx_14', 'plus_di', 'minus_di', 'trend_direction']
        
        for key in required_keys:
            assert key in all_ind, f"Missing indicator: {key}"
        
        print(f"Indicators calculated:")
        for key, value in all_ind.items():
            if isinstance(value, bool):
                print(f"  {key}: {value}")
            elif isinstance(value, int):
                print(f"  {key}: {value}")
            else:
                print(f"  {key}: {value:.4f}")
        
        print_result(True, "All indicators calculated")
        tests_passed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 5: Current Regime Detection
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(5, "Current Regime Detection")
    
    try:
        result = detector.detect_regime(eurusd_h1)
        
        # Validate result structure
        assert 'regime' in result, "Missing regime classification"
        assert 'score' in result, "Missing regime score"
        assert 'components' in result, "Missing score components"
        
        print(f"Regime: {result['regime'].value}")
        print(f"Score: {result['score']:.1f}%")
        print(f"Components:")
        for comp, value in result['components'].items():
            print(f"  {comp}: {value:.1f}/25")
        
        print_result(True, f"Regime={result['regime'].value}")
        tests_passed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 6: Jan-Mar 2024 Period Analysis (Expected: RANGING)
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(6, "Jan-Mar 2024 Analysis (Expected: RANGING)")
    
    try:
        stats = detector.analyze_period(eurusd_h1, '2024-01-01', '2024-03-31')
        
        # Validate stats structure
        assert 'dominant_regime' in stats, "Missing dominant regime"
        assert 'regime_percentages' in stats, "Missing regime percentages"
        
        dominant = stats['dominant_regime']
        pct_trending = stats['regime_percentages']['trending']
        pct_ranging = stats['regime_percentages']['ranging']
        pct_trans = stats['regime_percentages']['transitional']
        
        print(f"Period: {stats['period']}")
        print(f"Total Checks: {stats['total_checks']}")
        print(f"Distribution:")
        print(f"  Trending: {pct_trending:.1f}%")
        print(f"  Ranging: {pct_ranging:.1f}%")
        print(f"  Transitional: {pct_trans:.1f}%")
        print(f"Dominant: {dominant.value}")
        print(f"Decisiveness: {stats['regime_decisiveness']:.1f}%")
        
        # Check if ranging is dominant or at least significant
        is_ranging_dominant = (dominant == RegimeType.RANGING or 
                             pct_ranging >= pct_trending)
        
        print_result(is_ranging_dominant, 
                    f"Dominant regime: {dominant.value}")
        
        if is_ranging_dominant:
            tests_passed += 1
        else:
            tests_failed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 7: Sep-Nov 2024 Period Analysis (Expected: TRENDING)
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(7, "Sep-Nov 2024 Analysis (Expected: TRENDING)")
    
    try:
        stats = detector.analyze_period(eurusd_h1, '2024-09-01', '2024-11-30')
        
        # Validate stats structure
        assert 'dominant_regime' in stats, "Missing dominant regime"
        assert 'regime_percentages' in stats, "Missing regime percentages"
        
        dominant = stats['dominant_regime']
        pct_trending = stats['regime_percentages']['trending']
        pct_ranging = stats['regime_percentages']['ranging']
        pct_trans = stats['regime_percentages']['transitional']
        
        print(f"Period: {stats['period']}")
        print(f"Total Checks: {stats['total_checks']}")
        print(f"Distribution:")
        print(f"  Trending: {pct_trending:.1f}%")
        print(f"  Ranging: {pct_ranging:.1f}%")
        print(f"  Transitional: {pct_trans:.1f}%")
        print(f"Dominant: {dominant.value}")
        print(f"Decisiveness: {stats['regime_decisiveness']:.1f}%")
        
        # Check if trending is dominant
        is_trending_dominant = (dominant == RegimeType.TRENDING or 
                              pct_trending >= pct_ranging)
        
        print_result(is_trending_dominant, 
                    f"Dominant regime: {dominant.value}")
        
        if is_trending_dominant:
            tests_passed += 1
        else:
            tests_failed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TEST 8: Regime Decisiveness Check
    # ═══════════════════════════════════════════════════════════════════════════
    print_test(8, "Regime Decisiveness (Target: >75% decisive)")
    
    try:
        # Check full year
        stats_full = detector.analyze_period(eurusd_h1, '2024-01-01', '2024-12-31')
        
        decisiveness = stats_full['regime_decisiveness']
        pct_trans = stats_full['regime_percentages']['transitional']
        
        print(f"Full Year 2024:")
        print(f"  Decisiveness: {decisiveness:.1f}%")
        print(f"  Transitional: {pct_trans:.1f}%")
        print(f"  Target: >75% decisive (<25% transitional)")
        
        # Aim for <25% transitional states
        is_decisive = pct_trans < 25.0
        
        print_result(is_decisive, 
                    f"Decisiveness: {decisiveness:.1f}%")
        
        if is_decisive:
            tests_passed += 1
        else:
            tests_failed += 1
        
    except Exception as e:
        print_result(False, str(e))
        tests_failed += 1
    
    # ═══════════════════════════════════════════════════════════════════════════
    # FINAL SUMMARY
    # ═══════════════════════════════════════════════════════════════════════════
    print_section("PHASE 2 TEST RESULTS")
    
    total_tests = tests_passed + tests_failed
    pass_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    print(f"Tests Failed: {tests_failed}/{total_tests}")
    print(f"Pass Rate: {pass_rate:.1f}%")
    
    if tests_failed == 0:
        print("\n" + "🎉 "*20)
        print("ALL PHASE 2 TESTS PASSED!")
        print("✅ Technical indicators operational")
        print("✅ Regime detection working correctly")
        print("✅ Period analysis accurate")
        print("\n🚀 READY FOR PHASE 3: STRATEGY ENGINES")
        print("🎉 "*20)
    else:
        print("\n⚠️  SOME TESTS FAILED - PLEASE REVIEW ERRORS ABOVE")
    
    print("\n" + "═"*80 + "\n")
    
    return tests_failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
