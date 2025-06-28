#!/usr/bin/env python3

import pandas as pd
import os

def test_csv_loading():
    print("=== Testing CSV Loading ===")
    
    csv_files = ["driver_stats.csv", "../Scraper/driver_stats.csv"]
    
    for csv_file in csv_files:
        print(f"\nTesting: {csv_file}")
        print(f"File exists: {os.path.exists(csv_file)}")
        
        if os.path.exists(csv_file):
            try:
                print(f"Current directory: {os.getcwd()}")
                print(f"Full path: {os.path.abspath(csv_file)}")
                
                df = pd.read_csv(csv_file)
                print(f"✅ Loaded successfully!")
                print(f"Shape: {df.shape}")
                print(f"Columns: {list(df.columns)}")
                
                # Clean columns like FastAPI does
                df.columns = df.columns.str.strip().str.lower().str.replace('.', '', regex=False)
                print(f"Cleaned columns: {list(df.columns)}")
                
                if 'season' in df.columns:
                    seasons = sorted(df['season'].unique())
                    print(f"Available seasons: {seasons}")
                    
                    # Check 2024 data specifically
                    data_2024 = df[df['season'] == 2024]
                    print(f"2024 records: {len(data_2024)}")
                    
                    if len(data_2024) > 0:
                        print("2024 sample:")
                        print(data_2024[['driver', 'team', 'pts']].head())
                else:
                    print("❌ No 'season' column found!")
                
                return df
                
            except Exception as e:
                print(f"❌ Error loading: {e}")
                import traceback
                traceback.print_exc()
    
    return None

if __name__ == "__main__":
    historical_data = test_csv_loading()
    
    if historical_data is not None:
        print(f"\n✅ CSV loading works!")
        print(f"Total records: {len(historical_data)}")
    else:
        print(f"\n❌ CSV loading failed!")
