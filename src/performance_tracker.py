"""
Performance Tracker - Calculate comprehensive backtest metrics
Tracks equity curve, drawdown, Sharpe ratio, and more
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime


class PerformanceTracker:
    """
    Track and calculate backtest performance metrics
    """
    
    def __init__(self, initial_balance: float = 10000.0):
        """
        Initialize performance tracker.
        
        Args:
            initial_balance: Starting account balance
        """
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        
        # Equity tracking
        self.equity_curve: List[Dict] = []
        self.peak_balance = initial_balance
        self.current_drawdown = 0.0
        self.max_drawdown = 0.0
        
        # Trade tracking
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_r = 0.0
        
        # Daily tracking
        self.daily_returns: List[float] = []
        self.daily_r: Dict[str, float] = {}  # date -> R-multiple
        
        # Risk tracking
        self.daily_loss_limit_r = -6.0
        self.daily_loss_limit_hit = False
        
    def record_trade(
        self,
        timestamp: datetime,
        r_multiple: float,
        profit_loss: float,
        strategy: str
    ):
        """
        Record a completed trade.
        
        Args:
            timestamp: Trade close time
            r_multiple: R-multiple result
            profit_loss: P&L in account currency
            strategy: Strategy name
        """
        self.total_trades += 1
        self.total_r += r_multiple
        self.current_balance += profit_loss
        
        if r_multiple > 0:
            self.winning_trades += 1
        else:
            self.losing_trades += 1
        
        # Update equity curve
        self.equity_curve.append({
            'timestamp': timestamp,
            'balance': self.current_balance,
            'r_multiple': r_multiple,
            'cumulative_r': self.total_r,
            'strategy': strategy
        })
        
        # Update drawdown
        if self.current_balance > self.peak_balance:
            self.peak_balance = self.current_balance
            self.current_drawdown = 0.0
        else:
            self.current_drawdown = (self.peak_balance - self.current_balance) / self.peak_balance * 100.0
            if self.current_drawdown > self.max_drawdown:
                self.max_drawdown = self.current_drawdown
        
        # Track daily R
        date_key = timestamp.strftime('%Y-%m-%d')
        if date_key not in self.daily_r:
            self.daily_r[date_key] = 0.0
        self.daily_r[date_key] += r_multiple
        
        # Check daily loss limit
        if self.daily_r[date_key] <= self.daily_loss_limit_r:
            self.daily_loss_limit_hit = True
    
    def is_daily_loss_limit_reached(self, current_date: str) -> bool:
        """
        Check if daily loss limit has been reached.
        
        Args:
            current_date: Date string (YYYY-MM-DD)
            
        Returns:
            True if daily loss limit reached
        """
        if current_date in self.daily_r:
            return self.daily_r[current_date] <= self.daily_loss_limit_r
        return False
    
    def get_daily_r(self, current_date: str) -> float:
        """Get R-multiple for specific date."""
        return self.daily_r.get(current_date, 0.0)
    
    def calculate_win_rate(self) -> float:
        """Calculate overall win rate."""
        if self.total_trades == 0:
            return 0.0
        return self.winning_trades / self.total_trades * 100.0
    
    def calculate_profit_factor(self) -> float:
        """Calculate profit factor (gross profit / gross loss)."""
        if not self.equity_curve:
            return 0.0
        
        gross_profit = sum(r for r in [t['r_multiple'] for t in self.equity_curve] if r > 0)
        gross_loss = abs(sum(r for r in [t['r_multiple'] for t in self.equity_curve] if r < 0))
        
        if gross_loss == 0:
            return float('inf') if gross_profit > 0 else 0.0
        
        return gross_profit / gross_loss
    
    def calculate_sharpe_ratio(self, risk_free_rate: float = 0.0) -> float:
        """
        Calculate Sharpe ratio from R-multiples.
        
        Args:
            risk_free_rate: Risk-free rate (annualized)
            
        Returns:
            Sharpe ratio
        """
        if len(self.equity_curve) < 2:
            return 0.0
        
        returns = [t['r_multiple'] for t in self.equity_curve]
        
        if len(returns) == 0:
            return 0.0
        
        avg_return = np.mean(returns)
        std_return = np.std(returns)
        
        if std_return == 0:
            return 0.0
        
        # Annualized Sharpe (assuming ~250 trading days)
        sharpe = (avg_return - risk_free_rate) / std_return
        return sharpe * np.sqrt(250 / len(returns))  # Annualize
    
    def calculate_expectancy(self) -> float:
        """
        Calculate expectancy (average R per trade).
        
        Returns:
            Average R-multiple
        """
        if self.total_trades == 0:
            return 0.0
        return self.total_r / self.total_trades
    
    def get_max_consecutive_losses(self) -> int:
        """Calculate maximum consecutive losing trades."""
        if not self.equity_curve:
            return 0
        
        max_losses = 0
        current_losses = 0
        
        for trade in self.equity_curve:
            if trade['r_multiple'] < 0:
                current_losses += 1
                max_losses = max(max_losses, current_losses)
            else:
                current_losses = 0
        
        return max_losses
    
    def get_max_consecutive_wins(self) -> int:
        """Calculate maximum consecutive winning trades."""
        if not self.equity_curve:
            return 0
        
        max_wins = 0
        current_wins = 0
        
        for trade in self.equity_curve:
            if trade['r_multiple'] > 0:
                current_wins += 1
                max_wins = max(max_wins, current_wins)
            else:
                current_wins = 0
        
        return max_wins
    
    def get_equity_dataframe(self) -> pd.DataFrame:
        """Get equity curve as DataFrame."""
        if not self.equity_curve:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.equity_curve)
        df.set_index('timestamp', inplace=True)
        return df
    
    def get_comprehensive_stats(self) -> Dict:
        """
        Get comprehensive performance statistics.
        
        Returns:
            Dictionary with all performance metrics
        """
        return {
            # Basic metrics
            'initial_balance': self.initial_balance,
            'final_balance': self.current_balance,
            'net_profit': self.current_balance - self.initial_balance,
            'return_pct': (self.current_balance / self.initial_balance - 1) * 100.0,
            
            # Trade metrics
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'win_rate': self.calculate_win_rate(),
            
            # R-multiple metrics
            'total_r': self.total_r,
            'avg_r': self.calculate_expectancy(),
            'max_r': max([t['r_multiple'] for t in self.equity_curve]) if self.equity_curve else 0.0,
            'min_r': min([t['r_multiple'] for t in self.equity_curve]) if self.equity_curve else 0.0,
            
            # Risk metrics
            'max_drawdown_pct': self.max_drawdown,
            'max_drawdown_dollars': self.peak_balance - (self.peak_balance * (1 - self.max_drawdown / 100)),
            'current_drawdown_pct': self.current_drawdown,
            
            # Advanced metrics
            'profit_factor': self.calculate_profit_factor(),
            'sharpe_ratio': self.calculate_sharpe_ratio(),
            'max_consecutive_wins': self.get_max_consecutive_wins(),
            'max_consecutive_losses': self.get_max_consecutive_losses(),
            
            # Daily metrics
            'total_trading_days': len(self.daily_r),
            'daily_loss_limit_hit': self.daily_loss_limit_hit
        }
    
    def print_summary(self):
        """Print formatted performance summary."""
        stats = self.get_comprehensive_stats()
        
        print("\n" + "="*70)
        print("  BACKTEST PERFORMANCE SUMMARY")
        print("="*70)
        
        print("\n[CHART] OVERALL RESULTS:")
        print(f"  Initial Balance:  ${stats['initial_balance']:,.2f}")
        print(f"  Final Balance:    ${stats['final_balance']:,.2f}")
        print(f"  Net Profit:       ${stats['net_profit']:,.2f} ({stats['return_pct']:+.2f}%)")
        
        print("\n[TREND] TRADE STATISTICS:")
        print(f"  Total Trades:     {stats['total_trades']}")
        print(f"  Winning Trades:   {stats['winning_trades']}")
        print(f"  Losing Trades:    {stats['losing_trades']}")
        print(f"  Win Rate:         {stats['win_rate']:.1f}%")
        
        print("\n[MONEY] R-MULTIPLE ANALYSIS:")
        print(f"  Total R-Multiple: {stats['total_r']:+.2f}R")
        print(f"  Average R:        {stats['avg_r']:+.3f}R")
        print(f"  Best Trade:       {stats['max_r']:+.2f}R")
        print(f"  Worst Trade:      {stats['min_r']:+.2f}R")
        
        print("\n[WARN] RISK METRICS:")
        print(f"  Max Drawdown:     {stats['max_drawdown_pct']:.2f}%")
        print(f"  Current Drawdown: {stats['current_drawdown_pct']:.2f}%")
        print(f"  Profit Factor:    {stats['profit_factor']:.2f}")
        print(f"  Sharpe Ratio:     {stats['sharpe_ratio']:.2f}")
        
        print("\n[TARGET] CONSISTENCY METRICS:")
        print(f"  Max Consecutive Wins:   {stats['max_consecutive_wins']}")
        print(f"  Max Consecutive Losses: {stats['max_consecutive_losses']}")
        
        print("\n" + "="*70)
    
    def compare_to_baseline(self, baseline_stats: Dict):
        """
        Compare current results to MT5 baseline.
        
        Args:
            baseline_stats: Dictionary with baseline performance
        """
        current_stats = self.get_comprehensive_stats()
        
        print("\n" + "="*70)
        print("  COMPARISON TO MT5 BASELINE")
        print("="*70)
        
        print("\n[CHART] KEY METRICS:")
        print(f"                    Python      MT5         Difference")
        print(f"  Total R:          {current_stats['total_r']:+7.2f}R   {baseline_stats.get('total_r', 0):+7.2f}R   {current_stats['total_r'] - baseline_stats.get('total_r', 0):+7.2f}R")
        print(f"  Trades:           {current_stats['total_trades']:7d}     {baseline_stats.get('total_trades', 0):7d}     {current_stats['total_trades'] - baseline_stats.get('total_trades', 0):+7d}")
        print(f"  Win Rate:         {current_stats['win_rate']:6.1f}%    {baseline_stats.get('win_rate', 0):6.1f}%    {current_stats['win_rate'] - baseline_stats.get('win_rate', 0):+6.1f}%")
        
        # Calculate match percentage
        r_match = (1 - abs(current_stats['total_r'] - baseline_stats.get('total_r', 0)) / baseline_stats.get('total_r', 1)) * 100
        trade_match = (1 - abs(current_stats['total_trades'] - baseline_stats.get('total_trades', 1)) / baseline_stats.get('total_trades', 1)) * 100
        
        print(f"\n[OK] R-Multiple Match: {r_match:.1f}%")
        print(f"[OK] Trade Count Match: {trade_match:.1f}%")

        if r_match >= 95 and trade_match >= 95:
            print("\n[SUCCESS] EXCELLENT! Results match MT5 within 5%")
        elif r_match >= 90 and trade_match >= 90:
            print("\n[OK] GOOD! Results match MT5 within 10%")
        else:
            print("\n[WARN] Results differ from MT5 - investigate discrepancies")
        
        print("="*70)
