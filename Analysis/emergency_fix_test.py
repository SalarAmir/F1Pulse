#!/usr/bin/env python3

"""
Emergency fix test - Direct testing of the prediction fix
"""

import requests
import json
import time

def test_zero_fix():
    """Test the exact failing scenario"""
    print("🚨 EMERGENCY FIX TEST")
    print("="*50)
    
    # Your exact failing case
    test_case = {
        "season": 2023,
        "team_encoded": 0,  # Red Bull Racing
        "driver_name": "Max Verstappen",
        "race_name": "Singapore Grand Prix",
        "driver_experience": 7
    }
    
    print("Testing case that was returning zeros:")
    print(json.dumps(test_case, indent=2))
    
    try:
        response = requests.post("http://localhost:8000/predict", json=test_case, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Response received:")
            print(json.dumps(result, indent=2))
            
            # Check the exact issues
            position = result.get('predicted_position', 0)
            confidence = result.get('prediction_confidence', 0)
            
            if position == 0:
                print(f"\n❌ STILL BROKEN: Position is {position}")
                return False
            elif confidence == 0:
                print(f"\n❌ STILL BROKEN: Confidence is {confidence}")
                return False
            else:
                print(f"\n✅ FIXED: Position = {position}, Confidence = {confidence:.3f}")
                return True
        else:
            print(f"\n❌ HTTP Error: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API - is it running?")
        print("Start it with: python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_multiple_cases():
    """Test multiple cases to ensure consistency"""
    print("\n🧪 Testing multiple cases...")
    
    test_cases = [
        {"season": 2023, "team_encoded": 0, "driver_name": "Max Verstappen", "driver_experience": 7},
        {"season": 2024, "team_encoded": 1, "driver_name": "Lewis Hamilton", "driver_experience": 17},
        {"season": 2025, "team_encoded": 2, "driver_name": "Charles Leclerc", "driver_experience": 8},
        {"season": 2022, "team_encoded": 3, "driver_name": "Lando Norris", "driver_experience": 5},
    ]
    
    all_passed = True
    
    for i, case in enumerate(test_cases, 1):
        try:
            response = requests.post("http://localhost:8000/predict", json=case, timeout=5)
            if response.status_code == 200:
                result = response.json()
                pos = result.get('predicted_position', 0)
                conf = result.get('prediction_confidence', 0)
                
                if pos > 0 and conf > 0:
                    print(f"Test {i}: ✅ P{pos}, {conf:.3f}")
                else:
                    print(f"Test {i}: ❌ P{pos}, {conf:.3f}")
                    all_passed = False
            else:
                print(f"Test {i}: ❌ HTTP {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"Test {i}: ❌ {e}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    # Test the main failing case
    main_test_passed = test_zero_fix()
    
    if main_test_passed:
        # Test multiple cases
        multiple_tests_passed = test_multiple_cases()
        
        if multiple_tests_passed:
            print(f"\n🎉 ALL TESTS PASSED - Zero value issue is FIXED!")
        else:
            print(f"\n⚠️ Main test passed but some additional tests failed")
    else:
        print(f"\n🚨 MAIN TEST FAILED - Issue still exists")
        print("\nTroubleshooting steps:")
        print("1. Restart the API server")
        print("2. Check the API logs for errors")
        print("3. Delete any old .joblib files and restart")
