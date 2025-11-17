"""
═══════════════════════════════════════════════════════════════════════════════
JCAMP TRADING SYSTEM - MT5 v1.96 CONFIGURATION
═══════════════════════════════════════════════════════════════════════════════
All parameters extracted from Jcamp_BacktestEA.mq5 v1.96
Baseline Performance: +16.03R (149 trades, 52% win rate)
Test Period: 2024.01.01 - 2024.12.31
═══════════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════════
# ACCOUNT SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════
INITIAL_BALANCE = 10000.0          # Starting capital ($)
RISK_PERCENT = 2.0                 # Risk per trade (%)
LEVERAGE = 50                      # Broker leverage (1:50)

# ═══════════════════════════════════════════════════════════════════════════════
# TIMEFRAME SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════
ANALYSIS_TIMEFRAME = 'H1'          # H1 for indicators & regime detection
EXECUTION_TIMEFRAME = 'M15'        # M15 for entry signals
DATA_TIMEFRAME = 'M1'              # M1 for backtesting (CSV data)

# ═══════════════════════════════════════════════════════════════════════════════
# CSM (CURRENCY STRENGTH METER) SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════
CSM_LOOKBACK_HOURS = 48            # 48-hour lookback period
CSM_CALCULATION_PERIOD = 24        # Use 24H price changes

# 15 Major Pairs for CSM Calculation
CSM_PAIRS = [
    'EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'AUDUSD', 'NZDUSD', 'USDCAD',  # USD Majors (7)
    'EURJPY', 'GBPJPY', 'EURGBP', 'EURAUD', 'EURNZD', 'EURCAD', 'EURCHF',  # EUR Crosses (7)
    'GBPNZD'                                                                 # GBP Cross (1)
]

# 8 Major Currencies
CSM_CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'NZD', 'CAD', 'CHF']

# Currency pair weights (higher weight = more influence)
CSM_PAIR_WEIGHTS = {
    'EURUSD': 1.5,   # Most liquid pair
    'GBPUSD': 1.5,   # High liquidity
    'GBPNZD': 1.5,   # Volatility indicator
    # All other pairs default to 1.0
}

# CSM Calculation Constants
CSM_STRENGTH_MULTIPLIER = 100.0    # Multiply price change by 100
CSM_WEIGHT_FACTOR = 2.0            # Additional weight factor
CSM_NORMALIZATION_THRESHOLD = 0.001  # Min range for normalization

# ═══════════════════════════════════════════════════════════════════════════════
# REGIME DETECTION SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════
REGIME_CHECK_HOURS = 4             # Check regime every 4 hours
TRENDING_THRESHOLD_PERCENT = 55    # >= 55% trending score = TRENDING
RANGING_THRESHOLD_PERCENT = 40     # <= 40% trending score = RANGING
# Between 40-55% = TRANSITIONAL

# Regime Detection Indicators
MIN_ADX_FOR_TRENDING = 30.0        # ADX must be >= 30 for strong trend
MIN_EMA_SEPARATION = 0.40          # Min EMA separation (%)
REGIME_ADX_PERIOD = 14             # ADX calculation period
REGIME_EMA_FAST = 20               # Fast EMA period
REGIME_EMA_SLOW = 50               # Slow EMA period

# Dynamic Regime Detection (Phase 4E)
USE_DYNAMIC_REGIME = True          # Enable dynamic regime re-evaluation
DYNAMIC_REGIME_MIN_INTERVAL = 60   # Min 60 minutes between checks
DYNAMIC_REGIME_ADX_THRESHOLD = 35.0  # ADX threshold for dynamic recheck

# ═══════════════════════════════════════════════════════════════════════════════
# RISK MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════
RISK_REWARD_RATIO = 2.0            # Target R:R ratio
MAX_POSITIONS = 2                  # Max concurrent positions
DAILY_LOSS_LIMIT_R = -6.0          # Daily loss limit (R-multiple)
FORCE_CLOSE_ON_DAILY_LIMIT = False # Close all when daily limit hit

# Stop Loss Settings
ATR_PERIOD = 14                    # ATR calculation period
STOP_LOSS_ATR_MULTIPLIER = 0.5     # Default SL = ATR × 0.5
MIN_STOP_LOSS_PIPS = 20            # Minimum SL (pips)
MAX_STOP_LOSS_PIPS = 100           # Maximum SL (pips)

# Spread & Slippage
MAX_SPREAD_PIPS = 30.0             # Max allowed spread (pips)
SLIPPAGE_PIPS = 2.0                # Assumed slippage per trade

# ═══════════════════════════════════════════════════════════════════════════════
# ADVANCED ASYMMETRIC TRAILING STOP SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════
USE_ADVANCED_TRAILING = True       # Enable advanced trailing

# Phase 1: Initial Activation
TRAILING_ACTIVATION_R = 1.40       # Activate trailing at +1.4R
INITIAL_SL_BUFFER = 0.60           # SL buffer from activation (0.6R risk)
TP_EXTENSION = 0.50                # Extend TP by +0.5R on activation

# Phase 2: TP Trailing (Aggressive)
TP_TRAIL_STEP = 0.50               # TP trails every +0.5R
TP_TRAIL_ON_SL_MULTIPLIER = 2.0    # Trail TP every 2 × SL movements

# Phase 3: SL Trailing (Conservative)
SL_ACTIVATION_BUFFER = 0.50        # Wait 0.5R before SL trails
SL_TRAIL_STEP = 0.50               # SL lags 0.5R behind price

# ═══════════════════════════════════════════════════════════════════════════════
# TREND RIDER STRATEGY
# ═══════════════════════════════════════════════════════════════════════════════
ENABLE_TREND_RIDER = True          # Enable Trend Rider strategy
TREND_RIDER_MIN_CONFIDENCE = 65.0  # Min confidence score (%)
TREND_RIDER_MIN_CSM_DIFF = 15.0    # Min CSM differential
TREND_RIDER_STOP_LOSS_ATR = 1.2    # Tighter stop: 1.2 ATR (not 1.5!)

# Trend Rider Confidence Scoring (out of 135 total)
# EMA Alignment: 50 points max
# ADX Strength: 25 points max
# Momentum: 50 points max
# CSM Support: 10 points max

# ═══════════════════════════════════════════════════════════════════════════════
# RANGE RIDER STRATEGY
# ═══════════════════════════════════════════════════════════════════════════════
ENABLE_RANGE_RIDER = True          # Enable Range Rider strategy
RANGE_RIDER_MIN_EDGE_PROXIMITY = 10  # Must be within 10 pips of edge
RANGE_RIDER_BREAKEVEN_R = 0.5      # Move to break-even at +0.5R
RANGE_RIDER_MAX_HOLD_HOURS = 48    # Max hold time: 48 hours

# Range Detection
RANGE_MIN_TOUCHES = 3              # Min S/R touches to confirm range
RANGE_MIN_DURATION_HOURS = 24      # Min range duration (hours)
RANGE_MAX_HEIGHT_PIPS = 100        # Max range height (pips)

# ═══════════════════════════════════════════════════════════════════════════════
# MULTI-LAYER PROTECTION SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════
ENABLE_MULTI_DAY_PROTECTION = True # Enable multi-day protection
PORTFOLIO_LOSING_DAYS_LIMIT = 2    # Pause after 2 losing days
PORTFOLIO_PAUSE_HOURS = 48         # Pause duration (hours)
PAIR_LOSING_DAYS_LIMIT = 4         # Per-pair pause after 4 losing days
PAIR_PAUSE_HOURS = 24              # Per-pair pause duration

# USD Correlation Detection
ENABLE_USD_CORRELATION = True      # Detect USD correlation
TRADE_LOSING_STREAK_WARNING = 6    # Warning at 6 consecutive losses
TRADE_LOSING_STREAK_STOP = 18      # Emergency stop at 18 losses

# ═══════════════════════════════════════════════════════════════════════════════
# TRADING PAIRS (For backtesting)
# ═══════════════════════════════════════════════════════════════════════════════
TRADING_PAIRS = ['EURUSD', 'GBPUSD', 'GBPNZD']  # Current live pairs
BROKER_SUFFIX = '.sml'             # Oanda broker suffix

# ═══════════════════════════════════════════════════════════════════════════════
# BACKTESTING SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════
BACKTEST_START_DATE = '2024-01-01'  # Start date
BACKTEST_END_DATE = '2024-12-31'    # End date
VERBOSE_LOGGING = True              # Detailed logging for debugging

# Commission & Costs (Oanda broker)
COMMISSION_PER_LOT = 0.0            # No commission (included in spread)
SWAP_LONG = 0.0                     # Overnight swap (simplified)
SWAP_SHORT = 0.0                    # Overnight swap (simplified)

# ═══════════════════════════════════════════════════════════════════════════════
# POSITION SIZING
# ═══════════════════════════════════════════════════════════════════════════════
# Forex lot sizes
STANDARD_LOT = 100000               # 1.0 lot = 100,000 units
MINI_LOT = 10000                    # 0.1 lot = 10,000 units
MICRO_LOT = 1000                    # 0.01 lot = 1,000 units
MIN_LOT_SIZE = 0.01                 # Minimum trade size
MAX_LOT_SIZE = 10.0                 # Maximum trade size

# Pip values (for EURUSD-like pairs)
PIP_VALUE_STANDARD_LOT = 10.0       # $10 per pip for 1.0 lot
PIP_VALUE_MINI_LOT = 1.0            # $1 per pip for 0.1 lot
PIP_VALUE_MICRO_LOT = 0.1           # $0.1 per pip for 0.01 lot

# ═══════════════════════════════════════════════════════════════════════════════
# MASTER REVERSE MODE (For testing)
# ═══════════════════════════════════════════════════════════════════════════════
MASTER_REVERSE_MODE = False         # Invert all signals (BUY↔SELL)
# Note: Range Rider is exempt from reversal (already mean-reversion)

# ═══════════════════════════════════════════════════════════════════════════════
# BASELINE RESULTS (MT5 v1.96 - EURUSD 2024)
# ═══════════════════════════════════════════════════════════════════════════════
MT5_BASELINE = {
    'version': 'v1.96',
    'symbol': 'EURUSD.sml',
    'period': '2024.01.01 - 2024.12.31',
    'initial_balance': 10000.0,
    'total_r_multiple': 16.03,
    'total_trades': 149,
    'win_rate': 0.52,  # 52%
    'net_profit': 283.02,
    'max_drawdown': 273.14,
    'trend_rider_r': 9.18,
    'trend_rider_trades': [60, 61],  # [wins, losses]
    'range_rider_r': 6.86,
    'range_rider_trades': [18, 10],  # [wins, losses]
    'daily_loss_limit_r': -6.0
}

# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_pair_weight(pair: str) -> float:
    """Get CSM weight for a currency pair"""
    return CSM_PAIR_WEIGHTS.get(pair, 1.0)

def get_currency_index(currency: str) -> int:
    """Get index of currency in CSM array (0-7)"""
    try:
        return CSM_CURRENCIES.index(currency)
    except ValueError:
        return -1

def get_base_quote(pair: str) -> tuple:
    """Extract base and quote currencies from pair name"""
    if len(pair) < 6:
        raise ValueError(f"Invalid pair name: {pair}")
    base = pair[:3]
    quote = pair[3:6]
    return base, quote

def pips_to_price(pips: float, digits: int = 5) -> float:
    """Convert pips to price difference"""
    if digits == 3 or digits == 5:
        return pips * 0.0001  # 4-decimal pairs (EURUSD, GBPUSD)
    else:
        return pips * 0.01    # 2-decimal pairs (USDJPY)

def price_to_pips(price_diff: float, digits: int = 5) -> float:
    """Convert price difference to pips"""
    if digits == 3 or digits == 5:
        return price_diff / 0.0001
    else:
        return price_diff / 0.01

# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def validate_config():
    """Validate configuration settings"""
    assert INITIAL_BALANCE > 0, "Initial balance must be positive"
    assert 0 < RISK_PERCENT <= 100, "Risk percent must be between 0-100"
    assert MAX_POSITIONS > 0, "Max positions must be positive"
    assert len(CSM_PAIRS) == 15, "CSM requires exactly 15 pairs"
    assert len(CSM_CURRENCIES) == 8, "CSM requires exactly 8 currencies"
    print("✅ Configuration validated successfully")

if __name__ == "__main__":
    print("═" * 80)
    print("JCAMP TRADING SYSTEM - MT5 v1.96 CONFIGURATION")
    print("═" * 80)
    print(f"Initial Balance: ${INITIAL_BALANCE:,.2f}")
    print(f"Risk Per Trade: {RISK_PERCENT}%")
    print(f"Max Positions: {MAX_POSITIONS}")
    print(f"Daily Loss Limit: {DAILY_LOSS_LIMIT_R}R")
    print("-" * 80)
    print(f"CSM Pairs: {len(CSM_PAIRS)}")
    print(f"CSM Currencies: {len(CSM_CURRENCIES)}")
    print(f"CSM Lookback: {CSM_LOOKBACK_HOURS} hours")
    print("-" * 80)
    print(f"Trend Rider: {'ENABLED' if ENABLE_TREND_RIDER else 'DISABLED'}")
    print(f"  Min Confidence: {TREND_RIDER_MIN_CONFIDENCE}%")
    print(f"  Min CSM Diff: {TREND_RIDER_MIN_CSM_DIFF}")
    print(f"Range Rider: {'ENABLED' if ENABLE_RANGE_RIDER else 'DISABLED'}")
    print(f"  Break-even: +{RANGE_RIDER_BREAKEVEN_R}R")
    print("-" * 80)
    print("MT5 v1.96 BASELINE:")
    print(f"  Total R: +{MT5_BASELINE['total_r_multiple']}R")
    print(f"  Trades: {MT5_BASELINE['total_trades']}")
    print(f"  Win Rate: {MT5_BASELINE['win_rate']*100:.1f}%")
    print(f"  Net Profit: ${MT5_BASELINE['net_profit']:.2f}")
    print("═" * 80)
    validate_config()
