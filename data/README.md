# Historical Data Directory

This directory contains historical forex data for backtesting.

## Directory Structure

```
data/
|-- EURUSD_sml/      # EURUSD historical data
|-- GBPUSD_sml/      # GBPUSD historical data
|-- USDJPY_sml/      # USDJPY historical data
|-- EURJPY/          # EURJPY historical data
|-- AUDUSD_sml/      # AUDUSD historical data
|-- USDCHF/          # USDCHF historical data
|-- GBPJPY_sml/      # GBPJPY historical data
```

## Data Format

### CSV Format (M1 Bars)

```
<DATE>    <TIME>     <OPEN>   <HIGH>   <LOW>    <CLOSE>  <TICKVOL> <VOL> <SPREAD>
2024.01.01 00:00:00  1.10450  1.10520  1.10430  1.10500  1000      0     15
2024.01.01 00:01:00  1.10500  1.10580  1.10490  1.10550  1200      0     16
```

### Required Fields

- `DATE`: Trading date (YYYY.MM.DD)
- `TIME`: Bar time (HH:MM:SS)
- `OPEN`: Opening price (5 decimals for most pairs)
- `HIGH`: Highest price in bar
- `LOW`: Lowest price in bar
- `CLOSE`: Closing price
- `TICKVOL`: Tick volume
- `VOL`: Real volume (usually 0 for forex)
- `SPREAD`: Spread in points

## How to Export from MT5

1. Open MT5 terminal
2. Go to Tools > History Center (F2)
3. Select symbol (e.g., EURUSD.sml)
4. Select M1 timeframe
5. Click "Export" button
6. Save as CSV format
7. Place in appropriate directory

## File Naming Convention

- `SYMBOL_TIMEFRAME_STARTDATE_ENDDATE.csv`
- Example: `EURUSD_sml_M1_20240101_20241231.csv`

Or simply:
- `2024_M1.csv` (inside symbol directory)

## Notes

- Data files are gitignored due to size
- Keep at least full year 2024 data for validation
- M1 data will be converted to H1, M15, M5 automatically
- Ensure no gaps in data for accurate backtesting
