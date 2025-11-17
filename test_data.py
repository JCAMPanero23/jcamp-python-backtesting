import pandas as pd
import os

print("=== EURUSD DATA CHECK (FIXED) ===")

# Load with TAB delimiter
df = pd.read_csv("data/EURUSD_sml/2024_M1.csv", sep='\t')

print(f"\n=== FILE STRUCTURE ===")
print(f"Columns: {df.columns.tolist()}")
print(f"Rows: {len(df):,}")

print(f"\n=== FIRST 5 ROWS ===")
print(df.head())

print(f"\n=== DATA TYPES ===")
print(df.dtypes)

print(f"\n=== DATE RANGE ===")
print(f"Start: {df['<DATE>'].iloc[0]} {df['<TIME>'].iloc[0]}")
print(f"End: {df['<DATE>'].iloc[-1]} {df['<TIME>'].iloc[-1]}")

print(f"\n=== SAMPLE VALUES ===")
print(f"OPEN range: {df['<OPEN>'].min()} - {df['<OPEN>'].max()}")
print(f"HIGH range: {df['<HIGH>'].min()} - {df['<HIGH>'].max()}")
print(f"LOW range: {df['<LOW>'].min()} - {df['<LOW>'].max()}")
print(f"CLOSE range: {df['<CLOSE>'].min()} - {df['<CLOSE>'].max()}")