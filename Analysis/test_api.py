#!/usr/bin/env python3

import pandas as pd
import os
import json

# Test the exact logic that FastAPI uses
def test_historical_lookup():
    print("=== Testing Historical Data Lookup ===")
    
    # Load data exactly like FastAPI does
    csv_files = ['driver_stats.csv', '../Scraper/driver_stats.csv']
    historical_data = None
    
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            historical_data = pd.read_csv(csv_file)
            historical_data.columns = historical_data.columns.str.strip().str.lower().str.replace('.', '', regex=False)
            print(f"✅ Historical data loaded from {csv_file}")
            break
    
    if historical_data is None:
        print("❌ No historical data found")
        return None
    
    print(f"Columns: {historical_data.columns.tolist()}")
    
    # Test case: 2024 Lewis Hamilton Mercedes
    season = 2024
    driver_name = "Lewis Hamilton"
    team_encoded = 1  # Mercedes
    
    print(f"\n=== Testing: {season} {driver_name} (team_encoded={team_encoded}) ===")
    
    # Filter by season
    season_data = historical_data[historical_data['season'] == season]
    print(f"Found {len(season_data)} records for season {season}")
    
    if season_data.empty:
        print(f"❌ No data found for season {season}")
        return None
    
    # Driver search
    if driver_name:
        first_name = driver_name.split()[0]  # 'Lewis'
        print(f"Searching for first name: '{first_name}'")
        
        driver_matches = season_data[season_data['driver'].str.contains(first_name, case=False, na=False)]
        print(f"Driver matches found: {len(driver_matches)}")
        
        if not driver_matches.empty:
            print("\nMatches:")
            for idx, row in driver_matches.iterrows():
                print(f"  - {row['driver']} ({row['team']}) - {row['pts']} points")
            
            # Get first match
            result = driver_matches.iloc[0]
            print(f"\n✅ Selected result: {result['driver']} - {result['pts']} points")
            
            return {
                'position': int(result.get('pos', 0)) if pd.notna(result.get('pos')) and str(result.get('pos')).isdigit() else None,
                'points': float(result.get('pts', 0)) if pd.notna(result.get('pts')) else 0.0,
                'driver': result.get('driver'),
                'team': result.get('team', ''),
                'season': season
            }
    
    print("❌ No driver match found")
    return None

if __name__ == "__main__":
    result = test_historical_lookup()
    if result:
        print(f"\n=== Final Result ===")
        print(json.dumps(result, indent=2))
    else:
        print("\n❌ No historical result found")
