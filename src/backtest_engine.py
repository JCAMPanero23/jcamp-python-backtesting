"""
Backtest Engine - Main backtesting loop
Executes trades, manages positions, and tracks performance
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import sys
import os

# Add project paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'config'))

from mt5_settings import *
from src.data_loader import DataLoader
from src.csm_calculator import CSMCalculator
from src.indicators import TechnicalIndicators
from src.regime_detector import RegimeDetector
from src.strategies.trend_rider import TrendRiderStrategy
from src.strategies.range_rider import RangeRiderStrategy
from src.strategies.simple_test import SimpleTestStrategy
from src.position_manager import PositionManager, Position, ExitReason, PositionSide
from src.performance_tracker import PerformanceTracker


class BacktestEngine:
    """
    Main backtesting engine that simulates trading
    """
    
    def __init__(
        self,
        initial_balance: float = 10000.0,
        risk_percent: float = 2.0,
        max_positions: int = 2,
        timeframe: str = 'M15'
    ):
        """
        Initialize backtest engine.

        Args:
            initial_balance: Starting balance
            risk_percent: Risk per trade as percentage
            max_positions: Max concurrent positions
            timeframe: Chart timeframe (M15, H1, H4, etc.)
        """
        self.initial_balance = initial_balance
        self.risk_percent = risk_percent
        self.max_positions = max_positions
        self.timeframe = timeframe
        
        # Initialize components
        self.position_manager = PositionManager(max_positions)
        self.performance_tracker = PerformanceTracker(initial_balance)
        
        # Data components
        self.loader = DataLoader()
        self.csm_calc = CSMCalculator()
        self.indicators_calc = TechnicalIndicators()
        self.regime_detector = RegimeDetector()
        
        # Strategy components
        config = self._get_config()
        self.simple_test = SimpleTestStrategy(config)
        self.trend_rider = TrendRiderStrategy(config)
        self.range_rider = RangeRiderStrategy(config)
        
        # Tracking
        self.current_bar_index = 0
        self.verbose = True
        
    def _get_config(self) -> Dict:
        """Get configuration dictionary."""
        return {
            'initial_balance': self.initial_balance,
            'risk_percent': self.risk_percent,
            'trending_threshold_percent': TRENDING_THRESHOLD_PERCENT,
            'ranging_threshold_percent': RANGING_THRESHOLD_PERCENT,
            'min_adx_for_trending': MIN_ADX_FOR_TRENDING,
            'min_ema_separation': MIN_EMA_SEPARATION,
            'regime_adx_period': REGIME_ADX_PERIOD,
            'regime_ema_fast': REGIME_EMA_FAST,
            'regime_ema_slow': REGIME_EMA_SLOW,
            'atr_period': ATR_PERIOD,
            'trend_min_confidence': TREND_RIDER_MIN_CONFIDENCE,
            'trend_min_csm_diff': TREND_RIDER_MIN_CSM_DIFF,
            'trend_stop_loss_atr': TREND_RIDER_STOP_LOSS_ATR,
            'adx_strong_trend': MIN_ADX_FOR_TRENDING,
            'ema_separation_min': MIN_EMA_SEPARATION,
            'filter_ranging': True,
            'range_min_confidence': 60.0,
            'range_stop_loss_atr': 1.0,
            'range_break_even_r': RANGE_RIDER_BREAKEVEN_R,
            'range_max_hold_hours': RANGE_RIDER_MAX_HOLD_HOURS,
            'range_min_width_atr': 2.0,
            'range_edge_proximity_pct': 5.0,
            'rsi_oversold': 30.0,
            'rsi_overbought': 70.0,
        }
    
    def prepare_data(self, symbol: str, year: str) -> pd.DataFrame:
        """
        Load and prepare data with all indicators.
        
        Args:
            symbol: Trading pair (e.g., 'EURUSD')
            year: Year string (e.g., '2024')
            
        Returns:
            DataFrame with OHLC + indicators + CSM
        """
        if self.verbose:
            print(f"\n[DATA] Preparing data for {symbol} {year}...")
        
        # Load M1 data
        df_m1 = self.loader.load_pair_data(symbol, year)

        # Resample to specified timeframe
        df = self.loader.resample_to_timeframe(df_m1, self.timeframe)

        if self.verbose:
            print(f"[OK] Loaded {len(df):,} {self.timeframe} bars")
        
        # Add technical indicators
        if self.verbose:
            print("[TREND] Calculating technical indicators...")

        df['atr'] = self.indicators_calc.calculate_atr(df, 14)
        df['ema_fast'] = self.indicators_calc.calculate_ema(df, 20)
        df['ema_mid'] = self.indicators_calc.calculate_ema(df, 50)
        df['ema_slow'] = self.indicators_calc.calculate_ema(df, 100)

        adx_series, plus_di_series, minus_di_series = self.indicators_calc.calculate_adx(df, 14)
        df['adx'] = adx_series
        df['plus_di'] = plus_di_series
        df['minus_di'] = minus_di_series

        # Add RSI for Range Rider
        df['rsi'] = 50.0  # Simplified for now

        # Add CSM columns
        df['csm_base'] = 50.0
        df['csm_quote'] = 50.0
        df['csm_diff'] = 0.0

        if self.verbose:
            print("💪 Calculating Currency Strength Meter...")

        # Calculate CSM for each bar
        pair_data = {symbol: df}
        base, quote = symbol[:3], symbol[3:6]

        for idx in range(len(df)):
            current_time = df.index[idx]

            # Update CSM
            success = self.csm_calc.update_csm(pair_data, current_time.to_pydatetime(), self.timeframe)

            if success:
                base_strength = self.csm_calc.get_currency_strength(base)
                quote_strength = self.csm_calc.get_currency_strength(quote)
                diff = base_strength - quote_strength

                df.loc[current_time, 'csm_base'] = base_strength
                df.loc[current_time, 'csm_quote'] = quote_strength
                df.loc[current_time, 'csm_diff'] = diff

        if self.verbose:
            print("[OK] Data preparation complete!\n")

        return df
    
    def run_backtest(
        self,
        symbol: str,
        year: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """
        Run backtest on historical data.

        Args:
            symbol: Trading pair
            year: Year to test
            start_date: Optional start date (YYYY-MM-DD)
            end_date: Optional end date (YYYY-MM-DD)

        Returns:
            Dictionary with backtest results
        """
        print("\n" + "="*70)
        print(f"  JCAMP BACKTEST ENGINE - {symbol} {year}")
        print("="*70)

        # Prepare data
        df_full = self.prepare_data(symbol, year)

        # Define warmup period (500 M15 bars = ~5.2 days for H1 EMA100 calculation)
        WARMUP_BARS = 500

        # Calculate warmup start date
        if start_date:
            start_timestamp = pd.Timestamp(start_date)

            # Find the index of start_date in the full dataset
            start_idx = df_full.index.get_indexer([start_timestamp], method='bfill')[0]

            # Calculate warmup start index (ensure we don't go negative)
            warmup_start_idx = max(0, start_idx - WARMUP_BARS)

            # Check if we have enough warmup data
            actual_warmup_bars = start_idx - warmup_start_idx
            if actual_warmup_bars < WARMUP_BARS:
                print(f"\n[WARN] Insufficient warmup data!")
                print(f"[WARN] Need {WARMUP_BARS} M15 bars (~{WARMUP_BARS/96:.1f} days) for H1 EMA100")
                print(f"[WARN] Only have {actual_warmup_bars} bars (~{actual_warmup_bars/96:.1f} days)")
                print(f"[WARN] H1 EMAs may be inaccurate at the start of the backtest\n")
            else:
                print(f"\n[OK] Warmup data: {actual_warmup_bars} M15 bars (~{actual_warmup_bars/96:.1f} days)")

            # Include warmup bars before start_date for proper EMA calculation
            df = df_full.iloc[warmup_start_idx:]

            # Track the actual backtest start index (where we start trading)
            self.backtest_start_idx = start_idx - warmup_start_idx
        else:
            df = df_full
            self.backtest_start_idx = WARMUP_BARS

        # Filter end date if specified
        if end_date:
            # Include the entire end date (through 23:59:59)
            end_timestamp = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
            df = df[df.index <= end_timestamp]

        # Store dataframe and indicators for chart generation
        self.df = df
        self.indicators = self.indicators_calc

        print(f"\n[DATA] Full dataset: {df.index[0]} to {df.index[-1]} ({len(df):,} bars)")
        print(f"[TEST] Backtest period: {df.index[self.backtest_start_idx]} to {df.index[-1]}")
        print(f"[BAL] Initial balance: ${self.initial_balance:,.2f}")
        print(f"[RISK] Risk per trade: {self.risk_percent}%")
        print(f"[POS] Max positions: {self.max_positions}")

        print("\n" + "-"*70)
        print("Starting backtest simulation...")
        print("-"*70 + "\n")

        # Main backtest loop - start at backtest_start_idx to have warmup history
        for idx in range(self.backtest_start_idx, len(df)):
            self.current_bar_index = idx
            current_time = df.index[idx]
            current_price = df.iloc[idx]['close']
            
            # Check for exits first
            self._check_exits(df, idx)
            
            # Check daily loss limit
            date_key = current_time.strftime('%Y-%m-%d')
            if self.performance_tracker.is_daily_loss_limit_reached(date_key):
                continue  # Skip trading for rest of day
            
            # Check for new entries
            if self.position_manager.can_open_position():
                self._check_entries(df, idx, symbol)
        
        print("\n" + "-"*70)
        print("Backtest simulation complete!")
        print("-"*70)
        
        # Get results
        results = self._compile_results()
        
        # Print summary
        self.performance_tracker.print_summary()
        
        return results
    
    def _check_entries(self, df: pd.DataFrame, idx: int, symbol: str):
        """Check for new entry signals."""
        current_time = df.index[idx]
        current_price = df.iloc[idx]['close']
        
        # Get CSM data
        csm_data = {
            'differential': df.iloc[idx]['csm_diff'],
            'base_strength': df.iloc[idx]['csm_base'],
            'quote_strength': df.iloc[idx]['csm_quote']
        }
        
        # Detect regime
        regime_data = self.regime_detector.detect_regime(df, idx)
        regime = regime_data['regime']
        
        # Convert regime to string if it's an enum
        if hasattr(regime, 'value'):
            regime = regime.value
        elif hasattr(regime, 'name'):
            regime = regime.name
        else:
            regime = str(regime).split('.')[-1] if '.' in str(regime) else str(regime)
        
        # Check Simple Test Strategy (for chart testing)
        st_signal, st_confidence, st_details = self.simple_test.generate_signal(
            df, idx, csm_data, regime
        )

        if st_signal != 'NONE':
            self._open_position(
                symbol, st_signal, current_price, current_time,
                df, idx, 'SIMPLE_TEST', st_confidence, regime
            )
            return  # One entry per bar

        # DISABLED FOR TESTING: Check Trend Rider
        # tr_signal, tr_confidence, tr_details = self.trend_rider.generate_signal(
        #     df, idx, csm_data, regime
        # )
        #
        # if tr_signal != 'NONE':
        #     self._open_position(
        #         symbol, tr_signal, current_price, current_time,
        #         df, idx, 'TREND_RIDER', tr_confidence, regime
        #     )
        #     return  # One entry per bar

        # DISABLED FOR TESTING: Check Range Rider
        # rr_signal, rr_confidence, rr_details = self.range_rider.generate_signal(
        #     df, idx, csm_data, regime
        # )
        #
        # if rr_signal != 'NONE':
        #     self._open_position(
        #         symbol, rr_signal, current_price, current_time,
        #         df, idx, 'RANGE_RIDER', rr_confidence, regime
        #     )
    
    def _open_position(
        self,
        symbol: str,
        signal: str,
        entry_price: float,
        entry_time: datetime,
        df: pd.DataFrame,
        idx: int,
        strategy: str,
        confidence: float,
        regime: str
    ):
        """Open a new position."""
        # Get strategy object
        if strategy == 'SIMPLE_TEST':
            strategy_obj = self.simple_test
        elif strategy == 'TREND_RIDER':
            strategy_obj = self.trend_rider
        else:  # RANGE_RIDER
            strategy_obj = self.range_rider

        # Calculate stop loss
        stop_loss_distance = strategy_obj.get_stop_loss(df, idx, signal)
        
        # Calculate stop loss price
        if signal == 'BUY':
            stop_loss_price = entry_price - stop_loss_distance
        else:  # SELL
            stop_loss_price = entry_price + stop_loss_distance
        
        # Calculate position size based on risk
        risk_amount = self.performance_tracker.current_balance * (self.risk_percent / 100.0)
        position_size = risk_amount / (stop_loss_distance * 100000)  # Convert to lots
        position_size = round(position_size, 2)
        position_size = max(0.01, min(10.0, position_size))  # Clamp to reasonable range
        
        # Calculate take profit (optional - can be None for trailing only)
        take_profit = None
        if hasattr(strategy_obj, 'get_take_profit'):
            tp_distance = strategy_obj.get_take_profit(df, idx, signal)
            if signal == 'BUY':
                take_profit = entry_price + tp_distance
            else:  # SELL
                take_profit = entry_price - tp_distance
        
        # Open position
        position = self.position_manager.open_position(
            symbol=symbol,
            side=signal,
            entry_price=entry_price,
            entry_time=entry_time,
            stop_loss=stop_loss_price,
            take_profit=take_profit,
            position_size=position_size,
            strategy=strategy,
            confidence=confidence,
            regime=regime
        )
        
        if self.verbose:
            print(f"[ENTRY] {entry_time.strftime('%Y-%m-%d %H:%M')} | "
                  f"{signal:4s} {strategy:12s} | "
                  f"Price: {entry_price:.5f} | "
                  f"SL: {stop_loss_price:.5f} | "
                  f"Conf: {confidence:.1f}% | "
                  f"Regime: {regime}")
    
    def _check_exits(self, df: pd.DataFrame, idx: int):
        """Check if any open positions should be closed."""
        current_time = df.index[idx]
        current_price = df.iloc[idx]['close']
        current_high = df.iloc[idx]['high']
        current_low = df.iloc[idx]['low']
        
        positions_to_close = []
        
        for position in self.position_manager.open_positions:
            # Check stop loss
            if position.side == PositionSide.BUY:
                if current_low <= position.current_stop_loss:
                    positions_to_close.append((position, position.current_stop_loss, ExitReason.STOP_LOSS))
                    continue
            else:  # SELL
                if current_high >= position.current_stop_loss:
                    positions_to_close.append((position, position.current_stop_loss, ExitReason.STOP_LOSS))
                    continue
            
            # Check take profit
            if position.current_take_profit is not None:
                if position.side == PositionSide.BUY:
                    if current_high >= position.current_take_profit:
                        positions_to_close.append((position, position.current_take_profit, ExitReason.TAKE_PROFIT))
                        continue
                else:  # SELL
                    if current_low <= position.current_take_profit:
                        positions_to_close.append((position, position.current_take_profit, ExitReason.TAKE_PROFIT))
                        continue
            
            # Update position with current price
            self.position_manager.update_position(position, current_price, current_time)
            
            # Check Range Rider specific exits
            if position.strategy == 'RANGE_RIDER':
                # Check break-even exit
                current_r = position.calculate_current_r(current_price)
                if current_r >= 0.5:
                    positions_to_close.append((position, current_price, ExitReason.BREAK_EVEN))
                    continue
                
                # Check max hold time
                hold_hours = position.get_hold_time_hours(current_time)
                if hold_hours >= 48:
                    positions_to_close.append((position, current_price, ExitReason.MAX_HOLD_TIME))
                    continue
        
        # Close positions
        for position, exit_price, exit_reason in positions_to_close:
            self._close_position(position, exit_price, current_time, exit_reason)
    
    def _close_position(
        self,
        position: Position,
        exit_price: float,
        exit_time: datetime,
        exit_reason: ExitReason
    ):
        """Close a position and record results."""
        # Close in position manager
        self.position_manager.close_position(position, exit_price, exit_time, exit_reason)
        
        # Record in performance tracker
        self.performance_tracker.record_trade(
            timestamp=exit_time,
            r_multiple=position.r_multiple,
            profit_loss=position.profit_loss,
            strategy=position.strategy
        )
        
        if self.verbose:
            print(f"[EXIT] {exit_time.strftime('%Y-%m-%d %H:%M')} | "
                  f"CLOSE {position.strategy:12s} | "
                  f"Price: {exit_price:.5f} | "
                  f"R: {position.r_multiple:+.2f} | "
                  f"Exit: {exit_reason.value}")
    
    def _compile_results(self) -> Dict:
        """Compile final backtest results."""
        perf_stats = self.performance_tracker.get_comprehensive_stats()
        pos_stats = self.position_manager.get_statistics()
        strategy_breakdown = self.position_manager.get_strategy_breakdown()

        # Convert closed positions to list of dicts for API
        trades = [pos.to_dict() for pos in self.position_manager.closed_positions]

        # Convert equity DataFrame to list of dicts for API
        equity_df = self.performance_tracker.get_equity_dataframe()
        equity_curve = equity_df.reset_index().to_dict('records') if not equity_df.empty else []

        return {
            'performance': perf_stats,
            'positions': pos_stats,
            'strategies': strategy_breakdown,
            'trades': trades,  # Individual trade data
            'equity_curve': equity_curve  # List of dicts instead of DataFrame
        }
    
    def compare_to_mt5_baseline(self):
        """Compare results to MT5 v1.96 baseline."""
        baseline = {
            'total_r': 16.03,
            'total_trades': 149,
            'win_rate': 52.0,
            'net_profit': 283.02
        }
        
        self.performance_tracker.compare_to_baseline(baseline)


# Example usage
if __name__ == "__main__":
    print("JCAMP Python Backtesting Engine")
    print("="*70)
    
    # Initialize engine
    engine = BacktestEngine(
        initial_balance=10000.0,
        risk_percent=2.0,
        max_positions=2
    )
    
    # Run backtest
    results = engine.run_backtest(
        symbol='EURUSD',
        year='2024'
    )
    
    # Compare to MT5
    engine.compare_to_mt5_baseline()
    
    print("\n[OK] Backtest complete!")
