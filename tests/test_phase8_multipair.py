"""
Phase 8 Multi-Pair Backtest Tests
Tests multi-pair API endpoint, result merging, and statistics calculation
"""

import pytest
import sys
import os
from datetime import datetime

# Add project paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.api.services.backtest_service import BacktestService


class TestMultiPairModels:
    """Test Pydantic model validation"""

    def test_multi_pair_request_validation(self):
        """Test request model validates correctly"""
        from src.api.models.requests import MultiPairBacktestRequest, BacktestConfigModel

        # Valid request
        request = MultiPairBacktestRequest(
            pairs=["EURUSD", "GBPUSD"],
            strategies=["trend_rider", "range_rider"],
            start_date="2024-01-01",
            end_date="2024-12-31",
            timeframe="M15",
            config=BacktestConfigModel(
                initial_balance=10000.0,
                risk_percent=0.02,
                max_concurrent_positions=2
            )
        )

        assert len(request.pairs) == 2
        assert request.config.risk_percent == 0.02
        print("✓ Test 1/10: Multi-pair request validation passed")

    def test_invalid_pair_validation(self):
        """Test invalid pair raises error"""
        from src.api.models.requests import MultiPairBacktestRequest, BacktestConfigModel

        with pytest.raises(ValueError, match="Invalid pair"):
            MultiPairBacktestRequest(
                pairs=["XXXUSD"],  # Invalid
                strategies=["trend_rider"],
                start_date="2024-01-01",
                end_date="2024-12-31",
                config=BacktestConfigModel()
            )
        print("✓ Test 2/10: Invalid pair validation passed")

    def test_risk_percent_validation(self):
        """Test risk_percent validates range"""
        from src.api.models.requests import BacktestConfigModel

        with pytest.raises(ValueError, match="risk_percent must be between"):
            BacktestConfigModel(risk_percent=0.15)  # Too high (15%)
        print("✓ Test 3/10: Risk percent validation passed")


class TestMultiPairService:
    """Test service layer logic"""

    @pytest.fixture
    def service(self):
        """Create BacktestService instance"""
        return BacktestService()

    def test_convert_side_to_csharp(self, service):
        """Test BUY/SELL → LONG/SHORT conversion"""
        assert service._convert_side_to_csharp("BUY") == "LONG"
        assert service._convert_side_to_csharp("SELL") == "SHORT"
        assert service._convert_side_to_csharp("LONG") == "LONG"
        print("✓ Test 4/10: Side conversion passed")

    def test_convert_strategy_to_csharp(self, service):
        """Test strategy name conversion"""
        assert service._convert_strategy_to_csharp("trend_rider") == "TREND_RIDER"
        assert service._convert_strategy_to_csharp("TREND_RIDER") == "TREND_RIDER"
        assert service._convert_strategy_to_csharp("range_rider") == "RANGE_RIDER"
        print("✓ Test 5/10: Strategy conversion passed")

    def test_format_timestamp(self, service):
        """Test timestamp formatting"""
        dt = datetime(2024, 1, 5, 12, 0, 0)
        result = service._format_timestamp(dt)
        assert "2024-01-05" in result
        assert "12:00:00" in result
        print("✓ Test 6/10: Timestamp formatting passed")

    def test_calculate_overall_statistics(self, service):
        """Test overall statistics calculation"""
        trades = [
            {"r_multiple": 2.0, "profit_loss": 200.0, "exit_time": "2024-01-01T10:00:00"},
            {"r_multiple": -1.0, "profit_loss": -100.0, "exit_time": "2024-01-02T10:00:00"},
            {"r_multiple": 1.5, "profit_loss": 150.0, "exit_time": "2024-01-03T10:00:00"}
        ]

        stats = service._calculate_overall_statistics(trades, 10000.0)

        assert stats["total_trades"] == 3
        assert stats["wins"] == 2
        assert stats["losses"] == 1
        assert abs(stats["win_rate"] - 66.7) < 0.1
        assert abs(stats["total_r"] - 2.5) < 0.01
        assert abs(stats["net_profit"] - 250.0) < 0.01
        assert abs(stats["final_balance"] - 10250.0) < 0.01
        print("✓ Test 7/10: Overall statistics calculation passed")

    def test_calculate_pair_statistics(self, service):
        """Test per-pair statistics calculation"""
        trades = [
            {"symbol": "EURUSD", "r_multiple": 2.0, "profit_loss": 200.0},
            {"symbol": "EURUSD", "r_multiple": -1.0, "profit_loss": -100.0}
        ]

        stats = service._calculate_pair_statistics(trades)

        assert stats["trades"] == 2
        assert stats["wins"] == 1
        assert stats["losses"] == 1
        assert stats["win_rate"] == 50.0
        assert abs(stats["total_r"] - 1.0) < 0.01
        print("✓ Test 8/10: Pair statistics calculation passed")

    def test_build_unified_equity_curve(self, service):
        """Test equity curve construction"""
        trades = [
            {
                "entry_time": "2024-01-01T09:00:00",
                "exit_time": "2024-01-01T12:00:00",
                "r_multiple": 2.0,
                "profit_loss": 200.0,
                "strategy": "TREND_RIDER"
            },
            {
                "entry_time": "2024-01-02T09:00:00",
                "exit_time": "2024-01-02T12:00:00",
                "r_multiple": -1.0,
                "profit_loss": -100.0,
                "strategy": "RANGE_RIDER"
            }
        ]

        equity_curve = service._build_unified_equity_curve(trades, 10000.0)

        assert len(equity_curve) == 3  # Start + 2 trades
        assert equity_curve[0]["balance"] == 10000.0
        assert equity_curve[1]["balance"] == 10200.0
        assert equity_curve[2]["balance"] == 10100.0
        assert abs(equity_curve[2]["cumulative_r"] - 1.0) < 0.01
        print("✓ Test 9/10: Equity curve construction passed")

    def test_trade_chronological_sorting(self, service):
        """Test trades are sorted chronologically across pairs"""
        # Mock trades from multiple pairs
        all_trades = [
            {"symbol": "GBPUSD", "exit_time": "2024-01-05T14:00:00", "entry_time": "2024-01-05T10:00:00"},
            {"symbol": "EURUSD", "exit_time": "2024-01-05T10:00:00", "entry_time": "2024-01-05T09:00:00"},
            {"symbol": "USDJPY", "exit_time": "2024-01-05T12:00:00", "entry_time": "2024-01-05T11:00:00"}
        ]

        # Sort chronologically
        all_trades.sort(key=lambda t: t["exit_time"] if t["exit_time"] else t["entry_time"])

        # Verify order
        assert all_trades[0]["symbol"] == "EURUSD"  # 10:00
        assert all_trades[1]["symbol"] == "USDJPY"  # 12:00
        assert all_trades[2]["symbol"] == "GBPUSD"  # 14:00
        print("✓ Test 10/10: Chronological sorting passed")


def run_all_tests():
    """Run all tests and print summary"""
    print("\n" + "="*70)
    print("  PHASE 8 MULTI-PAIR BACKTEST TESTS")
    print("="*70 + "\n")

    # Model tests
    print("Model Validation Tests:")
    test_models = TestMultiPairModels()
    test_models.test_multi_pair_request_validation()
    test_models.test_invalid_pair_validation()
    test_models.test_risk_percent_validation()

    print("\nService Logic Tests:")
    test_service = TestMultiPairService()
    service = BacktestService()
    test_service.test_convert_side_to_csharp(service)
    test_service.test_convert_strategy_to_csharp(service)
    test_service.test_format_timestamp(service)
    test_service.test_calculate_overall_statistics(service)
    test_service.test_calculate_pair_statistics(service)
    test_service.test_build_unified_equity_curve(service)
    test_service.test_trade_chronological_sorting(service)

    print("\n" + "="*70)
    print("  ALL 10 TESTS PASSED!")
    print("="*70 + "\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
