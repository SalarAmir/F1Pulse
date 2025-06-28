#!/usr/bin/env python3

"""
Test the exact failing case: Lance Stroll Aston Martin 2023
"""

import requests
import json

def test_lance_stroll_case():
    """Test the exact case that was failing"""
    print("🏎️ Testing Lance Stroll Aston Martin 2023 Case")
    print("="*50)
    
    test_case = {
        "season": 2023,
        "team_encoded": 4,  # Aston Martin
        "driver_name": "Lance Stroll", 
        "race_name": "Monaco Grand Prix",
        "driver_experience": 6
    }
    
    print("Request:")
    print(json.dumps(test_case, indent=2))
    
    try:
        response = requests.post("http://localhost:8000/predict", json=test_case, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Response:")
            print(json.dumps(result, indent=2))
            
            position = result.get('predicted_position', 0)
            confidence = result.get('prediction_confidence', 0)
            
            print(f"\n📊 Results Analysis:")
            print(f"Position: {position} (Expected: 6-8 for Aston Martin)")
            print(f"Confidence: {confidence:.3f} (Expected: > 0.0)")
            print(f"Team: {result.get('team_name')}")
            print(f"Historical: {result.get('is_historical')}")
            
            if position > 0 and confidence > 0:
                print(f"\n🎉 SUCCESS: Lance Stroll case FIXED!")
                return True
            else:
                print(f"\n❌ FAILED: Still returning zeros")
                return False
        else:
            print(f"\n❌ HTTP Error: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to API. Please start it with:")
        print(f"python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_lance_stroll_case()
    
    if success:
        print(f"\n✅ Test passed! The zero values issue is fixed.")
    else:
        print(f"\n❌ Test failed. Please restart the API server and try again.")
        print(f"\nSteps to fix:")
        print(f"1. Stop the current API server")
        print(f"2. Restart it: python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print(f"3. Run this test again")
