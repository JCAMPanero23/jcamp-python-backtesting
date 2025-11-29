======================================================================
  PHASE 4 TEST SUITE - BACKTEST ENGINE
======================================================================
Testing: Complete backtesting workflow
Target: Match MT5 v1.96 baseline (+16.03R)

âš ï¸  Note: Tests 4-6 process real data and may take 10-15 minutes total
         (Still 20-30x faster than MT5's 180 minutes!)

======================================================================
  TEST 1: Position Manager
======================================================================

Position Manager
Status: âŒ FAILED
Details: Should be +1R
Traceback (most recent call last):
  File "D:\JcampFxTrading\jcamp-python-backtesting\tests\test_phase4.py", line 77, in test_position_manager
    assert pos.r_multiple == 1.0, "Should be +1R"
           ^^^^^^^^^^^^^^^^^^^^^
AssertionError: Should be +1R

======================================================================
  TEST 2: Performance Tracker
======================================================================

Performance Tracker
Status: âœ… PASSED
Details: Total R: +2.50, Win Rate: 66.7%

======================================================================
  TEST 3: Backtest Engine Initialization
======================================================================

Backtest Engine Initialization
Status: âœ… PASSED
Details: All components initialized successfully

======================================================================
  TEST 4: Data Preparation
======================================================================
âš ï¸  This test loads full EURUSD data and may take 1-2 minutes...
ðŸ“‚ Loading EURUSD data from data\EURUSD.sml\2024_M1.csv...
âš ï¸  Info: 270 gaps detected in EURUSD M1 data (weekends/holidays expected)
âœ“ Loaded 372,292 M1 bars for EURUSD
  Date range: 2024-01-02 00:03:00 to 2024-12-31 23:58:00
  Price range: 1.03321 - 1.12142
â±ï¸  Resampling to H1...
D:\JcampFxTrading\jcamp-python-backtesting\src\data_loader.py:149: FutureWarning: 'H' is deprecated and will be removed in a future version, please use 'h' instead.
  resampled = df.resample(rule).agg({
âœ“ Resampled to 6,240 H1 bars

Data Preparation
Status: âœ… PASSED
Details: Prepared 6,240 bars with all indicators

======================================================================
  TEST 5: Short Backtest (Jan-Mar 2024)
======================================================================
âš ï¸  Running 3-month backtest, this may take 2-3 minutes...

======================================================================
  JCAMP BACKTEST ENGINE - EURUSD 2024
======================================================================

ðŸ“Š Preparing data for EURUSD 2024...
ðŸ“‚ Loading EURUSD data from data\EURUSD.sml\2024_M1.csv...
âš ï¸  Info: 270 gaps detected in EURUSD M1 data (weekends/holidays expected)
âœ“ Loaded 372,292 M1 bars for EURUSD
  Date range: 2024-01-02 00:03:00 to 2024-12-31 23:58:00
  Price range: 1.03321 - 1.12142
â±ï¸  Resampling to H1...
D:\JcampFxTrading\jcamp-python-backtesting\src\data_loader.py:149: FutureWarning: 'H' is deprecated and will be removed in a future version, please use 'h' instead.
  resampled = df.resample(rule).agg({
âœ“ Resampled to 6,240 H1 bars
âœ“ Loaded 6,240 H1 bars
ðŸ“ˆ Calculating technical indicators...
ðŸ’ª Calculating Currency Strength Meter...
âœ“ Data preparation complete!


ðŸŽ¯ Testing period: 2024-01-02 to 2024-03-29
ðŸ“Š Total bars: 1,536
ðŸ’° Initial balance: $10,000.00
âš ï¸  Risk per trade: 2.0%
ðŸ“ˆ Max positions: 2

----------------------------------------------------------------------
Starting backtest simulation...
----------------------------------------------------------------------

ðŸ“ 2024-01-08 04:00 | SELL RANGE_RIDER  | Price: 1.09373 | SL: 1.09519 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-08 05:00 | SELL RANGE_RIDER  | Price: 1.09331 | SL: 1.09472 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-08 09:00 | CLOSE RANGE_RIDER  | Price: 1.09519 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-08 09:00 | CLOSE RANGE_RIDER  | Price: 1.09472 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-08 09:00 | SELL RANGE_RIDER  | Price: 1.09454 | SL: 1.09582 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-08 10:00 | CLOSE RANGE_RIDER  | Price: 1.09338 | R: +0.91 | Exit: BREAK_EVEN
ðŸ“ 2024-01-08 10:00 | SELL RANGE_RIDER  | Price: 1.09338 | SL: 1.09469 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-08 11:00 | SELL RANGE_RIDER  | Price: 1.09371 | SL: 1.09506 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-08 13:00 | CLOSE RANGE_RIDER  | Price: 1.09469 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-08 13:00 | CLOSE RANGE_RIDER  | Price: 1.09506 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-08 13:00 | SELL RANGE_RIDER  | Price: 1.09380 | SL: 1.09513 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-08 14:00 | SELL RANGE_RIDER  | Price: 1.09447 | SL: 1.09578 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-08 15:00 | CLOSE RANGE_RIDER  | Price: 1.09513 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-08 15:00 | SELL RANGE_RIDER  | Price: 1.09509 | SL: 1.09641 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-08 16:00 | CLOSE RANGE_RIDER  | Price: 1.09578 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-08 16:00 | SELL RANGE_RIDER  | Price: 1.09603 | SL: 1.09735 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-08 17:00 | CLOSE RANGE_RIDER  | Price: 1.09641 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-08 17:00 | CLOSE RANGE_RIDER  | Price: 1.09735 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-09 00:00 | SELL RANGE_RIDER  | Price: 1.09507 | SL: 1.09634 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-09 01:00 | SELL RANGE_RIDER  | Price: 1.09499 | SL: 1.09619 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-09 03:00 | CLOSE RANGE_RIDER  | Price: 1.09619 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-09 03:00 | SELL RANGE_RIDER  | Price: 1.09616 | SL: 1.09734 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-09 04:00 | CLOSE RANGE_RIDER  | Price: 1.09634 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-09 04:00 | SELL RANGE_RIDER  | Price: 1.09629 | SL: 1.09741 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-09 06:00 | CLOSE RANGE_RIDER  | Price: 1.09562 | R: +0.60 | Exit: BREAK_EVEN
ðŸ“ 2024-01-09 06:00 | SELL RANGE_RIDER  | Price: 1.09562 | SL: 1.09669 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-09 07:00 | CLOSE RANGE_RIDER  | Price: 1.09498 | R: +1.00 | Exit: BREAK_EVEN
ðŸ”š 2024-01-09 07:00 | CLOSE RANGE_RIDER  | Price: 1.09498 | R: +0.60 | Exit: BREAK_EVEN
ðŸ“ 2024-01-09 07:00 | SELL RANGE_RIDER  | Price: 1.09498 | SL: 1.09604 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-09 08:00 | SELL RANGE_RIDER  | Price: 1.09504 | SL: 1.09607 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-09 09:00 | CLOSE RANGE_RIDER  | Price: 1.09604 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-09 09:00 | CLOSE RANGE_RIDER  | Price: 1.09607 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-09 09:00 | SELL RANGE_RIDER  | Price: 1.09567 | SL: 1.09675 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-09 10:00 | CLOSE RANGE_RIDER  | Price: 1.09499 | R: +0.63 | Exit: BREAK_EVEN
ðŸ“ 2024-01-09 10:00 | SELL RANGE_RIDER  | Price: 1.09499 | SL: 1.09612 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-09 11:00 | CLOSE RANGE_RIDER  | Price: 1.09442 | R: +0.50 | Exit: BREAK_EVEN
ðŸ“ 2024-01-09 11:00 | SELL RANGE_RIDER  | Price: 1.09442 | SL: 1.09556 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-09 12:00 | CLOSE RANGE_RIDER  | Price: 1.09357 | R: +0.75 | Exit: BREAK_EVEN
ðŸ“ 2024-01-09 12:00 | SELL RANGE_RIDER  | Price: 1.09357 | SL: 1.09474 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-09 13:00 | SELL RANGE_RIDER  | Price: 1.09313 | SL: 1.09427 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-09 15:00 | CLOSE RANGE_RIDER  | Price: 1.09427 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-09 15:00 | SELL RANGE_RIDER  | Price: 1.09460 | SL: 1.09577 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-09 16:00 | CLOSE RANGE_RIDER  | Price: 1.09474 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-09 16:00 | SELL RANGE_RIDER  | Price: 1.09456 | SL: 1.09574 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-09 17:00 | CLOSE RANGE_RIDER  | Price: 1.09179 | R: +2.41 | Exit: BREAK_EVEN
ðŸ”š 2024-01-09 17:00 | CLOSE RANGE_RIDER  | Price: 1.09179 | R: +2.35 | Exit: BREAK_EVEN
ðŸ“ 2024-01-09 17:00 | SELL RANGE_RIDER  | Price: 1.09179 | SL: 1.09309 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-09 18:00 | CLOSE RANGE_RIDER  | Price: 1.09309 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-09 18:00 | SELL RANGE_RIDER  | Price: 1.09344 | SL: 1.09483 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-09 19:00 | SELL RANGE_RIDER  | Price: 1.09342 | SL: 1.09477 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-09 20:00 | CLOSE RANGE_RIDER  | Price: 1.09242 | R: +0.74 | Exit: BREAK_EVEN
ðŸ”š 2024-01-09 20:00 | CLOSE RANGE_RIDER  | Price: 1.09242 | R: +0.74 | Exit: BREAK_EVEN
ðŸ“ 2024-01-09 20:00 | SELL RANGE_RIDER  | Price: 1.09242 | SL: 1.09380 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-09 21:00 | SELL RANGE_RIDER  | Price: 1.09254 | SL: 1.09389 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-10 09:00 | CLOSE RANGE_RIDER  | Price: 1.09380 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-10 09:00 | CLOSE RANGE_RIDER  | Price: 1.09389 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-10 09:00 | SELL RANGE_RIDER  | Price: 1.09263 | SL: 1.09363 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-10 10:00 | CLOSE RANGE_RIDER  | Price: 1.09363 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-10 10:00 | SELL RANGE_RIDER  | Price: 1.09435 | SL: 1.09544 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-10 11:00 | SELL RANGE_RIDER  | Price: 1.09472 | SL: 1.09580 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-10 12:00 | CLOSE RANGE_RIDER  | Price: 1.09544 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-10 12:00 | SELL RANGE_RIDER  | Price: 1.09493 | SL: 1.09601 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-10 14:00 | CLOSE RANGE_RIDER  | Price: 1.09439 | R: +0.50 | Exit: BREAK_EVEN
ðŸ“ 2024-01-10 14:00 | SELL RANGE_RIDER  | Price: 1.09439 | SL: 1.09546 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-10 15:00 | CLOSE RANGE_RIDER  | Price: 1.09407 | R: +0.60 | Exit: BREAK_EVEN
ðŸ“ 2024-01-10 15:00 | SELL RANGE_RIDER  | Price: 1.09407 | SL: 1.09515 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-10 17:00 | CLOSE RANGE_RIDER  | Price: 1.09546 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-10 17:00 | CLOSE RANGE_RIDER  | Price: 1.09515 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-10 17:00 | SELL RANGE_RIDER  | Price: 1.09674 | SL: 1.09797 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-10 18:00 | CLOSE RANGE_RIDER  | Price: 1.09592 | R: +0.66 | Exit: BREAK_EVEN
ðŸ“ 2024-01-10 18:00 | SELL RANGE_RIDER  | Price: 1.09592 | SL: 1.09719 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-10 19:00 | SELL RANGE_RIDER  | Price: 1.09672 | SL: 1.09796 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-10 22:00 | CLOSE RANGE_RIDER  | Price: 1.09719 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-10 22:00 | SELL RANGE_RIDER  | Price: 1.09657 | SL: 1.09774 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-11 02:00 | CLOSE RANGE_RIDER  | Price: 1.09774 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-11 02:00 | SELL RANGE_RIDER  | Price: 1.09779 | SL: 1.09879 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-11 03:00 | CLOSE RANGE_RIDER  | Price: 1.09796 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-11 03:00 | SELL RANGE_RIDER  | Price: 1.09790 | SL: 1.09887 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-11 08:00 | CLOSE RANGE_RIDER  | Price: 1.09879 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-11 08:00 | SELL RANGE_RIDER  | Price: 1.09859 | SL: 1.09949 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-11 09:00 | CLOSE RANGE_RIDER  | Price: 1.09790 | R: +0.76 | Exit: BREAK_EVEN
ðŸ“ 2024-01-11 09:00 | SELL RANGE_RIDER  | Price: 1.09790 | SL: 1.09881 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-11 11:00 | CLOSE RANGE_RIDER  | Price: 1.09638 | R: +1.57 | Exit: BREAK_EVEN
ðŸ”š 2024-01-11 11:00 | CLOSE RANGE_RIDER  | Price: 1.09638 | R: +1.68 | Exit: BREAK_EVEN
ðŸ“ 2024-01-11 11:00 | SELL RANGE_RIDER  | Price: 1.09638 | SL: 1.09734 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-11 12:00 | SELL RANGE_RIDER  | Price: 1.09690 | SL: 1.09787 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-11 13:00 | CLOSE RANGE_RIDER  | Price: 1.09734 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-11 13:00 | CLOSE RANGE_RIDER  | Price: 1.09787 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-11 13:00 | SELL RANGE_RIDER  | Price: 1.09787 | SL: 1.09888 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-11 14:00 | CLOSE RANGE_RIDER  | Price: 1.09888 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-11 14:00 | SELL RANGE_RIDER  | Price: 1.09838 | SL: 1.09942 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-11 15:00 | CLOSE RANGE_RIDER  | Price: 1.09942 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-11 15:00 | SELL RANGE_RIDER  | Price: 1.09398 | SL: 1.09540 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-11 16:00 | CLOSE RANGE_RIDER  | Price: 1.09540 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-11 16:00 | SELL RANGE_RIDER  | Price: 1.09543 | SL: 1.09705 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-11 17:00 | SELL RANGE_RIDER  | Price: 1.09465 | SL: 1.09639 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-11 18:00 | CLOSE RANGE_RIDER  | Price: 1.09425 | R: +0.73 | Exit: BREAK_EVEN
ðŸ“ 2024-01-11 18:00 | SELL RANGE_RIDER  | Price: 1.09425 | SL: 1.09602 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-11 20:00 | CLOSE RANGE_RIDER  | Price: 1.09639 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-11 20:00 | CLOSE RANGE_RIDER  | Price: 1.09602 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-11 20:00 | SELL RANGE_RIDER  | Price: 1.09650 | SL: 1.09823 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-11 21:00 | CLOSE RANGE_RIDER  | Price: 1.09823 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-12 00:00 | SELL RANGE_RIDER  | Price: 1.09729 | SL: 1.09892 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-12 01:00 | SELL RANGE_RIDER  | Price: 1.09825 | SL: 1.09985 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-12 09:00 | CLOSE RANGE_RIDER  | Price: 1.09666 | R: +0.99 | Exit: BREAK_EVEN
ðŸ“ 2024-01-12 09:00 | SELL RANGE_RIDER  | Price: 1.09666 | SL: 1.09793 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-12 10:00 | CLOSE RANGE_RIDER  | Price: 1.09793 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-12 10:00 | SELL RANGE_RIDER  | Price: 1.09751 | SL: 1.09882 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-12 11:00 | CLOSE RANGE_RIDER  | Price: 1.09626 | R: +0.63 | Exit: BREAK_EVEN
ðŸ”š 2024-01-12 11:00 | CLOSE RANGE_RIDER  | Price: 1.09626 | R: +0.95 | Exit: BREAK_EVEN
ðŸ“ 2024-01-12 11:00 | SELL RANGE_RIDER  | Price: 1.09626 | SL: 1.09761 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-12 12:00 | SELL RANGE_RIDER  | Price: 1.09600 | SL: 1.09731 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-12 13:00 | CLOSE RANGE_RIDER  | Price: 1.09497 | R: +0.95 | Exit: BREAK_EVEN
ðŸ”š 2024-01-12 13:00 | CLOSE RANGE_RIDER  | Price: 1.09497 | R: +0.79 | Exit: BREAK_EVEN
ðŸ“ 2024-01-12 13:00 | SELL RANGE_RIDER  | Price: 1.09497 | SL: 1.09630 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-12 14:00 | CLOSE RANGE_RIDER  | Price: 1.09378 | R: +0.90 | Exit: BREAK_EVEN
ðŸ“ 2024-01-12 14:00 | SELL RANGE_RIDER  | Price: 1.09378 | SL: 1.09512 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-12 15:00 | CLOSE RANGE_RIDER  | Price: 1.09512 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-12 15:00 | SELL RANGE_RIDER  | Price: 1.09554 | SL: 1.09702 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-12 16:00 | CLOSE RANGE_RIDER  | Price: 1.09702 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-12 16:00 | SELL RANGE_RIDER  | Price: 1.09757 | SL: 1.09918 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-12 17:00 | CLOSE RANGE_RIDER  | Price: 1.09665 | R: +0.57 | Exit: BREAK_EVEN
ðŸ“ 2024-01-12 17:00 | SELL RANGE_RIDER  | Price: 1.09665 | SL: 1.09832 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-12 18:00 | SELL RANGE_RIDER  | Price: 1.09583 | SL: 1.09749 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-12 19:00 | CLOSE RANGE_RIDER  | Price: 1.09497 | R: +1.01 | Exit: BREAK_EVEN
ðŸ”š 2024-01-12 19:00 | CLOSE RANGE_RIDER  | Price: 1.09497 | R: +0.52 | Exit: BREAK_EVEN
ðŸ“ 2024-01-12 19:00 | SELL RANGE_RIDER  | Price: 1.09497 | SL: 1.09660 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-12 20:00 | SELL RANGE_RIDER  | Price: 1.09595 | SL: 1.09754 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-12 22:00 | CLOSE RANGE_RIDER  | Price: 1.09514 | R: +0.51 | Exit: BREAK_EVEN
ðŸ“ 2024-01-12 22:00 | SELL RANGE_RIDER  | Price: 1.09514 | SL: 1.09662 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-15 00:00 | CLOSE RANGE_RIDER  | Price: 1.09498 | R: -0.01 | Exit: MAX_HOLD_TIME
ðŸ”š 2024-01-15 00:00 | CLOSE RANGE_RIDER  | Price: 1.09498 | R: +0.11 | Exit: MAX_HOLD_TIME
ðŸ“ 2024-01-15 00:00 | SELL RANGE_RIDER  | Price: 1.09498 | SL: 1.09633 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-15 01:00 | SELL RANGE_RIDER  | Price: 1.09451 | SL: 1.09580 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-15 04:00 | CLOSE RANGE_RIDER  | Price: 1.09633 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-15 04:00 | CLOSE RANGE_RIDER  | Price: 1.09580 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-15 04:00 | SELL RANGE_RIDER  | Price: 1.09650 | SL: 1.09774 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-15 05:00 | SELL RANGE_RIDER  | Price: 1.09642 | SL: 1.09760 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-15 09:00 | CLOSE RANGE_RIDER  | Price: 1.09535 | R: +0.93 | Exit: BREAK_EVEN
ðŸ”š 2024-01-15 09:00 | CLOSE RANGE_RIDER  | Price: 1.09535 | R: +0.91 | Exit: BREAK_EVEN
ðŸ“ 2024-01-15 09:00 | SELL RANGE_RIDER  | Price: 1.09535 | SL: 1.09643 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-15 10:00 | CLOSE RANGE_RIDER  | Price: 1.09643 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-15 10:00 | SELL RANGE_RIDER  | Price: 1.09581 | SL: 1.09689 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-15 11:00 | CLOSE RANGE_RIDER  | Price: 1.09469 | R: +1.04 | Exit: BREAK_EVEN
ðŸ“ 2024-01-15 11:00 | SELL RANGE_RIDER  | Price: 1.09469 | SL: 1.09581 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-15 12:00 | CLOSE RANGE_RIDER  | Price: 1.09402 | R: +0.60 | Exit: BREAK_EVEN
ðŸ“ 2024-01-15 12:00 | SELL RANGE_RIDER  | Price: 1.09402 | SL: 1.09515 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-15 13:00 | SELL RANGE_RIDER  | Price: 1.09455 | SL: 1.09567 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-15 14:00 | CLOSE RANGE_RIDER  | Price: 1.09515 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-15 14:00 | CLOSE RANGE_RIDER  | Price: 1.09567 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-15 14:00 | SELL RANGE_RIDER  | Price: 1.09539 | SL: 1.09654 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-15 15:00 | SELL RANGE_RIDER  | Price: 1.09506 | SL: 1.09619 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-15 16:00 | CLOSE RANGE_RIDER  | Price: 1.09434 | R: +0.92 | Exit: BREAK_EVEN
ðŸ”š 2024-01-15 16:00 | CLOSE RANGE_RIDER  | Price: 1.09434 | R: +0.64 | Exit: BREAK_EVEN
ðŸ“ 2024-01-15 16:00 | SELL RANGE_RIDER  | Price: 1.09434 | SL: 1.09549 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-15 17:00 | SELL RANGE_RIDER  | Price: 1.09497 | SL: 1.09613 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-16 02:00 | CLOSE RANGE_RIDER  | Price: 1.09198 | R: +2.06 | Exit: BREAK_EVEN
ðŸ”š 2024-01-16 02:00 | CLOSE RANGE_RIDER  | Price: 1.09198 | R: +2.59 | Exit: BREAK_EVEN
ðŸ“ 2024-01-16 02:00 | SELL RANGE_RIDER  | Price: 1.09198 | SL: 1.09295 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-16 03:00 | CLOSE RANGE_RIDER  | Price: 1.09295 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-16 03:00 | SELL RANGE_RIDER  | Price: 1.09277 | SL: 1.09378 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-16 04:00 | SELL RANGE_RIDER  | Price: 1.09240 | SL: 1.09338 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-16 05:00 | CLOSE RANGE_RIDER  | Price: 1.09190 | R: +0.86 | Exit: BREAK_EVEN
ðŸ”š 2024-01-16 05:00 | CLOSE RANGE_RIDER  | Price: 1.09190 | R: +0.51 | Exit: BREAK_EVEN
ðŸ“ 2024-01-16 05:00 | SELL RANGE_RIDER  | Price: 1.09190 | SL: 1.09288 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-01-16 06:00 | SELL RANGE_RIDER  | Price: 1.09176 | SL: 1.09272 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-16 10:00 | CLOSE RANGE_RIDER  | Price: 1.09049 | R: +1.44 | Exit: BREAK_EVEN
ðŸ”š 2024-01-16 10:00 | CLOSE RANGE_RIDER  | Price: 1.09049 | R: +1.32 | Exit: BREAK_EVEN
ðŸ“ 2024-01-16 10:00 | SELL RANGE_RIDER  | Price: 1.09049 | SL: 1.09162 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-16 11:00 | CLOSE RANGE_RIDER  | Price: 1.08862 | R: +1.65 | Exit: BREAK_EVEN
ðŸ“ 2024-01-16 11:00 | SELL RANGE_RIDER  | Price: 1.08862 | SL: 1.08982 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-01-16 12:00 | SELL RANGE_RIDER  | Price: 1.08813 | SL: 1.08932 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-16 13:00 | CLOSE RANGE_RIDER  | Price: 1.08932 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-16 13:00 | SELL RANGE_RIDER  | Price: 1.08924 | SL: 1.09049 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-16 15:00 | CLOSE RANGE_RIDER  | Price: 1.08740 | R: +1.02 | Exit: BREAK_EVEN
ðŸ”š 2024-01-16 15:00 | CLOSE RANGE_RIDER  | Price: 1.08740 | R: +1.47 | Exit: BREAK_EVEN
ðŸ“ 2024-01-16 15:00 | SELL RANGE_RIDER  | Price: 1.08740 | SL: 1.08873 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-16 16:00 | CLOSE RANGE_RIDER  | Price: 1.08873 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-16 16:00 | SELL RANGE_RIDER  | Price: 1.08725 | SL: 1.08865 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-16 17:00 | CLOSE RANGE_RIDER  | Price: 1.08865 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-16 17:00 | SELL RANGE_RIDER  | Price: 1.08858 | SL: 1.09004 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-01-16 18:00 | SELL RANGE_RIDER  | Price: 1.08812 | SL: 1.08971 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-16 19:00 | CLOSE RANGE_RIDER  | Price: 1.08631 | R: +1.55 | Exit: BREAK_EVEN
ðŸ”š 2024-01-16 19:00 | CLOSE RANGE_RIDER  | Price: 1.08631 | R: +1.14 | Exit: BREAK_EVEN
ðŸ“ 2024-01-16 19:00 | SELL RANGE_RIDER  | Price: 1.08631 | SL: 1.08793 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-01-16 20:00 | SELL RANGE_RIDER  | Price: 1.08701 | SL: 1.08862 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-17 03:00 | CLOSE RANGE_RIDER  | Price: 1.08793 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-17 03:00 | SELL RANGE_RIDER  | Price: 1.08775 | SL: 1.08897 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-17 05:00 | CLOSE RANGE_RIDER  | Price: 1.08664 | R: +0.91 | Exit: BREAK_EVEN
ðŸ“ 2024-01-17 05:00 | SELL RANGE_RIDER  | Price: 1.08664 | SL: 1.08783 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-17 10:00 | CLOSE RANGE_RIDER  | Price: 1.08783 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-17 10:00 | SELL RANGE_RIDER  | Price: 1.08668 | SL: 1.08787 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-17 11:00 | CLOSE RANGE_RIDER  | Price: 1.08787 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-17 11:00 | SELL RANGE_RIDER  | Price: 1.08764 | SL: 1.08887 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-17 15:00 | CLOSE RANGE_RIDER  | Price: 1.08640 | R: +1.00 | Exit: BREAK_EVEN
ðŸ“ 2024-01-17 15:00 | SELL RANGE_RIDER  | Price: 1.08640 | SL: 1.08777 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-17 16:00 | CLOSE RANGE_RIDER  | Price: 1.08490 | R: +1.31 | Exit: BREAK_EVEN
ðŸ”š 2024-01-17 16:00 | CLOSE RANGE_RIDER  | Price: 1.08490 | R: +1.09 | Exit: BREAK_EVEN
ðŸ“ 2024-01-17 16:00 | SELL RANGE_RIDER  | Price: 1.08490 | SL: 1.08633 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-17 17:00 | CLOSE RANGE_RIDER  | Price: 1.08633 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-17 17:00 | SELL RANGE_RIDER  | Price: 1.08491 | SL: 1.08643 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-17 18:00 | CLOSE RANGE_RIDER  | Price: 1.08643 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-17 18:00 | SELL RANGE_RIDER  | Price: 1.08574 | SL: 1.08728 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-01-17 19:00 | SELL RANGE_RIDER  | Price: 1.08671 | SL: 1.08823 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-17 21:00 | CLOSE RANGE_RIDER  | Price: 1.08728 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-17 21:00 | SELL RANGE_RIDER  | Price: 1.08739 | SL: 1.08886 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-01-17 23:00 | CLOSE RANGE_RIDER  | Price: 1.08823 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-17 23:00 | SELL RANGE_RIDER  | Price: 1.08822 | SL: 1.08958 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-18 02:00 | CLOSE RANGE_RIDER  | Price: 1.08886 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-18 02:00 | SELL RANGE_RIDER  | Price: 1.08941 | SL: 1.09065 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-18 03:00 | CLOSE RANGE_RIDER  | Price: 1.08958 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-18 03:00 | SELL RANGE_RIDER  | Price: 1.08961 | SL: 1.09083 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-18 08:00 | CLOSE RANGE_RIDER  | Price: 1.09065 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-18 08:00 | SELL RANGE_RIDER  | Price: 1.09041 | SL: 1.09150 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-18 09:00 | CLOSE RANGE_RIDER  | Price: 1.08883 | R: +0.64 | Exit: BREAK_EVEN
ðŸ”š 2024-01-18 09:00 | CLOSE RANGE_RIDER  | Price: 1.08883 | R: +1.45 | Exit: BREAK_EVEN
ðŸ“ 2024-01-18 09:00 | SELL RANGE_RIDER  | Price: 1.08883 | SL: 1.08999 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-18 10:00 | CLOSE RANGE_RIDER  | Price: 1.08799 | R: +0.72 | Exit: BREAK_EVEN
ðŸ“ 2024-01-18 10:00 | SELL RANGE_RIDER  | Price: 1.08799 | SL: 1.08915 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-18 11:00 | CLOSE RANGE_RIDER  | Price: 1.08915 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-18 11:00 | SELL RANGE_RIDER  | Price: 1.08847 | SL: 1.08971 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-18 12:00 | SELL RANGE_RIDER  | Price: 1.08950 | SL: 1.09074 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-18 14:00 | CLOSE RANGE_RIDER  | Price: 1.08775 | R: +0.58 | Exit: BREAK_EVEN
ðŸ”š 2024-01-18 14:00 | CLOSE RANGE_RIDER  | Price: 1.08775 | R: +1.41 | Exit: BREAK_EVEN
ðŸ“ 2024-01-18 14:00 | SELL RANGE_RIDER  | Price: 1.08775 | SL: 1.08903 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-18 15:00 | CLOSE RANGE_RIDER  | Price: 1.08526 | R: +1.94 | Exit: BREAK_EVEN
ðŸ“ 2024-01-18 15:00 | SELL RANGE_RIDER  | Price: 1.08526 | SL: 1.08665 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-18 16:00 | CLOSE RANGE_RIDER  | Price: 1.08665 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-18 16:00 | SELL RANGE_RIDER  | Price: 1.08596 | SL: 1.08739 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-18 17:00 | CLOSE RANGE_RIDER  | Price: 1.08522 | R: +0.52 | Exit: BREAK_EVEN
ðŸ“ 2024-01-18 17:00 | SELL RANGE_RIDER  | Price: 1.08522 | SL: 1.08670 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-18 18:00 | CLOSE RANGE_RIDER  | Price: 1.08670 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-18 18:00 | SELL RANGE_RIDER  | Price: 1.08619 | SL: 1.08770 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-18 19:00 | SELL RANGE_RIDER  | Price: 1.08597 | SL: 1.08748 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-18 23:00 | CLOSE RANGE_RIDER  | Price: 1.08770 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-18 23:00 | CLOSE RANGE_RIDER  | Price: 1.08748 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-18 23:00 | SELL RANGE_RIDER  | Price: 1.08762 | SL: 1.08899 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-19 00:00 | SELL RANGE_RIDER  | Price: 1.08747 | SL: 1.08878 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-19 04:00 | CLOSE RANGE_RIDER  | Price: 1.08878 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-19 04:00 | SELL RANGE_RIDER  | Price: 1.08881 | SL: 1.08997 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-19 07:00 | CLOSE RANGE_RIDER  | Price: 1.08809 | R: +0.62 | Exit: BREAK_EVEN
ðŸ“ 2024-01-19 07:00 | SELL RANGE_RIDER  | Price: 1.08809 | SL: 1.08913 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-19 13:00 | CLOSE RANGE_RIDER  | Price: 1.08899 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-19 13:00 | CLOSE RANGE_RIDER  | Price: 1.08913 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-19 13:00 | SELL RANGE_RIDER  | Price: 1.08874 | SL: 1.08985 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-19 14:00 | SELL RANGE_RIDER  | Price: 1.08827 | SL: 1.08935 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-19 15:00 | CLOSE RANGE_RIDER  | Price: 1.08806 | R: +0.62 | Exit: BREAK_EVEN
ðŸ“ 2024-01-19 15:00 | SELL RANGE_RIDER  | Price: 1.08806 | SL: 1.08917 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-19 19:00 | CLOSE RANGE_RIDER  | Price: 1.08917 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-19 19:00 | SELL RANGE_RIDER  | Price: 1.08897 | SL: 1.09016 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-19 20:00 | CLOSE RANGE_RIDER  | Price: 1.08935 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-19 20:00 | SELL RANGE_RIDER  | Price: 1.08922 | SL: 1.09041 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-22 00:00 | CLOSE RANGE_RIDER  | Price: 1.08925 | R: -0.23 | Exit: MAX_HOLD_TIME
ðŸ”š 2024-01-22 00:00 | CLOSE RANGE_RIDER  | Price: 1.08925 | R: -0.03 | Exit: MAX_HOLD_TIME
ðŸ“ 2024-01-22 00:00 | SELL RANGE_RIDER  | Price: 1.08925 | SL: 1.09029 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-22 01:00 | SELL RANGE_RIDER  | Price: 1.08922 | SL: 1.09024 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-22 03:00 | CLOSE RANGE_RIDER  | Price: 1.09029 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-22 03:00 | CLOSE RANGE_RIDER  | Price: 1.09024 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-22 03:00 | SELL RANGE_RIDER  | Price: 1.09020 | SL: 1.09119 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-22 04:00 | SELL RANGE_RIDER  | Price: 1.09073 | SL: 1.09172 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-22 05:00 | CLOSE RANGE_RIDER  | Price: 1.09021 | R: +0.53 | Exit: BREAK_EVEN
ðŸ“ 2024-01-22 05:00 | SELL RANGE_RIDER  | Price: 1.09021 | SL: 1.09117 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-22 10:00 | CLOSE RANGE_RIDER  | Price: 1.08919 | R: +1.02 | Exit: BREAK_EVEN
ðŸ”š 2024-01-22 10:00 | CLOSE RANGE_RIDER  | Price: 1.08919 | R: +1.06 | Exit: BREAK_EVEN
ðŸ“ 2024-01-22 10:00 | SELL RANGE_RIDER  | Price: 1.08919 | SL: 1.09013 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-22 11:00 | CLOSE RANGE_RIDER  | Price: 1.09013 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-22 11:00 | SELL RANGE_RIDER  | Price: 1.08971 | SL: 1.09067 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-22 12:00 | CLOSE RANGE_RIDER  | Price: 1.08868 | R: +1.07 | Exit: BREAK_EVEN
ðŸ“ 2024-01-22 12:00 | SELL RANGE_RIDER  | Price: 1.08868 | SL: 1.08966 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-22 13:00 | SELL RANGE_RIDER  | Price: 1.08902 | SL: 1.08999 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-22 14:00 | CLOSE RANGE_RIDER  | Price: 1.08966 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-22 14:00 | SELL RANGE_RIDER  | Price: 1.08928 | SL: 1.09026 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-22 17:00 | CLOSE RANGE_RIDER  | Price: 1.08853 | R: +0.51 | Exit: BREAK_EVEN
ðŸ”š 2024-01-22 17:00 | CLOSE RANGE_RIDER  | Price: 1.08853 | R: +0.76 | Exit: BREAK_EVEN
ðŸ“ 2024-01-22 17:00 | SELL RANGE_RIDER  | Price: 1.08853 | SL: 1.08960 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-22 18:00 | SELL RANGE_RIDER  | Price: 1.08940 | SL: 1.09048 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-22 19:00 | CLOSE RANGE_RIDER  | Price: 1.08960 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-22 19:00 | SELL RANGE_RIDER  | Price: 1.08963 | SL: 1.09070 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-22 20:00 | CLOSE RANGE_RIDER  | Price: 1.08903 | R: +0.56 | Exit: BREAK_EVEN
ðŸ“ 2024-01-22 20:00 | SELL RANGE_RIDER  | Price: 1.08903 | SL: 1.09011 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-22 21:00 | CLOSE RANGE_RIDER  | Price: 1.08849 | R: +0.84 | Exit: BREAK_EVEN
ðŸ“ 2024-01-22 21:00 | SELL RANGE_RIDER  | Price: 1.08849 | SL: 1.08957 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-22 22:00 | CLOSE RANGE_RIDER  | Price: 1.08842 | R: +0.56 | Exit: BREAK_EVEN
ðŸ“ 2024-01-22 22:00 | SELL RANGE_RIDER  | Price: 1.08842 | SL: 1.08946 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-23 01:00 | CLOSE RANGE_RIDER  | Price: 1.08775 | R: +0.68 | Exit: BREAK_EVEN
ðŸ”š 2024-01-23 01:00 | CLOSE RANGE_RIDER  | Price: 1.08775 | R: +0.64 | Exit: BREAK_EVEN
ðŸ“ 2024-01-23 01:00 | SELL RANGE_RIDER  | Price: 1.08775 | SL: 1.08867 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-23 02:00 | SELL RANGE_RIDER  | Price: 1.08832 | SL: 1.08924 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-23 03:00 | CLOSE RANGE_RIDER  | Price: 1.08867 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-23 03:00 | SELL RANGE_RIDER  | Price: 1.08885 | SL: 1.08979 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-23 04:00 | CLOSE RANGE_RIDER  | Price: 1.08924 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-23 04:00 | SELL RANGE_RIDER  | Price: 1.08874 | SL: 1.08967 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-23 06:00 | CLOSE RANGE_RIDER  | Price: 1.08979 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-23 06:00 | CLOSE RANGE_RIDER  | Price: 1.08967 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-23 06:00 | SELL RANGE_RIDER  | Price: 1.08985 | SL: 1.09077 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-23 07:00 | CLOSE RANGE_RIDER  | Price: 1.09077 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-23 07:00 | SELL RANGE_RIDER  | Price: 1.09070 | SL: 1.09163 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-23 08:00 | SELL RANGE_RIDER  | Price: 1.09141 | SL: 1.09237 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-23 09:00 | CLOSE RANGE_RIDER  | Price: 1.09083 | R: +0.61 | Exit: BREAK_EVEN
ðŸ“ 2024-01-23 09:00 | SELL RANGE_RIDER  | Price: 1.09083 | SL: 1.09181 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-23 10:00 | CLOSE RANGE_RIDER  | Price: 1.08951 | R: +1.27 | Exit: BREAK_EVEN
ðŸ”š 2024-01-23 10:00 | CLOSE RANGE_RIDER  | Price: 1.08951 | R: +1.35 | Exit: BREAK_EVEN
ðŸ“ 2024-01-23 10:00 | SELL RANGE_RIDER  | Price: 1.08951 | SL: 1.09055 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-23 11:00 | CLOSE RANGE_RIDER  | Price: 1.08876 | R: +0.72 | Exit: BREAK_EVEN
ðŸ“ 2024-01-23 11:00 | SELL RANGE_RIDER  | Price: 1.08876 | SL: 1.08981 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-23 12:00 | CLOSE RANGE_RIDER  | Price: 1.08695 | R: +1.73 | Exit: BREAK_EVEN
ðŸ“ 2024-01-23 12:00 | SELL RANGE_RIDER  | Price: 1.08695 | SL: 1.08807 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-23 13:00 | SELL RANGE_RIDER  | Price: 1.08665 | SL: 1.08778 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-23 16:00 | CLOSE RANGE_RIDER  | Price: 1.08528 | R: +1.49 | Exit: BREAK_EVEN
ðŸ”š 2024-01-23 16:00 | CLOSE RANGE_RIDER  | Price: 1.08528 | R: +1.21 | Exit: BREAK_EVEN
ðŸ“ 2024-01-23 16:00 | SELL RANGE_RIDER  | Price: 1.08528 | SL: 1.08653 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-23 17:00 | CLOSE RANGE_RIDER  | Price: 1.08310 | R: +1.75 | Exit: BREAK_EVEN
ðŸ“ 2024-01-23 17:00 | SELL RANGE_RIDER  | Price: 1.08310 | SL: 1.08452 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-23 18:00 | SELL RANGE_RIDER  | Price: 1.08282 | SL: 1.08424 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-23 21:00 | CLOSE RANGE_RIDER  | Price: 1.08452 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-23 21:00 | CLOSE RANGE_RIDER  | Price: 1.08424 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-23 21:00 | SELL RANGE_RIDER  | Price: 1.08452 | SL: 1.08587 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-01-23 22:00 | SELL RANGE_RIDER  | Price: 1.08499 | SL: 1.08629 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-24 01:00 | CLOSE RANGE_RIDER  | Price: 1.08587 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-24 01:00 | SELL RANGE_RIDER  | Price: 1.08574 | SL: 1.08692 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-24 06:00 | CLOSE RANGE_RIDER  | Price: 1.08629 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-24 06:00 | SELL RANGE_RIDER  | Price: 1.08646 | SL: 1.08747 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-24 09:00 | CLOSE RANGE_RIDER  | Price: 1.08692 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-24 09:00 | CLOSE RANGE_RIDER  | Price: 1.08747 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-24 09:00 | SELL RANGE_RIDER  | Price: 1.08734 | SL: 1.08835 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-24 10:00 | SELL RANGE_RIDER  | Price: 1.08701 | SL: 1.08808 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-24 11:00 | CLOSE RANGE_RIDER  | Price: 1.08835 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-24 11:00 | CLOSE RANGE_RIDER  | Price: 1.08808 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-25 00:00 | SELL RANGE_RIDER  | Price: 1.08862 | SL: 1.08996 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-01-25 01:00 | SELL RANGE_RIDER  | Price: 1.08812 | SL: 1.08940 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-25 02:00 | CLOSE RANGE_RIDER  | Price: 1.08742 | R: +0.90 | Exit: BREAK_EVEN
ðŸ”š 2024-01-25 02:00 | CLOSE RANGE_RIDER  | Price: 1.08742 | R: +0.55 | Exit: BREAK_EVEN
ðŸ“ 2024-01-25 02:00 | SELL RANGE_RIDER  | Price: 1.08742 | SL: 1.08868 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-25 03:00 | SELL RANGE_RIDER  | Price: 1.08777 | SL: 1.08900 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-25 09:00 | CLOSE RANGE_RIDER  | Price: 1.08868 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-25 09:00 | CLOSE RANGE_RIDER  | Price: 1.08900 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-25 09:00 | SELL RANGE_RIDER  | Price: 1.08879 | SL: 1.08982 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-25 10:00 | CLOSE RANGE_RIDER  | Price: 1.08982 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-25 10:00 | SELL RANGE_RIDER  | Price: 1.08991 | SL: 1.09098 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-25 11:00 | SELL RANGE_RIDER  | Price: 1.08960 | SL: 1.09065 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-25 12:00 | CLOSE RANGE_RIDER  | Price: 1.08930 | R: +0.57 | Exit: BREAK_EVEN
ðŸ“ 2024-01-25 12:00 | SELL RANGE_RIDER  | Price: 1.08930 | SL: 1.09033 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-25 14:00 | CLOSE RANGE_RIDER  | Price: 1.08882 | R: +0.74 | Exit: BREAK_EVEN
ðŸ“ 2024-01-25 14:00 | SELL RANGE_RIDER  | Price: 1.08882 | SL: 1.08984 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-25 15:00 | CLOSE RANGE_RIDER  | Price: 1.08793 | R: +1.33 | Exit: BREAK_EVEN
ðŸ”š 2024-01-25 15:00 | CLOSE RANGE_RIDER  | Price: 1.08984 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-25 15:00 | SELL RANGE_RIDER  | Price: 1.08793 | SL: 1.08913 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-25 16:00 | CLOSE RANGE_RIDER  | Price: 1.08603 | R: +1.59 | Exit: BREAK_EVEN
ðŸ“ 2024-01-25 16:00 | SELL RANGE_RIDER  | Price: 1.08603 | SL: 1.08733 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-25 17:00 | CLOSE RANGE_RIDER  | Price: 1.08317 | R: +2.20 | Exit: BREAK_EVEN
ðŸ“ 2024-01-25 17:00 | SELL RANGE_RIDER  | Price: 1.08317 | SL: 1.08461 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-25 18:00 | SELL RANGE_RIDER  | Price: 1.08364 | SL: 1.08509 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-25 19:00 | CLOSE RANGE_RIDER  | Price: 1.08461 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-25 19:00 | CLOSE RANGE_RIDER  | Price: 1.08509 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-25 19:00 | SELL RANGE_RIDER  | Price: 1.08378 | SL: 1.08527 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-25 20:00 | CLOSE RANGE_RIDER  | Price: 1.08302 | R: +0.51 | Exit: BREAK_EVEN
ðŸ“ 2024-01-25 20:00 | SELL RANGE_RIDER  | Price: 1.08302 | SL: 1.08453 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-25 21:00 | SELL RANGE_RIDER  | Price: 1.08360 | SL: 1.08511 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-25 23:00 | CLOSE RANGE_RIDER  | Price: 1.08453 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-25 23:00 | SELL RANGE_RIDER  | Price: 1.08473 | SL: 1.08615 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-26 02:00 | CLOSE RANGE_RIDER  | Price: 1.08400 | R: +0.52 | Exit: BREAK_EVEN
ðŸ“ 2024-01-26 02:00 | SELL RANGE_RIDER  | Price: 1.08400 | SL: 1.08526 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-26 08:00 | CLOSE RANGE_RIDER  | Price: 1.08294 | R: +0.84 | Exit: BREAK_EVEN
ðŸ“ 2024-01-26 08:00 | SELL RANGE_RIDER  | Price: 1.08294 | SL: 1.08401 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-26 09:00 | CLOSE RANGE_RIDER  | Price: 1.08196 | R: +1.08 | Exit: BREAK_EVEN
ðŸ”š 2024-01-26 09:00 | CLOSE RANGE_RIDER  | Price: 1.08196 | R: +0.91 | Exit: BREAK_EVEN
ðŸ“ 2024-01-26 09:00 | SELL RANGE_RIDER  | Price: 1.08196 | SL: 1.08308 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-26 10:00 | CLOSE RANGE_RIDER  | Price: 1.08308 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-26 10:00 | SELL RANGE_RIDER  | Price: 1.08404 | SL: 1.08526 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-01-26 11:00 | SELL RANGE_RIDER  | Price: 1.08442 | SL: 1.08567 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-26 12:00 | CLOSE RANGE_RIDER  | Price: 1.08526 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-26 12:00 | CLOSE RANGE_RIDER  | Price: 1.08567 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-26 12:00 | SELL RANGE_RIDER  | Price: 1.08649 | SL: 1.08781 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-01-26 13:00 | SELL RANGE_RIDER  | Price: 1.08747 | SL: 1.08878 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-26 14:00 | CLOSE RANGE_RIDER  | Price: 1.08675 | R: +0.55 | Exit: BREAK_EVEN
ðŸ“ 2024-01-26 14:00 | SELL RANGE_RIDER  | Price: 1.08675 | SL: 1.08804 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-26 15:00 | CLOSE RANGE_RIDER  | Price: 1.08781 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-26 15:00 | CLOSE RANGE_RIDER  | Price: 1.08804 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-26 15:00 | SELL RANGE_RIDER  | Price: 1.08721 | SL: 1.08862 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-26 16:00 | SELL RANGE_RIDER  | Price: 1.08740 | SL: 1.08885 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-26 17:00 | CLOSE RANGE_RIDER  | Price: 1.08641 | R: +0.57 | Exit: BREAK_EVEN
ðŸ”š 2024-01-26 17:00 | CLOSE RANGE_RIDER  | Price: 1.08641 | R: +0.68 | Exit: BREAK_EVEN
ðŸ“ 2024-01-26 17:00 | SELL RANGE_RIDER  | Price: 1.08641 | SL: 1.08789 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-26 18:00 | SELL RANGE_RIDER  | Price: 1.08650 | SL: 1.08795 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-26 20:00 | CLOSE RANGE_RIDER  | Price: 1.08558 | R: +0.56 | Exit: BREAK_EVEN
ðŸ”š 2024-01-26 20:00 | CLOSE RANGE_RIDER  | Price: 1.08558 | R: +0.63 | Exit: BREAK_EVEN
ðŸ“ 2024-01-26 20:00 | SELL RANGE_RIDER  | Price: 1.08558 | SL: 1.08699 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-26 21:00 | SELL RANGE_RIDER  | Price: 1.08583 | SL: 1.08719 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-29 00:00 | CLOSE RANGE_RIDER  | Price: 1.08458 | R: +0.71 | Exit: BREAK_EVEN
ðŸ”š 2024-01-29 00:00 | CLOSE RANGE_RIDER  | Price: 1.08458 | R: +0.92 | Exit: BREAK_EVEN
ðŸ“ 2024-01-29 00:00 | SELL RANGE_RIDER  | Price: 1.08458 | SL: 1.08585 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-29 01:00 | SELL RANGE_RIDER  | Price: 1.08424 | SL: 1.08547 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-29 09:00 | CLOSE RANGE_RIDER  | Price: 1.08372 | R: +0.68 | Exit: BREAK_EVEN
ðŸ“ 2024-01-29 09:00 | SELL RANGE_RIDER  | Price: 1.08372 | SL: 1.08471 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-29 10:00 | CLOSE RANGE_RIDER  | Price: 1.08348 | R: +0.62 | Exit: BREAK_EVEN
ðŸ“ 2024-01-29 10:00 | SELL RANGE_RIDER  | Price: 1.08348 | SL: 1.08447 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-29 11:00 | CLOSE RANGE_RIDER  | Price: 1.08253 | R: +1.20 | Exit: BREAK_EVEN
ðŸ”š 2024-01-29 11:00 | CLOSE RANGE_RIDER  | Price: 1.08253 | R: +0.96 | Exit: BREAK_EVEN
ðŸ“ 2024-01-29 11:00 | SELL RANGE_RIDER  | Price: 1.08253 | SL: 1.08354 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-29 12:00 | CLOSE RANGE_RIDER  | Price: 1.08192 | R: +0.61 | Exit: BREAK_EVEN
ðŸ“ 2024-01-29 12:00 | SELL RANGE_RIDER  | Price: 1.08192 | SL: 1.08294 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-29 13:00 | SELL RANGE_RIDER  | Price: 1.08230 | SL: 1.08332 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-29 14:00 | CLOSE RANGE_RIDER  | Price: 1.08294 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-29 14:00 | CLOSE RANGE_RIDER  | Price: 1.08332 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-29 14:00 | SELL RANGE_RIDER  | Price: 1.08221 | SL: 1.08328 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-29 15:00 | SELL RANGE_RIDER  | Price: 1.08204 | SL: 1.08311 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-29 16:00 | CLOSE RANGE_RIDER  | Price: 1.08071 | R: +1.41 | Exit: BREAK_EVEN
ðŸ”š 2024-01-29 16:00 | CLOSE RANGE_RIDER  | Price: 1.08071 | R: +1.25 | Exit: BREAK_EVEN
ðŸ“ 2024-01-29 16:00 | SELL RANGE_RIDER  | Price: 1.08071 | SL: 1.08183 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-29 17:00 | CLOSE RANGE_RIDER  | Price: 1.07975 | R: +0.86 | Exit: BREAK_EVEN
ðŸ“ 2024-01-29 17:00 | SELL RANGE_RIDER  | Price: 1.07975 | SL: 1.08090 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-29 18:00 | SELL RANGE_RIDER  | Price: 1.08061 | SL: 1.08177 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-29 19:00 | CLOSE RANGE_RIDER  | Price: 1.08090 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-29 19:00 | SELL RANGE_RIDER  | Price: 1.08117 | SL: 1.08232 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-29 21:00 | CLOSE RANGE_RIDER  | Price: 1.08177 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-29 21:00 | SELL RANGE_RIDER  | Price: 1.08190 | SL: 1.08299 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-29 22:00 | CLOSE RANGE_RIDER  | Price: 1.08232 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-29 22:00 | CLOSE RANGE_RIDER  | Price: 1.08299 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-29 22:00 | SELL RANGE_RIDER  | Price: 1.08312 | SL: 1.08428 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-29 23:00 | SELL RANGE_RIDER  | Price: 1.08334 | SL: 1.08448 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-30 06:00 | CLOSE RANGE_RIDER  | Price: 1.08254 | R: +0.70 | Exit: BREAK_EVEN
ðŸ“ 2024-01-30 06:00 | SELL RANGE_RIDER  | Price: 1.08254 | SL: 1.08349 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-30 07:00 | CLOSE RANGE_RIDER  | Price: 1.08225 | R: +0.75 | Exit: BREAK_EVEN
ðŸ“ 2024-01-30 07:00 | SELL RANGE_RIDER  | Price: 1.08225 | SL: 1.08318 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-30 08:00 | CLOSE RANGE_RIDER  | Price: 1.08152 | R: +1.08 | Exit: BREAK_EVEN
ðŸ”š 2024-01-30 08:00 | CLOSE RANGE_RIDER  | Price: 1.08152 | R: +0.78 | Exit: BREAK_EVEN
ðŸ“ 2024-01-30 08:00 | SELL RANGE_RIDER  | Price: 1.08152 | SL: 1.08247 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-30 09:00 | SELL RANGE_RIDER  | Price: 1.08228 | SL: 1.08325 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-30 10:00 | CLOSE RANGE_RIDER  | Price: 1.08247 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-30 10:00 | SELL RANGE_RIDER  | Price: 1.08221 | SL: 1.08323 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-30 12:00 | CLOSE RANGE_RIDER  | Price: 1.08325 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-30 12:00 | CLOSE RANGE_RIDER  | Price: 1.08323 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-30 12:00 | SELL RANGE_RIDER  | Price: 1.08384 | SL: 1.08492 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-30 13:00 | SELL RANGE_RIDER  | Price: 1.08419 | SL: 1.08527 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-30 14:00 | CLOSE RANGE_RIDER  | Price: 1.08492 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-30 14:00 | SELL RANGE_RIDER  | Price: 1.08477 | SL: 1.08587 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-30 15:00 | CLOSE RANGE_RIDER  | Price: 1.08345 | R: +0.69 | Exit: BREAK_EVEN
ðŸ”š 2024-01-30 15:00 | CLOSE RANGE_RIDER  | Price: 1.08345 | R: +1.20 | Exit: BREAK_EVEN
ðŸ“ 2024-01-30 15:00 | SELL RANGE_RIDER  | Price: 1.08345 | SL: 1.08457 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-30 16:00 | CLOSE RANGE_RIDER  | Price: 1.08457 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-30 16:00 | SELL RANGE_RIDER  | Price: 1.08505 | SL: 1.08629 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-30 17:00 | CLOSE RANGE_RIDER  | Price: 1.08371 | R: +1.08 | Exit: BREAK_EVEN
ðŸ“ 2024-01-30 17:00 | SELL RANGE_RIDER  | Price: 1.08371 | SL: 1.08506 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-30 18:00 | SELL RANGE_RIDER  | Price: 1.08432 | SL: 1.08564 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-30 20:00 | CLOSE RANGE_RIDER  | Price: 1.08358 | R: +0.56 | Exit: BREAK_EVEN
ðŸ“ 2024-01-30 20:00 | SELL RANGE_RIDER  | Price: 1.08358 | SL: 1.08484 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-30 22:00 | CLOSE RANGE_RIDER  | Price: 1.08484 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-30 22:00 | SELL RANGE_RIDER  | Price: 1.08447 | SL: 1.08569 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-31 03:00 | CLOSE RANGE_RIDER  | Price: 1.08314 | R: +1.09 | Exit: BREAK_EVEN
ðŸ“ 2024-01-31 03:00 | SELL RANGE_RIDER  | Price: 1.08314 | SL: 1.08419 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-31 04:00 | CLOSE RANGE_RIDER  | Price: 1.08184 | R: +1.39 | Exit: BREAK_EVEN
ðŸ”š 2024-01-31 04:00 | CLOSE RANGE_RIDER  | Price: 1.08184 | R: +1.24 | Exit: BREAK_EVEN
ðŸ“ 2024-01-31 04:00 | SELL RANGE_RIDER  | Price: 1.08184 | SL: 1.08292 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-31 05:00 | SELL RANGE_RIDER  | Price: 1.08188 | SL: 1.08290 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-31 11:00 | CLOSE RANGE_RIDER  | Price: 1.08292 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-31 11:00 | CLOSE RANGE_RIDER  | Price: 1.08290 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-31 11:00 | SELL RANGE_RIDER  | Price: 1.08223 | SL: 1.08333 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-31 12:00 | SELL RANGE_RIDER  | Price: 1.08255 | SL: 1.08364 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-31 13:00 | CLOSE RANGE_RIDER  | Price: 1.08333 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-31 13:00 | CLOSE RANGE_RIDER  | Price: 1.08364 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-31 13:00 | SELL RANGE_RIDER  | Price: 1.08390 | SL: 1.08502 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-01-31 14:00 | SELL RANGE_RIDER  | Price: 1.08368 | SL: 1.08479 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-31 15:00 | CLOSE RANGE_RIDER  | Price: 1.08502 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-31 15:00 | CLOSE RANGE_RIDER  | Price: 1.08479 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-31 15:00 | SELL RANGE_RIDER  | Price: 1.08576 | SL: 1.08699 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-01-31 16:00 | CLOSE RANGE_RIDER  | Price: 1.08699 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-31 16:00 | SELL RANGE_RIDER  | Price: 1.08801 | SL: 1.08940 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-31 17:00 | CLOSE RANGE_RIDER  | Price: 1.08612 | R: +1.36 | Exit: BREAK_EVEN
ðŸ“ 2024-01-31 17:00 | SELL RANGE_RIDER  | Price: 1.08612 | SL: 1.08765 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-31 18:00 | SELL RANGE_RIDER  | Price: 1.08545 | SL: 1.08704 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-31 19:00 | CLOSE RANGE_RIDER  | Price: 1.08498 | R: +0.75 | Exit: BREAK_EVEN
ðŸ“ 2024-01-31 19:00 | SELL RANGE_RIDER  | Price: 1.08498 | SL: 1.08654 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-31 20:00 | CLOSE RANGE_RIDER  | Price: 1.08465 | R: +0.50 | Exit: BREAK_EVEN
ðŸ“ 2024-01-31 20:00 | SELL RANGE_RIDER  | Price: 1.08465 | SL: 1.08616 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-01-31 21:00 | CLOSE RANGE_RIDER  | Price: 1.08406 | R: +0.59 | Exit: BREAK_EVEN
ðŸ”š 2024-01-31 21:00 | CLOSE RANGE_RIDER  | Price: 1.08616 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-31 21:00 | SELL RANGE_RIDER  | Price: 1.08406 | SL: 1.08581 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-01-31 22:00 | CLOSE RANGE_RIDER  | Price: 1.08079 | R: +1.87 | Exit: BREAK_EVEN
ðŸ“ 2024-01-31 22:00 | SELL RANGE_RIDER  | Price: 1.08079 | SL: 1.08275 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-01-31 23:00 | SELL RANGE_RIDER  | Price: 1.08175 | SL: 1.08367 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-01 01:00 | CLOSE RANGE_RIDER  | Price: 1.08040 | R: +0.70 | Exit: BREAK_EVEN
ðŸ“ 2024-02-01 01:00 | SELL RANGE_RIDER  | Price: 1.08040 | SL: 1.08223 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-01 08:00 | CLOSE RANGE_RIDER  | Price: 1.07962 | R: +0.60 | Exit: BREAK_EVEN
ðŸ“ 2024-02-01 08:00 | SELL RANGE_RIDER  | Price: 1.07962 | SL: 1.08110 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-01 09:00 | CLOSE RANGE_RIDER  | Price: 1.07934 | R: +0.58 | Exit: BREAK_EVEN
ðŸ“ 2024-02-01 09:00 | SELL RANGE_RIDER  | Price: 1.07934 | SL: 1.08081 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-01 13:00 | CLOSE RANGE_RIDER  | Price: 1.08110 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-01 13:00 | CLOSE RANGE_RIDER  | Price: 1.08081 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-01 13:00 | SELL RANGE_RIDER  | Price: 1.08085 | SL: 1.08234 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-02-01 14:00 | SELL RANGE_RIDER  | Price: 1.08153 | SL: 1.08302 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-01 15:00 | CLOSE RANGE_RIDER  | Price: 1.08234 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-01 15:00 | SELL RANGE_RIDER  | Price: 1.08139 | SL: 1.08290 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-01 16:00 | CLOSE RANGE_RIDER  | Price: 1.08290 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-01 16:00 | SELL RANGE_RIDER  | Price: 1.08271 | SL: 1.08425 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-01 17:00 | CLOSE RANGE_RIDER  | Price: 1.08302 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-01 17:00 | SELL RANGE_RIDER  | Price: 1.08267 | SL: 1.08429 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-01 18:00 | CLOSE RANGE_RIDER  | Price: 1.08425 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-01 18:00 | CLOSE RANGE_RIDER  | Price: 1.08429 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-01 18:00 | SELL RANGE_RIDER  | Price: 1.08645 | SL: 1.08823 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-01 19:00 | SELL RANGE_RIDER  | Price: 1.08728 | SL: 1.08904 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-02 07:00 | CLOSE RANGE_RIDER  | Price: 1.08823 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-02 07:00 | SELL RANGE_RIDER  | Price: 1.08775 | SL: 1.08888 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-02 10:00 | CLOSE RANGE_RIDER  | Price: 1.08888 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-02 10:00 | SELL RANGE_RIDER  | Price: 1.08794 | SL: 1.08909 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-02 11:00 | CLOSE RANGE_RIDER  | Price: 1.08904 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-02 11:00 | CLOSE RANGE_RIDER  | Price: 1.08909 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-02 11:00 | SELL RANGE_RIDER  | Price: 1.08908 | SL: 1.09028 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-02 12:00 | CLOSE RANGE_RIDER  | Price: 1.08846 | R: +0.52 | Exit: BREAK_EVEN
ðŸ“ 2024-02-02 12:00 | SELL RANGE_RIDER  | Price: 1.08846 | SL: 1.08968 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-02 13:00 | SELL RANGE_RIDER  | Price: 1.08837 | SL: 1.08956 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-02 15:00 | CLOSE RANGE_RIDER  | Price: 1.08072 | R: +6.37 | Exit: BREAK_EVEN
ðŸ”š 2024-02-02 15:00 | CLOSE RANGE_RIDER  | Price: 1.08072 | R: +6.44 | Exit: BREAK_EVEN
ðŸ“ 2024-02-02 15:00 | SELL RANGE_RIDER  | Price: 1.08072 | SL: 1.08238 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-02 16:00 | SELL RANGE_RIDER  | Price: 1.08091 | SL: 1.08264 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-02 18:00 | CLOSE RANGE_RIDER  | Price: 1.07862 | R: +1.26 | Exit: BREAK_EVEN
ðŸ”š 2024-02-02 18:00 | CLOSE RANGE_RIDER  | Price: 1.07862 | R: +1.33 | Exit: BREAK_EVEN
ðŸ“ 2024-02-02 18:00 | SELL RANGE_RIDER  | Price: 1.07862 | SL: 1.08045 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-02 19:00 | SELL RANGE_RIDER  | Price: 1.07835 | SL: 1.08013 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-05 00:00 | CLOSE RANGE_RIDER  | Price: 1.07810 | R: +0.28 | Exit: MAX_HOLD_TIME
ðŸ”š 2024-02-05 00:00 | CLOSE RANGE_RIDER  | Price: 1.07810 | R: +0.14 | Exit: MAX_HOLD_TIME
ðŸ“ 2024-02-05 00:00 | SELL RANGE_RIDER  | Price: 1.07810 | SL: 1.07958 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-05 01:00 | SELL RANGE_RIDER  | Price: 1.07799 | SL: 1.07947 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-05 02:00 | CLOSE RANGE_RIDER  | Price: 1.07727 | R: +0.56 | Exit: BREAK_EVEN
ðŸ“ 2024-02-05 02:00 | SELL RANGE_RIDER  | Price: 1.07727 | SL: 1.07875 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-05 10:00 | CLOSE RANGE_RIDER  | Price: 1.07669 | R: +0.88 | Exit: BREAK_EVEN
ðŸ“ 2024-02-05 10:00 | SELL RANGE_RIDER  | Price: 1.07669 | SL: 1.07797 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-05 11:00 | CLOSE RANGE_RIDER  | Price: 1.07538 | R: +1.27 | Exit: BREAK_EVEN
ðŸ”š 2024-02-05 11:00 | CLOSE RANGE_RIDER  | Price: 1.07538 | R: +1.02 | Exit: BREAK_EVEN
ðŸ“ 2024-02-05 11:00 | SELL RANGE_RIDER  | Price: 1.07538 | SL: 1.07672 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-05 12:00 | SELL RANGE_RIDER  | Price: 1.07494 | SL: 1.07624 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-05 15:00 | CLOSE RANGE_RIDER  | Price: 1.07375 | R: +1.22 | Exit: BREAK_EVEN
ðŸ”š 2024-02-05 15:00 | CLOSE RANGE_RIDER  | Price: 1.07375 | R: +0.92 | Exit: BREAK_EVEN
ðŸ“ 2024-02-05 15:00 | SELL RANGE_RIDER  | Price: 1.07375 | SL: 1.07502 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-05 16:00 | SELL RANGE_RIDER  | Price: 1.07424 | SL: 1.07549 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-05 17:00 | CLOSE RANGE_RIDER  | Price: 1.07254 | R: +0.95 | Exit: BREAK_EVEN
ðŸ”š 2024-02-05 17:00 | CLOSE RANGE_RIDER  | Price: 1.07254 | R: +1.36 | Exit: BREAK_EVEN
ðŸ“ 2024-02-05 17:00 | SELL RANGE_RIDER  | Price: 1.07254 | SL: 1.07384 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-05 18:00 | SELL RANGE_RIDER  | Price: 1.07354 | SL: 1.07483 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-05 19:00 | CLOSE RANGE_RIDER  | Price: 1.07384 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-05 19:00 | SELL RANGE_RIDER  | Price: 1.07394 | SL: 1.07520 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-06 04:00 | CLOSE RANGE_RIDER  | Price: 1.07483 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-06 04:00 | SELL RANGE_RIDER  | Price: 1.07460 | SL: 1.07550 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-06 07:00 | CLOSE RANGE_RIDER  | Price: 1.07520 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-06 07:00 | SELL RANGE_RIDER  | Price: 1.07536 | SL: 1.07620 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-06 09:00 | CLOSE RANGE_RIDER  | Price: 1.07550 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-06 09:00 | CLOSE RANGE_RIDER  | Price: 1.07620 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-06 09:00 | SELL RANGE_RIDER  | Price: 1.07520 | SL: 1.07604 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-06 10:00 | CLOSE RANGE_RIDER  | Price: 1.07463 | R: +0.68 | Exit: BREAK_EVEN
ðŸ“ 2024-02-06 10:00 | SELL RANGE_RIDER  | Price: 1.07463 | SL: 1.07552 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-06 11:00 | CLOSE RANGE_RIDER  | Price: 1.07293 | R: +1.91 | Exit: BREAK_EVEN
ðŸ“ 2024-02-06 11:00 | SELL RANGE_RIDER  | Price: 1.07293 | SL: 1.07391 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-06 12:00 | SELL RANGE_RIDER  | Price: 1.07293 | SL: 1.07391 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-06 13:00 | CLOSE RANGE_RIDER  | Price: 1.07391 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-06 13:00 | CLOSE RANGE_RIDER  | Price: 1.07391 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-06 13:00 | SELL RANGE_RIDER  | Price: 1.07387 | SL: 1.07491 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-06 14:00 | SELL RANGE_RIDER  | Price: 1.07360 | SL: 1.07468 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-06 15:00 | CLOSE RANGE_RIDER  | Price: 1.07306 | R: +0.78 | Exit: BREAK_EVEN
ðŸ“ 2024-02-06 15:00 | SELL RANGE_RIDER  | Price: 1.07306 | SL: 1.07418 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-06 16:00 | CLOSE RANGE_RIDER  | Price: 1.07418 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-06 16:00 | SELL RANGE_RIDER  | Price: 1.07404 | SL: 1.07519 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-06 17:00 | CLOSE RANGE_RIDER  | Price: 1.07468 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-06 17:00 | SELL RANGE_RIDER  | Price: 1.07433 | SL: 1.07548 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-06 18:00 | CLOSE RANGE_RIDER  | Price: 1.07519 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-06 18:00 | SELL RANGE_RIDER  | Price: 1.07506 | SL: 1.07623 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-06 19:00 | CLOSE RANGE_RIDER  | Price: 1.07548 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-07 00:00 | SELL RANGE_RIDER  | Price: 1.07540 | SL: 1.07641 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-07 03:00 | CLOSE RANGE_RIDER  | Price: 1.07623 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-07 03:00 | CLOSE RANGE_RIDER  | Price: 1.07641 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-07 03:00 | SELL RANGE_RIDER  | Price: 1.07637 | SL: 1.07726 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-07 04:00 | SELL RANGE_RIDER  | Price: 1.07637 | SL: 1.07723 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-07 05:00 | CLOSE RANGE_RIDER  | Price: 1.07589 | R: +0.54 | Exit: BREAK_EVEN
ðŸ”š 2024-02-07 05:00 | CLOSE RANGE_RIDER  | Price: 1.07589 | R: +0.56 | Exit: BREAK_EVEN
ðŸ“ 2024-02-07 05:00 | SELL RANGE_RIDER  | Price: 1.07589 | SL: 1.07674 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-07 06:00 | SELL RANGE_RIDER  | Price: 1.07592 | SL: 1.07674 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-07 09:00 | CLOSE RANGE_RIDER  | Price: 1.07674 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-07 09:00 | CLOSE RANGE_RIDER  | Price: 1.07674 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-07 09:00 | SELL RANGE_RIDER  | Price: 1.07727 | SL: 1.07811 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-07 10:00 | CLOSE RANGE_RIDER  | Price: 1.07629 | R: +1.17 | Exit: BREAK_EVEN
ðŸ“ 2024-02-07 10:00 | SELL RANGE_RIDER  | Price: 1.07629 | SL: 1.07716 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-07 11:00 | SELL RANGE_RIDER  | Price: 1.07694 | SL: 1.07785 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-07 12:00 | CLOSE RANGE_RIDER  | Price: 1.07643 | R: +0.56 | Exit: BREAK_EVEN
ðŸ“ 2024-02-07 12:00 | SELL RANGE_RIDER  | Price: 1.07643 | SL: 1.07733 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-07 13:00 | CLOSE RANGE_RIDER  | Price: 1.07716 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-07 13:00 | CLOSE RANGE_RIDER  | Price: 1.07733 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-07 13:00 | SELL RANGE_RIDER  | Price: 1.07712 | SL: 1.07804 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-07 14:00 | SELL RANGE_RIDER  | Price: 1.07738 | SL: 1.07830 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-07 15:00 | CLOSE RANGE_RIDER  | Price: 1.07804 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-07 15:00 | CLOSE RANGE_RIDER  | Price: 1.07830 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-07 15:00 | SELL RANGE_RIDER  | Price: 1.07703 | SL: 1.07801 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-02-07 16:00 | SELL RANGE_RIDER  | Price: 1.07714 | SL: 1.07814 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-07 17:00 | CLOSE RANGE_RIDER  | Price: 1.07569 | R: +1.37 | Exit: BREAK_EVEN
ðŸ”š 2024-02-07 17:00 | CLOSE RANGE_RIDER  | Price: 1.07569 | R: +1.45 | Exit: BREAK_EVEN
ðŸ“ 2024-02-07 17:00 | SELL RANGE_RIDER  | Price: 1.07569 | SL: 1.07679 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-07 18:00 | CLOSE RANGE_RIDER  | Price: 1.07679 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-07 18:00 | SELL RANGE_RIDER  | Price: 1.07677 | SL: 1.07790 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-02-07 19:00 | SELL RANGE_RIDER  | Price: 1.07648 | SL: 1.07759 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-08 01:00 | CLOSE RANGE_RIDER  | Price: 1.07759 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-08 01:00 | SELL RANGE_RIDER  | Price: 1.07756 | SL: 1.07844 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-08 02:00 | CLOSE RANGE_RIDER  | Price: 1.07790 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-08 02:00 | SELL RANGE_RIDER  | Price: 1.07780 | SL: 1.07866 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-08 05:00 | CLOSE RANGE_RIDER  | Price: 1.07844 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-08 05:00 | SELL RANGE_RIDER  | Price: 1.07824 | SL: 1.07901 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-08 06:00 | CLOSE RANGE_RIDER  | Price: 1.07866 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-08 06:00 | SELL RANGE_RIDER  | Price: 1.07798 | SL: 1.07876 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-08 09:00 | CLOSE RANGE_RIDER  | Price: 1.07876 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-08 09:00 | SELL RANGE_RIDER  | Price: 1.07803 | SL: 1.07881 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-08 10:00 | CLOSE RANGE_RIDER  | Price: 1.07774 | R: +0.65 | Exit: BREAK_EVEN
ðŸ“ 2024-02-08 10:00 | SELL RANGE_RIDER  | Price: 1.07774 | SL: 1.07858 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-08 12:00 | CLOSE RANGE_RIDER  | Price: 1.07717 | R: +1.10 | Exit: BREAK_EVEN
ðŸ”š 2024-02-08 12:00 | CLOSE RANGE_RIDER  | Price: 1.07717 | R: +0.68 | Exit: BREAK_EVEN
ðŸ“ 2024-02-08 12:00 | SELL RANGE_RIDER  | Price: 1.07717 | SL: 1.07807 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-08 13:00 | CLOSE RANGE_RIDER  | Price: 1.07631 | R: +0.96 | Exit: BREAK_EVEN
ðŸ“ 2024-02-08 13:00 | SELL RANGE_RIDER  | Price: 1.07631 | SL: 1.07723 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-08 14:00 | CLOSE RANGE_RIDER  | Price: 1.07568 | R: +0.69 | Exit: BREAK_EVEN
ðŸ“ 2024-02-08 14:00 | SELL RANGE_RIDER  | Price: 1.07568 | SL: 1.07663 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-08 15:00 | CLOSE RANGE_RIDER  | Price: 1.07442 | R: +1.33 | Exit: BREAK_EVEN
ðŸ“ 2024-02-08 15:00 | SELL RANGE_RIDER  | Price: 1.07442 | SL: 1.07545 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-08 16:00 | CLOSE RANGE_RIDER  | Price: 1.07545 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-08 16:00 | SELL RANGE_RIDER  | Price: 1.07650 | SL: 1.07763 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-02-08 17:00 | SELL RANGE_RIDER  | Price: 1.07614 | SL: 1.07730 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-08 18:00 | CLOSE RANGE_RIDER  | Price: 1.07730 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-08 18:00 | SELL RANGE_RIDER  | Price: 1.07734 | SL: 1.07852 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-08 19:00 | CLOSE RANGE_RIDER  | Price: 1.07763 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-08 19:00 | SELL RANGE_RIDER  | Price: 1.07734 | SL: 1.07847 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-09 10:00 | CLOSE RANGE_RIDER  | Price: 1.07847 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-09 10:00 | SELL RANGE_RIDER  | Price: 1.07729 | SL: 1.07809 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-09 11:00 | CLOSE RANGE_RIDER  | Price: 1.07671 | R: +0.53 | Exit: BREAK_EVEN
ðŸ”š 2024-02-09 11:00 | CLOSE RANGE_RIDER  | Price: 1.07671 | R: +0.73 | Exit: BREAK_EVEN
ðŸ“ 2024-02-09 11:00 | SELL RANGE_RIDER  | Price: 1.07671 | SL: 1.07753 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-09 12:00 | SELL RANGE_RIDER  | Price: 1.07667 | SL: 1.07749 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-09 14:00 | CLOSE RANGE_RIDER  | Price: 1.07753 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-09 14:00 | CLOSE RANGE_RIDER  | Price: 1.07749 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-09 14:00 | SELL RANGE_RIDER  | Price: 1.07673 | SL: 1.07760 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-09 15:00 | CLOSE RANGE_RIDER  | Price: 1.07760 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-09 15:00 | SELL RANGE_RIDER  | Price: 1.07831 | SL: 1.07933 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-09 16:00 | CLOSE RANGE_RIDER  | Price: 1.07933 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-09 16:00 | SELL RANGE_RIDER  | Price: 1.07818 | SL: 1.07927 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-09 17:00 | SELL RANGE_RIDER  | Price: 1.07864 | SL: 1.07972 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-12 00:00 | CLOSE RANGE_RIDER  | Price: 1.07859 | R: -0.38 | Exit: MAX_HOLD_TIME
ðŸ”š 2024-02-12 00:00 | CLOSE RANGE_RIDER  | Price: 1.07859 | R: +0.05 | Exit: MAX_HOLD_TIME
ðŸ“ 2024-02-12 00:00 | SELL RANGE_RIDER  | Price: 1.07859 | SL: 1.07950 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-12 01:00 | CLOSE RANGE_RIDER  | Price: 1.07950 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-12 01:00 | SELL RANGE_RIDER  | Price: 1.07979 | SL: 1.08073 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-02-12 02:00 | SELL RANGE_RIDER  | Price: 1.07988 | SL: 1.08078 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-12 05:00 | CLOSE RANGE_RIDER  | Price: 1.07919 | R: +0.64 | Exit: BREAK_EVEN
ðŸ”š 2024-02-12 05:00 | CLOSE RANGE_RIDER  | Price: 1.07919 | R: +0.77 | Exit: BREAK_EVEN
ðŸ“ 2024-02-12 05:00 | SELL RANGE_RIDER  | Price: 1.07919 | SL: 1.08001 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-02-12 06:00 | SELL RANGE_RIDER  | Price: 1.07906 | SL: 1.07986 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-12 09:00 | CLOSE RANGE_RIDER  | Price: 1.08001 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-12 09:00 | CLOSE RANGE_RIDER  | Price: 1.07986 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-12 09:00 | SELL RANGE_RIDER  | Price: 1.08033 | SL: 1.08113 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-12 10:00 | CLOSE RANGE_RIDER  | Price: 1.07755 | R: +3.46 | Exit: BREAK_EVEN
ðŸ“ 2024-02-12 10:00 | SELL RANGE_RIDER  | Price: 1.07755 | SL: 1.07850 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-12 11:00 | CLOSE RANGE_RIDER  | Price: 1.07692 | R: +0.66 | Exit: BREAK_EVEN
ðŸ“ 2024-02-12 11:00 | SELL RANGE_RIDER  | Price: 1.07692 | SL: 1.07788 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-12 12:00 | CLOSE RANGE_RIDER  | Price: 1.07788 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-12 12:00 | SELL RANGE_RIDER  | Price: 1.07768 | SL: 1.07866 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-12 13:00 | CLOSE RANGE_RIDER  | Price: 1.07695 | R: +0.74 | Exit: BREAK_EVEN
ðŸ“ 2024-02-12 13:00 | SELL RANGE_RIDER  | Price: 1.07695 | SL: 1.07797 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-12 14:00 | SELL RANGE_RIDER  | Price: 1.07699 | SL: 1.07799 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-12 15:00 | CLOSE RANGE_RIDER  | Price: 1.07639 | R: +0.55 | Exit: BREAK_EVEN
ðŸ”š 2024-02-12 15:00 | CLOSE RANGE_RIDER  | Price: 1.07639 | R: +0.60 | Exit: BREAK_EVEN
ðŸ“ 2024-02-12 15:00 | SELL RANGE_RIDER  | Price: 1.07639 | SL: 1.07741 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-12 16:00 | CLOSE RANGE_RIDER  | Price: 1.07741 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-12 16:00 | SELL RANGE_RIDER  | Price: 1.07722 | SL: 1.07825 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-12 17:00 | SELL RANGE_RIDER  | Price: 1.07675 | SL: 1.07782 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-12 19:00 | CLOSE RANGE_RIDER  | Price: 1.07825 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-12 19:00 | CLOSE RANGE_RIDER  | Price: 1.07782 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-12 19:00 | SELL RANGE_RIDER  | Price: 1.07824 | SL: 1.07931 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-12 20:00 | SELL RANGE_RIDER  | Price: 1.07813 | SL: 1.07917 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-12 21:00 | CLOSE RANGE_RIDER  | Price: 1.07695 | R: +1.20 | Exit: BREAK_EVEN
ðŸ”š 2024-02-12 21:00 | CLOSE RANGE_RIDER  | Price: 1.07695 | R: +1.14 | Exit: BREAK_EVEN
ðŸ“ 2024-02-12 21:00 | SELL RANGE_RIDER  | Price: 1.07695 | SL: 1.07802 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-12 22:00 | SELL RANGE_RIDER  | Price: 1.07743 | SL: 1.07846 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-13 03:00 | CLOSE RANGE_RIDER  | Price: 1.07669 | R: +0.72 | Exit: BREAK_EVEN
ðŸ“ 2024-02-13 03:00 | SELL RANGE_RIDER  | Price: 1.07669 | SL: 1.07758 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-13 05:00 | CLOSE RANGE_RIDER  | Price: 1.07618 | R: +0.72 | Exit: BREAK_EVEN
ðŸ”š 2024-02-13 05:00 | CLOSE RANGE_RIDER  | Price: 1.07618 | R: +0.57 | Exit: BREAK_EVEN
ðŸ“ 2024-02-13 05:00 | SELL RANGE_RIDER  | Price: 1.07618 | SL: 1.07701 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-02-13 06:00 | SELL RANGE_RIDER  | Price: 1.07638 | SL: 1.07717 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-13 08:00 | CLOSE RANGE_RIDER  | Price: 1.07701 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-13 08:00 | CLOSE RANGE_RIDER  | Price: 1.07717 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-13 08:00 | SELL RANGE_RIDER  | Price: 1.07705 | SL: 1.07781 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-02-13 09:00 | SELL RANGE_RIDER  | Price: 1.07714 | SL: 1.07793 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-13 11:00 | CLOSE RANGE_RIDER  | Price: 1.07668 | R: +0.58 | Exit: BREAK_EVEN
ðŸ“ 2024-02-13 11:00 | SELL RANGE_RIDER  | Price: 1.07668 | SL: 1.07753 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-13 12:00 | CLOSE RANGE_RIDER  | Price: 1.07753 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-13 12:00 | SELL RANGE_RIDER  | Price: 1.07723 | SL: 1.07809 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-13 13:00 | CLOSE RANGE_RIDER  | Price: 1.07781 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-13 13:00 | CLOSE RANGE_RIDER  | Price: 1.07809 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-13 13:00 | SELL RANGE_RIDER  | Price: 1.07779 | SL: 1.07866 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-13 14:00 | CLOSE RANGE_RIDER  | Price: 1.07866 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-13 14:00 | SELL RANGE_RIDER  | Price: 1.07857 | SL: 1.07945 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-13 15:00 | CLOSE RANGE_RIDER  | Price: 1.07945 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-13 15:00 | SELL RANGE_RIDER  | Price: 1.07086 | SL: 1.07236 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-13 16:00 | CLOSE RANGE_RIDER  | Price: 1.07236 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-13 16:00 | SELL RANGE_RIDER  | Price: 1.07181 | SL: 1.07337 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-02-13 17:00 | SELL RANGE_RIDER  | Price: 1.07169 | SL: 1.07329 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-13 20:00 | CLOSE RANGE_RIDER  | Price: 1.07083 | R: +0.63 | Exit: BREAK_EVEN
ðŸ”š 2024-02-13 20:00 | CLOSE RANGE_RIDER  | Price: 1.07083 | R: +0.54 | Exit: BREAK_EVEN
ðŸ“ 2024-02-13 20:00 | SELL RANGE_RIDER  | Price: 1.07083 | SL: 1.07231 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-02-13 21:00 | SELL RANGE_RIDER  | Price: 1.07014 | SL: 1.07157 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-14 08:00 | CLOSE RANGE_RIDER  | Price: 1.07157 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-14 08:00 | SELL RANGE_RIDER  | Price: 1.07165 | SL: 1.07259 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-14 09:00 | CLOSE RANGE_RIDER  | Price: 1.07077 | R: +0.93 | Exit: BREAK_EVEN
ðŸ“ 2024-02-14 09:00 | SELL RANGE_RIDER  | Price: 1.07077 | SL: 1.07173 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-14 10:00 | CLOSE RANGE_RIDER  | Price: 1.07023 | R: +0.56 | Exit: BREAK_EVEN
ðŸ“ 2024-02-14 10:00 | SELL RANGE_RIDER  | Price: 1.07023 | SL: 1.07122 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-14 11:00 | CLOSE RANGE_RIDER  | Price: 1.07001 | R: +0.55 | Exit: BREAK_EVEN
ðŸ“ 2024-02-14 11:00 | SELL RANGE_RIDER  | Price: 1.07001 | SL: 1.07100 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-14 13:00 | CLOSE RANGE_RIDER  | Price: 1.07100 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-14 13:00 | SELL RANGE_RIDER  | Price: 1.07080 | SL: 1.07180 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-14 15:00 | CLOSE RANGE_RIDER  | Price: 1.07122 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-14 15:00 | SELL RANGE_RIDER  | Price: 1.07087 | SL: 1.07187 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-14 16:00 | CLOSE RANGE_RIDER  | Price: 1.07180 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-14 16:00 | CLOSE RANGE_RIDER  | Price: 1.07187 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-14 16:00 | SELL RANGE_RIDER  | Price: 1.07162 | SL: 1.07267 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-14 17:00 | SELL RANGE_RIDER  | Price: 1.07213 | SL: 1.07319 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-14 18:00 | CLOSE RANGE_RIDER  | Price: 1.07267 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-14 18:00 | CLOSE RANGE_RIDER  | Price: 1.07319 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-14 18:00 | SELL RANGE_RIDER  | Price: 1.07339 | SL: 1.07448 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-14 19:00 | SELL RANGE_RIDER  | Price: 1.07307 | SL: 1.07413 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-14 20:00 | CLOSE RANGE_RIDER  | Price: 1.07270 | R: +0.63 | Exit: BREAK_EVEN
ðŸ“ 2024-02-14 20:00 | SELL RANGE_RIDER  | Price: 1.07270 | SL: 1.07374 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-15 09:00 | CLOSE RANGE_RIDER  | Price: 1.07413 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-15 09:00 | CLOSE RANGE_RIDER  | Price: 1.07374 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-15 09:00 | SELL RANGE_RIDER  | Price: 1.07331 | SL: 1.07409 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-02-15 10:00 | SELL RANGE_RIDER  | Price: 1.07309 | SL: 1.07387 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-15 13:00 | CLOSE RANGE_RIDER  | Price: 1.07387 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-15 13:00 | SELL RANGE_RIDER  | Price: 1.07355 | SL: 1.07432 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-15 14:00 | CLOSE RANGE_RIDER  | Price: 1.07409 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-15 14:00 | CLOSE RANGE_RIDER  | Price: 1.07432 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-15 14:00 | SELL RANGE_RIDER  | Price: 1.07450 | SL: 1.07531 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-15 15:00 | CLOSE RANGE_RIDER  | Price: 1.07531 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-16 00:00 | SELL RANGE_RIDER  | Price: 1.07731 | SL: 1.07823 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-16 01:00 | SELL RANGE_RIDER  | Price: 1.07728 | SL: 1.07817 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-16 02:00 | CLOSE RANGE_RIDER  | Price: 1.07649 | R: +0.89 | Exit: BREAK_EVEN
ðŸ”š 2024-02-16 02:00 | CLOSE RANGE_RIDER  | Price: 1.07649 | R: +0.89 | Exit: BREAK_EVEN
ðŸ“ 2024-02-16 02:00 | SELL RANGE_RIDER  | Price: 1.07649 | SL: 1.07740 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-16 03:00 | SELL RANGE_RIDER  | Price: 1.07650 | SL: 1.07738 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-16 04:00 | CLOSE RANGE_RIDER  | Price: 1.07605 | R: +0.51 | Exit: BREAK_EVEN
ðŸ“ 2024-02-16 04:00 | SELL RANGE_RIDER  | Price: 1.07605 | SL: 1.07691 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-16 05:00 | CLOSE RANGE_RIDER  | Price: 1.07600 | R: +0.54 | Exit: BREAK_EVEN
ðŸ“ 2024-02-16 05:00 | SELL RANGE_RIDER  | Price: 1.07600 | SL: 1.07682 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-16 10:00 | CLOSE RANGE_RIDER  | Price: 1.07691 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-16 10:00 | CLOSE RANGE_RIDER  | Price: 1.07682 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-16 10:00 | SELL RANGE_RIDER  | Price: 1.07699 | SL: 1.07776 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-16 11:00 | SELL RANGE_RIDER  | Price: 1.07662 | SL: 1.07739 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-16 13:00 | CLOSE RANGE_RIDER  | Price: 1.07776 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-16 13:00 | CLOSE RANGE_RIDER  | Price: 1.07739 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-16 13:00 | SELL RANGE_RIDER  | Price: 1.07776 | SL: 1.07857 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-16 14:00 | CLOSE RANGE_RIDER  | Price: 1.07681 | R: +1.17 | Exit: BREAK_EVEN
ðŸ“ 2024-02-16 14:00 | SELL RANGE_RIDER  | Price: 1.07681 | SL: 1.07764 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-16 15:00 | CLOSE RANGE_RIDER  | Price: 1.07467 | R: +2.58 | Exit: BREAK_EVEN
ðŸ“ 2024-02-16 15:00 | SELL RANGE_RIDER  | Price: 1.07467 | SL: 1.07572 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-16 16:00 | SELL RANGE_RIDER  | Price: 1.07499 | SL: 1.07608 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-16 17:00 | CLOSE RANGE_RIDER  | Price: 1.07572 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-16 17:00 | CLOSE RANGE_RIDER  | Price: 1.07608 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-16 17:00 | SELL RANGE_RIDER  | Price: 1.07709 | SL: 1.07830 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-16 18:00 | SELL RANGE_RIDER  | Price: 1.07685 | SL: 1.07805 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-16 20:00 | CLOSE RANGE_RIDER  | Price: 1.07830 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-16 20:00 | CLOSE RANGE_RIDER  | Price: 1.07805 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-16 20:00 | SELL RANGE_RIDER  | Price: 1.07851 | SL: 1.07973 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-16 21:00 | CLOSE RANGE_RIDER  | Price: 1.07771 | R: +0.66 | Exit: BREAK_EVEN
ðŸ“ 2024-02-16 21:00 | SELL RANGE_RIDER  | Price: 1.07771 | SL: 1.07893 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-16 22:00 | SELL RANGE_RIDER  | Price: 1.07766 | SL: 1.07882 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-19 00:00 | CLOSE RANGE_RIDER  | Price: 1.07757 | R: +0.11 | Exit: MAX_HOLD_TIME
ðŸ”š 2024-02-19 00:00 | CLOSE RANGE_RIDER  | Price: 1.07757 | R: +0.08 | Exit: MAX_HOLD_TIME
ðŸ“ 2024-02-19 00:00 | SELL RANGE_RIDER  | Price: 1.07757 | SL: 1.07862 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-02-19 01:00 | SELL RANGE_RIDER  | Price: 1.07841 | SL: 1.07946 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-19 02:00 | CLOSE RANGE_RIDER  | Price: 1.07862 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-19 02:00 | SELL RANGE_RIDER  | Price: 1.07869 | SL: 1.07970 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-19 03:00 | CLOSE RANGE_RIDER  | Price: 1.07805 | R: +0.63 | Exit: BREAK_EVEN
ðŸ“ 2024-02-19 03:00 | SELL RANGE_RIDER  | Price: 1.07805 | SL: 1.07906 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-19 05:00 | CLOSE RANGE_RIDER  | Price: 1.07756 | R: +0.81 | Exit: BREAK_EVEN
ðŸ“ 2024-02-19 05:00 | SELL RANGE_RIDER  | Price: 1.07756 | SL: 1.07852 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-19 08:00 | CLOSE RANGE_RIDER  | Price: 1.07852 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-19 08:00 | SELL RANGE_RIDER  | Price: 1.07864 | SL: 1.07954 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-19 10:00 | CLOSE RANGE_RIDER  | Price: 1.07784 | R: +0.89 | Exit: BREAK_EVEN
ðŸ“ 2024-02-19 10:00 | SELL RANGE_RIDER  | Price: 1.07784 | SL: 1.07875 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-19 11:00 | CLOSE RANGE_RIDER  | Price: 1.07749 | R: +0.55 | Exit: BREAK_EVEN
ðŸ“ 2024-02-19 11:00 | SELL RANGE_RIDER  | Price: 1.07749 | SL: 1.07841 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-19 14:00 | CLOSE RANGE_RIDER  | Price: 1.07705 | R: +0.87 | Exit: BREAK_EVEN
ðŸ“ 2024-02-19 14:00 | SELL RANGE_RIDER  | Price: 1.07705 | SL: 1.07796 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-19 16:00 | CLOSE RANGE_RIDER  | Price: 1.07666 | R: +0.90 | Exit: BREAK_EVEN
ðŸ“ 2024-02-19 16:00 | SELL RANGE_RIDER  | Price: 1.07666 | SL: 1.07757 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-19 19:00 | CLOSE RANGE_RIDER  | Price: 1.07757 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-19 19:00 | SELL RANGE_RIDER  | Price: 1.07763 | SL: 1.07851 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-19 20:00 | CLOSE RANGE_RIDER  | Price: 1.07796 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-19 20:00 | SELL RANGE_RIDER  | Price: 1.07791 | SL: 1.07878 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-20 02:00 | CLOSE RANGE_RIDER  | Price: 1.07697 | R: +0.75 | Exit: BREAK_EVEN
ðŸ”š 2024-02-20 02:00 | CLOSE RANGE_RIDER  | Price: 1.07697 | R: +1.08 | Exit: BREAK_EVEN
ðŸ“ 2024-02-20 02:00 | SELL RANGE_RIDER  | Price: 1.07697 | SL: 1.07773 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-20 03:00 | SELL RANGE_RIDER  | Price: 1.07660 | SL: 1.07735 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-20 09:00 | CLOSE RANGE_RIDER  | Price: 1.07735 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-20 09:00 | SELL RANGE_RIDER  | Price: 1.07698 | SL: 1.07765 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-20 10:00 | CLOSE RANGE_RIDER  | Price: 1.07773 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-20 10:00 | CLOSE RANGE_RIDER  | Price: 1.07765 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-20 10:00 | SELL RANGE_RIDER  | Price: 1.07759 | SL: 1.07827 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-20 11:00 | CLOSE RANGE_RIDER  | Price: 1.07827 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-20 11:00 | SELL RANGE_RIDER  | Price: 1.07980 | SL: 1.08061 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-20 12:00 | CLOSE RANGE_RIDER  | Price: 1.08061 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-20 12:00 | SELL RANGE_RIDER  | Price: 1.08040 | SL: 1.08126 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-20 13:00 | CLOSE RANGE_RIDER  | Price: 1.07984 | R: +0.65 | Exit: BREAK_EVEN
ðŸ“ 2024-02-20 13:00 | SELL RANGE_RIDER  | Price: 1.07984 | SL: 1.08071 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-20 14:00 | SELL RANGE_RIDER  | Price: 1.07982 | SL: 1.08070 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-20 15:00 | CLOSE RANGE_RIDER  | Price: 1.08071 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-20 15:00 | CLOSE RANGE_RIDER  | Price: 1.08070 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-20 15:00 | SELL RANGE_RIDER  | Price: 1.08235 | SL: 1.08337 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-20 16:00 | CLOSE RANGE_RIDER  | Price: 1.08337 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-20 16:00 | SELL RANGE_RIDER  | Price: 1.08293 | SL: 1.08403 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-20 17:00 | CLOSE RANGE_RIDER  | Price: 1.08228 | R: +0.59 | Exit: BREAK_EVEN
ðŸ“ 2024-02-20 17:00 | SELL RANGE_RIDER  | Price: 1.08228 | SL: 1.08342 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-20 18:00 | CLOSE RANGE_RIDER  | Price: 1.08130 | R: +0.86 | Exit: BREAK_EVEN
ðŸ“ 2024-02-20 18:00 | SELL RANGE_RIDER  | Price: 1.08130 | SL: 1.08244 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-20 19:00 | SELL RANGE_RIDER  | Price: 1.08119 | SL: 1.08229 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-20 21:00 | CLOSE RANGE_RIDER  | Price: 1.08064 | R: +0.58 | Exit: BREAK_EVEN
ðŸ“ 2024-02-20 21:00 | SELL RANGE_RIDER  | Price: 1.08064 | SL: 1.08167 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-21 04:00 | CLOSE RANGE_RIDER  | Price: 1.08167 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-21 04:00 | SELL RANGE_RIDER  | Price: 1.08152 | SL: 1.08234 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-21 09:00 | CLOSE RANGE_RIDER  | Price: 1.08109 | R: +0.53 | Exit: BREAK_EVEN
ðŸ“ 2024-02-21 09:00 | SELL RANGE_RIDER  | Price: 1.08109 | SL: 1.08185 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-21 10:00 | CLOSE RANGE_RIDER  | Price: 1.07989 | R: +1.18 | Exit: BREAK_EVEN
ðŸ”š 2024-02-21 10:00 | CLOSE RANGE_RIDER  | Price: 1.07989 | R: +1.58 | Exit: BREAK_EVEN
ðŸ“ 2024-02-21 10:00 | SELL RANGE_RIDER  | Price: 1.07989 | SL: 1.08072 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-21 11:00 | SELL RANGE_RIDER  | Price: 1.07999 | SL: 1.08083 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-21 15:00 | CLOSE RANGE_RIDER  | Price: 1.08072 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-21 15:00 | CLOSE RANGE_RIDER  | Price: 1.08083 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-21 15:00 | SELL RANGE_RIDER  | Price: 1.08102 | SL: 1.08184 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-02-21 16:00 | SELL RANGE_RIDER  | Price: 1.08132 | SL: 1.08216 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-21 17:00 | CLOSE RANGE_RIDER  | Price: 1.08184 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-21 17:00 | CLOSE RANGE_RIDER  | Price: 1.08053 | R: +0.94 | Exit: BREAK_EVEN
ðŸ“ 2024-02-21 17:00 | SELL RANGE_RIDER  | Price: 1.08053 | SL: 1.08142 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-21 18:00 | CLOSE RANGE_RIDER  | Price: 1.08142 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-21 18:00 | SELL RANGE_RIDER  | Price: 1.08171 | SL: 1.08266 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-21 19:00 | CLOSE RANGE_RIDER  | Price: 1.08077 | R: +0.99 | Exit: BREAK_EVEN
ðŸ“ 2024-02-21 19:00 | SELL RANGE_RIDER  | Price: 1.08077 | SL: 1.08173 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-02-21 20:00 | SELL RANGE_RIDER  | Price: 1.08120 | SL: 1.08219 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-21 21:00 | CLOSE RANGE_RIDER  | Price: 1.08173 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-21 21:00 | CLOSE RANGE_RIDER  | Price: 1.08219 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-21 21:00 | SELL RANGE_RIDER  | Price: 1.08166 | SL: 1.08272 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-02-21 22:00 | SELL RANGE_RIDER  | Price: 1.08173 | SL: 1.08277 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-22 02:00 | CLOSE RANGE_RIDER  | Price: 1.08272 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-22 02:00 | CLOSE RANGE_RIDER  | Price: 1.08277 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-22 02:00 | SELL RANGE_RIDER  | Price: 1.08302 | SL: 1.08398 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-02-22 03:00 | SELL RANGE_RIDER  | Price: 1.08267 | SL: 1.08359 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-22 07:00 | CLOSE RANGE_RIDER  | Price: 1.08359 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-22 07:00 | SELL RANGE_RIDER  | Price: 1.08334 | SL: 1.08419 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-22 08:00 | CLOSE RANGE_RIDER  | Price: 1.08398 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-22 08:00 | SELL RANGE_RIDER  | Price: 1.08386 | SL: 1.08470 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-22 09:00 | CLOSE RANGE_RIDER  | Price: 1.08419 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-22 09:00 | CLOSE RANGE_RIDER  | Price: 1.08470 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-23 00:00 | SELL RANGE_RIDER  | Price: 1.08229 | SL: 1.08341 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-23 01:00 | SELL RANGE_RIDER  | Price: 1.08255 | SL: 1.08362 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-23 11:00 | CLOSE RANGE_RIDER  | Price: 1.08175 | R: +0.75 | Exit: BREAK_EVEN
ðŸ“ 2024-02-23 11:00 | SELL RANGE_RIDER  | Price: 1.08175 | SL: 1.08268 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-23 13:00 | CLOSE RANGE_RIDER  | Price: 1.08268 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-23 13:00 | SELL RANGE_RIDER  | Price: 1.08271 | SL: 1.08363 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-23 14:00 | CLOSE RANGE_RIDER  | Price: 1.08341 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-23 14:00 | CLOSE RANGE_RIDER  | Price: 1.08363 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-23 14:00 | SELL RANGE_RIDER  | Price: 1.08362 | SL: 1.08458 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-23 15:00 | SELL RANGE_RIDER  | Price: 1.08320 | SL: 1.08416 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-23 16:00 | CLOSE RANGE_RIDER  | Price: 1.08255 | R: +1.12 | Exit: BREAK_EVEN
ðŸ”š 2024-02-23 16:00 | CLOSE RANGE_RIDER  | Price: 1.08255 | R: +0.68 | Exit: BREAK_EVEN
ðŸ“ 2024-02-23 16:00 | SELL RANGE_RIDER  | Price: 1.08255 | SL: 1.08353 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-23 17:00 | SELL RANGE_RIDER  | Price: 1.08207 | SL: 1.08308 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-26 00:00 | CLOSE RANGE_RIDER  | Price: 1.08242 | R: +0.13 | Exit: MAX_HOLD_TIME
ðŸ”š 2024-02-26 00:00 | CLOSE RANGE_RIDER  | Price: 1.08308 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-26 00:00 | SELL RANGE_RIDER  | Price: 1.08242 | SL: 1.08334 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-26 01:00 | CLOSE RANGE_RIDER  | Price: 1.08191 | R: +0.55 | Exit: BREAK_EVEN
ðŸ“ 2024-02-26 01:00 | SELL RANGE_RIDER  | Price: 1.08191 | SL: 1.08280 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-26 02:00 | SELL RANGE_RIDER  | Price: 1.08167 | SL: 1.08253 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-26 08:00 | CLOSE RANGE_RIDER  | Price: 1.08253 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-26 08:00 | SELL RANGE_RIDER  | Price: 1.08241 | SL: 1.08313 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-26 09:00 | CLOSE RANGE_RIDER  | Price: 1.08280 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-26 09:00 | CLOSE RANGE_RIDER  | Price: 1.08313 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-26 09:00 | SELL RANGE_RIDER  | Price: 1.08322 | SL: 1.08399 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-26 10:00 | SELL RANGE_RIDER  | Price: 1.08322 | SL: 1.08399 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-26 11:00 | CLOSE RANGE_RIDER  | Price: 1.08399 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-26 11:00 | CLOSE RANGE_RIDER  | Price: 1.08399 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-26 11:00 | SELL RANGE_RIDER  | Price: 1.08401 | SL: 1.08480 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-26 12:00 | CLOSE RANGE_RIDER  | Price: 1.08480 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-27 00:00 | SELL RANGE_RIDER  | Price: 1.08505 | SL: 1.08583 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-02-27 01:00 | SELL RANGE_RIDER  | Price: 1.08504 | SL: 1.08579 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-27 09:00 | CLOSE RANGE_RIDER  | Price: 1.08583 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-27 09:00 | CLOSE RANGE_RIDER  | Price: 1.08579 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-27 09:00 | SELL RANGE_RIDER  | Price: 1.08560 | SL: 1.08629 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-27 10:00 | CLOSE RANGE_RIDER  | Price: 1.08629 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-27 10:00 | SELL RANGE_RIDER  | Price: 1.08576 | SL: 1.08649 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-27 11:00 | CLOSE RANGE_RIDER  | Price: 1.08530 | R: +0.63 | Exit: BREAK_EVEN
ðŸ“ 2024-02-27 11:00 | SELL RANGE_RIDER  | Price: 1.08530 | SL: 1.08603 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-02-27 12:00 | SELL RANGE_RIDER  | Price: 1.08517 | SL: 1.08593 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-27 14:00 | CLOSE RANGE_RIDER  | Price: 1.08603 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-27 14:00 | CLOSE RANGE_RIDER  | Price: 1.08593 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-27 14:00 | SELL RANGE_RIDER  | Price: 1.08568 | SL: 1.08646 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-27 15:00 | CLOSE RANGE_RIDER  | Price: 1.08481 | R: +1.11 | Exit: BREAK_EVEN
ðŸ“ 2024-02-27 15:00 | SELL RANGE_RIDER  | Price: 1.08481 | SL: 1.08563 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-27 16:00 | CLOSE RANGE_RIDER  | Price: 1.08403 | R: +0.95 | Exit: BREAK_EVEN
ðŸ“ 2024-02-27 16:00 | SELL RANGE_RIDER  | Price: 1.08403 | SL: 1.08490 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-27 17:00 | CLOSE RANGE_RIDER  | Price: 1.08490 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-27 17:00 | SELL RANGE_RIDER  | Price: 1.08469 | SL: 1.08563 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-27 18:00 | CLOSE RANGE_RIDER  | Price: 1.08563 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-27 18:00 | SELL RANGE_RIDER  | Price: 1.08561 | SL: 1.08657 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-27 19:00 | CLOSE RANGE_RIDER  | Price: 1.08509 | R: +0.54 | Exit: BREAK_EVEN
ðŸ“ 2024-02-27 19:00 | SELL RANGE_RIDER  | Price: 1.08509 | SL: 1.08604 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-27 20:00 | SELL RANGE_RIDER  | Price: 1.08496 | SL: 1.08590 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-27 21:00 | CLOSE RANGE_RIDER  | Price: 1.08443 | R: +0.70 | Exit: BREAK_EVEN
ðŸ”š 2024-02-27 21:00 | CLOSE RANGE_RIDER  | Price: 1.08443 | R: +0.57 | Exit: BREAK_EVEN
ðŸ“ 2024-02-27 21:00 | SELL RANGE_RIDER  | Price: 1.08443 | SL: 1.08536 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-27 22:00 | SELL RANGE_RIDER  | Price: 1.08442 | SL: 1.08533 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-28 03:00 | CLOSE RANGE_RIDER  | Price: 1.08396 | R: +0.50 | Exit: BREAK_EVEN
ðŸ”š 2024-02-28 03:00 | CLOSE RANGE_RIDER  | Price: 1.08396 | R: +0.51 | Exit: BREAK_EVEN
ðŸ“ 2024-02-28 03:00 | SELL RANGE_RIDER  | Price: 1.08396 | SL: 1.08472 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-28 04:00 | SELL RANGE_RIDER  | Price: 1.08376 | SL: 1.08449 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-28 05:00 | CLOSE RANGE_RIDER  | Price: 1.08344 | R: +0.68 | Exit: BREAK_EVEN
ðŸ“ 2024-02-28 05:00 | SELL RANGE_RIDER  | Price: 1.08344 | SL: 1.08416 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-28 06:00 | CLOSE RANGE_RIDER  | Price: 1.08322 | R: +0.74 | Exit: BREAK_EVEN
ðŸ“ 2024-02-28 06:00 | SELL RANGE_RIDER  | Price: 1.08322 | SL: 1.08391 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-28 07:00 | CLOSE RANGE_RIDER  | Price: 1.08267 | R: +1.07 | Exit: BREAK_EVEN
ðŸ”š 2024-02-28 07:00 | CLOSE RANGE_RIDER  | Price: 1.08267 | R: +0.79 | Exit: BREAK_EVEN
ðŸ“ 2024-02-28 07:00 | SELL RANGE_RIDER  | Price: 1.08267 | SL: 1.08337 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-02-28 08:00 | CLOSE RANGE_RIDER  | Price: 1.08224 | R: +0.61 | Exit: BREAK_EVEN
ðŸ“ 2024-02-28 08:00 | SELL RANGE_RIDER  | Price: 1.08224 | SL: 1.08294 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-02-28 09:00 | SELL RANGE_RIDER  | Price: 1.08234 | SL: 1.08305 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-28 10:00 | CLOSE RANGE_RIDER  | Price: 1.08090 | R: +1.91 | Exit: BREAK_EVEN
ðŸ”š 2024-02-28 10:00 | CLOSE RANGE_RIDER  | Price: 1.08090 | R: +2.02 | Exit: BREAK_EVEN
ðŸ“ 2024-02-28 10:00 | SELL RANGE_RIDER  | Price: 1.08090 | SL: 1.08167 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-28 11:00 | CLOSE RANGE_RIDER  | Price: 1.08000 | R: +1.16 | Exit: BREAK_EVEN
ðŸ“ 2024-02-28 11:00 | SELL RANGE_RIDER  | Price: 1.08000 | SL: 1.08083 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-28 12:00 | CLOSE RANGE_RIDER  | Price: 1.08083 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-28 12:00 | SELL RANGE_RIDER  | Price: 1.08156 | SL: 1.08246 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-28 13:00 | SELL RANGE_RIDER  | Price: 1.08156 | SL: 1.08245 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-28 14:00 | CLOSE RANGE_RIDER  | Price: 1.08088 | R: +0.75 | Exit: BREAK_EVEN
ðŸ”š 2024-02-28 14:00 | CLOSE RANGE_RIDER  | Price: 1.08088 | R: +0.76 | Exit: BREAK_EVEN
ðŸ“ 2024-02-28 14:00 | SELL RANGE_RIDER  | Price: 1.08088 | SL: 1.08180 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-28 15:00 | CLOSE RANGE_RIDER  | Price: 1.08180 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-28 15:00 | SELL RANGE_RIDER  | Price: 1.08278 | SL: 1.08381 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-28 16:00 | SELL RANGE_RIDER  | Price: 1.08300 | SL: 1.08405 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-28 18:00 | CLOSE RANGE_RIDER  | Price: 1.08381 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-02-28 18:00 | CLOSE RANGE_RIDER  | Price: 1.08405 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-28 18:00 | SELL RANGE_RIDER  | Price: 1.08422 | SL: 1.08528 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-02-28 19:00 | SELL RANGE_RIDER  | Price: 1.08384 | SL: 1.08491 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-02-28 20:00 | CLOSE RANGE_RIDER  | Price: 1.08344 | R: +0.73 | Exit: BREAK_EVEN
ðŸ“ 2024-02-28 20:00 | SELL RANGE_RIDER  | Price: 1.08344 | SL: 1.08449 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-02-29 03:00 | CLOSE RANGE_RIDER  | Price: 1.08292 | R: +0.86 | Exit: BREAK_EVEN
ðŸ“ 2024-02-29 03:00 | SELL RANGE_RIDER  | Price: 1.08292 | SL: 1.08379 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-29 05:00 | CLOSE RANGE_RIDER  | Price: 1.08379 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-29 05:00 | SELL RANGE_RIDER  | Price: 1.08370 | SL: 1.08453 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-29 09:00 | CLOSE RANGE_RIDER  | Price: 1.08288 | R: +0.53 | Exit: BREAK_EVEN
ðŸ”š 2024-02-29 09:00 | CLOSE RANGE_RIDER  | Price: 1.08288 | R: +0.98 | Exit: BREAK_EVEN
ðŸ“ 2024-02-29 09:00 | SELL RANGE_RIDER  | Price: 1.08288 | SL: 1.08369 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-29 10:00 | CLOSE RANGE_RIDER  | Price: 1.08369 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-29 10:00 | SELL RANGE_RIDER  | Price: 1.08376 | SL: 1.08465 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-29 11:00 | CLOSE RANGE_RIDER  | Price: 1.08465 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-29 11:00 | SELL RANGE_RIDER  | Price: 1.08506 | SL: 1.08599 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-29 12:00 | CLOSE RANGE_RIDER  | Price: 1.08378 | R: +1.38 | Exit: BREAK_EVEN
ðŸ“ 2024-02-29 12:00 | SELL RANGE_RIDER  | Price: 1.08378 | SL: 1.08476 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-29 13:00 | SELL RANGE_RIDER  | Price: 1.08343 | SL: 1.08444 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-29 14:00 | CLOSE RANGE_RIDER  | Price: 1.08289 | R: +0.91 | Exit: BREAK_EVEN
ðŸ”š 2024-02-29 14:00 | CLOSE RANGE_RIDER  | Price: 1.08289 | R: +0.53 | Exit: BREAK_EVEN
ðŸ“ 2024-02-29 14:00 | SELL RANGE_RIDER  | Price: 1.08289 | SL: 1.08390 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-29 15:00 | CLOSE RANGE_RIDER  | Price: 1.08390 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-29 15:00 | SELL RANGE_RIDER  | Price: 1.08379 | SL: 1.08490 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-29 16:00 | CLOSE RANGE_RIDER  | Price: 1.08490 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-02-29 16:00 | SELL RANGE_RIDER  | Price: 1.08467 | SL: 1.08580 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-29 17:00 | CLOSE RANGE_RIDER  | Price: 1.08226 | R: +2.12 | Exit: BREAK_EVEN
ðŸ“ 2024-02-29 17:00 | SELL RANGE_RIDER  | Price: 1.08226 | SL: 1.08358 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-02-29 18:00 | CLOSE RANGE_RIDER  | Price: 1.08063 | R: +1.24 | Exit: BREAK_EVEN
ðŸ“ 2024-02-29 18:00 | SELL RANGE_RIDER  | Price: 1.08063 | SL: 1.08200 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-02-29 19:00 | SELL RANGE_RIDER  | Price: 1.08000 | SL: 1.08135 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-01 03:00 | CLOSE RANGE_RIDER  | Price: 1.08200 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-01 03:00 | CLOSE RANGE_RIDER  | Price: 1.08135 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-01 03:00 | SELL RANGE_RIDER  | Price: 1.08213 | SL: 1.08321 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-01 04:00 | SELL RANGE_RIDER  | Price: 1.08184 | SL: 1.08288 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-01 06:00 | CLOSE RANGE_RIDER  | Price: 1.08136 | R: +0.72 | Exit: BREAK_EVEN
ðŸ“ 2024-03-01 06:00 | SELL RANGE_RIDER  | Price: 1.08136 | SL: 1.08232 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-01 07:00 | CLOSE RANGE_RIDER  | Price: 1.08122 | R: +0.60 | Exit: BREAK_EVEN
ðŸ“ 2024-03-01 07:00 | SELL RANGE_RIDER  | Price: 1.08122 | SL: 1.08213 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-01 12:00 | CLOSE RANGE_RIDER  | Price: 1.08213 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-01 12:00 | SELL RANGE_RIDER  | Price: 1.08106 | SL: 1.08207 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-01 14:00 | CLOSE RANGE_RIDER  | Price: 1.08232 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-01 14:00 | CLOSE RANGE_RIDER  | Price: 1.08207 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-01 14:00 | SELL RANGE_RIDER  | Price: 1.08131 | SL: 1.08233 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-01 15:00 | SELL RANGE_RIDER  | Price: 1.08129 | SL: 1.08230 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-01 16:00 | CLOSE RANGE_RIDER  | Price: 1.08004 | R: +1.24 | Exit: BREAK_EVEN
ðŸ”š 2024-03-01 16:00 | CLOSE RANGE_RIDER  | Price: 1.08004 | R: +1.24 | Exit: BREAK_EVEN
ðŸ“ 2024-03-01 16:00 | SELL RANGE_RIDER  | Price: 1.08004 | SL: 1.08113 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-01 17:00 | CLOSE RANGE_RIDER  | Price: 1.08113 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-01 17:00 | SELL RANGE_RIDER  | Price: 1.08351 | SL: 1.08482 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-01 18:00 | SELL RANGE_RIDER  | Price: 1.08309 | SL: 1.08440 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-04 00:00 | CLOSE RANGE_RIDER  | Price: 1.08409 | R: -0.44 | Exit: MAX_HOLD_TIME
ðŸ”š 2024-03-04 00:00 | CLOSE RANGE_RIDER  | Price: 1.08409 | R: -0.76 | Exit: MAX_HOLD_TIME
ðŸ“ 2024-03-04 00:00 | SELL RANGE_RIDER  | Price: 1.08409 | SL: 1.08520 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-04 01:00 | SELL RANGE_RIDER  | Price: 1.08418 | SL: 1.08523 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-04 09:00 | CLOSE RANGE_RIDER  | Price: 1.08520 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-04 09:00 | CLOSE RANGE_RIDER  | Price: 1.08523 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-04 09:00 | SELL RANGE_RIDER  | Price: 1.08538 | SL: 1.08622 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-04 10:00 | CLOSE RANGE_RIDER  | Price: 1.08449 | R: +1.06 | Exit: BREAK_EVEN
ðŸ“ 2024-03-04 10:00 | SELL RANGE_RIDER  | Price: 1.08449 | SL: 1.08541 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-04 11:00 | SELL RANGE_RIDER  | Price: 1.08491 | SL: 1.08584 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-04 12:00 | CLOSE RANGE_RIDER  | Price: 1.08541 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-04 12:00 | SELL RANGE_RIDER  | Price: 1.08536 | SL: 1.08629 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-04 14:00 | CLOSE RANGE_RIDER  | Price: 1.08428 | R: +0.68 | Exit: BREAK_EVEN
ðŸ”š 2024-03-04 14:00 | CLOSE RANGE_RIDER  | Price: 1.08428 | R: +1.17 | Exit: BREAK_EVEN
ðŸ“ 2024-03-04 14:00 | SELL RANGE_RIDER  | Price: 1.08428 | SL: 1.08523 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-04 15:00 | SELL RANGE_RIDER  | Price: 1.08488 | SL: 1.08583 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-04 16:00 | CLOSE RANGE_RIDER  | Price: 1.08523 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-04 16:00 | CLOSE RANGE_RIDER  | Price: 1.08583 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-04 16:00 | SELL RANGE_RIDER  | Price: 1.08598 | SL: 1.08698 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-04 17:00 | SELL RANGE_RIDER  | Price: 1.08633 | SL: 1.08732 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-04 19:00 | CLOSE RANGE_RIDER  | Price: 1.08580 | R: +0.54 | Exit: BREAK_EVEN
ðŸ“ 2024-03-04 19:00 | SELL RANGE_RIDER  | Price: 1.08580 | SL: 1.08677 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-05 00:00 | CLOSE RANGE_RIDER  | Price: 1.08539 | R: +0.59 | Exit: BREAK_EVEN
ðŸ“ 2024-03-05 00:00 | SELL RANGE_RIDER  | Price: 1.08539 | SL: 1.08617 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-05 02:00 | CLOSE RANGE_RIDER  | Price: 1.08531 | R: +0.51 | Exit: BREAK_EVEN
ðŸ“ 2024-03-05 02:00 | SELL RANGE_RIDER  | Price: 1.08531 | SL: 1.08604 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-05 03:00 | CLOSE RANGE_RIDER  | Price: 1.08495 | R: +0.56 | Exit: BREAK_EVEN
ðŸ“ 2024-03-05 03:00 | SELL RANGE_RIDER  | Price: 1.08495 | SL: 1.08568 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-05 08:00 | CLOSE RANGE_RIDER  | Price: 1.08468 | R: +0.86 | Exit: BREAK_EVEN
ðŸ“ 2024-03-05 08:00 | SELL RANGE_RIDER  | Price: 1.08468 | SL: 1.08536 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-05 11:00 | CLOSE RANGE_RIDER  | Price: 1.08536 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-05 11:00 | SELL RANGE_RIDER  | Price: 1.08515 | SL: 1.08587 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-05 14:00 | CLOSE RANGE_RIDER  | Price: 1.08473 | R: +0.58 | Exit: BREAK_EVEN
ðŸ“ 2024-03-05 14:00 | SELL RANGE_RIDER  | Price: 1.08473 | SL: 1.08542 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-05 16:00 | CLOSE RANGE_RIDER  | Price: 1.08455 | R: +0.55 | Exit: BREAK_EVEN
ðŸ”š 2024-03-05 16:00 | CLOSE RANGE_RIDER  | Price: 1.08542 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-05 16:00 | SELL RANGE_RIDER  | Price: 1.08455 | SL: 1.08531 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-05 17:00 | CLOSE RANGE_RIDER  | Price: 1.08531 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-05 17:00 | SELL RANGE_RIDER  | Price: 1.08714 | SL: 1.08806 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-05 18:00 | CLOSE RANGE_RIDER  | Price: 1.08611 | R: +1.12 | Exit: BREAK_EVEN
ðŸ“ 2024-03-05 18:00 | SELL RANGE_RIDER  | Price: 1.08611 | SL: 1.08707 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-05 19:00 | SELL RANGE_RIDER  | Price: 1.08600 | SL: 1.08694 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-05 20:00 | CLOSE RANGE_RIDER  | Price: 1.08528 | R: +0.87 | Exit: BREAK_EVEN
ðŸ”š 2024-03-05 20:00 | CLOSE RANGE_RIDER  | Price: 1.08528 | R: +0.77 | Exit: BREAK_EVEN
ðŸ“ 2024-03-05 20:00 | SELL RANGE_RIDER  | Price: 1.08528 | SL: 1.08621 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-05 21:00 | SELL RANGE_RIDER  | Price: 1.08529 | SL: 1.08620 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-06 03:00 | CLOSE RANGE_RIDER  | Price: 1.08440 | R: +0.95 | Exit: BREAK_EVEN
ðŸ”š 2024-03-06 03:00 | CLOSE RANGE_RIDER  | Price: 1.08440 | R: +0.98 | Exit: BREAK_EVEN
ðŸ“ 2024-03-06 03:00 | SELL RANGE_RIDER  | Price: 1.08440 | SL: 1.08519 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-06 04:00 | CLOSE RANGE_RIDER  | Price: 1.08519 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-06 04:00 | SELL RANGE_RIDER  | Price: 1.08527 | SL: 1.08607 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-06 05:00 | SELL RANGE_RIDER  | Price: 1.08508 | SL: 1.08585 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-06 08:00 | CLOSE RANGE_RIDER  | Price: 1.08585 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-06 08:00 | SELL RANGE_RIDER  | Price: 1.08596 | SL: 1.08667 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-06 09:00 | CLOSE RANGE_RIDER  | Price: 1.08607 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-06 09:00 | SELL RANGE_RIDER  | Price: 1.08621 | SL: 1.08692 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-06 10:00 | CLOSE RANGE_RIDER  | Price: 1.08667 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-06 10:00 | CLOSE RANGE_RIDER  | Price: 1.08692 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-06 10:00 | SELL RANGE_RIDER  | Price: 1.08732 | SL: 1.08809 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-06 11:00 | SELL RANGE_RIDER  | Price: 1.08765 | SL: 1.08843 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-06 14:00 | CLOSE RANGE_RIDER  | Price: 1.08688 | R: +0.57 | Exit: BREAK_EVEN
ðŸ”š 2024-03-06 14:00 | CLOSE RANGE_RIDER  | Price: 1.08688 | R: +0.99 | Exit: BREAK_EVEN
ðŸ“ 2024-03-06 14:00 | SELL RANGE_RIDER  | Price: 1.08688 | SL: 1.08766 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-06 15:00 | CLOSE RANGE_RIDER  | Price: 1.08766 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-06 15:00 | SELL RANGE_RIDER  | Price: 1.08849 | SL: 1.08934 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-06 16:00 | SELL RANGE_RIDER  | Price: 1.08871 | SL: 1.08954 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-06 17:00 | CLOSE RANGE_RIDER  | Price: 1.08934 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-06 17:00 | CLOSE RANGE_RIDER  | Price: 1.08954 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-06 17:00 | SELL RANGE_RIDER  | Price: 1.09052 | SL: 1.09149 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-06 18:00 | CLOSE RANGE_RIDER  | Price: 1.09149 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-06 18:00 | SELL RANGE_RIDER  | Price: 1.09122 | SL: 1.09223 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-06 19:00 | CLOSE RANGE_RIDER  | Price: 1.09024 | R: +0.97 | Exit: BREAK_EVEN
ðŸ“ 2024-03-06 19:00 | SELL RANGE_RIDER  | Price: 1.09024 | SL: 1.09129 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-06 20:00 | SELL RANGE_RIDER  | Price: 1.09031 | SL: 1.09134 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-06 21:00 | CLOSE RANGE_RIDER  | Price: 1.08968 | R: +0.53 | Exit: BREAK_EVEN
ðŸ”š 2024-03-06 21:00 | CLOSE RANGE_RIDER  | Price: 1.08968 | R: +0.61 | Exit: BREAK_EVEN
ðŸ“ 2024-03-06 21:00 | SELL RANGE_RIDER  | Price: 1.08968 | SL: 1.09071 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-06 22:00 | SELL RANGE_RIDER  | Price: 1.08991 | SL: 1.09091 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-07 02:00 | CLOSE RANGE_RIDER  | Price: 1.09071 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-07 02:00 | SELL RANGE_RIDER  | Price: 1.09032 | SL: 1.09120 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-07 03:00 | CLOSE RANGE_RIDER  | Price: 1.08979 | R: +0.60 | Exit: BREAK_EVEN
ðŸ“ 2024-03-07 03:00 | SELL RANGE_RIDER  | Price: 1.08979 | SL: 1.09066 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-07 09:00 | CLOSE RANGE_RIDER  | Price: 1.08938 | R: +0.53 | Exit: BREAK_EVEN
ðŸ“ 2024-03-07 09:00 | SELL RANGE_RIDER  | Price: 1.08938 | SL: 1.09019 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-07 11:00 | CLOSE RANGE_RIDER  | Price: 1.09019 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-07 11:00 | SELL RANGE_RIDER  | Price: 1.09016 | SL: 1.09100 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-07 12:00 | CLOSE RANGE_RIDER  | Price: 1.08965 | R: +0.61 | Exit: BREAK_EVEN
ðŸ“ 2024-03-07 12:00 | SELL RANGE_RIDER  | Price: 1.08965 | SL: 1.09052 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-07 15:00 | CLOSE RANGE_RIDER  | Price: 1.08724 | R: +2.92 | Exit: BREAK_EVEN
ðŸ”š 2024-03-07 15:00 | CLOSE RANGE_RIDER  | Price: 1.08724 | R: +2.78 | Exit: BREAK_EVEN
ðŸ“ 2024-03-07 15:00 | SELL RANGE_RIDER  | Price: 1.08724 | SL: 1.08824 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-07 16:00 | CLOSE RANGE_RIDER  | Price: 1.08824 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-07 16:00 | SELL RANGE_RIDER  | Price: 1.09156 | SL: 1.09285 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-07 17:00 | CLOSE RANGE_RIDER  | Price: 1.09285 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-07 17:00 | SELL RANGE_RIDER  | Price: 1.09300 | SL: 1.09435 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-07 18:00 | SELL RANGE_RIDER  | Price: 1.09402 | SL: 1.09540 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-07 20:00 | CLOSE RANGE_RIDER  | Price: 1.09435 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-07 20:00 | SELL RANGE_RIDER  | Price: 1.09422 | SL: 1.09554 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-08 02:00 | CLOSE RANGE_RIDER  | Price: 1.09540 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-08 02:00 | CLOSE RANGE_RIDER  | Price: 1.09554 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-08 02:00 | SELL RANGE_RIDER  | Price: 1.09514 | SL: 1.09617 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-08 03:00 | SELL RANGE_RIDER  | Price: 1.09480 | SL: 1.09580 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-08 04:00 | CLOSE RANGE_RIDER  | Price: 1.09457 | R: +0.56 | Exit: BREAK_EVEN
ðŸ“ 2024-03-08 04:00 | SELL RANGE_RIDER  | Price: 1.09457 | SL: 1.09554 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-08 09:00 | CLOSE RANGE_RIDER  | Price: 1.09337 | R: +1.43 | Exit: BREAK_EVEN
ðŸ”š 2024-03-08 09:00 | CLOSE RANGE_RIDER  | Price: 1.09337 | R: +1.24 | Exit: BREAK_EVEN
ðŸ“ 2024-03-08 09:00 | SELL RANGE_RIDER  | Price: 1.09337 | SL: 1.09428 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-08 10:00 | SELL RANGE_RIDER  | Price: 1.09359 | SL: 1.09451 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-08 15:00 | CLOSE RANGE_RIDER  | Price: 1.09428 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-08 15:00 | CLOSE RANGE_RIDER  | Price: 1.09451 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-08 15:00 | SELL RANGE_RIDER  | Price: 1.09583 | SL: 1.09713 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-08 16:00 | SELL RANGE_RIDER  | Price: 1.09578 | SL: 1.09715 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-08 18:00 | CLOSE RANGE_RIDER  | Price: 1.09405 | R: +1.37 | Exit: BREAK_EVEN
ðŸ”š 2024-03-08 18:00 | CLOSE RANGE_RIDER  | Price: 1.09405 | R: +1.27 | Exit: BREAK_EVEN
ðŸ“ 2024-03-08 18:00 | SELL RANGE_RIDER  | Price: 1.09405 | SL: 1.09552 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-08 19:00 | SELL RANGE_RIDER  | Price: 1.09394 | SL: 1.09537 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-11 00:00 | CLOSE RANGE_RIDER  | Price: 1.09396 | R: +0.06 | Exit: MAX_HOLD_TIME
ðŸ”š 2024-03-11 00:00 | CLOSE RANGE_RIDER  | Price: 1.09396 | R: -0.01 | Exit: MAX_HOLD_TIME
ðŸ“ 2024-03-11 00:00 | SELL RANGE_RIDER  | Price: 1.09396 | SL: 1.09516 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-11 01:00 | SELL RANGE_RIDER  | Price: 1.09377 | SL: 1.09492 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-11 15:00 | CLOSE RANGE_RIDER  | Price: 1.09296 | R: +0.83 | Exit: BREAK_EVEN
ðŸ”š 2024-03-11 15:00 | CLOSE RANGE_RIDER  | Price: 1.09296 | R: +0.70 | Exit: BREAK_EVEN
ðŸ“ 2024-03-11 15:00 | SELL RANGE_RIDER  | Price: 1.09296 | SL: 1.09391 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-11 16:00 | CLOSE RANGE_RIDER  | Price: 1.09197 | R: +1.04 | Exit: BREAK_EVEN
ðŸ“ 2024-03-11 16:00 | SELL RANGE_RIDER  | Price: 1.09197 | SL: 1.09295 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-11 17:00 | SELL RANGE_RIDER  | Price: 1.09245 | SL: 1.09343 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-11 20:00 | CLOSE RANGE_RIDER  | Price: 1.09295 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-11 20:00 | SELL RANGE_RIDER  | Price: 1.09253 | SL: 1.09348 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-12 04:00 | CLOSE RANGE_RIDER  | Price: 1.09343 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-12 04:00 | SELL RANGE_RIDER  | Price: 1.09338 | SL: 1.09414 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-12 05:00 | CLOSE RANGE_RIDER  | Price: 1.09348 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-12 05:00 | SELL RANGE_RIDER  | Price: 1.09363 | SL: 1.09438 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-12 10:00 | CLOSE RANGE_RIDER  | Price: 1.09321 | R: +0.56 | Exit: BREAK_EVEN
ðŸ“ 2024-03-12 10:00 | SELL RANGE_RIDER  | Price: 1.09321 | SL: 1.09388 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-12 11:00 | CLOSE RANGE_RIDER  | Price: 1.09249 | R: +1.17 | Exit: BREAK_EVEN
ðŸ”š 2024-03-12 11:00 | CLOSE RANGE_RIDER  | Price: 1.09249 | R: +1.08 | Exit: BREAK_EVEN
ðŸ“ 2024-03-12 11:00 | SELL RANGE_RIDER  | Price: 1.09249 | SL: 1.09319 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-12 12:00 | CLOSE RANGE_RIDER  | Price: 1.09319 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-12 12:00 | SELL RANGE_RIDER  | Price: 1.09303 | SL: 1.09376 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-12 13:00 | SELL RANGE_RIDER  | Price: 1.09340 | SL: 1.09413 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-12 15:00 | CLOSE RANGE_RIDER  | Price: 1.09376 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-12 15:00 | CLOSE RANGE_RIDER  | Price: 1.09413 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-12 15:00 | SELL RANGE_RIDER  | Price: 1.09201 | SL: 1.09296 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-12 16:00 | CLOSE RANGE_RIDER  | Price: 1.09108 | R: +0.98 | Exit: BREAK_EVEN
ðŸ“ 2024-03-12 16:00 | SELL RANGE_RIDER  | Price: 1.09108 | SL: 1.09211 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-12 17:00 | SELL RANGE_RIDER  | Price: 1.09171 | SL: 1.09276 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-12 21:00 | CLOSE RANGE_RIDER  | Price: 1.09211 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-12 21:00 | SELL RANGE_RIDER  | Price: 1.09242 | SL: 1.09340 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-13 00:00 | CLOSE RANGE_RIDER  | Price: 1.09276 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-13 00:00 | SELL RANGE_RIDER  | Price: 1.09270 | SL: 1.09354 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-13 14:00 | CLOSE RANGE_RIDER  | Price: 1.09340 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-13 14:00 | CLOSE RANGE_RIDER  | Price: 1.09354 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-13 14:00 | SELL RANGE_RIDER  | Price: 1.09422 | SL: 1.09501 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-13 15:00 | CLOSE RANGE_RIDER  | Price: 1.09367 | R: +0.70 | Exit: BREAK_EVEN
ðŸ“ 2024-03-13 15:00 | SELL RANGE_RIDER  | Price: 1.09367 | SL: 1.09450 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-13 16:00 | SELL RANGE_RIDER  | Price: 1.09373 | SL: 1.09454 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-13 18:00 | CLOSE RANGE_RIDER  | Price: 1.09450 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-13 18:00 | CLOSE RANGE_RIDER  | Price: 1.09454 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-13 18:00 | SELL RANGE_RIDER  | Price: 1.09436 | SL: 1.09521 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-13 19:00 | SELL RANGE_RIDER  | Price: 1.09492 | SL: 1.09578 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-13 20:00 | CLOSE RANGE_RIDER  | Price: 1.09521 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-13 20:00 | CLOSE RANGE_RIDER  | Price: 1.09578 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-14 00:00 | SELL RANGE_RIDER  | Price: 1.09497 | SL: 1.09578 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-14 01:00 | SELL RANGE_RIDER  | Price: 1.09488 | SL: 1.09566 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-14 05:00 | CLOSE RANGE_RIDER  | Price: 1.09439 | R: +0.71 | Exit: BREAK_EVEN
ðŸ”š 2024-03-14 05:00 | CLOSE RANGE_RIDER  | Price: 1.09439 | R: +0.63 | Exit: BREAK_EVEN
ðŸ“ 2024-03-14 05:00 | SELL RANGE_RIDER  | Price: 1.09439 | SL: 1.09515 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-14 06:00 | SELL RANGE_RIDER  | Price: 1.09423 | SL: 1.09496 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-14 08:00 | CLOSE RANGE_RIDER  | Price: 1.09397 | R: +0.55 | Exit: BREAK_EVEN
ðŸ“ 2024-03-14 08:00 | SELL RANGE_RIDER  | Price: 1.09397 | SL: 1.09466 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-14 09:00 | CLOSE RANGE_RIDER  | Price: 1.09379 | R: +0.60 | Exit: BREAK_EVEN
ðŸ“ 2024-03-14 09:00 | SELL RANGE_RIDER  | Price: 1.09379 | SL: 1.09446 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-14 10:00 | CLOSE RANGE_RIDER  | Price: 1.09353 | R: +0.64 | Exit: BREAK_EVEN
ðŸ“ 2024-03-14 10:00 | SELL RANGE_RIDER  | Price: 1.09353 | SL: 1.09424 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-14 11:00 | CLOSE RANGE_RIDER  | Price: 1.09424 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-14 11:00 | SELL RANGE_RIDER  | Price: 1.09379 | SL: 1.09451 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-14 13:00 | CLOSE RANGE_RIDER  | Price: 1.09446 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-14 13:00 | CLOSE RANGE_RIDER  | Price: 1.09451 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-14 13:00 | SELL RANGE_RIDER  | Price: 1.09396 | SL: 1.09468 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-14 14:00 | SELL RANGE_RIDER  | Price: 1.09416 | SL: 1.09488 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-14 15:00 | CLOSE RANGE_RIDER  | Price: 1.09300 | R: +1.33 | Exit: BREAK_EVEN
ðŸ”š 2024-03-14 15:00 | CLOSE RANGE_RIDER  | Price: 1.09300 | R: +1.62 | Exit: BREAK_EVEN
ðŸ“ 2024-03-14 15:00 | SELL RANGE_RIDER  | Price: 1.09300 | SL: 1.09381 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-14 16:00 | CLOSE RANGE_RIDER  | Price: 1.09121 | R: +2.20 | Exit: BREAK_EVEN
ðŸ“ 2024-03-14 16:00 | SELL RANGE_RIDER  | Price: 1.09121 | SL: 1.09213 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-14 17:00 | CLOSE RANGE_RIDER  | Price: 1.08978 | R: +1.56 | Exit: BREAK_EVEN
ðŸ“ 2024-03-14 17:00 | SELL RANGE_RIDER  | Price: 1.08978 | SL: 1.09076 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-14 18:00 | CLOSE RANGE_RIDER  | Price: 1.08877 | R: +1.03 | Exit: BREAK_EVEN
ðŸ“ 2024-03-14 18:00 | SELL RANGE_RIDER  | Price: 1.08877 | SL: 1.08980 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-14 19:00 | SELL RANGE_RIDER  | Price: 1.08871 | SL: 1.08972 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-15 03:00 | CLOSE RANGE_RIDER  | Price: 1.08780 | R: +0.94 | Exit: BREAK_EVEN
ðŸ”š 2024-03-15 03:00 | CLOSE RANGE_RIDER  | Price: 1.08780 | R: +0.90 | Exit: BREAK_EVEN
ðŸ“ 2024-03-15 03:00 | SELL RANGE_RIDER  | Price: 1.08780 | SL: 1.08864 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-15 04:00 | SELL RANGE_RIDER  | Price: 1.08772 | SL: 1.08853 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-15 05:00 | CLOSE RANGE_RIDER  | Price: 1.08733 | R: +0.56 | Exit: BREAK_EVEN
ðŸ“ 2024-03-15 05:00 | SELL RANGE_RIDER  | Price: 1.08733 | SL: 1.08812 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-15 10:00 | CLOSE RANGE_RIDER  | Price: 1.08812 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-15 10:00 | SELL RANGE_RIDER  | Price: 1.08810 | SL: 1.08879 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-15 11:00 | CLOSE RANGE_RIDER  | Price: 1.08853 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-15 11:00 | SELL RANGE_RIDER  | Price: 1.08829 | SL: 1.08899 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-15 12:00 | CLOSE RANGE_RIDER  | Price: 1.08879 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-15 12:00 | CLOSE RANGE_RIDER  | Price: 1.08899 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-15 12:00 | SELL RANGE_RIDER  | Price: 1.08983 | SL: 1.09060 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-15 13:00 | CLOSE RANGE_RIDER  | Price: 1.08912 | R: +0.92 | Exit: BREAK_EVEN
ðŸ“ 2024-03-15 13:00 | SELL RANGE_RIDER  | Price: 1.08912 | SL: 1.08991 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-15 14:00 | SELL RANGE_RIDER  | Price: 1.08936 | SL: 1.09017 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-15 15:00 | CLOSE RANGE_RIDER  | Price: 1.08873 | R: +0.78 | Exit: BREAK_EVEN
ðŸ“ 2024-03-15 15:00 | SELL RANGE_RIDER  | Price: 1.08873 | SL: 1.08955 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-15 16:00 | CLOSE RANGE_RIDER  | Price: 1.08866 | R: +0.58 | Exit: BREAK_EVEN
ðŸ“ 2024-03-15 16:00 | SELL RANGE_RIDER  | Price: 1.08866 | SL: 1.08951 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-18 00:00 | CLOSE RANGE_RIDER  | Price: 1.08896 | R: -0.28 | Exit: MAX_HOLD_TIME
ðŸ”š 2024-03-18 00:00 | CLOSE RANGE_RIDER  | Price: 1.08896 | R: -0.35 | Exit: MAX_HOLD_TIME
ðŸ“ 2024-03-18 00:00 | SELL RANGE_RIDER  | Price: 1.08896 | SL: 1.08972 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-18 01:00 | SELL RANGE_RIDER  | Price: 1.08866 | SL: 1.08940 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-18 02:00 | CLOSE RANGE_RIDER  | Price: 1.08837 | R: +0.78 | Exit: BREAK_EVEN
ðŸ“ 2024-03-18 02:00 | SELL RANGE_RIDER  | Price: 1.08837 | SL: 1.08910 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-18 05:00 | CLOSE RANGE_RIDER  | Price: 1.08910 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-18 05:00 | SELL RANGE_RIDER  | Price: 1.08893 | SL: 1.08964 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-18 06:00 | CLOSE RANGE_RIDER  | Price: 1.08855 | R: +0.54 | Exit: BREAK_EVEN
ðŸ“ 2024-03-18 06:00 | SELL RANGE_RIDER  | Price: 1.08855 | SL: 1.08924 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-18 10:00 | CLOSE RANGE_RIDER  | Price: 1.08940 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-18 10:00 | CLOSE RANGE_RIDER  | Price: 1.08924 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-18 10:00 | SELL RANGE_RIDER  | Price: 1.08924 | SL: 1.08987 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-18 11:00 | SELL RANGE_RIDER  | Price: 1.08939 | SL: 1.09002 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-18 12:00 | CLOSE RANGE_RIDER  | Price: 1.08987 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-18 12:00 | CLOSE RANGE_RIDER  | Price: 1.09002 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-18 12:00 | SELL RANGE_RIDER  | Price: 1.08995 | SL: 1.09059 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-18 13:00 | SELL RANGE_RIDER  | Price: 1.08999 | SL: 1.09063 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-18 14:00 | CLOSE RANGE_RIDER  | Price: 1.09059 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-18 14:00 | SELL RANGE_RIDER  | Price: 1.09025 | SL: 1.09090 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-18 15:00 | CLOSE RANGE_RIDER  | Price: 1.08923 | R: +1.19 | Exit: BREAK_EVEN
ðŸ”š 2024-03-18 15:00 | CLOSE RANGE_RIDER  | Price: 1.08923 | R: +1.58 | Exit: BREAK_EVEN
ðŸ“ 2024-03-18 15:00 | SELL RANGE_RIDER  | Price: 1.08923 | SL: 1.08994 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-18 16:00 | SELL RANGE_RIDER  | Price: 1.08892 | SL: 1.08963 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-18 17:00 | CLOSE RANGE_RIDER  | Price: 1.08857 | R: +0.93 | Exit: BREAK_EVEN
ðŸ“ 2024-03-18 17:00 | SELL RANGE_RIDER  | Price: 1.08857 | SL: 1.08930 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-18 18:00 | CLOSE RANGE_RIDER  | Price: 1.08854 | R: +0.53 | Exit: BREAK_EVEN
ðŸ“ 2024-03-18 18:00 | SELL RANGE_RIDER  | Price: 1.08854 | SL: 1.08927 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-18 19:00 | CLOSE RANGE_RIDER  | Price: 1.08725 | R: +1.82 | Exit: BREAK_EVEN
ðŸ”š 2024-03-18 19:00 | CLOSE RANGE_RIDER  | Price: 1.08725 | R: +1.76 | Exit: BREAK_EVEN
ðŸ“ 2024-03-18 19:00 | SELL RANGE_RIDER  | Price: 1.08725 | SL: 1.08804 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-18 20:00 | SELL RANGE_RIDER  | Price: 1.08686 | SL: 1.08766 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-19 04:00 | CLOSE RANGE_RIDER  | Price: 1.08683 | R: +0.53 | Exit: BREAK_EVEN
ðŸ“ 2024-03-19 04:00 | SELL RANGE_RIDER  | Price: 1.08683 | SL: 1.08745 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-19 05:00 | CLOSE RANGE_RIDER  | Price: 1.08745 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-19 05:00 | SELL RANGE_RIDER  | Price: 1.08734 | SL: 1.08796 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-19 08:00 | CLOSE RANGE_RIDER  | Price: 1.08642 | R: +0.55 | Exit: BREAK_EVEN
ðŸ”š 2024-03-19 08:00 | CLOSE RANGE_RIDER  | Price: 1.08642 | R: +1.48 | Exit: BREAK_EVEN
ðŸ“ 2024-03-19 08:00 | SELL RANGE_RIDER  | Price: 1.08642 | SL: 1.08709 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-19 09:00 | SELL RANGE_RIDER  | Price: 1.08677 | SL: 1.08744 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-19 10:00 | CLOSE RANGE_RIDER  | Price: 1.08548 | R: +1.41 | Exit: BREAK_EVEN
ðŸ”š 2024-03-19 10:00 | CLOSE RANGE_RIDER  | Price: 1.08548 | R: +1.94 | Exit: BREAK_EVEN
ðŸ“ 2024-03-19 10:00 | SELL RANGE_RIDER  | Price: 1.08548 | SL: 1.08621 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-19 11:00 | CLOSE RANGE_RIDER  | Price: 1.08476 | R: +0.98 | Exit: BREAK_EVEN
ðŸ“ 2024-03-19 11:00 | SELL RANGE_RIDER  | Price: 1.08476 | SL: 1.08554 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-19 12:00 | CLOSE RANGE_RIDER  | Price: 1.08368 | R: +1.39 | Exit: BREAK_EVEN
ðŸ“ 2024-03-19 12:00 | SELL RANGE_RIDER  | Price: 1.08368 | SL: 1.08451 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-19 13:00 | CLOSE RANGE_RIDER  | Price: 1.08451 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-19 13:00 | SELL RANGE_RIDER  | Price: 1.08445 | SL: 1.08529 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-19 14:00 | SELL RANGE_RIDER  | Price: 1.08504 | SL: 1.08588 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-19 15:00 | CLOSE RANGE_RIDER  | Price: 1.08529 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-19 15:00 | SELL RANGE_RIDER  | Price: 1.08518 | SL: 1.08604 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-19 17:00 | CLOSE RANGE_RIDER  | Price: 1.08588 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-19 17:00 | CLOSE RANGE_RIDER  | Price: 1.08604 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-19 17:00 | SELL RANGE_RIDER  | Price: 1.08624 | SL: 1.08712 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-19 18:00 | SELL RANGE_RIDER  | Price: 1.08585 | SL: 1.08673 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-19 20:00 | CLOSE RANGE_RIDER  | Price: 1.08673 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-19 20:00 | SELL RANGE_RIDER  | Price: 1.08636 | SL: 1.08724 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-20 06:00 | CLOSE RANGE_RIDER  | Price: 1.08712 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-20 06:00 | SELL RANGE_RIDER  | Price: 1.08700 | SL: 1.08765 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-20 07:00 | CLOSE RANGE_RIDER  | Price: 1.08667 | R: +0.51 | Exit: BREAK_EVEN
ðŸ“ 2024-03-20 07:00 | SELL RANGE_RIDER  | Price: 1.08667 | SL: 1.08730 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-20 11:00 | CLOSE RANGE_RIDER  | Price: 1.08523 | R: +1.29 | Exit: BREAK_EVEN
ðŸ”š 2024-03-20 11:00 | CLOSE RANGE_RIDER  | Price: 1.08523 | R: +2.29 | Exit: BREAK_EVEN
ðŸ“ 2024-03-20 11:00 | SELL RANGE_RIDER  | Price: 1.08523 | SL: 1.08591 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-20 12:00 | CLOSE RANGE_RIDER  | Price: 1.08392 | R: +1.93 | Exit: BREAK_EVEN
ðŸ“ 2024-03-20 12:00 | SELL RANGE_RIDER  | Price: 1.08392 | SL: 1.08466 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-20 13:00 | SELL RANGE_RIDER  | Price: 1.08397 | SL: 1.08471 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-20 17:00 | CLOSE RANGE_RIDER  | Price: 1.08466 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-20 17:00 | CLOSE RANGE_RIDER  | Price: 1.08471 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-20 17:00 | SELL RANGE_RIDER  | Price: 1.08498 | SL: 1.08572 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-20 18:00 | SELL RANGE_RIDER  | Price: 1.08547 | SL: 1.08621 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-20 19:00 | CLOSE RANGE_RIDER  | Price: 1.08572 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-20 19:00 | SELL RANGE_RIDER  | Price: 1.08608 | SL: 1.08682 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-20 20:00 | CLOSE RANGE_RIDER  | Price: 1.08621 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-20 20:00 | SELL RANGE_RIDER  | Price: 1.08652 | SL: 1.08727 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-20 21:00 | CLOSE RANGE_RIDER  | Price: 1.08682 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-20 21:00 | CLOSE RANGE_RIDER  | Price: 1.08727 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-20 21:00 | SELL RANGE_RIDER  | Price: 1.09144 | SL: 1.09252 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-20 22:00 | SELL RANGE_RIDER  | Price: 1.09210 | SL: 1.09325 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-21 01:00 | CLOSE RANGE_RIDER  | Price: 1.09252 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-21 01:00 | SELL RANGE_RIDER  | Price: 1.09323 | SL: 1.09428 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-21 02:00 | CLOSE RANGE_RIDER  | Price: 1.09325 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-21 02:00 | SELL RANGE_RIDER  | Price: 1.09375 | SL: 1.09479 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-21 08:00 | CLOSE RANGE_RIDER  | Price: 1.09317 | R: +0.56 | Exit: BREAK_EVEN
ðŸ“ 2024-03-21 08:00 | SELL RANGE_RIDER  | Price: 1.09317 | SL: 1.09400 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-21 10:00 | CLOSE RANGE_RIDER  | Price: 1.09400 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-21 10:00 | SELL RANGE_RIDER  | Price: 1.09289 | SL: 1.09377 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-21 11:00 | CLOSE RANGE_RIDER  | Price: 1.08919 | R: +3.84 | Exit: BREAK_EVEN
ðŸ”š 2024-03-21 11:00 | CLOSE RANGE_RIDER  | Price: 1.08919 | R: +4.19 | Exit: BREAK_EVEN
ðŸ“ 2024-03-21 11:00 | SELL RANGE_RIDER  | Price: 1.08919 | SL: 1.09031 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-21 12:00 | CLOSE RANGE_RIDER  | Price: 1.09031 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-21 12:00 | SELL RANGE_RIDER  | Price: 1.09130 | SL: 1.09252 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-21 13:00 | SELL RANGE_RIDER  | Price: 1.09195 | SL: 1.09317 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-21 14:00 | CLOSE RANGE_RIDER  | Price: 1.09097 | R: +0.81 | Exit: BREAK_EVEN
ðŸ“ 2024-03-21 14:00 | SELL RANGE_RIDER  | Price: 1.09097 | SL: 1.09221 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-21 16:00 | CLOSE RANGE_RIDER  | Price: 1.08858 | R: +2.23 | Exit: BREAK_EVEN
ðŸ”š 2024-03-21 16:00 | CLOSE RANGE_RIDER  | Price: 1.08858 | R: +1.93 | Exit: BREAK_EVEN
ðŸ“ 2024-03-21 16:00 | SELL RANGE_RIDER  | Price: 1.08858 | SL: 1.08994 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-21 17:00 | CLOSE RANGE_RIDER  | Price: 1.08788 | R: +0.52 | Exit: BREAK_EVEN
ðŸ“ 2024-03-21 17:00 | SELL RANGE_RIDER  | Price: 1.08788 | SL: 1.08925 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-21 18:00 | CLOSE RANGE_RIDER  | Price: 1.08605 | R: +1.34 | Exit: BREAK_EVEN
ðŸ“ 2024-03-21 18:00 | SELL RANGE_RIDER  | Price: 1.08605 | SL: 1.08749 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-21 19:00 | SELL RANGE_RIDER  | Price: 1.08610 | SL: 1.08748 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-22 04:00 | CLOSE RANGE_RIDER  | Price: 1.08505 | R: +0.69 | Exit: BREAK_EVEN
ðŸ”š 2024-03-22 04:00 | CLOSE RANGE_RIDER  | Price: 1.08505 | R: +0.76 | Exit: BREAK_EVEN
ðŸ“ 2024-03-22 04:00 | SELL RANGE_RIDER  | Price: 1.08505 | SL: 1.08608 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-22 05:00 | CLOSE RANGE_RIDER  | Price: 1.08391 | R: +1.11 | Exit: BREAK_EVEN
ðŸ“ 2024-03-22 05:00 | SELL RANGE_RIDER  | Price: 1.08391 | SL: 1.08496 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-22 06:00 | SELL RANGE_RIDER  | Price: 1.08380 | SL: 1.08481 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-22 07:00 | CLOSE RANGE_RIDER  | Price: 1.08334 | R: +0.54 | Exit: BREAK_EVEN
ðŸ“ 2024-03-22 07:00 | SELL RANGE_RIDER  | Price: 1.08334 | SL: 1.08433 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-22 09:00 | CLOSE RANGE_RIDER  | Price: 1.08306 | R: +0.73 | Exit: BREAK_EVEN
ðŸ“ 2024-03-22 09:00 | SELL RANGE_RIDER  | Price: 1.08306 | SL: 1.08408 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-22 10:00 | CLOSE RANGE_RIDER  | Price: 1.08248 | R: +0.87 | Exit: BREAK_EVEN
ðŸ”š 2024-03-22 10:00 | CLOSE RANGE_RIDER  | Price: 1.08248 | R: +0.57 | Exit: BREAK_EVEN
ðŸ“ 2024-03-22 10:00 | SELL RANGE_RIDER  | Price: 1.08248 | SL: 1.08352 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-22 11:00 | CLOSE RANGE_RIDER  | Price: 1.08118 | R: +1.25 | Exit: BREAK_EVEN
ðŸ“ 2024-03-22 11:00 | SELL RANGE_RIDER  | Price: 1.08118 | SL: 1.08230 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-22 12:00 | CLOSE RANGE_RIDER  | Price: 1.08230 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-22 12:00 | SELL RANGE_RIDER  | Price: 1.08162 | SL: 1.08275 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-22 13:00 | SELL RANGE_RIDER  | Price: 1.08164 | SL: 1.08274 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-22 15:00 | CLOSE RANGE_RIDER  | Price: 1.08275 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-22 15:00 | CLOSE RANGE_RIDER  | Price: 1.08274 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-22 15:00 | SELL RANGE_RIDER  | Price: 1.08265 | SL: 1.08379 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-22 16:00 | SELL RANGE_RIDER  | Price: 1.08296 | SL: 1.08410 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-22 17:00 | CLOSE RANGE_RIDER  | Price: 1.08151 | R: +1.00 | Exit: BREAK_EVEN
ðŸ”š 2024-03-22 17:00 | CLOSE RANGE_RIDER  | Price: 1.08151 | R: +1.28 | Exit: BREAK_EVEN
ðŸ“ 2024-03-22 17:00 | SELL RANGE_RIDER  | Price: 1.08151 | SL: 1.08269 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-22 18:00 | SELL RANGE_RIDER  | Price: 1.08159 | SL: 1.08276 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-22 19:00 | CLOSE RANGE_RIDER  | Price: 1.08058 | R: +0.79 | Exit: BREAK_EVEN
ðŸ”š 2024-03-22 19:00 | CLOSE RANGE_RIDER  | Price: 1.08058 | R: +0.86 | Exit: BREAK_EVEN
ðŸ“ 2024-03-22 19:00 | SELL RANGE_RIDER  | Price: 1.08058 | SL: 1.08175 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-22 20:00 | SELL RANGE_RIDER  | Price: 1.08060 | SL: 1.08173 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-25 00:00 | CLOSE RANGE_RIDER  | Price: 1.08089 | R: -0.26 | Exit: MAX_HOLD_TIME
ðŸ”š 2024-03-25 00:00 | CLOSE RANGE_RIDER  | Price: 1.08089 | R: -0.26 | Exit: MAX_HOLD_TIME
ðŸ“ 2024-03-25 00:00 | SELL RANGE_RIDER  | Price: 1.08089 | SL: 1.08184 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-25 01:00 | SELL RANGE_RIDER  | Price: 1.08087 | SL: 1.08178 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-25 03:00 | CLOSE RANGE_RIDER  | Price: 1.08036 | R: +0.56 | Exit: BREAK_EVEN
ðŸ”š 2024-03-25 03:00 | CLOSE RANGE_RIDER  | Price: 1.08036 | R: +0.56 | Exit: BREAK_EVEN
ðŸ“ 2024-03-25 03:00 | SELL RANGE_RIDER  | Price: 1.08036 | SL: 1.08122 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-25 04:00 | CLOSE RANGE_RIDER  | Price: 1.08122 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-25 04:00 | SELL RANGE_RIDER  | Price: 1.08170 | SL: 1.08262 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-25 05:00 | SELL RANGE_RIDER  | Price: 1.08219 | SL: 1.08309 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-25 06:00 | CLOSE RANGE_RIDER  | Price: 1.08136 | R: +0.92 | Exit: BREAK_EVEN
ðŸ“ 2024-03-25 06:00 | SELL RANGE_RIDER  | Price: 1.08136 | SL: 1.08227 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-25 10:00 | CLOSE RANGE_RIDER  | Price: 1.08227 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-25 10:00 | SELL RANGE_RIDER  | Price: 1.08139 | SL: 1.08225 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-25 11:00 | CLOSE RANGE_RIDER  | Price: 1.08225 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-25 11:00 | SELL RANGE_RIDER  | Price: 1.08139 | SL: 1.08231 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-25 14:00 | CLOSE RANGE_RIDER  | Price: 1.08262 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-25 14:00 | CLOSE RANGE_RIDER  | Price: 1.08231 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-25 14:00 | SELL RANGE_RIDER  | Price: 1.08285 | SL: 1.08378 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-25 15:00 | SELL RANGE_RIDER  | Price: 1.08307 | SL: 1.08398 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-25 16:00 | CLOSE RANGE_RIDER  | Price: 1.08378 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-25 16:00 | SELL RANGE_RIDER  | Price: 1.08351 | SL: 1.08441 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-25 17:00 | CLOSE RANGE_RIDER  | Price: 1.08398 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-25 17:00 | SELL RANGE_RIDER  | Price: 1.08391 | SL: 1.08481 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-26 04:00 | CLOSE RANGE_RIDER  | Price: 1.08441 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-26 04:00 | SELL RANGE_RIDER  | Price: 1.08405 | SL: 1.08470 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-26 06:00 | CLOSE RANGE_RIDER  | Price: 1.08369 | R: +0.55 | Exit: BREAK_EVEN
ðŸ“ 2024-03-26 06:00 | SELL RANGE_RIDER  | Price: 1.08369 | SL: 1.08434 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-26 08:00 | CLOSE RANGE_RIDER  | Price: 1.08481 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-26 08:00 | CLOSE RANGE_RIDER  | Price: 1.08434 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-26 08:00 | SELL RANGE_RIDER  | Price: 1.08472 | SL: 1.08537 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-26 09:00 | SELL RANGE_RIDER  | Price: 1.08508 | SL: 1.08573 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-26 10:00 | CLOSE RANGE_RIDER  | Price: 1.08425 | R: +0.72 | Exit: BREAK_EVEN
ðŸ”š 2024-03-26 10:00 | CLOSE RANGE_RIDER  | Price: 1.08425 | R: +1.28 | Exit: BREAK_EVEN
ðŸ“ 2024-03-26 10:00 | SELL RANGE_RIDER  | Price: 1.08425 | SL: 1.08495 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-26 11:00 | CLOSE RANGE_RIDER  | Price: 1.08495 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-26 11:00 | SELL RANGE_RIDER  | Price: 1.08496 | SL: 1.08570 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-26 12:00 | SELL RANGE_RIDER  | Price: 1.08538 | SL: 1.08614 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-26 13:00 | CLOSE RANGE_RIDER  | Price: 1.08570 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-26 13:00 | CLOSE RANGE_RIDER  | Price: 1.08614 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-26 13:00 | SELL RANGE_RIDER  | Price: 1.08553 | SL: 1.08632 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-26 14:00 | SELL RANGE_RIDER  | Price: 1.08570 | SL: 1.08648 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-26 15:00 | CLOSE RANGE_RIDER  | Price: 1.08521 | R: +0.63 | Exit: BREAK_EVEN
ðŸ“ 2024-03-26 15:00 | SELL RANGE_RIDER  | Price: 1.08521 | SL: 1.08601 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-26 17:00 | CLOSE RANGE_RIDER  | Price: 1.08412 | R: +1.79 | Exit: BREAK_EVEN
ðŸ”š 2024-03-26 17:00 | CLOSE RANGE_RIDER  | Price: 1.08412 | R: +1.36 | Exit: BREAK_EVEN
ðŸ“ 2024-03-26 17:00 | SELL RANGE_RIDER  | Price: 1.08412 | SL: 1.08501 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-26 18:00 | CLOSE RANGE_RIDER  | Price: 1.08283 | R: +1.45 | Exit: BREAK_EVEN
ðŸ“ 2024-03-26 18:00 | SELL RANGE_RIDER  | Price: 1.08283 | SL: 1.08379 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-26 19:00 | SELL RANGE_RIDER  | Price: 1.08284 | SL: 1.08379 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-27 04:00 | CLOSE RANGE_RIDER  | Price: 1.08236 | R: +0.50 | Exit: BREAK_EVEN
ðŸ“ 2024-03-27 04:00 | SELL RANGE_RIDER  | Price: 1.08236 | SL: 1.08310 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-27 09:00 | CLOSE RANGE_RIDER  | Price: 1.08310 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-27 09:00 | SELL RANGE_RIDER  | Price: 1.08323 | SL: 1.08390 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-27 10:00 | CLOSE RANGE_RIDER  | Price: 1.08265 | R: +0.87 | Exit: BREAK_EVEN
ðŸ“ 2024-03-27 10:00 | SELL RANGE_RIDER  | Price: 1.08265 | SL: 1.08335 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-27 12:00 | CLOSE RANGE_RIDER  | Price: 1.08379 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-27 12:00 | CLOSE RANGE_RIDER  | Price: 1.08335 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-27 12:00 | SELL RANGE_RIDER  | Price: 1.08278 | SL: 1.08353 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-27 13:00 | SELL RANGE_RIDER  | Price: 1.08330 | SL: 1.08406 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-27 14:00 | CLOSE RANGE_RIDER  | Price: 1.08210 | R: +0.90 | Exit: BREAK_EVEN
ðŸ”š 2024-03-27 14:00 | CLOSE RANGE_RIDER  | Price: 1.08210 | R: +1.58 | Exit: BREAK_EVEN
ðŸ“ 2024-03-27 14:00 | SELL RANGE_RIDER  | Price: 1.08210 | SL: 1.08293 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-27 15:00 | SELL RANGE_RIDER  | Price: 1.08189 | SL: 1.08271 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-27 17:00 | CLOSE RANGE_RIDER  | Price: 1.08147 | R: +0.76 | Exit: BREAK_EVEN
ðŸ”š 2024-03-27 17:00 | CLOSE RANGE_RIDER  | Price: 1.08147 | R: +0.51 | Exit: BREAK_EVEN
ðŸ“ 2024-03-27 17:00 | SELL RANGE_RIDER  | Price: 1.08147 | SL: 1.08229 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-27 18:00 | SELL RANGE_RIDER  | Price: 1.08203 | SL: 1.08285 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-27 19:00 | CLOSE RANGE_RIDER  | Price: 1.08229 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-27 19:00 | SELL RANGE_RIDER  | Price: 1.08232 | SL: 1.08313 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-27 23:00 | CLOSE RANGE_RIDER  | Price: 1.08285 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-27 23:00 | SELL RANGE_RIDER  | Price: 1.08279 | SL: 1.08353 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-28 01:00 | CLOSE RANGE_RIDER  | Price: 1.08137 | R: +1.17 | Exit: BREAK_EVEN
ðŸ”š 2024-03-28 01:00 | CLOSE RANGE_RIDER  | Price: 1.08137 | R: +1.91 | Exit: BREAK_EVEN
ðŸ“ 2024-03-28 01:00 | SELL RANGE_RIDER  | Price: 1.08137 | SL: 1.08215 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-28 02:00 | SELL RANGE_RIDER  | Price: 1.08126 | SL: 1.08201 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-28 03:00 | CLOSE RANGE_RIDER  | Price: 1.08201 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-28 03:00 | SELL RANGE_RIDER  | Price: 1.08176 | SL: 1.08255 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-28 05:00 | CLOSE RANGE_RIDER  | Price: 1.08215 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-28 05:00 | CLOSE RANGE_RIDER  | Price: 1.08255 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-28 05:00 | SELL RANGE_RIDER  | Price: 1.08223 | SL: 1.08300 | Conf: 85.0% | Regime: RANGING
ðŸ“ 2024-03-28 06:00 | SELL RANGE_RIDER  | Price: 1.08216 | SL: 1.08289 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-28 09:00 | CLOSE RANGE_RIDER  | Price: 1.08181 | R: +0.55 | Exit: BREAK_EVEN
ðŸ“ 2024-03-28 09:00 | SELL RANGE_RIDER  | Price: 1.08181 | SL: 1.08252 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-28 10:00 | CLOSE RANGE_RIDER  | Price: 1.08010 | R: +2.81 | Exit: BREAK_EVEN
ðŸ”š 2024-03-28 10:00 | CLOSE RANGE_RIDER  | Price: 1.08010 | R: +2.42 | Exit: BREAK_EVEN
ðŸ“ 2024-03-28 10:00 | SELL RANGE_RIDER  | Price: 1.08010 | SL: 1.08089 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-28 11:00 | CLOSE RANGE_RIDER  | Price: 1.07920 | R: +1.14 | Exit: BREAK_EVEN
ðŸ“ 2024-03-28 11:00 | SELL RANGE_RIDER  | Price: 1.07920 | SL: 1.08002 | Conf: 85.0% | Regime: RANGING
ðŸ”š 2024-03-28 12:00 | CLOSE RANGE_RIDER  | Price: 1.07755 | R: +2.01 | Exit: BREAK_EVEN
ðŸ“ 2024-03-28 12:00 | SELL RANGE_RIDER  | Price: 1.07755 | SL: 1.07843 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-28 13:00 | CLOSE RANGE_RIDER  | Price: 1.07843 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-28 13:00 | SELL RANGE_RIDER  | Price: 1.07892 | SL: 1.07987 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-28 14:00 | CLOSE RANGE_RIDER  | Price: 1.07841 | R: +0.54 | Exit: BREAK_EVEN
ðŸ“ 2024-03-28 14:00 | SELL RANGE_RIDER  | Price: 1.07841 | SL: 1.07938 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-28 15:00 | CLOSE RANGE_RIDER  | Price: 1.07938 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-28 15:00 | SELL RANGE_RIDER  | Price: 1.08082 | SL: 1.08190 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-28 16:00 | SELL RANGE_RIDER  | Price: 1.08124 | SL: 1.08235 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-28 17:00 | CLOSE RANGE_RIDER  | Price: 1.08004 | R: +0.72 | Exit: BREAK_EVEN
ðŸ”š 2024-03-28 17:00 | CLOSE RANGE_RIDER  | Price: 1.08004 | R: +1.08 | Exit: BREAK_EVEN
ðŸ“ 2024-03-28 17:00 | SELL RANGE_RIDER  | Price: 1.08004 | SL: 1.08122 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-28 18:00 | SELL RANGE_RIDER  | Price: 1.08014 | SL: 1.08134 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-28 21:00 | CLOSE RANGE_RIDER  | Price: 1.07874 | R: +1.10 | Exit: BREAK_EVEN
ðŸ”š 2024-03-28 21:00 | CLOSE RANGE_RIDER  | Price: 1.07874 | R: +1.17 | Exit: BREAK_EVEN
ðŸ“ 2024-03-28 21:00 | SELL RANGE_RIDER  | Price: 1.07874 | SL: 1.07991 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-28 22:00 | SELL RANGE_RIDER  | Price: 1.07881 | SL: 1.07993 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-29 04:00 | CLOSE RANGE_RIDER  | Price: 1.07761 | R: +0.97 | Exit: BREAK_EVEN
ðŸ”š 2024-03-29 04:00 | CLOSE RANGE_RIDER  | Price: 1.07761 | R: +1.07 | Exit: BREAK_EVEN
ðŸ“ 2024-03-29 04:00 | SELL RANGE_RIDER  | Price: 1.07761 | SL: 1.07855 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-29 05:00 | SELL RANGE_RIDER  | Price: 1.07789 | SL: 1.07880 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-29 10:00 | CLOSE RANGE_RIDER  | Price: 1.07685 | R: +0.81 | Exit: BREAK_EVEN
ðŸ”š 2024-03-29 10:00 | CLOSE RANGE_RIDER  | Price: 1.07685 | R: +1.14 | Exit: BREAK_EVEN
ðŸ“ 2024-03-29 10:00 | SELL RANGE_RIDER  | Price: 1.07685 | SL: 1.07766 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-29 11:00 | CLOSE RANGE_RIDER  | Price: 1.07766 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-29 11:00 | SELL RANGE_RIDER  | Price: 1.07788 | SL: 1.07871 | Conf: 75.0% | Regime: RANGING
ðŸ“ 2024-03-29 12:00 | SELL RANGE_RIDER  | Price: 1.07828 | SL: 1.07912 | Conf: 75.0% | Regime: RANGING
ðŸ”š 2024-03-29 13:00 | CLOSE RANGE_RIDER  | Price: 1.07871 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-29 13:00 | SELL RANGE_RIDER  | Price: 1.07851 | SL: 1.07934 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-29 14:00 | CLOSE RANGE_RIDER  | Price: 1.07912 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-29 14:00 | SELL RANGE_RIDER  | Price: 1.07871 | SL: 1.07953 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-29 15:00 | CLOSE RANGE_RIDER  | Price: 1.07934 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-29 15:00 | CLOSE RANGE_RIDER  | Price: 1.07953 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-29 15:00 | SELL RANGE_RIDER  | Price: 1.07986 | SL: 1.08079 | Conf: 79.0% | Regime: RANGING
ðŸ“ 2024-03-29 16:00 | SELL RANGE_RIDER  | Price: 1.07984 | SL: 1.08078 | Conf: 79.0% | Regime: RANGING
ðŸ”š 2024-03-29 18:00 | CLOSE RANGE_RIDER  | Price: 1.07925 | R: +0.65 | Exit: BREAK_EVEN
ðŸ”š 2024-03-29 18:00 | CLOSE RANGE_RIDER  | Price: 1.07925 | R: +0.63 | Exit: BREAK_EVEN
ðŸ“ 2024-03-29 18:00 | SELL RANGE_RIDER  | Price: 1.07925 | SL: 1.08015 | Conf: 82.0% | Regime: RANGING
ðŸ“ 2024-03-29 19:00 | SELL RANGE_RIDER  | Price: 1.07885 | SL: 1.07973 | Conf: 82.0% | Regime: RANGING
ðŸ”š 2024-03-29 23:00 | CLOSE RANGE_RIDER  | Price: 1.07973 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-29 23:00 | SELL RANGE_RIDER  | Price: 1.07932 | SL: 1.08009 | Conf: 85.0% | Regime: RANGING

----------------------------------------------------------------------
Backtest simulation complete!
----------------------------------------------------------------------

======================================================================
  BACKTEST PERFORMANCE SUMMARY
======================================================================

ðŸ“Š OVERALL RESULTS:
  Initial Balance:  $10,000.00
  Final Balance:    $9,018.42
  Net Profit:       $-981.58 (-9.82%)

ðŸ“ˆ TRADE STATISTICS:
  Total Trades:     731
  Winning Trades:   366
  Losing Trades:    365
  Win Rate:         50.1%

ðŸ’° R-MULTIPLE ANALYSIS:
  Total R-Multiple: +10.01R
  Average R:        +0.014R
  Best Trade:       +6.44R
  Worst Trade:      -1.00R

âš ï¸  RISK METRICS:
  Max Drawdown:     66.49%
  Current Drawdown: 27.58%
  Profit Factor:    1.03
  Sharpe Ratio:     0.01

ðŸŽ¯ CONSISTENCY METRICS:
  Max Consecutive Wins:   15
  Max Consecutive Losses: 11

======================================================================

Short Backtest
Status: âœ… PASSED
Details: Trades: 731, Total R: +10.01

======================================================================
  TEST 6: Full Year Backtest (2024)
======================================================================
âš ï¸  Running full year backtest, this may take 5-10 minutes...
     (MT5 takes 180 minutes, so this is 20-30x faster!)

======================================================================
  JCAMP BACKTEST ENGINE - EURUSD 2024
======================================================================

ðŸ“Š Preparing data for EURUSD 2024...
ðŸ“‚ Loading EURUSD data from data\EURUSD.sml\2024_M1.csv...
âš ï¸  Info: 270 gaps detected in EURUSD M1 data (weekends/holidays expected)
âœ“ Loaded 372,292 M1 bars for EURUSD
  Date range: 2024-01-02 00:03:00 to 2024-12-31 23:58:00
  Price range: 1.03321 - 1.12142
â±ï¸  Resampling to H1...
D:\JcampFxTrading\jcamp-python-backtesting\src\data_loader.py:149: FutureWarning: 'H' is deprecated and will be removed in a future version, please use 'h' instead.
  resampled = df.resample(rule).agg({
âœ“ Resampled to 6,240 H1 bars
âœ“ Loaded 6,240 H1 bars
ðŸ“ˆ Calculating technical indicators...
ðŸ’ª Calculating Currency Strength Meter...
âœ“ Data preparation complete!


ðŸŽ¯ Testing period: 2024-01-02 to 2024-12-31
ðŸ“Š Total bars: 6,240
ðŸ’° Initial balance: $10,000.00
âš ï¸  Risk per trade: 2.0%
ðŸ“ˆ Max positions: 2

----------------------------------------------------------------------
Starting backtest simulation...
----------------------------------------------------------------------

ðŸ“ 2024-01-08 18:00 | BUY  TREND_RIDER  | Price: 1.09755 | SL: 1.09594 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-01-08 20:00 | CLOSE TREND_RIDER  | Price: 1.09594 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-09 18:00 | SELL TREND_RIDER  | Price: 1.09344 | SL: 1.09510 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ“ 2024-01-09 20:00 | SELL TREND_RIDER  | Price: 1.09242 | SL: 1.09408 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-01-10 09:00 | CLOSE TREND_RIDER  | Price: 1.09408 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-10 11:00 | CLOSE TREND_RIDER  | Price: 1.09510 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-10 20:00 | BUY  TREND_RIDER  | Price: 1.09696 | SL: 1.09548 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ“ 2024-01-10 21:00 | BUY  TREND_RIDER  | Price: 1.09704 | SL: 1.09563 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-01-11 15:00 | CLOSE TREND_RIDER  | Price: 1.09548 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-01-11 15:00 | CLOSE TREND_RIDER  | Price: 1.09563 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-12 14:00 | SELL TREND_RIDER  | Price: 1.09378 | SL: 1.09538 | Conf: 66.7% | Regime: TRANSITIONAL
ðŸ”š 2024-01-12 15:00 | CLOSE TREND_RIDER  | Price: 1.09538 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-15 11:00 | SELL TREND_RIDER  | Price: 1.09469 | SL: 1.09603 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ“ 2024-01-15 12:00 | SELL TREND_RIDER  | Price: 1.09402 | SL: 1.09538 | Conf: 77.8% | Regime: TRANSITIONAL
ðŸ”š 2024-01-15 14:00 | CLOSE TREND_RIDER  | Price: 1.09538 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-16 02:00 | SELL TREND_RIDER  | Price: 1.09198 | SL: 1.09314 | Conf: 85.2% | Regime: TRANSITIONAL
ðŸ”š 2024-01-16 03:00 | CLOSE TREND_RIDER  | Price: 1.09314 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-01-16 03:00 | SELL TREND_RIDER  | Price: 1.09277 | SL: 1.09399 | Conf: 92.6% | Regime: TRANSITIONAL
ðŸ”š 2024-03-07 18:00 | CLOSE TREND_RIDER  | Price: 1.09399 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-07 18:00 | BUY  TREND_RIDER  | Price: 1.09402 | SL: 1.09236 | Conf: 81.5% | Regime: TRANSITIONAL
ðŸ”š 2024-03-08 15:00 | CLOSE TREND_RIDER  | Price: 1.09603 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-08 15:00 | CLOSE TREND_RIDER  | Price: 1.09236 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-08 15:00 | BUY  TREND_RIDER  | Price: 1.09583 | SL: 1.09427 | Conf: 92.6% | Regime: TRANSITIONAL
ðŸ“ 2024-03-08 16:00 | BUY  TREND_RIDER  | Price: 1.09578 | SL: 1.09414 | Conf: 92.6% | Regime: TRANSITIONAL
ðŸ”š 2024-03-08 18:00 | CLOSE TREND_RIDER  | Price: 1.09427 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-08 18:00 | CLOSE TREND_RIDER  | Price: 1.09414 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-11 02:00 | BUY  TREND_RIDER  | Price: 1.09428 | SL: 1.09294 | Conf: 81.5% | Regime: TRANSITIONAL
ðŸ“ 2024-03-11 03:00 | BUY  TREND_RIDER  | Price: 1.09424 | SL: 1.09292 | Conf: 81.5% | Regime: TRANSITIONAL
ðŸ”š 2024-03-11 15:00 | CLOSE TREND_RIDER  | Price: 1.09294 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-11 16:00 | CLOSE TREND_RIDER  | Price: 1.09292 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-12 00:00 | SELL TREND_RIDER  | Price: 1.09263 | SL: 1.09365 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ“ 2024-03-12 01:00 | SELL TREND_RIDER  | Price: 1.09253 | SL: 1.09350 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-03-12 05:00 | CLOSE TREND_RIDER  | Price: 1.09350 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-12 06:00 | CLOSE TREND_RIDER  | Price: 1.09365 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-12 15:00 | SELL TREND_RIDER  | Price: 1.09201 | SL: 1.09315 | Conf: 81.5% | Regime: TRANSITIONAL
ðŸ“ 2024-03-12 16:00 | SELL TREND_RIDER  | Price: 1.09108 | SL: 1.09232 | Conf: 85.2% | Regime: TRANSITIONAL
ðŸ”š 2024-03-12 21:00 | CLOSE TREND_RIDER  | Price: 1.09232 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-13 04:00 | SELL TREND_RIDER  | Price: 1.09239 | SL: 1.09325 | Conf: 85.2% | Regime: TRANSITIONAL
ðŸ”š 2024-03-13 10:00 | CLOSE TREND_RIDER  | Price: 1.09315 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-13 11:00 | CLOSE TREND_RIDER  | Price: 1.09325 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-13 12:00 | SELL TREND_RIDER  | Price: 1.09234 | SL: 1.09318 | Conf: 81.5% | Regime: TRANSITIONAL
ðŸ”š 2024-03-13 13:00 | CLOSE TREND_RIDER  | Price: 1.09318 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-13 15:00 | BUY  TREND_RIDER  | Price: 1.09367 | SL: 1.09267 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ“ 2024-03-13 16:00 | BUY  TREND_RIDER  | Price: 1.09373 | SL: 1.09275 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ”š 2024-03-14 15:00 | CLOSE TREND_RIDER  | Price: 1.09267 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-14 15:00 | CLOSE TREND_RIDER  | Price: 1.09275 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-14 16:00 | SELL TREND_RIDER  | Price: 1.09121 | SL: 1.09231 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ“ 2024-03-14 17:00 | SELL TREND_RIDER  | Price: 1.08978 | SL: 1.09096 | Conf: 81.5% | Regime: TRANSITIONAL
ðŸ”š 2024-03-20 21:00 | CLOSE TREND_RIDER  | Price: 1.09096 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-20 21:00 | BUY  TREND_RIDER  | Price: 1.09144 | SL: 1.09015 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-03-21 00:00 | CLOSE TREND_RIDER  | Price: 1.09231 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-21 00:00 | BUY  TREND_RIDER  | Price: 1.09215 | SL: 1.09089 | Conf: 96.3% | Regime: TRANSITIONAL
ðŸ”š 2024-03-21 11:00 | CLOSE TREND_RIDER  | Price: 1.09015 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-03-21 11:00 | CLOSE TREND_RIDER  | Price: 1.09089 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-03-21 20:00 | SELL TREND_RIDER  | Price: 1.08579 | SL: 1.08742 | Conf: 77.8% | Regime: TRANSITIONAL
ðŸ“ 2024-03-21 21:00 | SELL TREND_RIDER  | Price: 1.08625 | SL: 1.08781 | Conf: 88.9% | Regime: TRANSITIONAL
ðŸ”š 2024-04-04 16:00 | CLOSE TREND_RIDER  | Price: 1.08742 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-04-04 16:00 | BUY  TREND_RIDER  | Price: 1.08699 | SL: 1.08586 | Conf: 100.0% | Regime: TRANSITIONAL
ðŸ”š 2024-04-04 19:00 | CLOSE TREND_RIDER  | Price: 1.08586 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-04-04 19:00 | BUY  TREND_RIDER  | Price: 1.08589 | SL: 1.08478 | Conf: 92.6% | Regime: TRANSITIONAL
ðŸ”š 2024-04-04 21:00 | CLOSE TREND_RIDER  | Price: 1.08478 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-04-05 16:00 | SELL TREND_RIDER  | Price: 1.08012 | SL: 1.08156 | Conf: 77.8% | Regime: TRANSITIONAL
ðŸ”š 2024-04-05 17:00 | CLOSE TREND_RIDER  | Price: 1.08156 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-04-08 17:00 | BUY  TREND_RIDER  | Price: 1.08534 | SL: 1.08405 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-04-09 15:00 | CLOSE TREND_RIDER  | Price: 1.08781 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-04-09 15:00 | BUY  TREND_RIDER  | Price: 1.08805 | SL: 1.08698 | Conf: 77.8% | Regime: TRANSITIONAL
ðŸ”š 2024-04-09 17:00 | CLOSE TREND_RIDER  | Price: 1.08698 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-04-10 15:00 | CLOSE TREND_RIDER  | Price: 1.08405 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-04-10 15:00 | SELL TREND_RIDER  | Price: 1.07809 | SL: 1.07962 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ“ 2024-04-10 16:00 | SELL TREND_RIDER  | Price: 1.07511 | SL: 1.07681 | Conf: 92.6% | Regime: TRANSITIONAL
ðŸ”š 2024-05-03 15:00 | CLOSE TREND_RIDER  | Price: 1.07962 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-05-03 15:00 | CLOSE TREND_RIDER  | Price: 1.07681 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-03 15:00 | BUY  TREND_RIDER  | Price: 1.07937 | SL: 1.07777 | Conf: 100.0% | Regime: TRANSITIONAL
ðŸ”š 2024-05-03 16:00 | CLOSE TREND_RIDER  | Price: 1.07777 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-03 16:00 | BUY  TREND_RIDER  | Price: 1.07770 | SL: 1.07600 | Conf: 100.0% | Regime: TRANSITIONAL
ðŸ”š 2024-05-03 17:00 | CLOSE TREND_RIDER  | Price: 1.07600 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-03 17:00 | BUY  TREND_RIDER  | Price: 1.07659 | SL: 1.07461 | Conf: 100.0% | Regime: TRANSITIONAL
ðŸ“ 2024-05-03 18:00 | BUY  TREND_RIDER  | Price: 1.07692 | SL: 1.07494 | Conf: 92.6% | Regime: TRANSITIONAL
ðŸ”š 2024-05-07 21:00 | CLOSE TREND_RIDER  | Price: 1.07494 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-05-08 04:00 | CLOSE TREND_RIDER  | Price: 1.07461 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-08 05:00 | SELL TREND_RIDER  | Price: 1.07414 | SL: 1.07508 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ“ 2024-05-08 06:00 | SELL TREND_RIDER  | Price: 1.07413 | SL: 1.07505 | Conf: 66.7% | Regime: TRANSITIONAL
ðŸ”š 2024-05-08 12:00 | CLOSE TREND_RIDER  | Price: 1.07508 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-05-08 12:00 | CLOSE TREND_RIDER  | Price: 1.07505 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-09 09:00 | SELL TREND_RIDER  | Price: 1.07375 | SL: 1.07448 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ“ 2024-05-09 10:00 | SELL TREND_RIDER  | Price: 1.07348 | SL: 1.07426 | Conf: 77.8% | Regime: TRANSITIONAL
ðŸ”š 2024-05-09 15:00 | CLOSE TREND_RIDER  | Price: 1.07448 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-05-09 15:00 | CLOSE TREND_RIDER  | Price: 1.07426 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-09 18:00 | BUY  TREND_RIDER  | Price: 1.07704 | SL: 1.07579 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ“ 2024-05-09 19:00 | BUY  TREND_RIDER  | Price: 1.07760 | SL: 1.07637 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ”š 2024-05-10 17:00 | CLOSE TREND_RIDER  | Price: 1.07637 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-13 12:00 | BUY  TREND_RIDER  | Price: 1.07829 | SL: 1.07742 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-05-14 15:00 | CLOSE TREND_RIDER  | Price: 1.07742 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-15 15:00 | BUY  TREND_RIDER  | Price: 1.08613 | SL: 1.08498 | Conf: 85.2% | Regime: TRANSITIONAL
ðŸ”š 2024-05-15 16:00 | CLOSE TREND_RIDER  | Price: 1.08498 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-15 16:00 | BUY  TREND_RIDER  | Price: 1.08351 | SL: 1.08215 | Conf: 85.2% | Regime: TRANSITIONAL
ðŸ”š 2024-05-22 21:00 | CLOSE TREND_RIDER  | Price: 1.08215 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-22 21:00 | SELL TREND_RIDER  | Price: 1.08214 | SL: 1.08329 | Conf: 88.9% | Regime: TRANSITIONAL
ðŸ”š 2024-05-23 10:00 | CLOSE TREND_RIDER  | Price: 1.08329 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-23 10:00 | SELL TREND_RIDER  | Price: 1.08292 | SL: 1.08387 | Conf: 88.9% | Regime: TRANSITIONAL
ðŸ”š 2024-05-23 11:00 | CLOSE TREND_RIDER  | Price: 1.08387 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-23 16:00 | SELL TREND_RIDER  | Price: 1.08344 | SL: 1.08470 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-05-24 15:00 | CLOSE TREND_RIDER  | Price: 1.08470 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-24 16:00 | BUY  TREND_RIDER  | Price: 1.08427 | SL: 1.08316 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-05-29 11:00 | CLOSE TREND_RIDER  | Price: 1.08316 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-29 11:00 | SELL TREND_RIDER  | Price: 1.08372 | SL: 1.08473 | Conf: 85.2% | Regime: TRANSITIONAL
ðŸ”š 2024-05-29 12:00 | CLOSE TREND_RIDER  | Price: 1.08473 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-29 12:00 | SELL TREND_RIDER  | Price: 1.08517 | SL: 1.08627 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-05-31 15:00 | CLOSE TREND_RIDER  | Price: 1.08627 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-31 15:00 | BUY  TREND_RIDER  | Price: 1.08803 | SL: 1.08679 | Conf: 96.3% | Regime: TRANSITIONAL
ðŸ”š 2024-05-31 16:00 | CLOSE TREND_RIDER  | Price: 1.08679 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-31 16:00 | BUY  TREND_RIDER  | Price: 1.08691 | SL: 1.08563 | Conf: 96.3% | Regime: TRANSITIONAL
ðŸ”š 2024-05-31 17:00 | CLOSE TREND_RIDER  | Price: 1.08563 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-31 17:00 | BUY  TREND_RIDER  | Price: 1.08557 | SL: 1.08415 | Conf: 88.9% | Regime: TRANSITIONAL
ðŸ”š 2024-05-31 19:00 | CLOSE TREND_RIDER  | Price: 1.08415 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-05-31 19:00 | BUY  TREND_RIDER  | Price: 1.08474 | SL: 1.08327 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ”š 2024-06-03 12:00 | CLOSE TREND_RIDER  | Price: 1.08327 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-03 17:00 | BUY  TREND_RIDER  | Price: 1.08702 | SL: 1.08571 | Conf: 85.2% | Regime: TRANSITIONAL
ðŸ”š 2024-06-05 19:00 | CLOSE TREND_RIDER  | Price: 1.08571 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-06 04:00 | BUY  TREND_RIDER  | Price: 1.08942 | SL: 1.08842 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-06-06 08:00 | CLOSE TREND_RIDER  | Price: 1.08842 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-06 20:00 | BUY  TREND_RIDER  | Price: 1.08924 | SL: 1.08789 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-06-07 15:00 | CLOSE TREND_RIDER  | Price: 1.08789 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-07 16:00 | SELL TREND_RIDER  | Price: 1.08195 | SL: 1.08360 | Conf: 81.5% | Regime: TRANSITIONAL
ðŸ”š 2024-06-10 06:00 | CLOSE TREND_RIDER  | Price: 1.07579 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-10 06:00 | SELL TREND_RIDER  | Price: 1.07556 | SL: 1.07696 | Conf: 100.0% | Regime: TRANSITIONAL
ðŸ”š 2024-06-11 07:00 | CLOSE TREND_RIDER  | Price: 1.07696 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-11 11:00 | SELL TREND_RIDER  | Price: 1.07454 | SL: 1.07559 | Conf: 85.2% | Regime: TRANSITIONAL
ðŸ”š 2024-06-11 13:00 | CLOSE TREND_RIDER  | Price: 1.07559 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-11 14:00 | SELL TREND_RIDER  | Price: 1.07292 | SL: 1.07417 | Conf: 96.3% | Regime: TRANSITIONAL
ðŸ”š 2024-06-11 20:00 | CLOSE TREND_RIDER  | Price: 1.07417 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-11 20:00 | SELL TREND_RIDER  | Price: 1.07424 | SL: 1.07549 | Conf: 77.8% | Regime: TRANSITIONAL
ðŸ”š 2024-06-12 13:00 | CLOSE TREND_RIDER  | Price: 1.07549 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-12 15:00 | BUY  TREND_RIDER  | Price: 1.08267 | SL: 1.08119 | Conf: 81.5% | Regime: TRANSITIONAL
ðŸ”š 2024-06-12 16:00 | CLOSE TREND_RIDER  | Price: 1.08360 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-12 16:00 | BUY  TREND_RIDER  | Price: 1.08367 | SL: 1.08214 | Conf: 85.2% | Regime: TRANSITIONAL
ðŸ”š 2024-06-12 17:00 | CLOSE TREND_RIDER  | Price: 1.08214 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-12 17:00 | BUY  TREND_RIDER  | Price: 1.08480 | SL: 1.08310 | Conf: 85.2% | Regime: TRANSITIONAL
ðŸ”š 2024-06-12 21:00 | CLOSE TREND_RIDER  | Price: 1.08119 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-06-12 21:00 | CLOSE TREND_RIDER  | Price: 1.08310 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-12 21:00 | BUY  TREND_RIDER  | Price: 1.08120 | SL: 1.07943 | Conf: 92.6% | Regime: TRANSITIONAL
ðŸ“ 2024-06-12 22:00 | BUY  TREND_RIDER  | Price: 1.08066 | SL: 1.07889 | Conf: 85.2% | Regime: TRANSITIONAL
ðŸ”š 2024-06-13 13:00 | CLOSE TREND_RIDER  | Price: 1.07943 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-06-13 14:00 | CLOSE TREND_RIDER  | Price: 1.07889 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-13 19:00 | SELL TREND_RIDER  | Price: 1.07353 | SL: 1.07536 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ“ 2024-06-13 20:00 | SELL TREND_RIDER  | Price: 1.07425 | SL: 1.07602 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ”š 2024-06-18 17:00 | CLOSE TREND_RIDER  | Price: 1.07536 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-06-18 17:00 | CLOSE TREND_RIDER  | Price: 1.07602 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-18 17:00 | BUY  TREND_RIDER  | Price: 1.07384 | SL: 1.07253 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ“ 2024-06-18 18:00 | BUY  TREND_RIDER  | Price: 1.07385 | SL: 1.07256 | Conf: 81.5% | Regime: TRANSITIONAL
ðŸ”š 2024-06-19 10:00 | CLOSE TREND_RIDER  | Price: 1.07253 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-06-19 10:00 | CLOSE TREND_RIDER  | Price: 1.07256 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-19 14:00 | BUY  TREND_RIDER  | Price: 1.07510 | SL: 1.07408 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-06-20 05:00 | CLOSE TREND_RIDER  | Price: 1.07408 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-20 11:00 | SELL TREND_RIDER  | Price: 1.07169 | SL: 1.07248 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ”š 2024-06-20 12:00 | CLOSE TREND_RIDER  | Price: 1.07248 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-20 12:00 | SELL TREND_RIDER  | Price: 1.07254 | SL: 1.07340 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ“ 2024-06-20 13:00 | SELL TREND_RIDER  | Price: 1.07287 | SL: 1.07373 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ”š 2024-06-24 14:00 | CLOSE TREND_RIDER  | Price: 1.07340 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-24 14:00 | BUY  TREND_RIDER  | Price: 1.07359 | SL: 1.07249 | Conf: 81.5% | Regime: TRANSITIONAL
ðŸ”š 2024-06-24 16:00 | CLOSE TREND_RIDER  | Price: 1.07373 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-24 16:00 | BUY  TREND_RIDER  | Price: 1.07429 | SL: 1.07318 | Conf: 88.9% | Regime: TRANSITIONAL
ðŸ”š 2024-06-24 17:00 | CLOSE TREND_RIDER  | Price: 1.07318 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-24 17:00 | BUY  TREND_RIDER  | Price: 1.07301 | SL: 1.07182 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ”š 2024-06-24 18:00 | CLOSE TREND_RIDER  | Price: 1.07249 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-24 18:00 | BUY  TREND_RIDER  | Price: 1.07272 | SL: 1.07153 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ”š 2024-06-25 14:00 | CLOSE TREND_RIDER  | Price: 1.07182 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-06-25 14:00 | CLOSE TREND_RIDER  | Price: 1.07153 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-25 15:00 | SELL TREND_RIDER  | Price: 1.07052 | SL: 1.07154 | Conf: 66.7% | Regime: TRANSITIONAL
ðŸ“ 2024-06-25 16:00 | SELL TREND_RIDER  | Price: 1.07027 | SL: 1.07133 | Conf: 66.7% | Regime: TRANSITIONAL
ðŸ”š 2024-06-25 20:00 | CLOSE TREND_RIDER  | Price: 1.07133 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-25 20:00 | SELL TREND_RIDER  | Price: 1.07137 | SL: 1.07245 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-06-25 21:00 | CLOSE TREND_RIDER  | Price: 1.07154 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-26 01:00 | SELL TREND_RIDER  | Price: 1.07124 | SL: 1.07213 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ”š 2024-06-27 15:00 | CLOSE TREND_RIDER  | Price: 1.07213 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-06-27 16:00 | CLOSE TREND_RIDER  | Price: 1.07245 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-27 16:00 | BUY  TREND_RIDER  | Price: 1.07206 | SL: 1.07084 | Conf: 74.1% | Regime: TRANSITIONAL
ðŸ”š 2024-06-27 17:00 | CLOSE TREND_RIDER  | Price: 1.07084 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-27 17:00 | BUY  TREND_RIDER  | Price: 1.07126 | SL: 1.06997 | Conf: 66.7% | Regime: TRANSITIONAL
ðŸ”š 2024-06-28 03:00 | CLOSE TREND_RIDER  | Price: 1.06997 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-28 07:00 | SELL TREND_RIDER  | Price: 1.06868 | SL: 1.06969 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ“ 2024-06-28 08:00 | SELL TREND_RIDER  | Price: 1.06904 | SL: 1.07003 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-06-28 09:00 | CLOSE TREND_RIDER  | Price: 1.06969 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-06-28 10:00 | CLOSE TREND_RIDER  | Price: 1.07003 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-06-28 20:00 | BUY  TREND_RIDER  | Price: 1.07145 | SL: 1.07002 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ“ 2024-07-01 00:00 | BUY  TREND_RIDER  | Price: 1.07396 | SL: 1.07246 | Conf: 85.2% | Regime: TRANSITIONAL
ðŸ”š 2024-07-01 18:00 | CLOSE TREND_RIDER  | Price: 1.07246 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-07-03 01:00 | BUY  TREND_RIDER  | Price: 1.07491 | SL: 1.07392 | Conf: 70.4% | Regime: TRANSITIONAL
ðŸ”š 2024-07-03 08:00 | CLOSE TREND_RIDER  | Price: 1.07392 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-07-03 10:00 | BUY  TREND_RIDER  | Price: 1.07597 | SL: 1.07505 | Conf: 77.8% | Regime: TRANSITIONAL
ðŸ”š 2024-11-06 05:00 | CLOSE TREND_RIDER  | Price: 1.07505 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-11-06 05:00 | SELL TREND_RIDER  | Price: 1.07469 | SL: 1.07774 | Conf: 100.0% | Regime: TRANSITIONAL
ðŸ”š 2024-11-06 06:00 | CLOSE TREND_RIDER  | Price: 1.07774 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-11-06 06:00 | SELL TREND_RIDER  | Price: 1.07779 | SL: 1.08104 | Conf: 100.0% | Regime: TRANSITIONAL
ðŸ”š 2024-11-06 14:00 | CLOSE TREND_RIDER  | Price: 1.07002 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-11-06 14:00 | SELL TREND_RIDER  | Price: 1.06886 | SL: 1.07267 | Conf: 100.0% | Regime: TRANSITIONAL
ðŸ”š 2024-11-06 17:00 | CLOSE TREND_RIDER  | Price: 1.07267 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-11-06 17:00 | SELL TREND_RIDER  | Price: 1.07384 | SL: 1.07756 | Conf: 100.0% | Regime: TRANSITIONAL
ðŸ”š 2024-11-07 14:00 | CLOSE TREND_RIDER  | Price: 1.07756 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-11-07 16:00 | CLOSE TREND_RIDER  | Price: 1.08104 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-11-07 16:00 | BUY  TREND_RIDER  | Price: 1.08092 | SL: 1.07844 | Conf: 66.7% | Regime: TRANSITIONAL
ðŸ“ 2024-11-07 17:00 | BUY  TREND_RIDER  | Price: 1.08110 | SL: 1.07863 | Conf: 66.7% | Regime: TRANSITIONAL
ðŸ”š 2024-11-07 18:00 | CLOSE TREND_RIDER  | Price: 1.07863 | R: -1.00 | Exit: STOP_LOSS
ðŸ”š 2024-11-07 21:00 | CLOSE TREND_RIDER  | Price: 1.07844 | R: -1.00 | Exit: STOP_LOSS
ðŸ“ 2024-11-08 15:00 | SELL TREND_RIDER  | Price: 1.07532 | SL: 1.07731 | Conf: 77.8% | Regime: TRANSITIONAL
ðŸ“ 2024-11-08 16:00 | SELL TREND_RIDER  | Price: 1.07517 | SL: 1.07716 | Conf: 85.2% | Regime: TRANSITIONAL

----------------------------------------------------------------------
Backtest simulation complete!
----------------------------------------------------------------------

======================================================================
  BACKTEST PERFORMANCE SUMMARY
======================================================================

ðŸ“Š OVERALL RESULTS:
  Initial Balance:  $10,000.00
  Final Balance:    $1,238.97
  Net Profit:       $-8,761.03 (-87.61%)

ðŸ“ˆ TRADE STATISTICS:
  Total Trades:     102
  Winning Trades:   0
  Losing Trades:    102
  Win Rate:         0.0%

ðŸ’° R-MULTIPLE ANALYSIS:
  Total R-Multiple: -102.00R
  Average R:        -1.000R
  Best Trade:       -1.00R
  Worst Trade:      -1.00R

âš ï¸  RISK METRICS:
  Max Drawdown:     87.61%
  Current Drawdown: 87.61%
  Profit Factor:    0.00
  Sharpe Ratio:     0.00

ðŸŽ¯ CONSISTENCY METRICS:
  Max Consecutive Wins:   0
  Max Consecutive Losses: 102

======================================================================

  Trend Rider: -102.00R (0/102)

  ðŸ“Š Comparing to MT5 v1.96 baseline...

======================================================================
  COMPARISON TO MT5 BASELINE
======================================================================

ðŸ“Š KEY METRICS:
                    Python      MT5         Difference
  Total R:          -102.00R    +16.03R   -118.03R
  Trades:               102         149         -47
  Win Rate:            0.0%      52.0%     -52.0%

âœ… R-Multiple Match: -636.3%
âœ… Trade Count Match: 68.5%

âš ï¸  Results differ from MT5 - investigate discrepancies
======================================================================

Full Year Backtest
Status: âœ… PASSED
Details: Completed! Total R: -102.00, Trades: 102, Win Rate: 0.0%

======================================================================
  TEST 7: MT5 Baseline Comparison
======================================================================

======================================================================
  COMPARISON TO MT5 BASELINE
======================================================================

ðŸ“Š KEY METRICS:
                    Python      MT5         Difference
  Total R:            +0.77R    +16.03R    -15.26R
  Trades:               149         149          +0
  Win Rate:           52.3%      52.0%      +0.3%

âœ… R-Multiple Match: 4.8%
âœ… Trade Count Match: 100.0%

âš ï¸  Results differ from MT5 - investigate discrepancies
======================================================================

MT5 Baseline Comparison
Status: âœ… PASSED
Details: Comparison logic working correctly

======================================================================
  TEST SUMMARY
======================================================================
âŒ FAILED - Test 1: Position Manager
âœ… PASSED - Test 2: Performance Tracker
âœ… PASSED - Test 3: Engine Init
âœ… PASSED - Test 4: Data Preparation
âœ… PASSED - Test 5: Short Backtest
âœ… PASSED - Test 6: Full Year Backtest
âœ… PASSED - Test 7: MT5 Comparison

======================================================================
PHASE 4 RESULTS: 6/7 tests passing (85.7%)
======================================================================

âš ï¸  1 test(s) failed - review and fix
(venv) PS D:\JcampFxTrading\jcamp-python-backtesting>