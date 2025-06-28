#!/usr/bin/env python3

# Test the core logic that's failing
def test_year_comparison():
    print("=== Testing Year Comparison Logic ===")
    
    # Test cases
    test_cases = [
        (2022, "should be historical"),
        (2023, "should be historical"), 
        (2024, "should be historical"),
        (2025, "should NOT be historical"),
        (2026, "should NOT be historical")
    ]
    
    current_year = 2025
    
    for season, expected in test_cases:
        # Test the exact logic from FastAPI
        is_historical = season < current_year
        status = "✅ CORRECT" if (is_historical and "should be" in expected) or (not is_historical and "should NOT" in expected) else "❌ WRONG"
        
        print(f"Season {season}: is_historical = {is_historical} ({expected}) {status}")

def test_team_mapping():
    print("\n=== Testing Team Mapping ===")
    
    team_mapping = {
        "Red Bull Racing": 0, "Mercedes": 1, "Ferrari": 2, "McLaren": 3,
        "Aston Martin": 4, "Alpine": 5, "Haas": 6, "RB": 7,
        "Williams": 8, "Kick Sauber": 9, "AlphaTauri": 7, "Alfa Romeo": 9
    }
    
    def get_team_name(team_encoded):
        print(f"Looking for team_encoded = {team_encoded}")
        for team, encoding in team_mapping.items():
            if encoding == team_encoded:
                print(f"Found: {team}")
                return team
        print(f"Not found, returning default: Team {team_encoded}")
        return f"Team {team_encoded}"
    
    # Test cases
    test_cases = [1, 2, 3, 0, 99]  # Mercedes, Ferrari, McLaren, Red Bull, Invalid
    
    for team_encoded in test_cases:
        result = get_team_name(team_encoded)
        print(f"team_encoded {team_encoded} -> '{result}'")

def test_request_simulation():
    print("\n=== Simulating FastAPI Request Processing ===")
    
    # Simulate the exact data from your test
    class MockRequest:
        def __init__(self, season, team_encoded, driver_name, race_name):
            self.season = season
            self.team_encoded = team_encoded
            self.driver_name = driver_name
            self.race_name = race_name
    
    # Your test case: 2022 Sergio Perez
    request = MockRequest(2022, 0, "Sergio Perez", "Italian Grand Prix")  # Red Bull = 0
    
    print(f"Request: season={request.season}, team_encoded={request.team_encoded}, driver={request.driver_name}")
    
    # Test the year logic
    current_year = 2025
    is_historical = request.season < current_year
    print(f"Year comparison: {request.season} < {current_year} = {is_historical}")
    
    # Test team mapping
    team_mapping = {
        "Red Bull Racing": 0, "Mercedes": 1, "Ferrari": 2, "McLaren": 3,
        "Aston Martin": 4, "Alpine": 5, "Haas": 6, "RB": 7,
        "Williams": 8, "Kick Sauber": 9, "AlphaTauri": 7, "Alfa Romeo": 9
    }
    
    team_name = None
    for team, encoding in team_mapping.items():
        if encoding == request.team_encoded:
            team_name = team
            break
    
    print(f"Team mapping: {request.team_encoded} -> '{team_name}'")
    
    print(f"\nExpected results:")
    print(f"  - is_historical: True (2022 < 2025)")
    print(f"  - team_name: 'Red Bull Racing'")
    print(f"  - predicted_pts: some positive number")

if __name__ == "__main__":
    test_year_comparison()
    test_team_mapping()
    test_request_simulation()
