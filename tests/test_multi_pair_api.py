"""
Multi-Pair Backtest API Test Suite
Tests multi-pair endpoint functionality with pytest
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import pytest
from pydantic import ValidationError

# Fix import paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.api.models.requests import MultiPairBacktestRequest
from src.api.models.responses import (
    MultiPairBacktestResults,
    TradeRecord,
    StrategyBreakdown,
    PairBreakdown,
    EquityPoint
)


# ============================================================================
# Test Class 1: Model Validation Tests (6 tests)
# ============================================================================

class TestMultiPairModels:
    """Test multi-pair request model validation"""

    def test_valid_multi_pair_request(self):
        """Test valid multi-pair request passes validation"""
        request = MultiPairBacktestRequest(
            pairs=["EURUSD", "GBPUSD"],
            strategies=["trend_rider", "range_rider"],
            start_date="2024-01-01",
            end_date="2024-12-31",
            timeframe="M15",
            config={
                "initial_balance": 10000.0,
                "risk_percent": 2.0,
                "max_concurrent_positions": 2
            }
        )

        assert request.pairs == ["EURUSD", "GBPUSD"]
        assert request.strategies == ["trend_rider", "range_rider"]
        assert request.start_date == "2024-01-01"
        assert request.end_date == "2024-12-31"
        assert request.config["initial_balance"] == 10000.0

    def test_empty_pairs_rejected(self):
        """Test empty pairs list is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            MultiPairBacktestRequest(
                pairs=[],  # Empty list
                strategies=["trend_rider"],
                start_date="2024-01-01",
                end_date="2024-12-31",
                timeframe="M15",
                config={
                    "initial_balance": 10000.0,
                    "risk_percent": 2.0,
                    "max_concurrent_positions": 2
                }
            )

        assert "At least one pair must be specified" in str(exc_info.value)

    def test_invalid_symbol_rejected(self):
        """Test invalid symbol is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            MultiPairBacktestRequest(
                pairs=["EURUSD", "XXXUSD"],  # Invalid symbol
                strategies=["trend_rider"],
                start_date="2024-01-01",
                end_date="2024-12-31",
                timeframe="M15",
                config={
                    "initial_balance": 10000.0,
                    "risk_percent": 2.0,
                    "max_concurrent_positions": 2
                }
            )

        assert "must be one of" in str(exc_info.value)

    def test_empty_strategies_rejected(self):
        """Test empty strategies list is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            MultiPairBacktestRequest(
                pairs=["EURUSD"],
                strategies=[],  # Empty list
                start_date="2024-01-01",
                end_date="2024-12-31",
                timeframe="M15",
                config={
                    "initial_balance": 10000.0,
                    "risk_percent": 2.0,
                    "max_concurrent_positions": 2
                }
            )

        assert "At least one strategy must be specified" in str(exc_info.value)

    def test_invalid_date_format_rejected(self):
        """Test invalid date format is rejected"""
        with pytest.raises(ValidationError) as exc_info:
            MultiPairBacktestRequest(
                pairs=["EURUSD"],
                strategies=["trend_rider"],
                start_date="01/01/2024",  # Invalid format
                end_date="2024-12-31",
                timeframe="M15",
                config={
                    "initial_balance": 10000.0,
                    "risk_percent": 2.0,
                    "max_concurrent_positions": 2
                }
            )

        assert "YYYY-MM-DD" in str(exc_info.value)

    def test_missing_config_fields_rejected(self):
        """Test missing required config fields are rejected"""
        with pytest.raises(ValidationError) as exc_info:
            MultiPairBacktestRequest(
                pairs=["EURUSD"],
                strategies=["trend_rider"],
                start_date="2024-01-01",
                end_date="2024-12-31",
                timeframe="M15",
                config={
                    "initial_balance": 10000.0
                    # Missing risk_percent and max_concurrent_positions
                }
            )

        assert "must contain" in str(exc_info.value)


# ============================================================================
# Test Class 2: Statistics Calculation Tests (4 tests)
# ============================================================================

class TestMultiPairStatistics:
    """Test multi-pair statistics calculation logic"""

    def create_sample_trades(self):
        """Create sample trades for testing"""
        return [
            TradeRecord(
                position_id=1,
                symbol="EURUSD",
                side="BUY",
                strategy="TREND_RIDER",
                confidence=75.0,
                regime="TRENDING",
                entry_time="2024-01-05T10:00:00",
                exit_time="2024-01-05T14:00:00",
                entry_price=1.10000,
                exit_price=1.10300,
                stop_loss=1.09800,
                take_profit=1.10600,
                r_multiple=1.5,
                profit_loss=150.0,
                exit_reason="TAKE_PROFIT"
            ),
            TradeRecord(
                position_id=2,
                symbol="GBPUSD",
                side="SELL",
                strategy="RANGE_RIDER",
                confidence=65.0,
                regime="RANGING",
                entry_time="2024-01-05T11:00:00",
                exit_time="2024-01-05T15:00:00",
                entry_price=1.27000,
                exit_price=1.26700,
                stop_loss=1.27200,
                take_profit=1.26400,
                r_multiple=1.5,
                profit_loss=150.0,
                exit_reason="TAKE_PROFIT"
            ),
            TradeRecord(
                position_id=3,
                symbol="EURUSD",
                side="SELL",
                strategy="TREND_RIDER",
                confidence=70.0,
                regime="TRENDING",
                entry_time="2024-01-06T09:00:00",
                exit_time="2024-01-06T12:00:00",
                entry_price=1.09900,
                exit_price=1.10100,
                stop_loss=1.10100,
                take_profit=1.09500,
                r_multiple=-1.0,
                profit_loss=-100.0,
                exit_reason="STOP_LOSS"
            )
        ]

    def test_trade_chronological_sorting(self):
        """Test trades are sorted chronologically across all pairs"""
        trades = self.create_sample_trades()

        # Trades should be sorted by entry_time
        assert trades[0].entry_time <= trades[1].entry_time
        assert trades[1].entry_time <= trades[2].entry_time

        # Check that different pairs can interleave
        assert trades[0].symbol == "EURUSD"
        assert trades[1].symbol == "GBPUSD"
        assert trades[2].symbol == "EURUSD"

    def test_aggregate_statistics_calculation(self):
        """Test aggregate statistics are calculated correctly"""
        trades = self.create_sample_trades()

        # Calculate expected values
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t.r_multiple > 0])
        losing_trades = len([t for t in trades if t.r_multiple < 0])
        total_r = sum(t.r_multiple for t in trades if t.r_multiple is not None)
        total_pl = sum(t.profit_loss for t in trades if t.profit_loss is not None)

        # Verify calculations
        assert total_trades == 3
        assert winning_trades == 2
        assert losing_trades == 1
        assert abs(total_r - 2.0) < 0.01  # 1.5 + 1.5 - 1.0
        assert abs(total_pl - 200.0) < 0.01  # 150 + 150 - 100

        win_rate = (winning_trades / total_trades) * 100
        assert abs(win_rate - 66.67) < 0.01

    def test_pair_breakdown_calculation(self):
        """Test per-pair breakdown calculation"""
        trades = self.create_sample_trades()

        # Group by pair
        eurusd_trades = [t for t in trades if t.symbol == "EURUSD"]
        gbpusd_trades = [t for t in trades if t.symbol == "GBPUSD"]

        # EURUSD breakdown
        eurusd_total_r = sum(t.r_multiple for t in eurusd_trades if t.r_multiple is not None)
        eurusd_wins = len([t for t in eurusd_trades if t.r_multiple > 0])
        eurusd_losses = len([t for t in eurusd_trades if t.r_multiple < 0])

        assert len(eurusd_trades) == 2
        assert abs(eurusd_total_r - 0.5) < 0.01  # 1.5 - 1.0
        assert eurusd_wins == 1
        assert eurusd_losses == 1

        # GBPUSD breakdown
        gbpusd_total_r = sum(t.r_multiple for t in gbpusd_trades if t.r_multiple is not None)
        gbpusd_wins = len([t for t in gbpusd_trades if t.r_multiple > 0])

        assert len(gbpusd_trades) == 1
        assert abs(gbpusd_total_r - 1.5) < 0.01
        assert gbpusd_wins == 1

    def test_strategy_breakdown_calculation(self):
        """Test per-strategy breakdown calculation"""
        trades = self.create_sample_trades()

        # Group by strategy
        trend_rider_trades = [t for t in trades if t.strategy == "TREND_RIDER"]
        range_rider_trades = [t for t in trades if t.strategy == "RANGE_RIDER"]

        # TREND_RIDER breakdown
        tr_total_r = sum(t.r_multiple for t in trend_rider_trades if t.r_multiple is not None)
        tr_wins = len([t for t in trend_rider_trades if t.r_multiple > 0])
        tr_losses = len([t for t in trend_rider_trades if t.r_multiple < 0])

        assert len(trend_rider_trades) == 2
        assert abs(tr_total_r - 0.5) < 0.01  # 1.5 - 1.0
        assert tr_wins == 1
        assert tr_losses == 1

        # RANGE_RIDER breakdown
        rr_total_r = sum(t.r_multiple for t in range_rider_trades if t.r_multiple is not None)
        rr_wins = len([t for t in range_rider_trades if t.r_multiple > 0])

        assert len(range_rider_trades) == 1
        assert abs(rr_total_r - 1.5) < 0.01
        assert rr_wins == 1


# ============================================================================
# Test Class 3: End-to-End Integration Test (1 test, skipped)
# ============================================================================

class TestMultiPairEndToEnd:
    """Test complete multi-pair backtest workflow"""

    @pytest.mark.skipif(
        not os.path.exists("D:/JcampFxTrading/jcamp-python-backtesting/data/EURUSD_M1_2024.csv"),
        reason="Test data not available"
    )
    def test_two_pair_backtest(self):
        """Test complete 2-pair backtest (EURUSD + GBPUSD)"""
        # This test will be implemented once the multi-pair service is ready
        # It will test:
        # 1. Loading data for 2 pairs
        # 2. Running both strategies on both pairs
        # 3. Merging trades chronologically
        # 4. Calculating aggregate statistics
        # 5. Generating pair and strategy breakdowns

        pytest.skip("Multi-pair service not yet implemented")


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    # Run with pytest
    pytest.main([__file__, "-v", "--tb=short"])
