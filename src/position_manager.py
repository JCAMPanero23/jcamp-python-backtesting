"""
Position Manager - Track open positions and calculate R-multiples
Handles entry, stop loss, take profit, and position closing
"""

import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum


class PositionSide(Enum):
    """Position direction"""
    BUY = "BUY"
    SELL = "SELL"


class ExitReason(Enum):
    """Why position was closed"""
    STOP_LOSS = "STOP_LOSS"
    TAKE_PROFIT = "TAKE_PROFIT"
    TRAILING_STOP = "TRAILING_STOP"
    MAX_HOLD_TIME = "MAX_HOLD_TIME"
    BREAK_EVEN = "BREAK_EVEN"
    DAILY_LOSS_LIMIT = "DAILY_LOSS_LIMIT"


class Position:
    """
    Represents an open trading position
    """
    
    def __init__(
        self,
        position_id: int,
        symbol: str,
        side: PositionSide,
        entry_price: float,
        entry_time: datetime,
        stop_loss: float,
        take_profit: Optional[float],
        position_size: float,
        strategy: str,
        confidence: float,
        regime: str
    ):
        """
        Initialize position.
        
        Args:
            position_id: Unique identifier
            symbol: Trading pair
            side: BUY or SELL
            entry_price: Entry price
            entry_time: Entry timestamp
            stop_loss: Initial stop loss price
            take_profit: Initial take profit price (can be None)
            position_size: Position size in lots
            strategy: Strategy name (TREND_RIDER, RANGE_RIDER)
            confidence: Entry confidence score
            regime: Market regime at entry
        """
        self.position_id = position_id
        self.symbol = symbol
        self.side = side
        self.entry_price = entry_price
        self.entry_time = entry_time
        self.initial_stop_loss = stop_loss
        self.current_stop_loss = stop_loss
        self.initial_take_profit = take_profit
        self.current_take_profit = take_profit
        self.position_size = position_size
        self.strategy = strategy
        self.confidence = confidence
        self.regime = regime
        
        # Calculate initial risk (1R)
        self.initial_risk = abs(entry_price - stop_loss)
        
        # Track peak profit for trailing
        self.peak_price = entry_price
        self.peak_r = 0.0
        
        # Exit info (filled when closed)
        self.exit_price: Optional[float] = None
        self.exit_time: Optional[datetime] = None
        self.exit_reason: Optional[ExitReason] = None
        self.r_multiple: Optional[float] = None
        self.profit_loss: Optional[float] = None
        
        # Status
        self.is_open = True
        
    def calculate_current_r(self, current_price: float) -> float:
        """
        Calculate current R-multiple.
        
        Args:
            current_price: Current market price
            
        Returns:
            Current R-multiple (positive = profit, negative = loss)
        """
        if self.side == PositionSide.BUY:
            price_movement = current_price - self.entry_price
        else:  # SELL
            price_movement = self.entry_price - current_price
        
        return price_movement / self.initial_risk
    
    def update_peak(self, current_price: float):
        """Update peak price and R-multiple for trailing stops."""
        current_r = self.calculate_current_r(current_price)
        
        if current_r > self.peak_r:
            self.peak_r = current_r
            self.peak_price = current_price
    
    def update_stop_loss(self, new_stop: float):
        """Update stop loss price."""
        # Ensure stop only moves in favorable direction
        if self.side == PositionSide.BUY:
            self.current_stop_loss = max(self.current_stop_loss, new_stop)
        else:  # SELL
            self.current_stop_loss = min(self.current_stop_loss, new_stop)
    
    def update_take_profit(self, new_tp: float):
        """Update take profit price."""
        self.current_take_profit = new_tp
    
    def close_position(
        self,
        exit_price: float,
        exit_time: datetime,
        exit_reason: ExitReason
    ):
        """
        Close position and calculate final P&L.
        
        Args:
            exit_price: Exit price
            exit_time: Exit timestamp
            exit_reason: Reason for closing
        """
        self.exit_price = exit_price
        self.exit_time = exit_time
        self.exit_reason = exit_reason
        self.is_open = False
        
        # Calculate final R-multiple
        self.r_multiple = self.calculate_current_r(exit_price)
        
        # Calculate P&L in account currency
        if self.side == PositionSide.BUY:
            price_diff = exit_price - self.entry_price
        else:  # SELL
            price_diff = self.entry_price - exit_price
        
        # Assuming standard lot sizing
        # For forex: 1 lot = 100,000 units, 1 pip = 0.0001 for EURUSD
        pip_value = 10.0  # $10 per pip for 1.0 lot EURUSD
        pips = price_diff / 0.0001
        self.profit_loss = pips * pip_value * self.position_size
    
    def get_hold_time_hours(self, current_time: datetime) -> float:
        """Calculate how long position has been held."""
        if self.is_open:
            delta = current_time - self.entry_time
        else:
            delta = self.exit_time - self.entry_time
        
        return delta.total_seconds() / 3600.0
    
    def to_dict(self) -> Dict:
        """Convert position to dictionary for logging."""
        return {
            'position_id': self.position_id,
            'symbol': self.symbol,
            'side': self.side.value,
            'strategy': self.strategy,
            'confidence': self.confidence,
            'regime': self.regime,
            'entry_price': self.entry_price,
            'entry_time': self.entry_time,
            'exit_price': self.exit_price,
            'exit_time': self.exit_time,
            'exit_reason': self.exit_reason.value if self.exit_reason else None,
            'initial_stop': self.initial_stop_loss,
            'final_stop': self.current_stop_loss,
            'initial_tp': self.initial_take_profit,
            'r_multiple': self.r_multiple,
            'profit_loss': self.profit_loss,
            'hold_hours': self.get_hold_time_hours(self.exit_time) if self.exit_time else None
        }


class PositionManager:
    """
    Manages all open and closed positions
    """
    
    def __init__(self, max_positions: int = 2):
        """
        Initialize position manager.
        
        Args:
            max_positions: Maximum concurrent positions
        """
        self.max_positions = max_positions
        self.positions: List[Position] = []
        self.open_positions: List[Position] = []
        self.closed_positions: List[Position] = []
        self.next_position_id = 1
    
    def can_open_position(self) -> bool:
        """Check if we can open a new position."""
        return len(self.open_positions) < self.max_positions
    
    def open_position(
        self,
        symbol: str,
        side: str,
        entry_price: float,
        entry_time: datetime,
        stop_loss: float,
        take_profit: Optional[float],
        position_size: float,
        strategy: str,
        confidence: float,
        regime: str
    ) -> Position:
        """
        Open a new position.
        
        Returns:
            Created Position object
        """
        if not self.can_open_position():
            raise RuntimeError(f"Cannot open position: limit of {self.max_positions} reached")
        
        position = Position(
            position_id=self.next_position_id,
            symbol=symbol,
            side=PositionSide.BUY if side == 'BUY' else PositionSide.SELL,
            entry_price=entry_price,
            entry_time=entry_time,
            stop_loss=stop_loss,
            take_profit=take_profit,
            position_size=position_size,
            strategy=strategy,
            confidence=confidence,
            regime=regime
        )
        
        self.next_position_id += 1
        self.positions.append(position)
        self.open_positions.append(position)
        
        return position
    
    def close_position(
        self,
        position: Position,
        exit_price: float,
        exit_time: datetime,
        exit_reason: ExitReason
    ):
        """Close an open position."""
        position.close_position(exit_price, exit_time, exit_reason)
        
        if position in self.open_positions:
            self.open_positions.remove(position)
        
        self.closed_positions.append(position)
    
    def update_position(
        self,
        position: Position,
        current_price: float,
        current_time: datetime
    ):
        """
        Update position with current price (for trailing stops, etc).
        
        Args:
            position: Position to update
            current_price: Current market price
            current_time: Current timestamp
        """
        # Update peak for trailing stop calculations
        position.update_peak(current_price)
    
    def get_position_by_id(self, position_id: int) -> Optional[Position]:
        """Get position by ID."""
        for pos in self.positions:
            if pos.position_id == position_id:
                return pos
        return None
    
    def get_open_positions_for_symbol(self, symbol: str) -> List[Position]:
        """Get all open positions for a specific symbol."""
        return [pos for pos in self.open_positions if pos.symbol == symbol]
    
    def get_total_r(self) -> float:
        """Calculate total R-multiple from all closed positions."""
        return sum(pos.r_multiple for pos in self.closed_positions if pos.r_multiple is not None)
    
    def get_win_rate(self) -> float:
        """Calculate win rate from closed positions."""
        if not self.closed_positions:
            return 0.0
        
        wins = sum(1 for pos in self.closed_positions if pos.r_multiple > 0)
        return wins / len(self.closed_positions) * 100.0
    
    def get_statistics(self) -> Dict:
        """Get position statistics."""
        if not self.closed_positions:
            return {
                'total_trades': 0,
                'win_rate': 0.0,
                'total_r': 0.0,
                'avg_r': 0.0,
                'total_pl': 0.0
            }
        
        wins = sum(1 for pos in self.closed_positions if pos.r_multiple > 0)
        total_r = sum(pos.r_multiple for pos in self.closed_positions)
        total_pl = sum(pos.profit_loss for pos in self.closed_positions if pos.profit_loss)
        
        return {
            'total_trades': len(self.closed_positions),
            'wins': wins,
            'losses': len(self.closed_positions) - wins,
            'win_rate': wins / len(self.closed_positions) * 100.0,
            'total_r': total_r,
            'avg_r': total_r / len(self.closed_positions),
            'total_pl': total_pl,
            'avg_pl': total_pl / len(self.closed_positions) if total_pl else 0.0
        }
    
    def get_strategy_breakdown(self) -> Dict[str, Dict]:
        """Get statistics broken down by strategy."""
        strategies = {}
        
        for pos in self.closed_positions:
            if pos.strategy not in strategies:
                strategies[pos.strategy] = {
                    'trades': 0,
                    'wins': 0,
                    'losses': 0,
                    'total_r': 0.0,
                    'total_pl': 0.0
                }
            
            strat = strategies[pos.strategy]
            strat['trades'] += 1
            if pos.r_multiple > 0:
                strat['wins'] += 1
            else:
                strat['losses'] += 1
            strat['total_r'] += pos.r_multiple
            if pos.profit_loss:
                strat['total_pl'] += pos.profit_loss
        
        # Calculate derived metrics
        for strat in strategies.values():
            if strat['trades'] > 0:
                strat['win_rate'] = strat['wins'] / strat['trades'] * 100.0
                strat['avg_r'] = strat['total_r'] / strat['trades']
        
        return strategies
