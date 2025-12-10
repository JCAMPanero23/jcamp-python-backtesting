#!/usr/bin/env python3
"""
Regime & CSM Validation Exporter
Exports Python regime detection and CSM values for comparison with MT5 EA
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

# Add src and config to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'config'))

from data_loader import DataLoader
from regime_detector import RegimeDetector, RegimeType
from csm_calculator import CSMCalculator
from indicators import TechnicalIndicators
from mt5_settings import *

class ValidationExporter:
    """Export regime and CSM data for validation"""

    def __init__(self, output_file: str = "validation_output_python.csv"):
        self.output_file = output_file
        self.data_loader = DataLoader()
        self.regime_detector = RegimeDetector()
        self.csm_calculator = CSMCalculator()
        self.indicators = TechnicalIndicators()

    def export_regime_csm_data(self,
                               pair: str = 'EURUSD',
                               year: int = 2024,
                               start_date: str = '2024-12-02',
                               end_date: str = '2024-12-06'):
        """
        Export regime and CSM data for validation

        Args:
            pair: Currency pair (e.g., 'EURUSD')
            year: Year to load
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        """

        print(f"\n{'='*80}")
        print(f"REGIME & CSM VALIDATION EXPORT")
        print(f"Pair: {pair}, Period: {start_date} to {end_date}")
        print(f"{'='*80}\n")

        # Load M1 data
        print("[1/5] Loading M1 data...")
        df_m1 = self.data_loader.load_pair_data(pair, year)

        # Filter date range
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        df_m1 = df_m1[(df_m1.index >= start) & (df_m1.index <= end)]
        print(f"  Filtered to {len(df_m1)} M1 bars")

        # Resample to H1
        print("[2/5] Resampling to H1...")
        df_h1 = self.data_loader.resample_to_timeframe(df_m1, 'H1')

        # Calculate indicators on H1
        print("[3/5] Calculating indicators...")
        indicator_dict = self.indicators.calculate_all_indicators(df_h1)

        # Merge indicator results back into dataframe
        for col_name, col_values in indicator_dict.items():
            if isinstance(col_values, pd.Series):
                df_h1[col_name] = col_values
            elif isinstance(col_values, (list, np.ndarray)):
                df_h1[col_name] = col_values

        # Initialize output list
        validation_rows = []

        # Process each H1 bar
        print("[4/5] Extracting regime and CSM for each bar...")

        for idx, (timestamp, row) in enumerate(df_h1.iterrows()):
            # Create dataframe up to current bar for regime detection
            df_to_current = df_h1.iloc[:idx+1]

            # Detect regime
            regime = self.regime_detector.detect_regime(df_to_current, idx)

            # Get component scores (if available from detector)
            regime_type = regime.value if hasattr(regime, 'value') else str(regime)

            # Calculate CSM
            pair_data = {pair: df_to_current}
            csm_valid = self.csm_calculator.update_csm(pair_data, timestamp)
            csm_values = self.csm_calculator.currency_strengths if csm_valid else {}

            # Build row
            row_data = {
                'DateTime': timestamp.strftime('%Y.%m.%d %H:%M'),
                'Regime': regime_type,
                'ADXScore': row.get('adx', np.nan),
                'EMAScore': row.get('ema_alignment', np.nan),
                'ATRScore': row.get('atr_score', np.nan),
                'PriceActionScore': row.get('price_action', np.nan),
                'CSM_EUR': csm_values.get('EUR', np.nan),
                'CSM_USD': csm_values.get('USD', np.nan),
                'CSM_GBP': csm_values.get('GBP', np.nan),
                'CSM_JPY': csm_values.get('JPY', np.nan),
                'CSM_CHF': csm_values.get('CHF', np.nan),
                'CSM_AUD': csm_values.get('AUD', np.nan),
                'CSM_CAD': csm_values.get('CAD', np.nan),
                'CSM_NZD': csm_values.get('NZD', np.nan),
            }
            validation_rows.append(row_data)

            if (idx + 1) % 24 == 0:
                print(f"  Processed {idx + 1} bars...")

        # Convert to DataFrame and save
        print(f"[5/5] Saving to {self.output_file}...")
        df_output = pd.DataFrame(validation_rows)
        df_output.to_csv(self.output_file, index=False)

        print(f"\n✅ Export complete!")
        print(f"  Output file: {self.output_file}")
        print(f"  Total bars: {len(df_output)}")
        print(f"  Date range: {df_output['DateTime'].iloc[0]} to {df_output['DateTime'].iloc[-1]}")

        return df_output


def main():
    exporter = ValidationExporter(
        output_file="data/validation_output_python.csv"
    )

    # Export validation data for Dec 2-6, 2024 (Monday-Friday business week)
    df = exporter.export_regime_csm_data(
        pair='EURUSD',
        year=2024,
        start_date='2024-12-02',
        end_date='2024-12-06'
    )

    # Show summary
    print(f"\n{'='*80}")
    print("VALIDATION DATA SUMMARY")
    print(f"{'='*80}")
    print(df.head(10))
    print(f"\n...{len(df)} total rows...")
    print(df.tail(10))


if __name__ == "__main__":
    main()